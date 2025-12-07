"""AI 分析器

使用 LLM 自动分析回测和实盘数据
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


# 回测分析 Prompt 模板
BACKTEST_ANALYSIS_PROMPT = """请分析以下策略回测结果，提供专业的量化投资分析报告。

## 策略信息

- 策略名称: {strategy_name}
- 回测区间: {start_date} 至 {end_date}
- 初始资金: ¥{initial_capital:,.0f}
- 基准指数: {benchmark}

## 回测指标

- 总收益率: {total_return:.2f}%
- 年化收益: {annual_return:.2f}%
- 最大回撤: {max_drawdown:.2f}%
- 夏普比率: {sharpe_ratio:.2f}
- 胜率: {win_rate:.2f}%
- 交易次数: {trade_count}
- 盈亏比: {profit_factor:.2f}
- 波动率: {volatility:.2f}%

## 分析要求

请从以下方面进行分析：

1. **收益风险评估**：评价策略的收益水平和风险控制能力
2. **交易行为分析**：分析交易频率、胜率、盈亏比是否合理
3. **策略优缺点**：总结策略的优势和潜在问题
4. **改进建议**：提出具体的优化方向
5. **适用场景**：分析策略适合的市场环境

请用中文输出，格式清晰，便于阅读。"""

# 实盘日报分析 Prompt 模板
LIVE_DAILY_PROMPT = """请分析以下实盘交易数据，生成当日交易分析报告。

## 账户概况

- 日期: {date}
- 账户净值: ¥{total_value:,.2f}
- 今日盈亏: ¥{daily_pnl:,.2f} ({daily_return:.2f}%)
- 持仓市值: ¥{positions_value:,.2f}
- 可用资金: ¥{available_cash:,.2f}

## 今日交易

{trades_summary}

## 当前持仓

{positions_summary}

## 分析要求

请分析：
1. 今日交易决策是否合理
2. 当前持仓结构是否健康
3. 风险提示和建议
4. 明日操作建议

请用中文输出，简明扼要。"""


class AIAnalyzer:
    """AI 分析器
    
    使用 LLM 分析回测和实盘数据，生成智能分析报告
    
    Example:
        >>> analyzer = AIAnalyzer()
        >>> report = analyzer.analyze_backtest(result)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """初始化分析器
        
        Args:
            api_key: API 密钥
            model: 模型名称
        """
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        """获取 LLM 客户端"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                logger.warning("OpenAI not installed, using mock mode")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        return self._client
    
    def analyze_backtest(self, result: Dict[str, Any]) -> str:
        """分析回测结果
        
        Args:
            result: 回测结果字典
            
        Returns:
            分析报告
        """
        config = result.get("config", {})
        metrics = result.get("metrics", {})
        
        # 构建 Prompt
        prompt = BACKTEST_ANALYSIS_PROMPT.format(
            strategy_name=config.get("strategy_name", "未知策略"),
            start_date=config.get("start_date", "N/A"),
            end_date=config.get("end_date", "N/A"),
            initial_capital=config.get("initial_capital", 0),
            benchmark=config.get("benchmark", "N/A"),
            total_return=metrics.get("total_return", 0),
            annual_return=metrics.get("annual_return", 0),
            max_drawdown=metrics.get("max_drawdown", 0),
            sharpe_ratio=metrics.get("sharpe_ratio", 0),
            win_rate=metrics.get("win_rate", 0),
            trade_count=metrics.get("trade_count", 0),
            profit_factor=metrics.get("profit_factor", 0),
            volatility=metrics.get("volatility", 0)
        )
        
        # 调用 LLM
        return self._call_llm(prompt)
    
    def analyze_live_daily(self, trading_data: Dict[str, Any]) -> str:
        """分析实盘日报
        
        Args:
            trading_data: 交易数据
            
        Returns:
            分析报告
        """
        # 构建交易摘要
        trades = trading_data.get("trades", [])
        trades_summary = "无交易" if not trades else "\n".join([
            f"- {t.get('time', 'N/A')}: {'买入' if t.get('direction') == 'buy' else '卖出'} {t.get('symbol', 'N/A')} {t.get('volume', 0)}股 @¥{t.get('price', 0):.2f}"
            for t in trades
        ])
        
        # 构建持仓摘要
        positions = trading_data.get("positions", [])
        positions_summary = "空仓" if not positions else "\n".join([
            f"- {p.get('symbol', 'N/A')} ({p.get('name', 'N/A')}): {p.get('volume', 0)}股, 成本¥{p.get('cost', 0):.2f}, 盈亏¥{p.get('pnl', 0):.2f}"
            for p in positions
        ])
        
        # 构建 Prompt
        prompt = LIVE_DAILY_PROMPT.format(
            date=trading_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            total_value=trading_data.get("total_value", 0),
            daily_pnl=trading_data.get("daily_pnl", 0),
            daily_return=trading_data.get("daily_return", 0),
            positions_value=trading_data.get("positions_value", 0),
            available_cash=trading_data.get("available_cash", 0),
            trades_summary=trades_summary,
            positions_summary=positions_summary
        )
        
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        """调用 LLM
        
        Args:
            prompt: 提示词
            
        Returns:
            LLM 响应
        """
        client = self._get_client()
        
        if client:
            try:
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一位专业的量化投资分析师，擅长分析策略回测数据和实盘交易表现。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"LLM call failed: {e}")
                return self._generate_mock_analysis(prompt)
        else:
            return self._generate_mock_analysis(prompt)
    
    def _generate_mock_analysis(self, prompt: str) -> str:
        """生成模拟分析（当 LLM 不可用时）"""
        # 从 prompt 中提取关键指标
        import re
        
        total_return = float(re.search(r'总收益率: ([-\d.]+)%', prompt).group(1)) if re.search(r'总收益率: ([-\d.]+)%', prompt) else 0
        annual_return = float(re.search(r'年化收益: ([-\d.]+)%', prompt).group(1)) if re.search(r'年化收益: ([-\d.]+)%', prompt) else 0
        max_drawdown = float(re.search(r'最大回撤: ([-\d.]+)%', prompt).group(1)) if re.search(r'最大回撤: ([-\d.]+)%', prompt) else 0
        sharpe_ratio = float(re.search(r'夏普比率: ([-\d.]+)', prompt).group(1)) if re.search(r'夏普比率: ([-\d.]+)', prompt) else 0
        
        # 生成基于规则的分析
        analysis = f"""# 策略分析报告

