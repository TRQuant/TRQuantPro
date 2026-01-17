# -*- coding: utf-8 -*-
"""
报告管理器
==========
T1.9.1 报告生成系统核心模块

功能：
1. 统一的报告生成接口
2. 多种报告类型（回测/分析/对比/诊断）
3. 多种输出格式（HTML/PDF/Markdown）
4. 报告模板管理
5. 报告存储和查询
6. GUI 友好的 API
"""

import logging
import os
import json
import uuid
import shutil
from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


# ==================== 枚举定义 ====================

class ReportType(Enum):
    """报告类型"""
    BACKTEST = "backtest"           # 回测报告
    ANALYSIS = "analysis"           # 策略分析报告
    COMPARISON = "comparison"       # 策略对比报告
    DIAGNOSIS = "diagnosis"         # 策略诊断报告
    FACTOR = "factor"               # 因子分析报告
    RISK = "risk"                   # 风险分析报告


class ReportFormat(Enum):
    """报告格式"""
    HTML = "html"
    PDF = "pdf"
    MARKDOWN = "md"
    JSON = "json"


class ReportStatus(Enum):
    """报告状态"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


# ==================== 数据类 ====================

@dataclass
class ReportConfig:
    """报告配置"""
    report_type: ReportType = ReportType.BACKTEST
    format: ReportFormat = ReportFormat.HTML
    title: str = "回测报告"
    
    # 内容配置
    include_charts: bool = True
    include_trades: bool = True
    include_positions: bool = True
    include_risk_analysis: bool = True
    
    # 样式配置
    theme: str = "dark"  # dark/light
    template: str = "default"
    
    # 输出配置
    output_dir: str = "output/reports"
    filename: str = None  # 自动生成
    
    def to_dict(self) -> Dict:
        return {
            "report_type": self.report_type.value,
            "format": self.format.value,
            "title": self.title,
            "include_charts": self.include_charts,
            "include_trades": self.include_trades,
            "include_positions": self.include_positions,
            "include_risk_analysis": self.include_risk_analysis,
            "theme": self.theme,
            "template": self.template,
            "output_dir": self.output_dir,
            "filename": self.filename,
        }


@dataclass
class ReportMetadata:
    """报告元数据"""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    report_type: str = "backtest"
    format: str = "html"
    title: str = ""
    status: str = "completed"
    
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    file_path: str = ""
    file_size: int = 0
    
    # 关联数据
    strategy_name: str = ""
    backtest_id: str = ""
    
    # 摘要指标
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ==================== 报告管理器 ====================

class ReportManager:
    """
    报告管理器
    
    提供统一的报告生成、存储、查询接口
    设计为 GUI 友好，支持异步生成和进度回调
    """
    
    def __init__(self, output_dir: str = "output/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 元数据存储
        self._metadata_file = self.output_dir / "reports_index.json"
        self._reports_index: Dict[str, ReportMetadata] = {}
        
        # MongoDB
        self._mongo_db = None
        self._init_mongodb()
        
        # 加载索引
        self._load_index()
        
        # 依赖检查
        self._check_dependencies()
    
    def _init_mongodb(self):
        """初始化 MongoDB"""
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            self._mongo_db = client.get_database("trquant")
            logger.info("✅ 报告系统 MongoDB 已连接")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB 连接失败: {e}")
    
    def _load_index(self):
        """加载报告索引"""
        if self._metadata_file.exists():
            try:
                with open(self._metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        meta = ReportMetadata(**item)
                        self._reports_index[meta.report_id] = meta
            except Exception as e:
                logger.warning(f"加载报告索引失败: {e}")
    
    def _save_index(self):
        """保存报告索引"""
        try:
            data = [m.to_dict() for m in self._reports_index.values()]
            with open(self._metadata_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存报告索引失败: {e}")
    
    def _check_dependencies(self):
        """检查依赖"""
        self._has_matplotlib = False
        self._has_reportlab = False
        self._has_bt_report = False
        
        try:
            import matplotlib
            self._has_matplotlib = True
        except ImportError:
            pass
        
        try:
            import reportlab
            self._has_reportlab = True
        except ImportError:
            pass
        
        try:
            from bullet_trade.core.analysis import generate_report
            self._has_bt_report = True
        except ImportError:
            pass
    
    # ==================== 生成报告 ====================
    
    def generate_backtest_report(
        self,
        result: Any,  # UnifiedBacktestResult or BTResult or Dict
        config: ReportConfig = None,
        strategy_name: str = "策略",
        progress_callback: callable = None
    ) -> Tuple[str, ReportMetadata]:
        """
        生成回测报告
        
        Args:
            result: 回测结果（支持多种格式）
            config: 报告配置
            strategy_name: 策略名称
            progress_callback: 进度回调 (progress: float, message: str)
            
        Returns:
            (报告文件路径, 元数据)
        """
        config = config or ReportConfig()
        config.title = config.title or f"{strategy_name} - 回测报告"
        
        if progress_callback:
            progress_callback(0.1, "准备生成报告...")
        
        # 标准化结果
        metrics, daily_returns, equity_curve, trades = self._normalize_result(result)
        
        if progress_callback:
            progress_callback(0.3, "生成报告内容...")
        
        # 根据格式生成报告
        if config.format == ReportFormat.HTML:
            file_path = self._generate_html_report(
                metrics, daily_returns, equity_curve, trades,
                config, strategy_name, progress_callback
            )
        elif config.format == ReportFormat.PDF:
            file_path = self._generate_pdf_report(
                metrics, daily_returns, equity_curve, trades,
                config, strategy_name, progress_callback
            )
        elif config.format == ReportFormat.MARKDOWN:
            file_path = self._generate_markdown_report(
                metrics, config, strategy_name
            )
        elif config.format == ReportFormat.JSON:
            file_path = self._generate_json_report(
                metrics, config, strategy_name
            )
        else:
            file_path = self._generate_html_report(
                metrics, daily_returns, equity_curve, trades,
                config, strategy_name, progress_callback
            )
        
        if progress_callback:
            progress_callback(0.9, "保存元数据...")
        
        # 创建元数据
        metadata = ReportMetadata(
            report_type=config.report_type.value,
            format=config.format.value,
            title=config.title,
            file_path=str(file_path),
            file_size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            strategy_name=strategy_name,
            summary={
                "total_return": metrics.get("total_return", 0),
                "sharpe_ratio": metrics.get("sharpe_ratio", 0),
                "max_drawdown": metrics.get("max_drawdown", 0),
            }
        )
        
        # 保存元数据
        self._reports_index[metadata.report_id] = metadata
        self._save_index()
        
        if self._mongo_db is not None:
            try:
                self._mongo_db.reports.insert_one(metadata.to_dict())
            except Exception as e:
                logger.warning(f"保存报告元数据到 MongoDB 失败: {e}")
        
        if progress_callback:
            progress_callback(1.0, "报告生成完成")
        
        logger.info(f"✅ 报告已生成: {file_path}")
        
        return str(file_path), metadata
    
    def generate_comparison_report(
        self,
        results: Dict[str, Any],  # {策略名: 结果}
        config: ReportConfig = None,
        progress_callback: callable = None
    ) -> Tuple[str, ReportMetadata]:
        """生成策略对比报告"""
        config = config or ReportConfig(report_type=ReportType.COMPARISON)
        config.title = config.title or "策略对比报告"
        
        if progress_callback:
            progress_callback(0.1, "准备对比数据...")
        
        # 收集所有策略的指标
        comparison_data = []
        equity_curves = {}
        
        for name, result in results.items():
            metrics, daily_returns, equity_curve, _ = self._normalize_result(result)
            comparison_data.append({
                "name": name,
                **metrics
            })
            if equity_curve is not None:
                equity_curves[name] = equity_curve
        
        if progress_callback:
            progress_callback(0.5, "生成对比报告...")
        
        # 生成对比报告
        file_path = self._generate_comparison_html(
            comparison_data, equity_curves, config
        )
        
        # 创建元数据
        metadata = ReportMetadata(
            report_type=ReportType.COMPARISON.value,
            format=config.format.value,
            title=config.title,
            file_path=str(file_path),
            file_size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            summary={"strategies_count": len(results)}
        )
        
        self._reports_index[metadata.report_id] = metadata
        self._save_index()
        
        if progress_callback:
            progress_callback(1.0, "对比报告生成完成")
        
        return str(file_path), metadata
    
    def generate_diagnosis_report(
        self,
        result: Any,
        strategy_name: str = "策略",
        config: ReportConfig = None
    ) -> Tuple[str, ReportMetadata]:
        """生成策略诊断报告"""
        config = config or ReportConfig(report_type=ReportType.DIAGNOSIS)
        config.title = f"{strategy_name} - 诊断报告"
        
        metrics, daily_returns, _, trades = self._normalize_result(result)
        
        # 诊断分析
        diagnosis = self._analyze_strategy(metrics, daily_returns, trades)
        
        # 生成报告
        file_path = self._generate_diagnosis_html(
            metrics, diagnosis, config, strategy_name
        )
        
        metadata = ReportMetadata(
            report_type=ReportType.DIAGNOSIS.value,
            format=config.format.value,
            title=config.title,
            file_path=str(file_path),
            strategy_name=strategy_name,
            summary={"diagnosis_score": diagnosis.get("score", 0)}
        )
        
        self._reports_index[metadata.report_id] = metadata
        self._save_index()
        
        return str(file_path), metadata
    
    # ==================== 内部方法 ====================
    
    def _normalize_result(self, result) -> Tuple[Dict, Any, Any, Any]:
        """标准化结果格式"""
        metrics = {}
        daily_returns = None
        equity_curve = None
        trades = None
        
        if isinstance(result, dict):
            metrics = result.get("metrics", result)
            daily_returns = result.get("daily_returns")
            equity_curve = result.get("equity_curve")
            trades = result.get("trades")
        else:
            # UnifiedBacktestResult or BTResult
            if hasattr(result, 'total_return'):
                metrics['total_return'] = result.total_return
            if hasattr(result, 'annual_return'):
                metrics['annual_return'] = result.annual_return
            if hasattr(result, 'sharpe_ratio'):
                metrics['sharpe_ratio'] = result.sharpe_ratio
            if hasattr(result, 'max_drawdown'):
                metrics['max_drawdown'] = result.max_drawdown
            if hasattr(result, 'win_rate'):
                metrics['win_rate'] = result.win_rate
            if hasattr(result, 'calmar_ratio'):
                metrics['calmar_ratio'] = result.calmar_ratio
            if hasattr(result, 'sortino_ratio'):
                metrics['sortino_ratio'] = result.sortino_ratio
            if hasattr(result, 'total_trades'):
                metrics['total_trades'] = result.total_trades
            if hasattr(result, 'profit_factor'):
                metrics['profit_factor'] = result.profit_factor
            
            if hasattr(result, 'daily_returns'):
                daily_returns = result.daily_returns
            if hasattr(result, 'equity_curve'):
                equity_curve = result.equity_curve
            if hasattr(result, 'trades'):
                trades = result.trades
            elif hasattr(result, 'daily_records'):
                # BTResult
                daily_returns = result.daily_records
        
        return metrics, daily_returns, equity_curve, trades
    
    def _generate_html_report(
        self, metrics, daily_returns, equity_curve, trades,
        config, strategy_name, progress_callback
    ) -> str:
        """生成 HTML 报告"""
        # 使用 result_analyzer
        try:
            from core.backtest.result_analyzer import BacktestResultAnalyzer
            
            analyzer = BacktestResultAnalyzer(str(self.output_dir))
            
            # 创建伪结果对象
            class FakeResult:
                pass
            
            fake = FakeResult()
            fake.total_return = metrics.get('total_return', 0)
            fake.annual_return = metrics.get('annual_return', 0)
            fake.sharpe_ratio = metrics.get('sharpe_ratio', 0)
            fake.max_drawdown = metrics.get('max_drawdown', 0)
            fake.win_rate = metrics.get('win_rate', 0)
            fake.calmar_ratio = metrics.get('calmar_ratio', 0)
            fake.sortino_ratio = metrics.get('sortino_ratio', 0)
            fake.total_trades = metrics.get('total_trades', 0)
            fake.profit_factor = metrics.get('profit_factor', 0)
            fake.daily_returns = daily_returns
            fake.equity_curve = equity_curve
            fake.drawdown_curve = None
            fake.trades = trades
            fake.engine_used = "unified"
            fake.duration_seconds = 0
            
            if progress_callback:
                progress_callback(0.6, "生成图表...")
            
            return analyzer.generate_enhanced_html_report(
                fake,
                output_dir=self.output_dir,
                strategy_name=strategy_name
            )
            
        except Exception as e:
            logger.warning(f"使用 result_analyzer 失败: {e}，使用简化版本")
            return self._generate_simple_html(metrics, config, strategy_name)
    
    def _generate_simple_html(self, metrics, config, strategy_name) -> str:
        """生成简化 HTML 报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = config.filename or f"{strategy_name}_report_{timestamp}.html"
        file_path = self.output_dir / filename
        
        theme_bg = "#1a1a2e" if config.theme == "dark" else "#ffffff"
        theme_text = "#eee" if config.theme == "dark" else "#333"
        theme_card = "#16213e" if config.theme == "dark" else "#f5f5f5"
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{config.title}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: {theme_bg}; color: {theme_text}; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ text-align: center; }}
        .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }}
        .metric {{ background: {theme_card}; padding: 20px; border-radius: 10px; text-align: center; }}
        .metric-value {{ font-size: 2rem; font-weight: bold; color: #2196F3; }}
        .metric-label {{ color: #888; margin-top: 5px; }}
        .positive {{ color: #4CAF50; }}
        .negative {{ color: #F44336; }}
        .footer {{ text-align: center; margin-top: 40px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {config.title}</h1>
        <p style="text-align:center;color:#888;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-value {'positive' if metrics.get('total_return', 0) >= 0 else 'negative'}">
                    {metrics.get('total_return', 0) * 100:.2f}%
                </div>
                <div class="metric-label">总收益率</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics.get('sharpe_ratio', 0):.2f}</div>
                <div class="metric-label">夏普比率</div>
            </div>
            <div class="metric">
                <div class="metric-value negative">{abs(metrics.get('max_drawdown', 0)) * 100:.2f}%</div>
                <div class="metric-label">最大回撤</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics.get('annual_return', 0) * 100:.2f}%</div>
                <div class="metric-label">年化收益</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics.get('win_rate', 0) * 100:.1f}%</div>
                <div class="metric-label">胜率</div>
            </div>
            <div class="metric">
                <div class="metric-value">{metrics.get('total_trades', 0)}</div>
                <div class="metric-label">交易次数</div>
            </div>
        </div>
        
        <div class="footer">
            <p>TRQuant 韬睿量化系统 | ReportManager</p>
        </div>
    </div>
</body>
</html>'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(file_path)
    
    def _generate_pdf_report(
        self, metrics, daily_returns, equity_curve, trades,
        config, strategy_name, progress_callback
    ) -> str:
        """生成 PDF 报告"""
        try:
            from core.report_generator import ReportGenerator
            
            generator = ReportGenerator()
            
            result_dict = {
                "metrics": metrics,
                "summary": {
                    "start_date": "N/A",
                    "end_date": "N/A",
                    "initial_capital": 1000000
                },
                "trades": trades or []
            }
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = config.filename or f"{strategy_name}_report_{timestamp}.pdf"
            file_path = self.output_dir / filename
            
            return generator.generate_report(result_dict, str(file_path), strategy_name)
            
        except Exception as e:
            logger.warning(f"PDF 生成失败: {e}，改用 HTML")
            config.format = ReportFormat.HTML
            return self._generate_simple_html(metrics, config, strategy_name)
    
    def _generate_markdown_report(self, metrics, config, strategy_name) -> str:
        """生成 Markdown 报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = config.filename or f"{strategy_name}_report_{timestamp}.md"
        file_path = self.output_dir / filename
        
        md = f'''# {config.title}

> 策略: {strategy_name}  
> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 核心指标

| 指标 | 数值 |
|------|------|
| 总收益率 | {metrics.get('total_return', 0) * 100:.2f}% |
| 年化收益 | {metrics.get('annual_return', 0) * 100:.2f}% |
| 夏普比率 | {metrics.get('sharpe_ratio', 0):.2f} |
| 最大回撤 | {abs(metrics.get('max_drawdown', 0)) * 100:.2f}% |
| 胜率 | {metrics.get('win_rate', 0) * 100:.1f}% |
| 交易次数 | {metrics.get('total_trades', 0)} |

## 风险指标

| 指标 | 数值 |
|------|------|
| 卡尔玛比率 | {metrics.get('calmar_ratio', 0):.2f} |
| 索提诺比率 | {metrics.get('sortino_ratio', 0):.2f} |
| 盈亏比 | {metrics.get('profit_factor', 0):.2f} |

---
*TRQuant 韬睿量化系统*
'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        return str(file_path)
    
    def _generate_json_report(self, metrics, config, strategy_name) -> str:
        """生成 JSON 报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = config.filename or f"{strategy_name}_report_{timestamp}.json"
        file_path = self.output_dir / filename
        
        data = {
            "title": config.title,
            "strategy": strategy_name,
            "generated_at": datetime.now().isoformat(),
            "metrics": metrics,
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return str(file_path)
    
    def _generate_comparison_html(self, comparison_data, equity_curves, config) -> str:
        """生成对比报告 HTML"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = config.filename or f"comparison_report_{timestamp}.html"
        file_path = self.output_dir / filename
        
        # 生成表格行
        rows = ""
        for data in comparison_data:
            ret_class = "positive" if data.get('total_return', 0) >= 0 else "negative"
            rows += f'''
            <tr>
                <td>{data.get('name', 'N/A')}</td>
                <td class="{ret_class}">{data.get('total_return', 0) * 100:.2f}%</td>
                <td>{data.get('sharpe_ratio', 0):.2f}</td>
                <td class="negative">{abs(data.get('max_drawdown', 0)) * 100:.2f}%</td>
                <td>{data.get('win_rate', 0) * 100:.1f}%</td>
            </tr>'''
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{config.title}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        th, td {{ padding: 15px; text-align: center; border-bottom: 1px solid #333; }}
        th {{ background: #16213e; }}
        .positive {{ color: #4CAF50; }}
        .negative {{ color: #F44336; }}
        tr:hover {{ background: rgba(255,255,255,0.05); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {config.title}</h1>
        <p style="text-align:center;color:#888;">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <table>
            <tr>
                <th>策略</th>
                <th>总收益</th>
                <th>夏普比率</th>
                <th>最大回撤</th>
                <th>胜率</th>
            </tr>
            {rows}
        </table>
        
        <div style="text-align:center;margin-top:40px;color:#666;">
            TRQuant 韬睿量化系统
        </div>
    </div>
</body>
</html>'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(file_path)
    
    def _analyze_strategy(self, metrics, daily_returns, trades) -> Dict:
        """分析策略，生成诊断"""
        diagnosis = {
            "score": 0,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
        }
        
        score = 50  # 基础分
        
        # 收益分析
        total_return = metrics.get('total_return', 0)
        if total_return > 0.2:
            score += 15
            diagnosis["strengths"].append("收益表现优秀 (>20%)")
        elif total_return > 0:
            score += 5
            diagnosis["strengths"].append("策略盈利")
        else:
            score -= 10
            diagnosis["weaknesses"].append("策略亏损")
            diagnosis["suggestions"].append("检查策略逻辑，考虑调整参数")
        
        # 风险分析
        sharpe = metrics.get('sharpe_ratio', 0)
        if sharpe > 1.5:
            score += 15
            diagnosis["strengths"].append("风险调整收益优秀 (夏普>1.5)")
        elif sharpe > 0.5:
            score += 5
            diagnosis["strengths"].append("风险调整收益良好")
        else:
            score -= 5
            diagnosis["weaknesses"].append("夏普比率偏低")
            diagnosis["suggestions"].append("考虑加入止损机制降低波动")
        
        # 回撤分析
        max_dd = abs(metrics.get('max_drawdown', 0))
        if max_dd < 0.1:
            score += 10
            diagnosis["strengths"].append("回撤控制优秀 (<10%)")
        elif max_dd < 0.2:
            score += 5
        else:
            score -= 10
            diagnosis["weaknesses"].append("最大回撤过大")
            diagnosis["suggestions"].append("加强风控，设置止损线")
        
        # 胜率分析
        win_rate = metrics.get('win_rate', 0)
        if win_rate > 0.6:
            score += 10
            diagnosis["strengths"].append("胜率较高 (>60%)")
        elif win_rate < 0.4:
            score -= 5
            diagnosis["weaknesses"].append("胜率偏低")
            diagnosis["suggestions"].append("优化选股逻辑")
        
        diagnosis["score"] = max(0, min(100, score))
        
        return diagnosis
    
    def _generate_diagnosis_html(self, metrics, diagnosis, config, strategy_name) -> str:
        """生成诊断报告 HTML"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = config.filename or f"{strategy_name}_diagnosis_{timestamp}.html"
        file_path = self.output_dir / filename
        
        # 评分颜色
        score = diagnosis.get("score", 0)
        if score >= 80:
            score_color = "#4CAF50"
            score_text = "优秀"
        elif score >= 60:
            score_color = "#2196F3"
            score_text = "良好"
        elif score >= 40:
            score_color = "#FF9800"
            score_text = "一般"
        else:
            score_color = "#F44336"
            score_text = "需改进"
        
        strengths_html = "".join(f"<li>✅ {s}</li>" for s in diagnosis.get("strengths", []))
        weaknesses_html = "".join(f"<li>⚠️ {w}</li>" for w in diagnosis.get("weaknesses", []))
        suggestions_html = "".join(f"<li>💡 {s}</li>" for s in diagnosis.get("suggestions", []))
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{config.title}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ text-align: center; }}
        .score-card {{ text-align: center; padding: 40px; background: #16213e; border-radius: 20px; margin: 30px 0; }}
        .score {{ font-size: 5rem; font-weight: bold; color: {score_color}; }}
        .score-label {{ font-size: 1.5rem; color: #888; }}
        .section {{ background: #16213e; border-radius: 12px; padding: 20px; margin: 20px 0; }}
        .section h3 {{ margin-top: 0; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 {config.title}</h1>
        <p style="text-align:center;color:#888;">策略: {strategy_name}</p>
        
        <div class="score-card">
            <div class="score">{score}</div>
            <div class="score-label">{score_text}</div>
        </div>
        
        <div class="section">
            <h3>💪 优势</h3>
            <ul>{strengths_html or '<li>暂无</li>'}</ul>
        </div>
        
        <div class="section">
            <h3>⚠️ 不足</h3>
            <ul>{weaknesses_html or '<li>暂无</li>'}</ul>
        </div>
        
        <div class="section">
            <h3>💡 建议</h3>
            <ul>{suggestions_html or '<li>暂无</li>'}</ul>
        </div>
        
        <div style="text-align:center;margin-top:40px;color:#666;">
            TRQuant 韬睿量化系统
        </div>
    </div>
</body>
</html>'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return str(file_path)
    
    # ==================== 查询接口 ====================
    
    def list_reports(
        self,
        report_type: ReportType = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[ReportMetadata], int]:
        """列出报告"""
        reports = list(self._reports_index.values())
        
        if report_type:
            reports = [r for r in reports if r.report_type == report_type.value]
        
        # 按创建时间倒序
        reports.sort(key=lambda r: r.created_at, reverse=True)
        
        total = len(reports)
        return reports[offset:offset + limit], total
    
    def get_report(self, report_id: str) -> Optional[ReportMetadata]:
        """获取报告信息"""
        return self._reports_index.get(report_id)
    
    def delete_report(self, report_id: str) -> bool:
        """删除报告"""
        if report_id not in self._reports_index:
            return False
        
        metadata = self._reports_index[report_id]
        
        # 删除文件
        if os.path.exists(metadata.file_path):
            try:
                os.remove(metadata.file_path)
            except Exception as e:
                logger.warning(f"删除报告文件失败: {e}")
        
        # 删除索引
        del self._reports_index[report_id]
        self._save_index()
        
        return True
    
    def get_report_content(self, report_id: str) -> Optional[str]:
        """获取报告内容（用于 GUI 显示）"""
        metadata = self.get_report(report_id)
        if not metadata:
            return None
        
        if os.path.exists(metadata.file_path):
            with open(metadata.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        return None


# ==================== 单例 ====================

_report_manager: Optional[ReportManager] = None


def get_report_manager() -> ReportManager:
    """获取报告管理器单例"""
    global _report_manager
    if _report_manager is None:
        _report_manager = ReportManager()
    return _report_manager


# ==================== 便捷函数（GUI 调用接口）====================

def generate_report(
    result: Any,
    report_type: str = "backtest",
    format: str = "html",
    strategy_name: str = "策略",
    **kwargs
) -> Dict[str, Any]:
    """
    生成报告（GUI 友好接口）
    
    Args:
        result: 回测结果
        report_type: 报告类型 (backtest/comparison/diagnosis)
        format: 输出格式 (html/pdf/md/json)
        strategy_name: 策略名称
        
    Returns:
        {"success": bool, "report_id": str, "file_path": str, "error": str}
    """
    try:
        manager = get_report_manager()
        
        config = ReportConfig(
            report_type=ReportType(report_type),
            format=ReportFormat(format),
            **kwargs
        )
        
        if report_type == "backtest":
            file_path, metadata = manager.generate_backtest_report(
                result, config, strategy_name
            )
        elif report_type == "comparison":
            file_path, metadata = manager.generate_comparison_report(
                result, config
            )
        elif report_type == "diagnosis":
            file_path, metadata = manager.generate_diagnosis_report(
                result, strategy_name, config
            )
        else:
            file_path, metadata = manager.generate_backtest_report(
                result, config, strategy_name
            )
        
        return {
            "success": True,
            "report_id": metadata.report_id,
            "file_path": file_path,
            "title": metadata.title,
        }
        
    except Exception as e:
        logger.error(f"生成报告失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def list_reports(
    report_type: str = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    列出报告（GUI 友好接口）
    """
    try:
        manager = get_report_manager()
        
        rt = ReportType(report_type) if report_type else None
        reports, total = manager.list_reports(rt, limit)
        
        return {
            "success": True,
            "total": total,
            "reports": [r.to_dict() for r in reports]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_report(report_id: str) -> Dict[str, Any]:
    """
    获取报告详情（GUI 友好接口）
    """
    try:
        manager = get_report_manager()
        
        metadata = manager.get_report(report_id)
        if not metadata:
            return {"success": False, "error": "报告不存在"}
        
        content = manager.get_report_content(report_id)
        
        return {
            "success": True,
            "metadata": metadata.to_dict(),
            "content": content,
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


__all__ = [
    "ReportManager",
    "ReportConfig",
    "ReportType",
    "ReportFormat",
    "ReportStatus",
    "ReportMetadata",
    "get_report_manager",
    "generate_report",
    "list_reports",
    "get_report",
]
