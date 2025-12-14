"""
文件名: code_8_6_generate_report.py
保存路径: code_library/008_Chapter8_Backtest/8.6/code_8_6_generate_report.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.6_Backtest_Report_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: generate_report

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, Any
from pathlib import Path
from jinja2 import Template
import json

class BacktestReportGenerator:
    """回测报告生成器"""
    
    def generate_report(
        self,
        bt_result: Any,
        return_analysis: Dict[str, Any] = None,
        risk_analysis: Dict[str, Any] = None,
        trade_analysis: Dict[str, Any] = None,
        output_format: str = 'html'
    ) -> Dict[str, Any]:
            """
    generate_report函数
    
    **设计原理**：
    - **核心功能**：实现generate_report的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        # 收集报告数据
        report_data = self._collect_report_data(
            bt_result, return_analysis, risk_analysis, trade_analysis
        )
        
        # 生成报告内容
        if output_format == 'html':
            report_content = self._generate_html_report(report_data)
        elif output_format == 'pdf':
            report_content = self._generate_pdf_report(report_data)
        elif output_format == 'markdown':
            report_content = self._generate_markdown_report(report_data)
        else:
            raise ValueError(f"不支持的报告格式: {output_format}")
        
        # 保存报告
        report_path = self._save_report(report_content, output_format)
        
        return {
            'report_path': report_path,
            'report_format': output_format,
            'report_data': report_data
        }
    
    def _collect_report_data(
        self,
        bt_result: Any,
        return_analysis: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        trade_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """收集报告数据"""
        return {
            'strategy_info': {
                'name': bt_result.strategy_name,
                'start_date': bt_result.start_date,
                'end_date': bt_result.end_date,
                'initial_capital': bt_result.initial_capital
            },
            'return_metrics': return_analysis or {},
            'risk_metrics': risk_analysis or {},
            'trade_metrics': trade_analysis or {},
            'equity_curve': bt_result.equity_curve.to_dict('records') if hasattr(bt_result, 'equity_curve') else []
        }
    
    def _generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """生成HTML报告"""
        template_path = Path(__file__).parent / 'templates' / 'backtest_report.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        return template.render(**report_data)