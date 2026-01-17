#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主线工作流集成示例

展示如何将MainlinePredictionFactorCombination集成到9步工作流的步骤3（投资主线）
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 导入依赖
try:
    from markets.ashare.mainline.engine import AShareMainlineEngine
    from core.mainline.mainline_factor_combination import MainlinePredictionFactorCombination
    from core.factors.jqdata_factor_engine import JQDataFactorEngine
    from jqdata.client import JQDataClient
    from config.config_manager import get_config_manager
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"集成依赖不可用: {e}")
    INTEGRATION_AVAILABLE = False


class MainlineWorkflowStep:
    """
    主线工作流步骤（步骤3：投资主线）
    
    集成主线识别引擎和因子组合，提供完整的主线识别和评分功能。
    """
    
    def __init__(self, jq_client: Optional[JQDataClient] = None):
        """
        初始化主线工作流步骤
        
        Args:
            jq_client: JQData客户端（可选，自动创建）
        """
        if not INTEGRATION_AVAILABLE:
            raise ImportError("集成依赖不可用，请检查导入")
        
        # 初始化数据源
        if jq_client:
            self.jq_client = jq_client
        else:
            config_manager = get_config_manager()
            jq_config = config_manager.get_jqdata_config()
            
            self.jq_client = JQDataClient()
            self.jq_client.authenticate(
                jq_config.get('username'),
                jq_config.get('password')
            )
        
        # 初始化引擎
        self.mainline_engine = AShareMainlineEngine()
        self.factor_engine = JQDataFactorEngine()
        self.factor_combo = MainlinePredictionFactorCombination(
            jq_client=self.jq_client,
            factor_engine=self.factor_engine
        )
    
    def execute(
        self,
        market_trend_result: Optional[Dict] = None,
        period: str = 'medium'  # short/medium/long
    ) -> Dict:
        """
        执行主线识别步骤
        
        Args:
            market_trend_result: 步骤2（市场趋势）的结果（可选）
            period: 主线期限（short/medium/long）
        
        Returns:
            {
                'mainlines': List[Mainline],
                'mainline_scores': Dict[str, Dict],  # 因子组合得分
                'validation_results': Optional[Dict],  # 历史数据验证结果
                'data_traces': List[DataTrace],
                'analysis_steps': List[AnalysisStep]
            }
        """
        logger.info(f"开始执行主线识别步骤（期限: {period}）")
        
        # 1. 运行主线识别引擎
        logger.info("步骤1: 运行主线识别引擎...")
        mainline_result = self.mainline_engine.run_full_analysis()
        
        mainlines = mainline_result.get('mainlines', [])
        logger.info(f"识别到 {len(mainlines)} 条主线")
        
        # 2. 使用因子组合对每条主线评分
        logger.info("步骤2: 使用因子组合对主线评分...")
        mainline_scores = {}
        
        for mainline in mainlines:
            try:
                # 获取主线相关行业代码
                industries = self._get_mainline_industries(mainline)
                
                if not industries:
                    logger.warning(f"主线 {mainline.name} 无法获取行业代码，跳过因子评分")
                    continue
                
                # 使用第一个行业代码计算因子组合得分
                industry_code = industries[0]
                current_date = datetime.now().strftime('%Y-%m-%d')
                
                logger.info(f"计算主线 '{mainline.name}' 的因子组合得分（行业: {industry_code}）")
                
                score_result = self.factor_combo.calculate_mainline_score(
                    industry_code=industry_code,
                    date=current_date,
                    period=period
                )
                
                mainline_scores[mainline.name] = {
                    'total_score': score_result['total_score'],
                    'factor_scores': {
                        'macro': score_result['macro_score'],
                        'capital_flow': score_result['capital_flow_score'],
                        'industry_prosperity': score_result['industry_prosperity_score'],
                        'technical_momentum': score_result['technical_momentum_score'],
                        'market_sentiment': score_result['market_sentiment_score']
                    },
                    'factor_details': score_result['factor_details'],
                    'industry_code': industry_code,
                    'period': period
                }
                
                logger.info(f"主线 '{mainline.name}' 因子组合得分: {score_result['total_score']:.2f}")
                
            except Exception as e:
                logger.error(f"计算主线 {mainline.name} 因子得分失败: {e}")
                continue
        
        # 3. 历史数据验证（可选）
        validation_results = None
        if len(mainlines) > 0:
            try:
                logger.info("步骤3: 运行历史数据验证...")
                validation_results = self._run_validation(mainlines, period)
            except Exception as e:
                logger.warning(f"历史数据验证失败: {e}")
        
        return {
            'mainlines': mainlines,
            'mainline_scores': mainline_scores,
            'validation_results': validation_results,
            'data_traces': mainline_result.get('data_traces', []),
            'analysis_steps': mainline_result.get('analysis_steps', []),
            'period': period,
            'execution_time': datetime.now().isoformat()
        }
    
    def _get_mainline_industries(self, mainline) -> List[str]:
        """
        获取主线相关行业代码
        
        Args:
            mainline: 主线对象
        
        Returns:
            行业代码列表（如 ['801010', '801020']）
        """
        # 方法1: 从主线对象获取行业信息
        if hasattr(mainline, 'sectors') and mainline.sectors:
            # 将行业名称转换为行业代码
            # 这里需要建立行业名称到代码的映射
            industries = []
            for sector in mainline.sectors:
                # 简化处理：假设行业名称可以直接使用
                # 实际应该使用行业映射表
                industry_code = self._map_sector_to_code(sector)
                if industry_code:
                    industries.append(industry_code)
            return industries
        
        # 方法2: 从主线名称推断行业
        # 这里简化处理，实际应该使用更智能的映射
        return []
    
    def _map_sector_to_code(self, sector_name: str) -> Optional[str]:
        """
        将行业名称映射到行业代码
        
        Args:
            sector_name: 行业名称（如 "人工智能"、"半导体"）
        
        Returns:
            行业代码（如 "801010"）或None
        """
        # 行业名称到代码的映射表（简化示例）
        # 实际应该从JQData获取完整的行业映射
        sector_mapping = {
            '人工智能': '801010',
            'AI': '801010',
            '半导体': '801020',
            '新能源': '801030',
            '消费电子': '801040',
            '医药生物': '801050',
            # 可以扩展更多映射
        }
        
        # 模糊匹配
        for key, code in sector_mapping.items():
            if key in sector_name or sector_name in key:
                return code
        
        return None
    
    def _run_validation(self, mainlines: List, period: str) -> Optional[Dict]:
        """
        运行历史数据验证
        
        Args:
            mainlines: 主线列表
            period: 期限
        
        Returns:
            验证结果
        """
        try:
            from research.mainline_factor_validation import MainlineFactorValidator
            
            validator = MainlineFactorValidator(self.jq_client)
            
            # 获取所有主线涉及的行业
            all_industries = []
            for mainline in mainlines:
                industries = self._get_mainline_industries(mainline)
                all_industries.extend(industries)
            
            if not all_industries:
                logger.warning("无法获取行业代码，跳过验证")
                return None
            
            # 去重
            unique_industries = list(set(all_industries))
            
            # 根据期限选择验证时间范围
            end_date = datetime.now().strftime('%Y-%m-%d')
            if period == 'short':
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            elif period == 'medium':
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            else:  # long
                start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
            
            # 获取行业股票列表
            all_stocks = []
            for industry_code in unique_industries:
                stocks = self.factor_combo._get_industry_stocks(industry_code, end_date)
                all_stocks.extend(stocks)
            
            if not all_stocks:
                logger.warning("无法获取股票列表，跳过验证")
                return None
            
            # 去重
            unique_stocks = list(set(all_stocks))[:100]  # 限制股票数量
            
            # 构建因子组合（使用默认权重）
            factor_combination = {
                'macro': 0.20,
                'capital_flow': 0.30,
                'industry_prosperity': 0.25,
                'technical_momentum': 0.15,
                'market_sentiment': 0.10
            }
            
            # 运行验证
            validation_result = validator.validate_factor_combination(
                factor_combination=factor_combination,
                stocks=unique_stocks,
                start_date=start_date,
                end_date=end_date,
                period='W'  # 周度调仓
            )
            
            return validation_result
            
        except Exception as e:
            logger.error(f"历史数据验证失败: {e}")
            return None


