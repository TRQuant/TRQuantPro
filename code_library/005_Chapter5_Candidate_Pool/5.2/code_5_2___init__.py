"""
文件名: code_5_2___init__.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.2/code_5_2___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.2_Filtering_Rules_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from dataclasses import dataclass
from typing import List, Dict, Callable
from enum import Enum

class RuleLogic(Enum):
    """规则逻辑"""
    AND = "AND"  # 所有规则必须满足
    OR = "OR"    # 任一规则满足即可
    NOT = "NOT"  # 规则不满足

@dataclass
class FilterRule:
    """筛选规则"""
    name: str                    # 规则名称
    rule_type: str              # 规则类型（basic/mainline/technical/fundamental）
    condition: Callable          # 筛选条件函数
    weight: float = 1.0         # 规则权重
    priority: int = 3            # 优先级（1最高，5最低）
    logic: RuleLogic = RuleLogic.AND  # 逻辑组合

class FilterEngine:
    """筛选规则引擎"""
    
    def __init__(self):
        self.rules: List[FilterRule] = []
        self.basic_filter = BasicFilter()
    
    def add_rule(self, rule: FilterRule):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        self.rules.append(rule)
    
    def filter(
        self,
        stocks: List[str],
        date: str = None,
        rule_combination: Dict = None
    ) -> List[str]:
        """
        执行筛选
        
        Args:
            stocks: 股票代码列表
            date: 日期
            rule_combination: 规则组合配置
                {
                    "logic": "AND",  # 逻辑组合
                    "weights": {...}  # 规则权重
                }
        
        Returns:
            筛选后的股票代码列表
        """
        if rule_combination is None:
            rule_combination = {
                "logic": "AND",
                "weights": {}
            }
        
        # 1. 基础筛选（优先执行）
        filtered = self.basic_filter.filter(stocks, date=date)
        
        # 2. 按优先级排序规则
        sorted_rules = sorted(self.rules, key=lambda r: r.priority)
        
        # 3. 执行规则
        logic = rule_combination.get("logic", "AND")
        weights = rule_combination.get("weights", {})
        
        if logic == "AND":
            # 所有规则必须满足
            for rule in sorted_rules:
                weight = weights.get(rule.name, rule.weight)
                filtered = self._apply_rule(filtered, rule, date=date, weight=weight)
        elif logic == "OR":
            # 任一规则满足即可（合并结果）
            all_results = []
            for rule in sorted_rules:
                weight = weights.get(rule.name, rule.weight)
                result = self._apply_rule(filtered, rule, date=date, weight=weight)
                all_results.extend(result)
            # 去重
            filtered = list(set(all_results))
        
        return filtered
    
    def _apply_rule(
        self,
        stocks: List[str],
        rule: FilterRule,
        date: str = None,
        weight: float = 1.0
    ) -> List[str]:
        """应用单个规则"""
        try:
            result = rule.condition(stocks, date=date)
            return result
        except Exception as e:
            logger.error(f"执行规则 {rule.name} 失败: {e}")
            return stocks

# 使用示例
engine = FilterEngine()

# 添加主线筛选规则
mainline_rule = FilterRule(
    name="主线筛选",
    rule_type="mainline",
    condition=lambda stocks, date: filter_by_mainline_industry(
        stocks, mainline_info, date
    ),
    weight=0.3,
    priority=1
)
engine.add_rule(mainline_rule)

# 添加技术筛选规则
tech_rule = FilterRule(
    name="技术突破",
    rule_type="technical",
    condition=lambda stocks, date: [
        c["code"] for c in filter_technical_breakthrough(stocks, date)
    ],
    weight=0.3,
    priority=2
)
engine.add_rule(tech_rule)

# 添加基本面筛选规则
fundamental_rule = FilterRule(
    name="基本面筛选",
    rule_type="fundamental",
    condition=lambda stocks, date: filter_fundamental(stocks, date),
    weight=0.4,
    priority=3
)
engine.add_rule(fundamental_rule)

# 执行筛选
rule_combination = {
    "logic": "AND",
    "weights": {
        "主线筛选": 0.3,
        "技术突破": 0.3,
        "基本面筛选": 0.4
    }
}

filtered_stocks = engine.filter(
    stocks=all_stocks,
    date="2024-12-12",
    rule_combination=rule_combination
)