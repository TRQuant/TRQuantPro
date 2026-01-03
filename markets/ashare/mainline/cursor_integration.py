"""
Cursor IDE 集成模块

参考机构级量化平台设计：
1. 在Cursor IDE中直接触发分析
2. 生成结构化的分析Prompt
3. 支持一键回测和报告查看
4. 版本管理和策略迭代

使用方式：
1. 在Cursor中打开此文件
2. 运行 generate_analysis_prompt() 获取分析Prompt
3. 将Prompt复制到Cursor Chat进行深度分析
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

from .analysis_engine import MainlineAnalysisEngine, MainlineResult
from .real_data_fetcher import RealDataFetcher


class CursorIntegration:
    """
    Cursor IDE 集成类
    
    功能：
    1. 生成分析Prompt供Cursor AI分析
    2. 保存分析结果到文件
    3. 管理分析历史
    """
    
    def __init__(self):
        self.engine = MainlineAnalysisEngine()
        self.output_dir = os.path.expanduser("~/.local/share/trquant/analysis_outputs")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_analysis_and_generate_prompt(self) -> str:
        """
        运行完整分析并生成Cursor分析Prompt
        
        Returns:
            可直接复制到Cursor Chat的Prompt
        """
        # 运行分析
        result = self.engine.run_full_analysis()
        
        # 保存结果
        self._save_result(result)
        
        # 返回Cursor Prompt
        return result["cursor_prompt"]
    
    def _save_result(self, result: Dict):
        """保存分析结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存完整结果
        output_file = os.path.join(self.output_dir, f"analysis_{timestamp}.json")
        
        # 转换为可序列化格式
        serializable = {
            "timestamp": timestamp,
            "mainlines": [ml.to_dict() for ml in result["mainlines"]],
            "steps": [s.to_dict() for s in result["steps"]],
            "summary": result["summary"],
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
        
        # 保存Prompt
        prompt_file = os.path.join(self.output_dir, f"prompt_{timestamp}.md")
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(result["cursor_prompt"])
        
        print(f"\n📁 分析结果已保存:")
        print(f"   - 完整结果: {output_file}")
        print(f"   - Cursor Prompt: {prompt_file}")
    
    def get_quick_prompt(self) -> str:
        """
        获取快速分析Prompt（不运行完整分析）
        
        适用于快速获取数据概览
        """
        fetcher = RealDataFetcher()
        data = fetcher.fetch_all_data()
        
        prompt = f"""# A股快速分析请求

## 📅 时间
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 数据概览

### 板块资金流向
"""
        
        sector_flow = data.get("sector_flow")
        if sector_flow and sector_flow.success and sector_flow.data:
            prompt += "| 板块 | 涨跌幅 | 主力净流入(亿) |\n"
            prompt += "|------|--------|----------------|\n"
            for s in sector_flow.data[:10]:
                prompt += f"| {s.get('sector_name', '')} | {s.get('change_pct', 0):.2f}% | {s.get('main_net_inflow', 0):.2f} |\n"
        
        prompt += f"""
### 北向资金
"""
        northbound = data.get("northbound_flow")
        if northbound and northbound.success and northbound.data:
            d = northbound.data
            prompt += f"- 今日: {d.get('today_net', 0):.2f}亿\n"
            prompt += f"- 本周: {d.get('week_net', 0):.2f}亿\n"
            prompt += f"- 本月: {d.get('month_net', 0):.2f}亿\n"
        
        prompt += f"""
### 市场情绪
"""
        sentiment = data.get("market_sentiment")
        if sentiment and sentiment.success and sentiment.data:
            d = sentiment.data
            prompt += f"- 情绪得分: {d.get('sentiment_score', 50)}/100\n"
            prompt += f"- 涨停家数: {d.get('up_limit_count', 0)}\n"
            prompt += f"- 跌停家数: {d.get('down_limit_count', 0)}\n"
        
        prompt += """
## 🎯 分析任务

请基于以上数据：
1. 判断当前市场主线方向
2. 识别最强板块和概念
3. 给出操作建议

请以简洁的JSON格式输出。
"""
        
        return prompt
    
    def generate_strategy_prompt(self, mainline_name: str) -> str:
        """
        为特定主线生成策略开发Prompt
        
        Args:
            mainline_name: 主线名称，如"人工智能"
        
        Returns:
            策略开发Prompt
        """
        return f"""# {mainline_name}主线策略开发

## 📋 策略需求

基于"{mainline_name}"主线，开发一个量化选股策略。

## 🎯 策略目标

1. **选股范围**: {mainline_name}相关板块的A股
2. **持仓周期**: 中短期（1-4周）
3. **风险控制**: 最大回撤控制在15%以内

## 📊 因子要求

请设计以下因子：
1. **动量因子**: 捕捉趋势启动
2. **资金因子**: 识别主力资金流入
3. **估值因子**: 避免追高

## 💻 代码框架

请使用以下框架生成策略代码：

```python
# {mainline_name}主线策略
# 生成时间: {datetime.now().strftime("%Y-%m-%d")}

import pandas as pd
import numpy as np

class {mainline_name.replace(' ', '')}Strategy:
    '''
    {mainline_name}主线量化策略
    '''
    
    def __init__(self):
        self.name = "{mainline_name}策略"
        self.max_positions = 10
        self.stop_loss = 0.08
        self.take_profit = 0.20
    
    def select_stocks(self, data: pd.DataFrame) -> list:
        '''选股逻辑'''
        # TODO: 实现选股逻辑
        pass
    
    def calculate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        '''计算交易信号'''
        # TODO: 实现信号计算
        pass
    
    def execute(self, signals: pd.DataFrame) -> dict:
        '''执行交易'''
        # TODO: 实现交易执行
        pass
```

## ✅ 输出要求

1. 完整的策略代码
2. 因子计算公式
3. 回测参数建议
4. 风险提示
"""


# ================================================================
# 便捷函数
# ================================================================

def generate_analysis_prompt() -> str:
    """
    生成主线分析Prompt
    
    使用方式：
    1. 在Cursor中运行此函数
    2. 复制返回的Prompt到Cursor Chat
    3. 获取AI深度分析
    """
    integration = CursorIntegration()
    return integration.run_analysis_and_generate_prompt()


def quick_analysis() -> str:
    """
    快速分析（不保存结果）
    """
    integration = CursorIntegration()
    return integration.get_quick_prompt()


def strategy_prompt(mainline: str = "人工智能") -> str:
    """
    生成策略开发Prompt
    """
    integration = CursorIntegration()
    return integration.generate_strategy_prompt(mainline)


# ================================================================
# 直接运行测试
# ================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Cursor集成分析模块")
    print("=" * 70)
    
    # 运行分析
    prompt = generate_analysis_prompt()
    
    print("\n" + "=" * 70)
    print("📋 以下是生成的Cursor分析Prompt:")
    print("=" * 70)
    print(prompt)