def main():
    """示例：使用主线工作流步骤"""
    try:
        # 创建主线工作流步骤
        workflow_step = MainlineWorkflowStep()
        
        # 执行主线识别
        result = workflow_step.execute(period='medium')
        
        # 输出结果
        print("\n" + "="*60)
        print("主线识别结果")
        print("="*60)
        
        print(f"\n识别到 {len(result['mainlines'])} 条主线:")
        for mainline in result['mainlines']:
            print(f"  - {mainline.name}")
        
        print(f"\n因子组合得分:")
        for mainline_name, score_data in result['mainline_scores'].items():
            print(f"\n  {mainline_name}:")
            print(f"    总分: {score_data['total_score']:.2f}")
            print(f"    宏观: {score_data['factor_scores']['macro']:.2f}")
            print(f"    资金流: {score_data['factor_scores']['capital_flow']:.2f}")
            print(f"    行业景气: {score_data['factor_scores']['industry_prosperity']:.2f}")
            print(f"    技术动量: {score_data['factor_scores']['technical_momentum']:.2f}")
            print(f"    市场情绪: {score_data['factor_scores']['market_sentiment']:.2f}")
        
        if result['validation_results']:
            print(f"\n历史数据验证结果:")
            print(f"  有效因子比例: {result['validation_results'].get('valid_ratio', 0):.2%}")
        
    except Exception as e:
        logger.error(f"执行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    from datetime import timedelta
    main()

