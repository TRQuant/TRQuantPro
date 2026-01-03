#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研究结果对比工具
================

对比多次研究/回测的结果，生成对比报告。

功能：
- 对比不同时间点的评估结果
- 对比不同参数设置的回测结果
- 生成可视化对比图表
- 导出对比报告（HTML/CSV）

使用方式:
    python compare_research_results.py result1.json result2.json
    python compare_research_results.py --dir results/ --pattern "*.json"
    python compare_research_results.py --latest 5  # 对比最近5个结果
"""

import sys
import os
import argparse
import json
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
import logging

# 项目路径
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 尝试导入可选依赖
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False


@dataclass
class ComparisonResult:
    """对比结果"""
    files: List[str] = field(default_factory=list)
    metrics: Dict[str, List[Any]] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "files": self.files,
            "metrics": self.metrics,
            "summary": self.summary,
            "timestamp": self.timestamp,
        }


class ResultComparator:
    """
    研究结果对比器
    """
    
    def __init__(self, output_dir: Optional[str] = None):
        self.output_dir = Path(output_dir) if output_dir else Path(PROJECT_ROOT) / "comparison_results"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[Dict] = []
        self.file_paths: List[str] = []
    
    def load_results(self, file_paths: List[str]) -> int:
        """
        加载多个结果文件
        
        Args:
            file_paths: 结果文件路径列表
            
        Returns:
            成功加载的文件数
        """
        loaded = 0
        for path in file_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.results.append(data)
                    self.file_paths.append(path)
                    loaded += 1
                    logger.info(f"✅ 加载: {path}")
            except Exception as e:
                logger.warning(f"⚠️ 加载失败 {path}: {e}")
        
        return loaded
    
    def load_from_directory(
        self, 
        directory: str, 
        pattern: str = "*.json",
        latest_n: Optional[int] = None
    ) -> int:
        """
        从目录加载结果文件
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式
            latest_n: 只加载最新的N个文件
            
        Returns:
            成功加载的文件数
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            logger.error(f"目录不存在: {directory}")
            return 0
        
        files = sorted(dir_path.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if latest_n:
            files = files[:latest_n]
        
        return self.load_results([str(f) for f in files])
    
    def compare(self) -> ComparisonResult:
        """
        执行对比
        
        Returns:
            ComparisonResult: 对比结果
        """
        if len(self.results) < 2:
            logger.warning("至少需要2个结果才能进行对比")
            return ComparisonResult()
        
        result = ComparisonResult(files=self.file_paths)
        
        # 提取关键指标
        metrics = self._extract_metrics()
        result.metrics = metrics
        
        # 计算汇总统计
        result.summary = self._calculate_summary(metrics)
        
        return result
    
    def _extract_metrics(self) -> Dict[str, List[Any]]:
        """提取关键指标"""
        metrics = {
            "file_name": [],
            "timestamp": [],
            "trend_score": [],
            "market_regime": [],
            "risk_score": [],
            "position_ratio": [],
            "accuracy": [],
            "sharpe_ratio": [],
            "max_drawdown": [],
            "total_return": [],
        }
        
        for i, data in enumerate(self.results):
            file_name = Path(self.file_paths[i]).name
            metrics["file_name"].append(file_name)
            
            # 尝试从不同结构中提取指标
            # 评估结果格式
            if "dynamic_signals" in data:
                signals = data["dynamic_signals"]
                metrics["timestamp"].append(signals.get("timestamp", ""))
                metrics["trend_score"].append(signals.get("trend_score"))
                metrics["market_regime"].append(signals.get("market_regime"))
                metrics["risk_score"].append(signals.get("risk_exposure_score"))
                metrics["position_ratio"].append(signals.get("suggested_position_ratio"))
            # 回测结果格式
            elif "targets" in data:
                metrics["timestamp"].append(data.get("timestamp", ""))
                targets = data.get("targets", {})
                metrics["trend_score"].append(targets.get("trend_accuracy_actual"))
                metrics["accuracy"].append(targets.get("trend_accuracy_actual"))
                metrics["sharpe_ratio"].append(targets.get("sharpe_actual"))
                metrics["max_drawdown"].append(targets.get("max_dd_actual"))
            # 策略结果格式
            elif "strategy" in data:
                strategy = data.get("strategy", {})
                metrics["timestamp"].append(data.get("timestamp", ""))
                metrics["sharpe_ratio"].append(strategy.get("sharpe_ratio"))
                metrics["max_drawdown"].append(strategy.get("max_drawdown"))
                metrics["total_return"].append(strategy.get("total_return"))
            else:
                metrics["timestamp"].append("")
            
            # 填充缺失值
            for key in metrics:
                if len(metrics[key]) <= i:
                    metrics[key].append(None)
        
        return metrics
    
    def _calculate_summary(self, metrics: Dict[str, List[Any]]) -> Dict[str, Any]:
        """计算汇总统计"""
        summary = {}
        
        for key, values in metrics.items():
            if key in ["file_name", "timestamp", "market_regime"]:
                continue
            
            # 过滤非空值
            valid_values = [v for v in values if v is not None]
            
            if valid_values:
                try:
                    summary[key] = {
                        "min": min(valid_values),
                        "max": max(valid_values),
                        "mean": sum(valid_values) / len(valid_values),
                        "count": len(valid_values),
                    }
                except (TypeError, ValueError):
                    pass
        
        return summary
    
    def generate_comparison_table(self) -> str:
        """生成对比表格（文本格式）"""
        if not self.results:
            return "无数据"
        
        metrics = self._extract_metrics()
        
        # 生成表格
        lines = []
        lines.append("=" * 80)
        lines.append("研究结果对比")
        lines.append("=" * 80)
        
        # 表头
        headers = ["指标"] + metrics["file_name"]
        col_width = max(15, max(len(h) for h in headers) + 2)
        
        lines.append("|".join(h.center(col_width) for h in headers))
        lines.append("-" * (col_width * len(headers) + len(headers) - 1))
        
        # 数据行
        display_metrics = [
            ("趋势得分", "trend_score"),
            ("市场环境", "market_regime"),
            ("风险得分", "risk_score"),
            ("建议仓位", "position_ratio"),
            ("准确率", "accuracy"),
            ("夏普比率", "sharpe_ratio"),
            ("最大回撤", "max_drawdown"),
            ("总收益", "total_return"),
        ]
        
        for display_name, metric_key in display_metrics:
            values = metrics.get(metric_key, [])
            if not any(v is not None for v in values):
                continue
            
            row = [display_name]
            for v in values:
                if v is None:
                    row.append("-")
                elif isinstance(v, float):
                    if metric_key in ["position_ratio", "accuracy", "max_drawdown", "total_return"]:
                        row.append(f"{v:.2%}")
                    else:
                        row.append(f"{v:.3f}")
                else:
                    row.append(str(v))
            
            lines.append("|".join(str(c).center(col_width) for c in row))
        
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def generate_html_report(self, comparison_result: ComparisonResult) -> str:
        """生成 HTML 对比报告"""
        metrics = comparison_result.metrics
        summary = comparison_result.summary
        
        # 构建表格行
        table_rows = ""
        display_metrics = [
            ("趋势得分", "trend_score"),
            ("市场环境", "market_regime"),
            ("风险得分", "risk_score"),
            ("建议仓位", "position_ratio"),
            ("准确率", "accuracy"),
            ("夏普比率", "sharpe_ratio"),
            ("最大回撤", "max_drawdown"),
            ("总收益", "total_return"),
        ]
        
        for display_name, metric_key in display_metrics:
            values = metrics.get(metric_key, [])
            if not any(v is not None for v in values):
                continue
            
            row = f"<tr><td><strong>{display_name}</strong></td>"
            for v in values:
                if v is None:
                    row += "<td>-</td>"
                elif isinstance(v, float):
                    if metric_key in ["position_ratio", "accuracy", "max_drawdown", "total_return"]:
                        css_class = "positive" if v > 0 else "negative" if v < 0 else ""
                        row += f'<td class="{css_class}">{v:.2%}</td>'
                    else:
                        css_class = "positive" if v > 0 else "negative" if v < 0 else ""
                        row += f'<td class="{css_class}">{v:.3f}</td>'
                else:
                    row += f"<td>{v}</td>"
            row += "</tr>"
            table_rows += row
        
        # 构建汇总行
        summary_rows = ""
        for metric_key, stats in summary.items():
            if isinstance(stats, dict):
                summary_rows += f"""
                <tr>
                    <td>{metric_key}</td>
                    <td>{stats.get('min', '-'):.3f if isinstance(stats.get('min'), float) else stats.get('min', '-')}</td>
                    <td>{stats.get('max', '-'):.3f if isinstance(stats.get('max'), float) else stats.get('max', '-')}</td>
                    <td>{stats.get('mean', '-'):.3f if isinstance(stats.get('mean'), float) else stats.get('mean', '-')}</td>
                </tr>
                """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>研究结果对比报告</title>
    <style>
        body {{
            font-family: "Microsoft YaHei", sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{ margin: 0; }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }}
        th {{
            background-color: #667eea;
            color: white;
        }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .positive {{ color: #26a69a; font-weight: bold; }}
        .negative {{ color: #ef5350; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>研究结果对比报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>对比文件数: {len(comparison_result.files)}</p>
    </div>
    
    <div class="section">
        <h2>指标对比</h2>
        <table>
            <tr>
                <th>指标</th>
                {"".join(f'<th>{Path(f).name}</th>' for f in comparison_result.files)}
            </tr>
            {table_rows}
        </table>
    </div>
    
    <div class="section">
        <h2>统计汇总</h2>
        <table>
            <tr><th>指标</th><th>最小值</th><th>最大值</th><th>平均值</th></tr>
            {summary_rows}
        </table>
    </div>
</body>
</html>"""
        
        return html
    
    def save_report(self, comparison_result: ComparisonResult, filename: str = None) -> str:
        """保存对比报告"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comparison_{timestamp}"
        
        # 保存 JSON
        json_path = self.output_dir / f"{filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(comparison_result.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info(f"✅ JSON报告: {json_path}")
        
        # 保存 HTML
        html_path = self.output_dir / f"{filename}.html"
        html_content = self.generate_html_report(comparison_result)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"✅ HTML报告: {html_path}")
        
        return str(html_path)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="研究结果对比工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument('files', nargs='*', help='要对比的结果文件')
    parser.add_argument('--dir', '-d', type=str, default=None,
                       help='从目录加载结果文件')
    parser.add_argument('--pattern', '-p', type=str, default="*.json",
                       help='文件匹配模式 (默认: *.json)')
    parser.add_argument('--latest', '-n', type=int, default=None,
                       help='只对比最新的N个文件')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='输出目录')
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    comparator = ResultComparator(output_dir=args.output)
    
    # 加载文件
    if args.files:
        comparator.load_results(args.files)
    elif args.dir:
        comparator.load_from_directory(args.dir, args.pattern, args.latest)
    else:
        # 默认目录
        default_dirs = [
            Path(PROJECT_ROOT) / "notebooks" / "research" / "output" / "data",
            Path(PROJECT_ROOT) / "backtest_results",
        ]
        
        for d in default_dirs:
            if d.exists():
                comparator.load_from_directory(str(d), "*.json", args.latest or 5)
    
    if len(comparator.results) < 2:
        logger.error("需要至少2个结果文件才能进行对比")
        return
    
    # 执行对比
    result = comparator.compare()
    
    # 打印文本报告
    print(comparator.generate_comparison_table())
    
    # 保存报告
    comparator.save_report(result)


if __name__ == "__main__":
    main()

