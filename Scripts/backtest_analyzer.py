#!/usr/bin/env python3
"""
回测结果分析器

用法:
    python backtest_analyzer.py <backtest_id> [--output output_dir]

功能:
    - 分析回测结果
    - 生成可视化图表
    - 输出分析报告
"""

import json
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import argparse


class BacktestAnalyzer:
    def __init__(self, backtest_id, output_dir="analysis_reports"):
        self.backtest_id = backtest_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 回测文件路径
        self.backtest_path = Path(f"backtests/{backtest_id}")
        self.summary_file = self.backtest_path / f"{backtest_id}-summary.json"
        self.orders_file = self.backtest_path / f"{backtest_id}-order-events.json"
        self.log_file = self.backtest_path / f"{backtest_id}-log.txt"
        
        # 数据
        self.summary = None
        self.orders = None
        self.logs = None
        
    def load_data(self):
        """加载回测数据"""
        print(f"正在加载回测数据: {self.backtest_id}")
        
        # 加载摘要
        if self.summary_file.exists():
            with open(self.summary_file, 'r') as f:
                self.summary = json.load(f)
            print("✅ 摘要数据加载完成")
        else:
            print(f"❌ 摘要文件不存在: {self.summary_file}")
            return False
            
        # 加载订单
        if self.orders_file.exists():
            with open(self.orders_file, 'r') as f:
                self.orders = json.load(f)
            print("✅ 订单数据加载完成")
        else:
            print(f"❌ 订单文件不存在: {self.orders_file}")
            
        # 加载日志
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                self.logs = f.read()
            print("✅ 日志数据加载完成")
        else:
            print(f"❌ 日志文件不存在: {self.log_file}")
            
        return True
    
    def analyze_performance(self):
        """分析性能指标"""
        if not self.summary:
            return None
            
        perf = self.summary.get('TotalPerformance', {})
        
        analysis = {
            '基本信息': {
                '回测ID': self.backtest_id,
                '开始时间': self.summary.get('StartTime', 'N/A'),
                '结束时间': self.summary.get('EndTime', 'N/A'),
                '回测天数': self.summary.get('BacktestDays', 'N/A')
            },
            '收益指标': {
                '总收益率': f"{perf.get('TotalReturn', 0):.2%}",
                '年化收益率': f"{perf.get('TotalReturn', 0):.2%}",
                '基准收益率': f"{perf.get('BenchmarkReturn', 0):.2%}",
                '超额收益': f"{perf.get('TotalReturn', 0) - perf.get('BenchmarkReturn', 0):.2%}"
            },
            '风险指标': {
                '夏普比率': f"{perf.get('SharpeRatio', 0):.2f}",
                '最大回撤': f"{perf.get('Drawdown', 0):.2%}",
                '波动率': f"{perf.get('Volatility', 0):.2%}",
                'VaR (95%)': f"{perf.get('VaR', 0):.2%}"
            },
            '交易指标': {
                '总交易次数': perf.get('TotalTrades', 0),
                '胜率': f"{perf.get('WinRate', 0):.2%}",
                '平均盈利': f"{perf.get('AverageWin', 0):.2%}",
                '平均亏损': f"{perf.get('AverageLoss', 0):.2%}",
                '盈亏比': f"{perf.get('ProfitLossRatio', 0):.2f}"
            }
        }
        
        return analysis
    
    def analyze_trades(self):
        """分析交易记录"""
        if not self.orders:
            return None
            
        trades_df = pd.DataFrame(self.orders)
        
        if trades_df.empty:
            return None
            
        # 基本统计
        total_trades = len(trades_df)
        buy_trades = len(trades_df[trades_df['Direction'] == 'Buy'])
        sell_trades = len(trades_df[trades_df['Direction'] == 'Sell'])
        
        # 按月份统计
        if 'Time' in trades_df.columns:
            trades_df['Time'] = pd.to_datetime(trades_df['Time'])
            trades_df['Month'] = trades_df['Time'].dt.to_period('M')
            monthly_trades = trades_df.groupby('Month').size()
        else:
            monthly_trades = None
            
        # 按符号统计
        if 'Symbol' in trades_df.columns:
            symbol_trades = trades_df['Symbol'].value_counts()
        else:
            symbol_trades = None
            
        return {
            '总交易次数': total_trades,
            '买入交易': buy_trades,
            '卖出交易': sell_trades,
            '月度交易分布': monthly_trades,
            '符号交易分布': symbol_trades,
            '交易详情': trades_df
        }
    
    def create_visualizations(self):
        """创建可视化图表"""
        if not self.summary:
            return
            
        # 设置图表样式
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. 收益曲线
        self._plot_equity_curve()
        
        # 2. 回撤图
        self._plot_drawdown()
        
        # 3. 月度收益热力图
        self._plot_monthly_returns()
        
        # 4. 交易分布图
        if self.orders:
            self._plot_trade_distribution()
    
    def _plot_equity_curve(self):
        """绘制权益曲线"""
        if 'Charts' not in self.summary:
            return
            
        equity_chart = self.summary['Charts'].get('Strategy Equity', {})
        if 'Series' not in equity_chart:
            return
            
        equity_series = equity_chart['Series'].get('Equity', {})
        if 'Values' not in equity_series:
            return
            
        # 提取数据
        equity_data = equity_series['Values']
        dates = [pd.to_datetime(point['x']) for point in equity_data]
        values = [point['y'] for point in equity_data]
        
        plt.figure(figsize=(15, 8))
        plt.plot(dates, values, linewidth=2, label='策略权益')
        
        # 添加基准线
        benchmark_series = equity_chart['Series'].get('Benchmark', {})
        if 'Values' in benchmark_series:
            benchmark_data = benchmark_series['Values']
            benchmark_dates = [pd.to_datetime(point['x']) for point in benchmark_data]
            benchmark_values = [point['y'] for point in benchmark_data]
            plt.plot(benchmark_dates, benchmark_values, linewidth=2, label='基准', alpha=0.7)
        
        plt.title('策略权益曲线', fontsize=16)
        plt.xlabel('日期')
        plt.ylabel('权益')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # 保存图片
        plt.savefig(self.output_dir / f"{self.backtest_id}_equity_curve.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_drawdown(self):
        """绘制回撤图"""
        if 'Charts' not in self.summary:
            return
            
        drawdown_chart = self.summary['Charts'].get('Drawdown', {})
        if 'Series' not in drawdown_chart:
            return
            
        drawdown_series = drawdown_chart['Series'].get('Drawdown', {})
        if 'Values' not in drawdown_series:
            return
            
        # 提取数据
        drawdown_data = drawdown_series['Values']
        dates = [pd.to_datetime(point['x']) for point in drawdown_data]
        values = [point['y'] for point in drawdown_data]
        
        plt.figure(figsize=(15, 6))
        plt.fill_between(dates, values, 0, alpha=0.3, color='red')
        plt.plot(dates, values, linewidth=2, color='red')
        
        plt.title('回撤图', fontsize=16)
        plt.xlabel('日期')
        plt.ylabel('回撤')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # 保存图片
        plt.savefig(self.output_dir / f"{self.backtest_id}_drawdown.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_monthly_returns(self):
        """绘制月度收益热力图"""
        if 'Charts' not in self.summary:
            return
            
        monthly_chart = self.summary['Charts'].get('Monthly Returns', {})
        if 'Series' not in monthly_chart:
            return
            
        monthly_series = monthly_chart['Series'].get('Monthly Returns', {})
        if 'Values' not in monthly_series:
            return
            
        # 提取数据
        monthly_data = monthly_series['Values']
        dates = [pd.to_datetime(point['x']) for point in monthly_data]
        values = [point['y'] for point in monthly_data]
        
        # 转换为DataFrame
        df = pd.DataFrame({'Date': dates, 'Return': values})
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        
        # 创建热力图
        pivot_table = df.pivot_table(values='Return', index='Year', columns='Month', aggfunc='sum')
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(pivot_table, annot=True, fmt='.2%', cmap='RdYlGn', center=0)
        plt.title('月度收益热力图', fontsize=16)
        plt.xlabel('月份')
        plt.ylabel('年份')
        plt.tight_layout()
        
        # 保存图片
        plt.savefig(self.output_dir / f"{self.backtest_id}_monthly_returns.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_trade_distribution(self):
        """绘制交易分布图"""
        if not self.orders:
            return
            
        trades_df = pd.DataFrame(self.orders)
        
        if 'Time' in trades_df.columns:
            trades_df['Time'] = pd.to_datetime(trades_df['Time'])
            
            # 按小时分布
            trades_df['Hour'] = trades_df['Time'].dt.hour
            hourly_dist = trades_df['Hour'].value_counts().sort_index()
            
            plt.figure(figsize=(12, 6))
            hourly_dist.plot(kind='bar')
            plt.title('交易时间分布', fontsize=16)
            plt.xlabel('小时')
            plt.ylabel('交易次数')
            plt.xticks(rotation=0)
            plt.tight_layout()
            
            # 保存图片
            plt.savefig(self.output_dir / f"{self.backtest_id}_trade_distribution.png", dpi=300, bbox_inches='tight')
            plt.close()
    
    def generate_report(self):
        """生成分析报告"""
        if not self.summary:
            print("❌ 无法生成报告：没有摘要数据")
            return
            
        # 分析数据
        performance = self.analyze_performance()
        trades = self.analyze_trades()
        
        # 创建报告
        report = f"""
# 回测分析报告

**回测ID**: {self.backtest_id}  
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**分析工具**: BacktestAnalyzer

## 基本信息

"""
        
        if performance and '基本信息' in performance:
            for key, value in performance['基本信息'].items():
                report += f"- **{key}**: {value}\n"
        
        report += "\n## 收益指标\n\n"
        if performance and '收益指标' in performance:
            for key, value in performance['收益指标'].items():
                report += f"- **{key}**: {value}\n"
        
        report += "\n## 风险指标\n\n"
        if performance and '风险指标' in performance:
            for key, value in performance['风险指标'].items():
                report += f"- **{key}**: {value}\n"
        
        report += "\n## 交易指标\n\n"
        if performance and '交易指标' in performance:
            for key, value in performance['交易指标'].items():
                report += f"- **{key}**: {value}\n"
        
        if trades:
            report += "\n## 交易分析\n\n"
            report += f"- **总交易次数**: {trades['总交易次数']}\n"
            report += f"- **买入交易**: {trades['买入交易']}\n"
            report += f"- **卖出交易**: {trades['卖出交易']}\n"
            
            if trades['符号交易分布'] is not None:
                report += "\n### 交易符号分布\n\n"
                for symbol, count in trades['符号交易分布'].head(10).items():
                    report += f"- **{symbol}**: {count} 次\n"
        
        report += "\n## 图表\n\n"
        report += "生成的图表文件：\n"
        report += f"- `{self.backtest_id}_equity_curve.png` - 权益曲线\n"
        report += f"- `{self.backtest_id}_drawdown.png` - 回撤图\n"
        report += f"- `{self.backtest_id}_monthly_returns.png` - 月度收益热力图\n"
        if self.orders:
            report += f"- `{self.backtest_id}_trade_distribution.png` - 交易分布图\n"
        
        # 保存报告
        report_file = self.output_dir / f"{self.backtest_id}_analysis_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ 分析报告已保存: {report_file}")
        return report_file


def main():
    parser = argparse.ArgumentParser(description='回测结果分析器')
    parser.add_argument('backtest_id', help='回测ID')
    parser.add_argument('--output', default='analysis_reports', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = BacktestAnalyzer(args.backtest_id, args.output)
    
    # 加载数据
    if not analyzer.load_data():
        print("❌ 数据加载失败")
        return
    
    # 生成可视化
    print("正在生成可视化图表...")
    analyzer.create_visualizations()
    
    # 生成报告
    print("正在生成分析报告...")
    report_file = analyzer.generate_report()
    
    if report_file:
        print(f"✅ 分析完成！报告保存在: {report_file}")
    else:
        print("❌ 报告生成失败")


if __name__ == "__main__":
    main() 