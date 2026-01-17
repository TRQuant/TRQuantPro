"""
Investment Advisor V4.0 主工作流

整合所有模块，提供统一的接口：
1. 训练模式：从历史案例提取预测因子，训练XGBoost模型
2. 回测模式：使用训练好的模型进行历史回测验证
3. 推荐模式：生成本周投资推荐
4. 优化模式：使用遗传算法优化策略参数

增强功能（防过拟合）：
- 特征工程流水线（特征选择、标准化）
- 时序交叉验证 / Walk-Forward验证
- 过拟合检测
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from tqdm import tqdm
import json
import logging
import time

from .predictor_factor_extractor import PredictorFactorExtractor
from .multi_factor_calculator import MultiFactorCalculator, FactorConfig
from .xgboost_predictor import XGBoostPredictor, train_model_from_data, REGULARIZED_MODEL_PARAMS
from .trading_strategy import TradingStrategy, TradingConfig, TradeSignal
from .backtest_engine import BacktestEngine, BacktestResult
from .param_optimizer import ParamOptimizer, OptimizationResult
from .joinquant_strategy_generator import JoinQuantStrategyGenerator
from .data_storage import (
    V4DataStorage, get_v4_storage,
    StrategyCodeRecord, BacktestResultRecord, RecommendationRecord, ModelParamsRecord,
    save_strategy_code, save_backtest_result as save_backtest_to_db, save_recommendation
)
# 新增：特征工程和交叉验证
from .feature_pipeline import FeaturePipeline, FeaturePipelineConfig
from .cross_validator import TimeSeriesCrossValidator, WalkForwardValidator, OverfittingDetector
from .weekly_layout_planner import WeeklyLayoutPlanner, LayoutTarget
from .factor_optimizer import FactorOptimizer, FactorOptimizationConfig, OptimizationResult
from .factor_optimization_report_generator import FactorOptimizationReportGenerator

logger = logging.getLogger(__name__)


@dataclass
class AdvisorV4Config:
    """V4配置"""
    # 数据路径（使用OutputManager统一管理，如果为None则自动生成到output/advisor_v4/）
    high_return_cases_path: Optional[str] = None  # 将使用OutputManager自动生成到output/advisor_v4/data/
    predictive_features_path: Optional[str] = None  # 将使用OutputManager自动生成到output/advisor_v4/data/
    training_data_path: Optional[str] = None  # 将使用OutputManager自动生成到output/advisor_v4/data/
    model_path: Optional[str] = None  # 将使用OutputManager自动生成到output/advisor_v4/models/
    feature_pipeline_path: Optional[str] = None  # 将使用OutputManager自动生成到output/advisor_v4/models/
    
    # 训练配置（周频：以“自然周”为唯一时间口径，动态适配节假日）
    lookback_weeks: int = 1         # 预测因子提前周数（默认1周）
    lookback_days: int = 5          # 兼容字段（历史遗留，不再作为口径使用）
    train_start: str = "2024-09-01"
    train_end: str = "2025-06-30"
    val_start: str = "2025-07-01"
    val_end: str = "2025-09-30"
    test_start: str = "2025-09-30"
    test_end: str = "2025-12-31"
    
    # 交易配置
    trading_config: TradingConfig = field(default_factory=TradingConfig)
    
    # 优化配置
    optimize_generations: int = 10
    optimize_population: int = 20
    
    # 特征工程配置（新增）
    use_feature_pipeline: bool = True      # 是否使用特征流水线
    top_k_features: int = 10               # 选择Top K特征
    feature_select_method: str = 'combined'  # 特征选择方法
    
    # 交叉验证配置（新增）
    use_cv: bool = True                    # 是否使用交叉验证
    cv_method: str = 'walk_forward'        # 'time_series' 或 'walk_forward'
    cv_n_splits: int = 5                   # 时序CV折数
    cv_train_months: int = 3               # Walk-Forward训练月数
    cv_test_months: int = 1                # Walk-Forward测试月数
    
    # 正则化配置（新增）
    use_regularization: bool = True        # 是否使用增强正则化
    early_stopping_rounds: int = 20        # 早停轮数


class AdvisorV4Workflow:
    """V4主工作流
    
    集成功能：
    1. 训练模式：从历史案例提取预测因子，训练XGBoost模型
    2. 回测模式：支持三层回测（Fast/Standard/Precise）
    3. 推荐模式：生成本周投资推荐
    4. 优化模式：使用遗传算法优化策略参数
    5. 策略生成：生成聚宽格式策略代码
    6. 数据存储：MongoDB存储策略、回测结果、推荐记录
    """
    
    def __init__(self, config: AdvisorV4Config = None, verbose: bool = True):
        """
        Args:
            config: 配置
            verbose: 是否打印详细信息
        """
        self.config = config or AdvisorV4Config()
        self.verbose = verbose
        
        self.factor_extractor = None
        self.factor_calculator = None
        self.predictor = None
        self.backtest_engine = None
        
        # 新增：特征流水线
        self.feature_pipeline = None
        self._feature_pipeline_used = False
        self._selected_features = None
        
        # 新增：策略生成器和数据存储
        self.strategy_generator = JoinQuantStrategyGenerator()
        self.data_storage = get_v4_storage()
        
        # 新增：过拟合检测器
        self.overfitting_detector = OverfittingDetector()
        
        # 新增：CV结果
        self.cv_result = None
        
        self.jq = None
        
        # 初始化输出路径（使用OutputManager统一管理）
        self._init_output_paths()
        
        self._init_jqdata()
    
    def _init_output_paths(self):
        """初始化输出路径（使用OutputManager统一管理）"""
        from core.utils.output_manager import get_output_manager, OutputCategory
        
        output_manager = get_output_manager()
        
        # 如果路径为None，使用OutputManager自动生成
        if self.config.high_return_cases_path is None:
            self.config.high_return_cases_path = str(
                output_manager.get_path(OutputCategory.ADVISOR_V4, "data", "high_return_cases_full_train.csv")
            )
        
        if self.config.predictive_features_path is None:
            self.config.predictive_features_path = str(
                output_manager.get_path(OutputCategory.ADVISOR_V4, "data", "predictive_features.csv")
            )
        
        if self.config.training_data_path is None:
            self.config.training_data_path = str(
                output_manager.get_path(OutputCategory.ADVISOR_V4, "data", "training_data_v4.csv")
            )
        
        if self.config.model_path is None:
            self.config.model_path = str(
                output_manager.get_path(OutputCategory.ADVISOR_V4, "models", "xgb_high_return_v4.pkl")
            )
        
        if self.config.feature_pipeline_path is None:
            self.config.feature_pipeline_path = str(
                output_manager.get_path(OutputCategory.ADVISOR_V4, "models", "feature_pipeline_v4.pkl")
            )
    
    def _init_jqdata(self):
        """初始化JQData"""
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            self.jq = jq
            
            if self.verbose:
                print("✅ JQData连接成功")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")

    # ==================== 周频时间工具（统一口径） ====================

    def get_trading_days_in_week(self, date: str) -> List[str]:
        """获取指定日期所属自然周的交易日列表（动态适配节假日）。

        Notes:
            - 自然周口径：周一~周日
            - 交易日口径：通过JQData交易日历获取（考虑节假日）
            - 返回：YYYY-MM-DD 字符串列表，按时间升序
        """
        if self.jq is None:
            raise RuntimeError("JQData未初始化，无法获取交易日历")

        dt = datetime.strptime(date, "%Y-%m-%d").date()
        week_start = dt - timedelta(days=dt.weekday())         # Monday
        week_end = week_start + timedelta(days=6)              # Sunday

        trade_days = self.jq.get_trade_days(start_date=week_start, end_date=week_end)
        return [str(d)[:10] for d in trade_days]

    def get_week_start_end(self, date: str) -> Optional[tuple]:
        """获取指定日期所属自然周的（首个交易日, 最后交易日）。"""
        days = self.get_trading_days_in_week(date)
        if not days:
            return None
        return days[0], days[-1]

    def get_prev_week_anchor(self, date: str) -> Optional[str]:
        """获取指定日期前一自然周的“锚点交易日”（通常为上周最后一个交易日）。"""
        if self.jq is None:
            raise RuntimeError("JQData未初始化，无法获取交易日历")

        dt = datetime.strptime(date, "%Y-%m-%d").date()
        this_week_start = dt - timedelta(days=dt.weekday())
        prev_week_end = this_week_start - timedelta(days=1)
        prev_week_start = prev_week_end - timedelta(days=prev_week_end.weekday())

        trade_days = self.jq.get_trade_days(start_date=prev_week_start, end_date=prev_week_end)
        if trade_days is None or len(trade_days) == 0:
            return None
        return str(trade_days[-1])[:10]
    
    def train(self, 
              skip_extraction: bool = False,
              skip_negative_sampling: bool = False,
              use_feature_pipeline: bool = None,
              use_cv: bool = None,
              cv_method: str = None) -> XGBoostPredictor:
        """训练模式（增强版 - 防过拟合）
        
        流程：
        1. 从历史案例提取预测性因子（T-5时刻）
        2. 采样负样本
        3. 特征工程（特征选择、标准化）
        4. 交叉验证（可选）
        5. 训练XGBoost模型（正则化 + 早停）
        6. 过拟合检测
        
        Args:
            skip_extraction: 是否跳过因子提取（使用已有文件）
            skip_negative_sampling: 是否跳过负样本采样
            use_feature_pipeline: 是否使用特征流水线（覆盖配置）
            use_cv: 是否使用交叉验证（覆盖配置）
            cv_method: CV方法（覆盖配置）
        """
        # 使用参数或配置
        use_feature_pipeline = use_feature_pipeline if use_feature_pipeline is not None else self.config.use_feature_pipeline
        use_cv = use_cv if use_cv is not None else self.config.use_cv
        cv_method = cv_method or self.config.cv_method
        
        print(f"\n{'='*60}")
        print(f"【训练模式】Investment Advisor V4.0 (增强版)")
        print(f"{'='*60}")
        print(f"特征流水线: {'✅' if use_feature_pipeline else '❌'}")
        print(f"交叉验证: {'✅ ' + cv_method if use_cv else '❌'}")
        print(f"正则化: {'✅' if self.config.use_regularization else '❌'}")
        print(f"{'='*60}\n")
        
        # Step 0: 数据验证和清洗（新增）
        print("\nStep 0: 数据验证和清洗...")
        from .data_validator import DataValidator, DataQualityConfig
        
        # 读取原始数据
        raw_cases_df = pd.read_csv(self.config.high_return_cases_path)
        
        # 验证和清洗
        validator = DataValidator(config=DataQualityConfig(), verbose=self.verbose)
        validation_result = validator.validate_and_clean(raw_cases_df)
        
        if not validation_result.is_valid:
            print(f"\n❌ 数据验证未通过，存在严重错误:")
            for issue in validation_result.issues:
                if issue['severity'] == 'error':
                    print(f"   - {issue['message']}")
            raise ValueError("数据质量不合格，请修复后重试")
        
        # 保存清洗后的数据
        cleaned_cases_path = self.config.high_return_cases_path.replace('.csv', '_cleaned.csv')
        validation_result.cleaned_data.to_csv(cleaned_cases_path, index=False, encoding='utf-8-sig')
        print(f"✅ 清洗后数据已保存: {cleaned_cases_path}")
        print(f"   数据保留率: {validation_result.valid_records/validation_result.total_records:.1%}")
        
        # Step 1: 提取预测性因子（使用并行+GPU加速）
        if not skip_extraction:
            print("\nStep 1: 提取预测性因子（并行+GPU加速）...")
            from .predictor_factor_extractor_parallel import ParallelPredictorFactorExtractor
            
            # 使用并行提取器（支持GPU批量加速）
            # 检查GPU可用性
            try:
                import torch
                use_gpu = torch.cuda.is_available()
            except ImportError:
                use_gpu = False
            
            self.factor_extractor = ParallelPredictorFactorExtractor(
                num_workers=3,  # JQData最多3个并发连接
                use_gpu=use_gpu,   # 自动检测GPU可用性
                batch_size=50,     # GPU批处理大小
                verbose=self.verbose
            )
            
            # 使用清洗后的数据
            predictive_df = self.factor_extractor.extract_from_historical_cases(
                cleaned_cases_path,  # 使用清洗后的数据
                lookback_weeks=self.config.lookback_weeks,
                lookback_days=self.config.lookback_days
            )
            
            predictive_df.to_csv(self.config.predictive_features_path, index=False, encoding='utf-8-sig')
            print(f"✅ 预测因子已保存: {self.config.predictive_features_path}")
        else:
            print("\nStep 1: 加载已有预测因子...")
            predictive_df = pd.read_csv(self.config.predictive_features_path)
        
        # Step 2: 构建训练数据集
        if not skip_negative_sampling:
            print("\nStep 2: 构建训练数据集...")
            training_df = self._build_training_dataset(predictive_df)
            training_df.to_csv(self.config.training_data_path, index=False, encoding='utf-8-sig')
            print(f"训练数据已保存: {self.config.training_data_path}")
        else:
            print("\nStep 2: 加载已有训练数据...")
            training_df = pd.read_csv(self.config.training_data_path)
        
        # 划分训练/验证集
        train_mask = training_df['prediction_date'] < self.config.val_start
        val_mask = (training_df['prediction_date'] >= self.config.val_start) & \
                   (training_df['prediction_date'] < self.config.test_start)
        
        train_df = training_df[train_mask]
        val_df = training_df[val_mask]
        
        if len(val_df) < 10:
            from sklearn.model_selection import train_test_split
            train_df, val_df = train_test_split(training_df, test_size=0.2, random_state=42)
        
        print(f"\n数据划分: 训练集 {len(train_df)} | 验证集 {len(val_df)}")
        
        # Step 3: 特征工程（新增）
        if use_feature_pipeline:
            print("\nStep 3: 特征工程流水线...")
            
            pipeline_config = FeaturePipelineConfig(
                top_k_features=self.config.top_k_features,
                select_method=self.config.feature_select_method
            )
            self.feature_pipeline = FeaturePipeline(pipeline_config)
            
            # 获取特征列
            feature_cols = XGBoostPredictor.FEATURE_COLUMNS.copy()
            available_cols = [c for c in feature_cols if c in train_df.columns]
            
            # Fit on train
            X_train = train_df[available_cols].copy()
            y_train = train_df['label'].copy()
            
            X_train_transformed = self.feature_pipeline.fit_transform(X_train, y_train)
            
            # Transform validation
            X_val = val_df[available_cols].copy()
            X_val_transformed = self.feature_pipeline.transform(X_val)
            
            # 更新DataFrame（使用转换后的特征）
            # 删除原始特征列，只保留转换后的特征
            for col in X_train_transformed.columns:
                train_df[col] = X_train_transformed[col].values
                val_df[col] = X_val_transformed[col].values
            
            # 删除原始特征列（如果还存在）
            for col in available_cols:
                if col in train_df.columns and col not in X_train_transformed.columns:
                    train_df.drop(columns=[col], inplace=True)
                if col in val_df.columns and col not in X_val_transformed.columns:
                    val_df.drop(columns=[col], inplace=True)
            
            # 保存特征流水线
            self.feature_pipeline.save(self.config.feature_pipeline_path)
            
            # 记录已使用特征流水线的标记
            train_df['_use_feature_pipeline'] = True
            val_df['_use_feature_pipeline'] = True
            self._feature_pipeline_used = True
            self._selected_features = self.feature_pipeline.get_selected_features()
        else:
            self._feature_pipeline_used = False
            self._selected_features = None
        
        # Step 4: 交叉验证（新增）
        if use_cv:
            print(f"\nStep 4: {cv_method}验证...")
            # 检查数据量是否足够进行Walk-Forward验证
            if cv_method == 'walk_forward' and len(training_df) < 100:
                print("⚠️ 数据量不足（<100样本），Walk-Forward验证降级为简单时序划分")
                cv_method = 'time_series'  # 降级到时序验证
            
            self.cv_result = self._run_cross_validation(training_df, cv_method)
            
            if self.cv_result:
                if self.cv_result.n_folds == 0:
                    print("⚠️ 交叉验证无法执行（数据时间跨度不足），跳过CV")
                elif not self.cv_result.is_stable:
                    print(f"\n⚠️ CV稳定性警告: {self.cv_result.stability_warning}")
        
        # Step 5: 训练最终模型
        print("\nStep 5: 训练XGBoost模型...")
        
        self.predictor = XGBoostPredictor(
            model_path=self.config.model_path,
            use_regularization=self.config.use_regularization,
            verbose=self.verbose
        )
        
        # 如果使用了特征流水线，告诉predictor不要再次标准化
        if self._feature_pipeline_used:
            # 特征已经标准化，predictor应该跳过scaler
            self.predictor._features_already_scaled = True
            self.predictor._selected_features = self._selected_features
        
        self.predictor.train(
            train_df, val_df,
            early_stopping_rounds=self.config.early_stopping_rounds if self.config.use_regularization else 0
        )
        
        # Step 6: 过拟合检测
        print("\nStep 6: 过拟合检测...")
        overfitting_report = self.predictor.detect_overfitting()
        
        if overfitting_report['is_overfitting']:
            print(f"\n⚠️ 检测到过拟合风险 (严重程度: {overfitting_report['severity']})")
            for warning in overfitting_report['warnings']:
                print(f"   - {warning}")
            print(f"   建议: {overfitting_report['recommendation']}")
        else:
            print("✅ 模型泛化能力良好")
        
        # 保存模型
        self.predictor.save()
        
        print("\n✅ 模型训练完成!")
        
        return self.predictor
    
    def _run_cross_validation(self, training_df: pd.DataFrame, cv_method: str):
        """执行交叉验证"""
        from .xgboost_predictor import XGBoostPredictor
        
        def train_func(df):
            """训练函数"""
            predictor = XGBoostPredictor(
                use_regularization=self.config.use_regularization,
                verbose=False
            )
            # 简化训练
            val_size = max(int(len(df) * 0.1), 10)
            train_part = df.iloc[:-val_size]
            val_part = df.iloc[-val_size:]
            predictor.train(train_part, val_part, early_stopping_rounds=10)
            return predictor
        
        def eval_func(predictor, df):
            """评估函数"""
            metrics = predictor.evaluate(df, 'label')
            return {
                'accuracy': metrics.accuracy,
                'precision': metrics.precision,
                'recall': metrics.recall,
                'f1': metrics.f1,
                'auc': metrics.auc,
            }
        
        if cv_method == 'time_series':
            validator = TimeSeriesCrossValidator(
                n_splits=self.config.cv_n_splits,
                verbose=self.verbose
            )
        else:  # walk_forward
            validator = WalkForwardValidator(
                train_months=self.config.cv_train_months,
                test_months=self.config.cv_test_months,
                verbose=self.verbose
            )
        
        return validator.validate(training_df, train_func, eval_func)
    
    def _build_training_dataset(self, positive_df: pd.DataFrame) -> pd.DataFrame:
        """构建训练数据集（正负样本）"""
        # 正样本
        positive_df = positive_df.copy()
        # 周频：label基于未来1周收益阈值（默认5%）重新打标
        if 'target_return' in positive_df.columns:
            positive_df['label'] = (positive_df['target_return'] >= 5.0).astype(int)
        elif 'is_high_return' in positive_df.columns:
            positive_df['label'] = positive_df['is_high_return'].astype(int)
        else:
            positive_df['label'] = 1
        
        # 负样本：随机采样非高收益股票
        print("采样负样本...")
        
        dates = positive_df['prediction_date'].unique()
        sample_dates = np.random.choice(dates, min(20, len(dates)), replace=False)
        
        negative_samples = []
        
        for date in tqdm(sample_dates, desc="负样本采样"):
            # 获取股票池
            stocks = self.jq.get_all_securities(types=['stock'], date=date)
            stocks = stocks[~stocks.index.str.startswith('688')]
            stocks = stocks[~stocks['display_name'].str.contains('ST')]
            stock_list = stocks.index.tolist()
            
            # 排除正样本
            positive_codes = positive_df[positive_df['prediction_date'] == date]['code'].tolist()
            stock_list = [s for s in stock_list if s not in positive_codes]
            
            # 随机抽样
            sample_size = min(100, len(stock_list))
            sample_codes = np.random.choice(stock_list, sample_size, replace=False)
            
            # 获取因子
            if self.factor_calculator is None:
                self.factor_calculator = MultiFactorCalculator(verbose=False)
            
            try:
                factors_df = self.factor_calculator.calculate_all_factors(list(sample_codes), date)
                
                if factors_df is not None and not factors_df.empty:
                    factors_df['prediction_date'] = date
                    factors_df['target_date'] = date  # 简化
                    factors_df['target_return'] = 0  # 假设为0
                    factors_df['is_high_return'] = False
                    factors_df['label'] = 0
                    
                    negative_samples.append(factors_df)
            except Exception as e:
                logger.warning(f"负样本采集失败 {date}: {e}")
        
        # 合并
        if negative_samples:
            negative_df = pd.concat(negative_samples, ignore_index=True)
            print(f"负样本采集: {len(negative_df)} 条")
        else:
            negative_df = pd.DataFrame()
        
        # 统一列
        common_cols = list(set(positive_df.columns) & set(negative_df.columns))
        
        dataset = pd.concat([
            positive_df[common_cols],
            negative_df[common_cols] if not negative_df.empty else pd.DataFrame()
        ], ignore_index=True)
        
        dataset = dataset.sample(frac=1).reset_index(drop=True)
        
        return dataset
    
    def backtest(self,
                 start_date: str = None,
                 end_date: str = None,
                 rebalance_freq: str = 'weekly',
                 backtest_levels: List[str] = None,
                 save_to_db: bool = True) -> BacktestResult:
        """回测模式 - 支持三层回测架构
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            rebalance_freq: 调仓频率
            backtest_levels: 回测层级列表 ['fast', 'standard', 'precise']
                - fast: 快速回测，向量化计算，<5秒
                - standard: 标准回测，事件驱动，<30秒
                - precise: 精确回测，BulletTrade/QMT，完整模拟
            save_to_db: 是否保存到MongoDB
        """
        start_date = start_date or self.config.test_start
        end_date = end_date or self.config.test_end
        backtest_levels = backtest_levels or ['fast']  # 默认快速回测

        # ==================== phase4-cache: 先查MongoDB缓存再跑回测 ====================
        try:
            from dataclasses import asdict
            from core.advisor_v4.data_storage import (
                get_v4_storage,
                compute_config_hash,
                compute_algorithm_version,
            )

            primary_level = backtest_levels[0] if backtest_levels else "fast"
            storage = get_v4_storage()
            cfg_for_hash = {
                "system": "advisor_v4",
                "start_date": start_date,
                "end_date": end_date,
                "backtest_level": primary_level,
                "trading_config": asdict(self.config.trading_config),
                "lookback_weeks": self.config.lookback_weeks,
                "data_source": "jqdata",
                "universe_mode": "hs300",
                "universe_limit": 500,
            }
            config_hash = compute_config_hash(cfg_for_hash)
            algo_ver = compute_algorithm_version()

            # 稳定ID：MongoDB可用则走MongoDB；否则走文件fallback（两者都可通过ID命中缓存）
            backtest_id = f"v4_{primary_level}_{config_hash[:12]}_{algo_ver}"
            cached = storage.get_backtest_result(backtest_id)
            if cached:
                print(f"✅ 命中回测缓存: id={backtest_id}")
                return BacktestResult(
                    start_date=cached.get("start_date", start_date),
                    end_date=cached.get("end_date", end_date),
                    initial_capital=float(cached.get("initial_capital", 1_000_000.0)),
                    final_capital=float(cached.get("initial_capital", 1_000_000.0))
                    * (1.0 + float(cached.get("total_return", 0.0))),
                    total_return=float(cached.get("total_return", 0.0)),
                    annualized_return=float(cached.get("annualized_return", 0.0)),
                    max_drawdown=float(cached.get("max_drawdown", 0.0)),
                    sharpe_ratio=float(cached.get("sharpe_ratio", 0.0)),
                    total_trades=int(cached.get("total_trades", 0)),
                    win_rate=float(cached.get("win_rate", 0.0)),
                    profit_factor=float(cached.get("profit_factor", 0.0)),
                    avg_return=float(cached.get("avg_return", 0.0)),
                    hit_10pct_rate=float(cached.get("hit_10pct_rate", 0.0)),
                    hit_5pct_rate=float(cached.get("hit_5pct_rate", 0.0)),
                )
        except Exception as e:
            logger.warning(f"回测缓存检查失败（忽略继续回测）: {e}")
        
        print(f"\n{'='*60}")
        print(f"【回测模式】{start_date} ~ {end_date}")
        print(f"回测层级: {backtest_levels}")
        print(f"{'='*60}\n")
        
        # 加载模型
        if self.predictor is None:
            self.predictor = XGBoostPredictor(model_path=self.config.model_path)
            try:
                self.predictor.load()
            except:
                print("⚠️ 模型未找到，请先运行训练模式")
                return None
        
        # 创建回测引擎
        self.backtest_engine = BacktestEngine(
            predictor=self.predictor,
            trading_config=self.config.trading_config,
            verbose=self.verbose
        )
        
        # 运行回测（支持三层回测）
        t0 = time.time()
        result = self.backtest_engine.run(
            start_date=start_date,
            end_date=end_date,
            rebalance_freq=rebalance_freq,
            backtest_levels=backtest_levels
        )
        elapsed = time.time() - t0
        
        # 保存结果到文件
        self._save_backtest_result(result)
        
        # 保存到MongoDB
        if save_to_db and result:
            self._save_backtest_to_mongodb(result, backtest_levels, duration_seconds=elapsed)
        
        return result
    
    def generate_strategy_code(self, 
                               strategy_name: str = None,
                               save_to_db: bool = True,
                               save_to_file: bool = True) -> str:
        """生成聚宽格式策略代码
        
        Args:
            strategy_name: 策略名称
            save_to_db: 是否保存到MongoDB
            save_to_file: 是否保存到文件
            
        Returns:
            策略代码字符串
        """
        strategy_name = strategy_name or f"V4.0多因子预测策略_{datetime.now().strftime('%Y%m%d')}"
        
        print(f"\n{'='*60}")
        print(f"【策略生成】{strategy_name}")
        print(f"{'='*60}\n")
        
        # 获取市场趋势（可选）
        market_trend = None
        try:
            from core.market_trend_storage import MarketTrendStorage
            storage = MarketTrendStorage()
            market_trend = storage.get_latest_signal()
        except:
            pass
        
        # 生成策略代码
        strategy_code = self.strategy_generator.generate_strategy_code(
            strategy_name=strategy_name,
            v4_config={
                'model_path': self.config.model_path,
                'lookback_days': self.config.lookback_days,
            },
            trading_config=self.config.trading_config,
            market_trend=market_trend
        )
        
        strategy_id = f"v4_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 保存到文件
        if save_to_file:
            output_dir = Path("strategies/generated")
            output_dir.mkdir(parents=True, exist_ok=True)
            filepath = output_dir / f"{strategy_id}.py"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(strategy_code)
            print(f"✅ 策略代码已保存: {filepath}")
        
        # 保存到MongoDB
        if save_to_db:
            save_strategy_code(
                strategy_id=strategy_id,
                strategy_name=strategy_name,
                strategy_code=strategy_code,
                config={
                    'model_path': self.config.model_path,
                    'trading_config': {
                        'min_probability': self.config.trading_config.min_probability,
                        'target_return': self.config.trading_config.target_return,
                        'stop_loss': self.config.trading_config.stop_loss,
                    }
                }
            )
            print(f"✅ 策略代码已保存到MongoDB: {strategy_id}")
        
        return strategy_code
    
    def run_multi_level_backtest(self,
                                  start_date: str = None,
                                  end_date: str = None,
                                  generate_strategy: bool = True) -> Dict:
        """运行多层级回测
        
        依次运行 Fast → Standard → Precise 回测，逐层验证策略
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            generate_strategy: 是否生成策略代码（用于Precise回测）
            
        Returns:
            各层级回测结果字典
        """
        start_date = start_date or self.config.test_start
        end_date = end_date or self.config.test_end
        
        print(f"\n{'='*60}")
        print(f"【多层级回测】{start_date} ~ {end_date}")
        print(f"{'='*60}\n")
        
        results = {}
        
        # 1. 快速回测
        print("\n📊 [1/3] 快速回测 (Fast)...")
        fast_result = self.backtest(
            start_date=start_date,
            end_date=end_date,
            backtest_levels=['fast'],
            save_to_db=True
        )
        results['fast'] = fast_result
        
        if fast_result and fast_result.sharpe_ratio < 0:
            print("⚠️ 快速回测夏普比率为负，跳过后续回测")
            return results
        
        # 2. 标准回测
        print("\n📊 [2/3] 标准回测 (Standard)...")
        standard_result = self.backtest(
            start_date=start_date,
            end_date=end_date,
            backtest_levels=['standard'],
            save_to_db=True
        )
        results['standard'] = standard_result
        
        # 3. 精确回测（需要生成策略代码）
        if generate_strategy:
            print("\n📊 [3/3] 精确回测 (Precise - BulletTrade)...")
            
            # 生成策略代码
            strategy_code = self.generate_strategy_code(save_to_db=True, save_to_file=True)
            
            # 运行BulletTrade回测
            precise_result = self.backtest(
                start_date=start_date,
                end_date=end_date,
                backtest_levels=['precise'],
                save_to_db=True
            )
            results['precise'] = precise_result
        
        # 打印对比结果
        self._print_backtest_comparison(results)
        
        return results
    
    def _print_backtest_comparison(self, results: Dict):
        """打印回测结果对比"""
        print(f"\n{'='*60}")
        print(f"【回测结果对比】")
        print(f"{'='*60}")
        print(f"{'层级':<10} {'总收益':>10} {'年化':>10} {'夏普':>8} {'最大回撤':>10} {'胜率':>8}")
        print(f"{'-'*60}")
        
        for level, result in results.items():
            if result:
                print(f"{level:<10} {result.total_return:>9.1%} {result.annualized_return:>9.1%} "
                      f"{result.sharpe_ratio:>7.2f} {result.max_drawdown:>9.1%} {result.win_rate:>7.1%}")
        
        print(f"{'='*60}")
    
    def _save_backtest_to_mongodb(self, result: BacktestResult, backtest_levels: List[str], duration_seconds: float = 0.0):
        """保存回测结果到MongoDB"""
        try:
            from dataclasses import asdict
            from core.advisor_v4.data_storage import compute_config_hash, compute_algorithm_version

            level = backtest_levels[0] if backtest_levels else "fast"
            cfg_for_hash = {
                "system": "advisor_v4",
                "start_date": result.start_date,
                "end_date": result.end_date,
                "backtest_level": level,
                "trading_config": asdict(self.config.trading_config),
                "lookback_weeks": self.config.lookback_weeks,
                "data_source": "jqdata",
                "universe_mode": "hs300",
                "universe_limit": 500,
            }
            config_hash = compute_config_hash(cfg_for_hash)
            algo_ver = compute_algorithm_version()

            # 稳定ID：同一配置 + 同一算法版本不会重复插入
            backtest_id = f"v4_{level}_{config_hash[:12]}_{algo_ver}"
            
            save_backtest_to_db(
                backtest_id=backtest_id,
                strategy_id="v4_default",
                start_date=result.start_date,
                end_date=result.end_date,
                metrics={
                    'total_return': result.total_return,
                    'annualized_return': result.annualized_return,
                    'max_drawdown': result.max_drawdown,
                    'sharpe_ratio': result.sharpe_ratio,
                    'win_rate': result.win_rate,
                    'total_trades': result.total_trades,
                    'hit_10pct_rate': result.hit_10pct_rate,
                    'hit_5pct_rate': result.hit_5pct_rate,
                    'profit_factor': result.profit_factor,
                    'avg_return': result.avg_return,
                },
                backtest_level=backtest_levels[0] if backtest_levels else 'fast',
                initial_capital=result.initial_capital,
                duration_seconds=float(duration_seconds),
                config_hash=config_hash,
                algorithm_version=algo_ver,
                config=cfg_for_hash,
            )
            
            logger.info(f"回测结果已保存到MongoDB: {backtest_id}")
        except Exception as e:
            logger.warning(f"保存回测结果到MongoDB失败: {e}")
    
    def recommend(self, date: str = None, top_n: int = 10, fast_mode: bool = False) -> List[TradeSignal]:
        """推荐模式
        
        Args:
            date: 推荐日期（默认今天）
            top_n: 推荐数量
            fast_mode: 快速模式（减少股票数量，加快速度）
        """
        from copy import deepcopy  # 导入deepcopy，用于复制配置
        
        date = date or datetime.now().strftime('%Y-%m-%d')
        self._fast_mode = fast_mode  # 标记快速模式
        
        print(f"\n{'='*60}")
        print(f"【推荐模式】{date}")
        print(f"{'='*60}\n")
        
        # 加载模型
        if self.predictor is None:
            self.predictor = XGBoostPredictor(model_path=self.config.model_path)
            try:
                self.predictor.load()
            except:
                print("⚠️ 模型未找到，请先运行训练模式")
                return []
        
        # 加载特征流水线（如果存在）
        if self.feature_pipeline is None and Path(self.config.feature_pipeline_path).exists():
            try:
                self.feature_pipeline = FeaturePipeline()
                self.feature_pipeline.load(self.config.feature_pipeline_path)
                print("✅ 特征流水线已加载")
            except Exception as e:
                logger.warning(f"加载特征流水线失败: {e}")
        
        # 初始化因子计算器
        if self.factor_calculator is None:
            self.factor_calculator = MultiFactorCalculator(verbose=self.verbose)
        
        # 获取股票池
        print("获取股票池...")
        stocks = self.jq.get_all_securities(types=['stock'], date=date)
        stocks = stocks[~stocks.index.str.startswith('688')]
        stocks = stocks[~stocks['display_name'].str.contains('ST')]
        
        # 限制数量（快速模式下减少股票数量以加快速度）
        # 快速模式：100只股票，完整模式：500只股票
        if hasattr(self, '_fast_mode') and self._fast_mode:
            sample_size = min(100, len(stocks))
            print(f"快速模式：只计算 {sample_size} 只股票的因子（加快速度）")
        else:
            sample_size = min(500, len(stocks))
        sample_codes = np.random.choice(stocks.index.tolist(), sample_size, replace=False).tolist()
        
        # 计算因子
        factors_df = self.factor_calculator.calculate_all_factors(sample_codes, date)
        
        if factors_df is None or factors_df.empty:
            print("因子计算失败")
            return []
        
        # 添加股票名称
        factors_df['name'] = factors_df['code'].map(stocks['display_name'])
        
        # 应用特征流水线（如果存在）
        if self.feature_pipeline is not None and self.feature_pipeline.fitted:
            print("应用特征流水线...")
            try:
                # 使用特征流水线转换（它会处理特征选择和标准化）
                feature_cols = [c for c in XGBoostPredictor.FEATURE_COLUMNS if c in factors_df.columns]
                X = factors_df[feature_cols].copy()
                X_transformed = self.feature_pipeline.transform(X)
                
                # 将转换后的特征添加到factors_df
                # 删除原始特征列，只保留转换后的特征
                for col in X_transformed.columns:
                    factors_df[col] = X_transformed[col].values
                
                # 删除原始特征列（避免混淆）
                for col in feature_cols:
                    if col in factors_df.columns and col not in X_transformed.columns:
                        factors_df.drop(columns=[col], inplace=True)
                
                print(f"特征流水线转换完成: {len(X_transformed.columns)} 个特征")
                print(f"转换后的特征: {list(X_transformed.columns)}")
            except Exception as e:
                logger.warning(f"特征流水线转换失败: {e}，使用原始因子")
                logger.exception(e)
        
        # 预测：predictor会使用特征流水线选择的特征（如果有）
        print("模型预测...")
        predictions = self.predictor.predict(factors_df)
        factors_df['probability'] = [p.probability for p in predictions]
        
        # 获取当前价格
        prices = self.jq.get_price(
            factors_df['code'].tolist(),
            end_date=date,
            count=1,
            frequency='daily',
            fields=['close', 'money'],
            panel=False,
            fq='post'
        )
        
        if prices is not None:
            price_dict = {row['code']: row['close'] for _, row in prices.iterrows()}
            money_dict = {row['code']: row['money'] / 10000 for _, row in prices.iterrows()}
            factors_df['current_price'] = factors_df['code'].map(price_dict)
            factors_df['avg_money'] = factors_df['code'].map(money_dict)

        # ==================== phase6.2: 规则引擎融合（可解释过滤/打分） ====================
        try:
            # 市场趋势代理（沪深300近20日涨跌幅，百分比）
            market_trend = 0.0
            try:
                idx_px = self.jq.get_price(
                    "000300.XSHG",
                    end_date=date,
                    count=21,
                    frequency="daily",
                    fields=["close"],
                    fq="post",
                )
                if idx_px is not None and len(idx_px) >= 2:
                    market_trend = (float(idx_px["close"].iloc[-1]) / float(idx_px["close"].iloc[0]) - 1.0) * 100.0
            except Exception:
                market_trend = 0.0

            factors_df["market_trend"] = market_trend

            from .rule_based_strategy import RuleBasedStrategy

            rule_engine = RuleBasedStrategy()
            scored_df = rule_engine.score_candidates(factors_df)

            # 将规则匹配度融入total_score（仍保留probability过滤）
            if "total_score" in scored_df.columns and "rule_score" in scored_df.columns:
                scored_df["total_score_raw"] = scored_df["total_score"]
                scored_df["total_score"] = (
                    0.7 * scored_df["total_score_raw"].astype(float) + 0.3 * scored_df["rule_score"].astype(float)
                ).clip(0, 100)

            # 优先使用规则通过的候选；若数量不足，回退到 rule_score 阈值
            preferred = scored_df[scored_df.get("rule_passed", False)]
            if len(preferred) < top_n:
                preferred = scored_df[scored_df.get("rule_score", 0) >= 60]
            factors_df = preferred if not preferred.empty else scored_df
        except Exception as e:
            logger.warning(f"规则引擎融合失败（忽略继续）: {e}")
        
        # 生成信号（快速模式下降低阈值以获取更多推荐）
        trading_config = self.config.trading_config
        if hasattr(self, '_fast_mode') and self._fast_mode:
            # 快速模式：降低阈值，确保能生成推荐
            trading_config = deepcopy(self.config.trading_config)
            trading_config.min_probability = 0.3  # 降低概率阈值
            trading_config.min_score = 50.0       # 降低得分阈值
        
        strategy = TradingStrategy(trading_config)
        signals = strategy.generate_entry_signals(factors_df, date)
        
        # 如果信号数量不足，进一步降低阈值重试
        if len(signals) < top_n and len(factors_df) > 0:
            if self.verbose:
                print(f"⚠️ 信号数量不足（{len(signals)}/{top_n}），降低阈值重试...")
            # 按probability排序，直接取top_n
            factors_df_sorted = factors_df.nlargest(top_n * 2, 'probability')  # 取2倍数量备选
            
            # 临时降低阈值
            temp_config = deepcopy(trading_config)
            temp_config.min_probability = max(0.1, factors_df_sorted['probability'].quantile(0.5) if len(factors_df_sorted) > 0 else 0.3)
            temp_config.min_score = max(40.0, factors_df_sorted['total_score'].quantile(0.5) if len(factors_df_sorted) > 0 else 50.0)
            
            strategy_temp = TradingStrategy(temp_config)
            signals = strategy_temp.generate_entry_signals(factors_df_sorted, date)
        
        # 排序并取TOP N
        signals = sorted(signals, key=lambda x: x.probability, reverse=True)[:top_n]
        
        # 打印推荐
        self._print_recommendations(signals, date)
        
        # 保存推荐
        self._save_recommendations(signals, date)
        
        return signals

    def optimize_factors(
        self,
        start_date: str = None,
        end_date: str = None,
        config: Optional[FactorOptimizationConfig] = None,
    ) -> OptimizationResult:
        """
        优化因子选择和权重（递归优化）
        
        Args:
            start_date: 优化开始日期（如果为None，使用train_start）
            end_date: 优化结束日期（如果为None，使用test_end）
            config: 优化配置（如果为None，使用默认配置）
        
        Returns:
            OptimizationResult
        """
        if start_date is None:
            start_date = self.config.train_start
        if end_date is None:
            end_date = self.config.test_end
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("【因子优化模式】")
            print(f"{'='*70}")
            print(f"优化区间: {start_date} ~ {end_date}")
        
        # 创建因子优化器
        optimizer = FactorOptimizer(
            config=config or FactorOptimizationConfig(),
            workflow=self,
            verbose=self.verbose,
        )
        
        # 执行递归优化
        result = optimizer.recursive_optimize(
            start_date=start_date,
            end_date=end_date,
        )
        
        # 保存优化结果到MongoDB（可选）
        if self.data_storage.is_connected():
            try:
                # TODO: 实现保存优化结果到MongoDB的逻辑
                pass
            except Exception as e:
                logger.warning(f"保存优化结果到MongoDB失败: {e}")
        
        # 生成优化报告
        if self.verbose:
            try:
                report_generator = FactorOptimizationReportGenerator(verbose=self.verbose)
                report_path = report_generator.generate_report(result)
                print(f"\n✅ 优化报告已生成: {report_path}")
            except Exception as e:
                logger.warning(f"生成优化报告失败: {e}")
        
        return result

    def recommend_weekly_layout(self, anchor_date: str = None, top_n: int = 5):
        """生成“提前一周布局”计划（周频，自然周口径）。

        逻辑：
        - 以 anchor_date 为当前参考，生成 **下一自然周** 的布局计划
        - 用“下一周首个交易日”的 **前一周锚点交易日** 作为信号计算日（提前一周）
        """
        anchor_date = anchor_date or datetime.now().strftime("%Y-%m-%d")

        # 1) 目标周：下一自然周
        dt = datetime.strptime(anchor_date, "%Y-%m-%d").date()
        next_week_date = (dt + timedelta(days=7)).strftime("%Y-%m-%d")
        week_range = self.get_week_start_end(next_week_date)
        if not week_range:
            raise RuntimeError("无法确定下一自然周交易日范围（可能JQData交易日历不可用）")
        week_start, week_end = week_range

        # 2) 信号日：下一周 week_start 对应的“前一周锚点交易日”（上周最后一个交易日）
        signal_date = self.get_prev_week_anchor(week_start)
        if not signal_date:
            signal_date = anchor_date

        # 3) 生成候选信号（复用 recommend 逻辑）
        # 根据top_n判断是否快速模式（快速模式通常top_n<=3）
        fast_mode = (top_n <= 3)
        signals = self.recommend(date=signal_date, top_n=top_n, fast_mode=fast_mode)

        # 4) 组装为周度布局结构
        candidates = []
        for s in signals:
            candidates.append(
                {
                    "code": s.code,
                    "name": s.name,
                    "score": float(s.score),
                    "entry_price": float(s.entry_price),
                    "reason": f"prob={s.probability:.0%}; score={s.score:.1f}; {s.factors.get('reason','') if isinstance(s.factors, dict) else ''}",
                    "tags": [],
                }
            )

        planner = WeeklyLayoutPlanner(verbose=self.verbose)
        plan = planner.build_from_candidates(
            week_start=week_start,
            week_end=week_end,
            candidates=candidates,
            market_outlook="neutral",
            position_advice=0.5,
            max_targets=top_n,
        )
        plan.meta = {
            **plan.meta,
            "anchor_date": anchor_date,
            "signal_date": signal_date,
            "week_start": week_start,
            "week_end": week_end,
        }
        return plan
    
    def generate_weekly_layout_report(
        self,
        anchor_date: str = None,
        top_n: int = 5,
        output_filename: str = None,
        fast_mode: bool = False,
    ) -> str:
        """
        生成周度布局HTML报告（阶段8.1）

        Args:
            anchor_date: 锚点日期（默认今天）
            top_n: 推荐数量
            output_filename: 输出文件名（默认自动生成）
            fast_mode: 快速模式（减少股票数量，加快速度）

        Returns:
            HTML报告文件路径
        """
        from .weekly_report_generator import WeeklyReportGenerator

        # 1) 生成周度布局计划（传入fast_mode参数）
        self._fast_mode = fast_mode
        plan = self.recommend_weekly_layout(anchor_date=anchor_date, top_n=top_n)

        # 2) 生成HTML报告
        generator = WeeklyReportGenerator(verbose=self.verbose)
        report_path = generator.generate(plan, output_filename=output_filename)

        if self.verbose:
            print(f"\n✅ 周度布局报告已生成: {report_path}")
            print(f"   - 周期范围: {plan.week_start} ~ {plan.week_end}")
            print(f"   - 推荐标的: {len(plan.targets)} 只")
            print(f"   - 建议仓位: {plan.position_advice:.1%}")

        return report_path
    
    def optimize(self, 
                 fitness_func: callable = None,
                 optimization_mode: str = "balanced") -> OptimizationResult:
        """优化模式
        
        Args:
            fitness_func: 自定义适应度函数
            optimization_mode: 优化模式
        """
        print(f"\n{'='*60}")
        print(f"【优化模式】")
        print(f"{'='*60}\n")
        
        # 默认适应度函数：简化回测
        if fitness_func is None:
            def default_fitness(params):
                # 更新交易配置
                config = TradingConfig(
                    min_probability=params.get('min_probability', 0.5),
                    min_score=params.get('min_score', 60),
                    target_return=params.get('target_return', 0.10),
                    stop_loss=params.get('stop_loss', -0.05),
                    trailing_stop=params.get('trailing_stop', 0.03),
                    max_holding_days=int(params.get('max_holding_days', 5)),
                    position_size=params.get('position_size', 0.10),
                )
                
                # 简化回测
                engine = BacktestEngine(
                    predictor=self.predictor,
                    trading_config=config,
                    verbose=False
                )
                
                try:
                    result = engine.run(
                        start_date=self.config.val_start,
                        end_date=self.config.val_end,
                        rebalance_freq='weekly'
                    )
                    
                    fitness = result.sharpe_ratio if result.sharpe_ratio > 0 else 0
                    metrics = {
                        'sharpe_ratio': result.sharpe_ratio,
                        'total_return': result.total_return,
                        'max_drawdown': result.max_drawdown,
                        'win_rate': result.win_rate,
                        'hit_10pct_rate': result.hit_10pct_rate,
                    }
                    
                    return fitness, metrics
                except:
                    return 0, {}
            
            fitness_func = default_fitness
        
        # 运行优化
        optimizer = ParamOptimizer(
            generations=self.config.optimize_generations,
            population_size=self.config.optimize_population,
            verbose=self.verbose
        )
        
        result = optimizer.optimize(fitness_func, optimization_mode)
        
        # 保存结果（使用OutputManager统一管理）
        from core.utils.output_manager import get_output_manager, OutputCategory
        
        output_manager = get_output_manager()
        optimization_path = output_manager.get_optimization_path(
            category=OutputCategory.ADVISOR_V4,
            filename="optimization_result.json",
            add_timestamp=True
        )
        optimizer.save_result(result, str(optimization_path))
        
        return result
    
    def _print_recommendations(self, signals: List[TradeSignal], date: str):
        """打印推荐"""
        print(f"\n{'='*60}")
        print(f"【{date} 投资推荐】")
        print(f"{'='*60}")
        print(f"{'代码':<12} {'名称':<8} {'概率':>6} {'得分':>6} {'价格':>8} {'止盈':>8} {'止损':>8} {'仓位':>6}")
        print(f"{'-'*60}")
        
        for sig in signals:
            print(f"{sig.code:<12} {sig.name:<8} {sig.probability:>5.0%} {sig.score:>6.1f} "
                  f"{sig.entry_price:>8.2f} {sig.target_price:>8.2f} {sig.stop_loss_price:>8.2f} {sig.position_size:>5.0%}")
        
        print(f"{'='*60}")
    
    def _save_recommendations(self, signals: List[TradeSignal], date: str):
        """保存推荐（文件 + MongoDB）"""
        data = []
        stocks_for_db = []
        
        for sig in signals:
            data.append({
                'date': date,
                'code': sig.code,
                'name': sig.name,
                'probability': sig.probability,
                'score': sig.score,
                'entry_price': sig.entry_price,
                'target_price': sig.target_price,
                'stop_loss_price': sig.stop_loss_price,
                'position_size': sig.position_size,
                **sig.factors
            })
            
            # MongoDB格式
            stocks_for_db.append({
                'code': sig.code,
                'name': sig.name,
                'score': sig.score,
                'weight': sig.position_size,
                'reason': f"概率:{sig.probability:.0%}, 得分:{sig.score:.1f}"
            })
        
        # 保存到CSV（使用OutputManager统一管理）
        from core.utils.output_manager import get_output_manager, OutputCategory
        
        df = pd.DataFrame(data)
        output_manager = get_output_manager()
        path = output_manager.get_recommendation_path(
            category=OutputCategory.ADVISOR_V4,
            filename=f"recommendations_{date.replace('-', '')}.csv"
        )
        df.to_csv(path, index=False, encoding='utf-8-sig')
        print(f"\n推荐已保存: {path}")
        
        # 保存到MongoDB
        try:
            recommendation_id = f"rec_{date.replace('-', '')}_{datetime.now().strftime('%H%M%S')}"
            save_recommendation(
                recommendation_id=recommendation_id,
                date=date,
                stocks=stocks_for_db,
                market_trend="neutral",  # TODO: 从市场分析获取
                position_advice=0.5,
                strategy_id="v4_default"
            )
            print(f"推荐已保存到MongoDB: {recommendation_id}")
        except Exception as e:
            logger.warning(f"保存推荐到MongoDB失败: {e}")
    
    def _save_backtest_result(self, result: BacktestResult):
        """保存回测结果"""
        # 保存交易记录
        if result.trades:
            trades_df = pd.DataFrame([{
                'code': t.code,
                'name': t.name,
                'entry_date': t.entry_date,
                'entry_price': t.entry_price,
                'exit_date': t.exit_date,
                'exit_price': t.exit_price,
                'shares': t.shares,
                'pnl': t.pnl,
                'return_pct': t.return_pct,
                'holding_days': t.holding_days,
                'exit_reason': t.exit_reason.value,
            } for t in result.trades])
            
            # 使用OutputManager统一管理输出路径
            from core.utils.output_manager import get_output_manager, OutputCategory
            
            output_manager = get_output_manager()
            path = output_manager.get_backtest_path(
                category=OutputCategory.ADVISOR_V4,
                filename="backtest_trades.csv",
                add_timestamp=True
            )
            trades_df.to_csv(path, index=False, encoding='utf-8-sig')
            print(f"交易记录已保存: {path}")
        
        # 保存权益曲线
        if result.daily_equity:
            equity_df = pd.DataFrame(result.daily_equity)
            from core.utils.output_manager import get_output_manager, OutputCategory
            
            output_manager = get_output_manager()
            path = output_manager.get_backtest_path(
                category=OutputCategory.ADVISOR_V4,
                filename="backtest_equity.csv",
                add_timestamp=True
            )
            equity_df.to_csv(path, index=False, encoding='utf-8-sig')
            print(f"权益曲线已保存: {path}")
        
        # 保存摘要
        summary = {
            'start_date': result.start_date,
            'end_date': result.end_date,
            'initial_capital': result.initial_capital,
            'final_capital': result.final_capital,
            'total_return': result.total_return,
            'annualized_return': result.annualized_return,
            'max_drawdown': result.max_drawdown,
            'sharpe_ratio': result.sharpe_ratio,
            'total_trades': result.total_trades,
            'win_rate': result.win_rate,
            'hit_10pct_rate': result.hit_10pct_rate,
        }
        
        from core.utils.output_manager import get_output_manager, OutputCategory
        
        output_manager = get_output_manager()
        path = output_manager.get_backtest_path(
            category=OutputCategory.ADVISOR_V4,
            filename="backtest_summary.json",
            add_timestamp=True
        )
        with open(path, 'w') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"回测摘要已保存: {path}")


def main():
    """测试工作流"""
    workflow = AdvisorV4Workflow()
    
    # 测试推荐
    signals = workflow.recommend(top_n=5)


if __name__ == '__main__':
    main()
