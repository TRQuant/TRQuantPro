"""
规则引擎 (Rule Engine) - 一票否决

负责"否决与保真"，让系统具备"杀死候选"的能力

否决规则:
- ST/退市风险
- 高质押+逼近平仓
- 现金流/应收/存货异常
- 非经常性损益主导利润
- 重大处罚/诉讼/审计意见异常

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class VetoRule:
    """否决规则"""
    rule_id: str
    name: str
    description: str
    check: Callable[[Dict], bool]  # True = 触发否决
    severity: str = "critical"  # critical/high/medium
    category: str = "financial"  # financial/governance/trading


@dataclass
class VetoResult:
    """否决结果"""
    symbol: str
    is_vetoed: bool
    triggered_rules: List[str] = field(default_factory=list)
    messages: List[str] = field(default_factory=list)
    severity: str = ""  # 最高严重级别
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class RuleEngine:
    """
    规则引擎 - 一票否决
    
    设计原则:
    - 规则引擎做"硬门槛"
    - 让系统具备"杀死候选"的能力
    - 解决A股常见雷区
    """
    
    # 预定义否决规则
    DEFAULT_RULES = [
        VetoRule(
            rule_id="st_delisting",
            name="ST/退市风险",
            description="ST股票或存在退市风险",
            check=lambda d: d.get("is_st", False) or d.get("delisting_risk", False),
            severity="critical",
            category="trading"
        ),
        VetoRule(
            rule_id="major_violation",
            name="重大违规",
            description="存在重大违规记录",
            check=lambda d: d.get("major_violation", False),
            severity="critical",
            category="governance"
        ),
        VetoRule(
            rule_id="cash_flow_negative",
            name="经营现金流长期为负",
            description="经营现金流连续2年以上为负且营收增长不足",
            check=lambda d: (
                d.get("cash_flow_negative_years", 0) >= 2 and
                d.get("revenue_growth", 0) < 10
            ),
            severity="critical",
            category="financial"
        ),
        VetoRule(
            rule_id="high_leverage_short_debt",
            name="高杠杆短债压力",
            description="负债率>70%且短债比例>80%",
            check=lambda d: (
                d.get("debt_ratio", 0) > 70 and
                d.get("short_debt_ratio", 0) > 0.8
            ),
            severity="critical",
            category="financial"
        ),
        VetoRule(
            rule_id="goodwill_dominant",
            name="商誉/非经常损益主导",
            description="商誉占比>50%或非经常损益占比>80%",
            check=lambda d: (
                d.get("goodwill_ratio", 0) > 0.5 or
                d.get("non_recurring_ratio", 0) > 0.8
            ),
            severity="high",
            category="financial"
        ),
        VetoRule(
            rule_id="high_pledge",
            name="高质押风险",
            description="大股东质押比例>80%且股价接近平仓线",
            check=lambda d: (
                d.get("pledge_ratio", 0) > 0.8 and
                d.get("near_pledge_liquidation", False)
            ),
            severity="critical",
            category="governance"
        ),
        VetoRule(
            rule_id="receivable_inventory_anomaly",
            name="应收存货异常",
            description="应收账款/营收>50%或存货/营收>100%",
            check=lambda d: (
                d.get("receivable_revenue_ratio", 0) > 0.5 or
                d.get("inventory_revenue_ratio", 0) > 1.0
            ),
            severity="high",
            category="financial"
        ),
        VetoRule(
            rule_id="audit_opinion_abnormal",
            name="审计意见异常",
            description="非标准审计意见",
            check=lambda d: d.get("audit_opinion", "standard") != "standard",
            severity="critical",
            category="governance"
        ),
        VetoRule(
            rule_id="major_lawsuit",
            name="重大诉讼风险",
            description="存在重大诉讼且金额超过净资产20%",
            check=lambda d: (
                d.get("has_major_lawsuit", False) and
                d.get("lawsuit_net_asset_ratio", 0) > 0.2
            ),
            severity="high",
            category="governance"
        ),
        VetoRule(
            rule_id="continuous_loss",
            name="连续亏损",
            description="连续3年以上亏损",
            check=lambda d: d.get("continuous_loss_years", 0) >= 3,
            severity="critical",
            category="financial"
        )
    ]
    
    def __init__(self, rules: List[VetoRule] = None):
        """
        初始化规则引擎
        
        Args:
            rules: 自定义规则列表，默认使用预定义规则
        """
        self.rules = rules or self.DEFAULT_RULES.copy()
        self._stats = {
            "total_checked": 0,
            "vetoed": 0,
            "passed": 0,
            "rule_triggers": {}
        }
        
        # 初始化规则触发统计
        for rule in self.rules:
            self._stats["rule_triggers"][rule.rule_id] = 0
    
    def check(self, symbol: str, data: Dict[str, Any]) -> VetoResult:
        """
        检查是否触发否决规则
        
        Args:
            symbol: 股票代码
            data: 财务/治理数据
            
        Returns:
            VetoResult
        """
        self._stats["total_checked"] += 1
        
        triggered_rules = []
        messages = []
        max_severity = ""
        severity_order = {"critical": 3, "high": 2, "medium": 1}
        
        for rule in self.rules:
            try:
                if rule.check(data):
                    triggered_rules.append(rule.rule_id)
                    messages.append(f"[{rule.severity.upper()}] {rule.name}: {rule.description}")
                    self._stats["rule_triggers"][rule.rule_id] += 1
                    
                    # 更新最高严重级别
                    if severity_order.get(rule.severity, 0) > severity_order.get(max_severity, 0):
                        max_severity = rule.severity
                        
            except Exception as e:
                logger.warning(f"Rule {rule.rule_id} check failed for {symbol}: {e}")
        
        is_vetoed = len(triggered_rules) > 0
        
        if is_vetoed:
            self._stats["vetoed"] += 1
        else:
            self._stats["passed"] += 1
        
        return VetoResult(
            symbol=symbol,
            is_vetoed=is_vetoed,
            triggered_rules=triggered_rules,
            messages=messages,
            severity=max_severity
        )
    
    def batch_check(self, stocks: List[Dict[str, Any]]) -> List[VetoResult]:
        """批量检查"""
        results = []
        for stock in stocks:
            result = self.check(
                symbol=stock.get("symbol", ""),
                data=stock.get("data", {})
            )
            results.append(result)
        return results
    
    def add_rule(self, rule: VetoRule):
        """添加自定义规则"""
        self.rules.append(rule)
        self._stats["rule_triggers"][rule.rule_id] = 0
    
    def remove_rule(self, rule_id: str):
        """移除规则"""
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        self._stats["rule_triggers"].pop(rule_id, None)
    
    def get_rule(self, rule_id: str) -> Optional[VetoRule]:
        """获取规则"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def list_rules(self) -> List[Dict[str, Any]]:
        """列出所有规则"""
        return [
            {
                "rule_id": r.rule_id,
                "name": r.name,
                "description": r.description,
                "severity": r.severity,
                "category": r.category,
                "trigger_count": self._stats["rule_triggers"].get(r.rule_id, 0)
            }
            for r in self.rules
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        veto_rate = self._stats["vetoed"] / max(1, self._stats["total_checked"])
        
        # 按触发次数排序的规则
        sorted_triggers = sorted(
            self._stats["rule_triggers"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "total_checked": self._stats["total_checked"],
            "vetoed": self._stats["vetoed"],
            "passed": self._stats["passed"],
            "veto_rate": f"{veto_rate:.1%}",
            "top_triggered_rules": sorted_triggers[:5],
            "rule_count": len(self.rules)
        }
    
    def reset_stats(self):
        """重置统计"""
        self._stats = {
            "total_checked": 0,
            "vetoed": 0,
            "passed": 0,
            "rule_triggers": {r.rule_id: 0 for r in self.rules}
        }


# 全局实例
_engine: Optional[RuleEngine] = None


def get_rule_engine() -> RuleEngine:
    """获取规则引擎"""
    global _engine
    if _engine is None:
        _engine = RuleEngine()
    return _engine

