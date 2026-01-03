"""
通过率控制器 (Pass Rate Controller)

系统级KPI：控制L2通过率在5%-20%

核心功能:
1. 实时监控通过率
2. 动态调整阈值
3. 生成一致性报告

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class PassRateStats:
    """通过率统计"""
    total_evaluated: int = 0
    l0_passed: int = 0
    l1_passed: int = 0
    l2_passed: int = 0
    rejected: int = 0
    
    @property
    def l2_pass_rate(self) -> float:
        """L2通过率"""
        if self.total_evaluated == 0:
            return 0.0
        return self.l2_passed / self.total_evaluated
    
    @property
    def overall_reject_rate(self) -> float:
        """总体拒绝率"""
        if self.total_evaluated == 0:
            return 0.0
        return self.rejected / self.total_evaluated


@dataclass
class ConsistencyReport:
    """一致性报告"""
    run_id: str
    timestamp: str
    
    # 配置
    config_snapshot: Dict[str, Any] = field(default_factory=dict)
    
    # 统计
    stats: PassRateStats = field(default_factory=PassRateStats)
    
    # 阈值
    thresholds_used: Dict[str, float] = field(default_factory=dict)
    
    # 等级映射
    grade_distribution: Dict[str, int] = field(default_factory=dict)
    
    # 警告
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "total_evaluated": self.stats.total_evaluated,
            "l2_passed": self.stats.l2_passed,
            "l2_pass_rate": f"{self.stats.l2_pass_rate:.1%}",
            "rejected": self.stats.rejected,
            "reject_rate": f"{self.stats.overall_reject_rate:.1%}",
            "thresholds": self.thresholds_used,
            "grade_distribution": self.grade_distribution,
            "warnings": self.warnings
        }


class PassRateController:
    """
    通过率控制器
    
    设计原则:
    - 通过率是系统级KPI
    - 目标: L2通过率5%-20%
    - 超过阈值自动收紧
    """
    
    # 默认配置
    DEFAULT_CONFIG = {
        "target_pass_rate": 0.15,  # 目标通过率15%
        "min_pass_rate": 0.05,     # 最低通过率5%
        "max_pass_rate": 0.20,     # 最高通过率20%
        "auto_adjust": True,       # 自动调整阈值
        "l1_threshold": 50,        # L1通过阈值
        "l2_threshold": 65,        # L2通过阈值
        "adjustment_step": 5       # 调整步长
    }
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化控制器
        
        Args:
            config: 配置覆盖
        """
        self.config = {**self.DEFAULT_CONFIG}
        if config:
            self.config.update(config)
        
        self.stats = PassRateStats()
        self._run_history: List[ConsistencyReport] = []
        self._current_run_id = None
    
    def start_run(self, run_id: str = None) -> str:
        """开始新的运行"""
        import uuid
        self._current_run_id = run_id or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.stats = PassRateStats()
        return self._current_run_id
    
    def record_evaluation(self, level: str):
        """
        记录评估结果
        
        Args:
            level: L0/L1/L2/REJECTED
        """
        self.stats.total_evaluated += 1
        
        if level == "L0":
            self.stats.l0_passed += 1
        elif level == "L1":
            self.stats.l0_passed += 1
            self.stats.l1_passed += 1
        elif level == "L2":
            self.stats.l0_passed += 1
            self.stats.l1_passed += 1
            self.stats.l2_passed += 1
        else:
            self.stats.rejected += 1
    
    def check_and_adjust(self) -> Tuple[bool, str]:
        """
        检查通过率并自动调整
        
        Returns:
            (needs_adjustment, message)
        """
        current_rate = self.stats.l2_pass_rate
        
        if current_rate > self.config["max_pass_rate"]:
            if self.config["auto_adjust"]:
                # 收紧阈值
                self.config["l2_threshold"] += self.config["adjustment_step"]
                return True, f"通过率过高({current_rate:.1%})，L2阈值收紧至{self.config['l2_threshold']}"
            else:
                return True, f"通过率过高({current_rate:.1%})，建议收紧阈值"
        
        elif current_rate < self.config["min_pass_rate"]:
            if self.config["auto_adjust"]:
                # 放宽阈值（谨慎）
                if self.config["l2_threshold"] > 50:
                    self.config["l2_threshold"] -= self.config["adjustment_step"]
                    return True, f"通过率过低({current_rate:.1%})，L2阈值放宽至{self.config['l2_threshold']}"
            return True, f"通过率过低({current_rate:.1%})，可考虑放宽阈值"
        
        return False, f"通过率正常({current_rate:.1%})"
    
    def get_thresholds(self) -> Dict[str, float]:
        """获取当前阈值"""
        return {
            "l1_threshold": self.config["l1_threshold"],
            "l2_threshold": self.config["l2_threshold"]
        }
    
    def generate_report(self, grade_distribution: Dict[str, int] = None) -> ConsistencyReport:
        """
        生成一致性报告
        
        Args:
            grade_distribution: 等级分布
            
        Returns:
            ConsistencyReport
        """
        warnings = []
        
        # 检查通过率
        if self.stats.l2_pass_rate > self.config["max_pass_rate"]:
            warnings.append(f"L2通过率过高: {self.stats.l2_pass_rate:.1%} > {self.config['max_pass_rate']:.0%}")
        
        if self.stats.l2_pass_rate < self.config["min_pass_rate"] and self.stats.total_evaluated > 10:
            warnings.append(f"L2通过率过低: {self.stats.l2_pass_rate:.1%} < {self.config['min_pass_rate']:.0%}")
        
        # 检查等级分布一致性
        if grade_distribution:
            s_plus_count = grade_distribution.get("S+", 0)
            s_count = grade_distribution.get("S", 0)
            total_high = s_plus_count + s_count
            
            if total_high > self.stats.l2_passed:
                warnings.append("等级分布与L2通过数不一致")
        
        report = ConsistencyReport(
            run_id=self._current_run_id or "unknown",
            timestamp=datetime.now().isoformat(),
            config_snapshot=self.config.copy(),
            stats=self.stats,
            thresholds_used=self.get_thresholds(),
            grade_distribution=grade_distribution or {},
            warnings=warnings
        )
        
        self._run_history.append(report)
        return report
    
    def validate_output(self, title: str, actual_count: int, expected_level: str) -> Tuple[bool, str]:
        """
        验证输出一致性
        
        Args:
            title: 报告标题（如"推荐股票(A级及以上)"）
            actual_count: 实际数量
            expected_level: 期望等级（如"A"）
            
        Returns:
            (is_valid, message)
        """
        # 检查标题与实际是否一致
        if expected_level == "A" and actual_count > self.stats.l2_passed:
            return False, f"标题声称'{title}'但实际A级以上数量({actual_count})超过L2通过数({self.stats.l2_passed})"
        
        return True, "输出一致性验证通过"
    
    def get_run_history(self) -> List[Dict[str, Any]]:
        """获取运行历史"""
        return [r.to_dict() for r in self._run_history]
    
    def reset(self):
        """重置"""
        self.stats = PassRateStats()
        self._current_run_id = None


# 全局实例
_controller: Optional[PassRateController] = None


def get_pass_rate_controller() -> PassRateController:
    """获取通过率控制器"""
    global _controller
    if _controller is None:
        _controller = PassRateController()
    return _controller