## 一、收益风险评估

### 收益表现
- 总收益率 **{total_return:.2f}%**，{'表现优异' if total_return > 30 else '表现良好' if total_return > 10 else '表现一般' if total_return > 0 else '出现亏损'}
- 年化收益 **{annual_return:.2f}%**，{'超过市场平均水平' if annual_return > 15 else '与市场平均水平相当' if annual_return > 8 else '低于市场平均水平'}

### 风险控制
- 最大回撤 **{max_drawdown:.2f}%**，{'风险控制优秀' if max_drawdown < 15 else '风险控制良好' if max_drawdown < 25 else '需要加强风险控制'}
- 夏普比率 **{sharpe_ratio:.2f}**，{'风险调整后收益优秀' if sharpe_ratio > 1.5 else '风险调整后收益良好' if sharpe_ratio > 1 else '风险调整后收益一般'}

## 二、策略优缺点

### 优势
- {'稳健的收益表现' if total_return > 20 else '正向收益'}
- {'优秀的风险控制能力' if max_drawdown < 20 else '可接受的风险水平'}
- {'良好的风险调整后收益' if sharpe_ratio > 1 else '有一定的超额收益'}

### 潜在问题
- {'最大回撤较大，可能影响投资者体验' if max_drawdown > 25 else '回撤控制有进一步优化空间'}
- {'夏普比率偏低，收益波动较大' if sharpe_ratio < 1 else ''}

## 三、改进建议

1. **风险管理**：建议设置更严格的止损线，控制单笔交易风险
2. **仓位管理**：根据市场环境动态调整仓位，降低系统性风险
3. **策略优化**：可尝试加入更多因子或信号，提高策略稳定性
4. **多市场验证**：建议在不同市场环境下验证策略有效性

## 四、适用场景

{'该策略适合稳健型投资者，可作为资产配置的一部分' if sharpe_ratio > 1 and max_drawdown < 25 else '该策略风险较高，适合有一定风险承受能力的投资者' if max_drawdown > 25 else '该策略表现一般，建议进一步优化后使用'}。

---

*注：本分析基于历史回测数据，不构成投资建议。实盘操作前请充分评估风险。*
"""
        return analysis


def analyze_backtest(result: Dict[str, Any], api_key: Optional[str] = None) -> str:
    """分析回测结果的便捷函数"""
    analyzer = AIAnalyzer(api_key=api_key)
    return analyzer.analyze_backtest(result)


