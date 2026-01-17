"""
报告生成器 (Report Generator)

确保报告口径一致性：
1. 标题由代码自动生成，禁止手写
2. 输出前打印过滤阈值、等级映射表、最终通过率
3. 验证实际内容与标题声称一致

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import json

from .evaluator_v2 import TenbaggerReportV2, TenbaggerEvaluatorV2
from .pass_rate_controller import ConsistencyReport

logger = logging.getLogger(__name__)


@dataclass
class ReportMetadata:
    """报告元数据"""
    run_id: str
    generated_at: str
    version: str
    
    # 配置快照
    thresholds: Dict[str, Any] = field(default_factory=dict)
    grade_mapping: Dict[str, str] = field(default_factory=dict)
    
    # 统计
    total_evaluated: int = 0
    total_passed: int = 0
    pass_rate: float = 0.0
    
    # 一致性检查
    consistency_status: str = "passed"  # passed/warning/failed
    warnings: List[str] = field(default_factory=list)


class ReportGenerator:
    """
    报告生成器
    
    核心原则:
    - 标题自动生成，与内容一致
    - 所有配置可追溯
    - 输出前验证一致性
    """
    
    # 等级映射（用于标题生成）
    GRADE_DESCRIPTIONS = {
        "S+": "顶级推荐",
        "S": "强烈推荐",
        "A": "推荐",
        "B": "关注",
        "C": "观察",
        "D": "暂不推荐",
        "REJECTED": "已排除"
    }
    
    # 标题模板
    TITLE_TEMPLATES = {
        "all": "十倍股早期识别报告 - 完整评估",
        "recommended": "十倍股早期识别报告 - 推荐股票({levels})",
        "by_level": "十倍股早期识别报告 - {level}级及以上",
        "by_stage": "十倍股早期识别报告 - {stage}阶段候选"
    }
    
    def __init__(self, evaluator: TenbaggerEvaluatorV2):
        """
        初始化报告生成器
        
        Args:
            evaluator: 评估器实例
        """
        self.evaluator = evaluator
        self._generated_reports: List[Dict[str, Any]] = []
    
    def _generate_title(
        self,
        reports: List[TenbaggerReportV2],
        filter_type: str = "all",
        filter_value: str = None
    ) -> str:
        """
        自动生成标题（确保与内容一致）
        
        Args:
            reports: 报告列表
            filter_type: 过滤类型 (all/recommended/by_level/by_stage)
            filter_value: 过滤值
            
        Returns:
            自动生成的标题
        """
        if filter_type == "all":
            return self.TITLE_TEMPLATES["all"]
        
        elif filter_type == "recommended":
            # 统计实际等级
            levels = set(r.recommendation_level for r in reports if r.is_recommended)
            if levels:
                level_str = "/".join(sorted(levels, key=lambda x: ["S+", "S", "A", "B", "C", "D"].index(x) if x in ["S+", "S", "A", "B", "C", "D"] else 99))
                return self.TITLE_TEMPLATES["recommended"].format(levels=level_str)
            else:
                return "十倍股早期识别报告 - 无推荐股票"
        
        elif filter_type == "by_level":
            # 验证实际内容
            actual_levels = set(r.recommendation_level for r in reports)
            expected_levels = self._get_levels_above(filter_value)
            
            if actual_levels.issubset(expected_levels):
                return self.TITLE_TEMPLATES["by_level"].format(level=filter_value)
            else:
                # 有不一致，使用更准确的标题
                actual_str = "/".join(sorted(actual_levels))
                logger.warning(f"标题等级与实际不一致: 期望{filter_value}+，实际{actual_str}")
                return f"十倍股早期识别报告 - {actual_str}级"
        
        elif filter_type == "by_stage":
            return self.TITLE_TEMPLATES["by_stage"].format(stage=filter_value)
        
        return "十倍股早期识别报告"
    
    def _get_levels_above(self, min_level: str) -> set:
        """获取指定等级及以上的等级集合"""
        order = ["S+", "S", "A", "B", "C", "D"]
        try:
            idx = order.index(min_level)
            return set(order[:idx + 1])
        except ValueError:
            return set(order)
    
    def _validate_consistency(
        self,
        title: str,
        reports: List[TenbaggerReportV2],
        filter_type: str,
        filter_value: str
    ) -> Tuple[bool, List[str]]:
        """
        验证报告一致性
        
        Returns:
            (is_valid, warnings)
        """
        warnings = []
        
        if filter_type == "by_level":
            expected_levels = self._get_levels_above(filter_value)
            for report in reports:
                if report.recommendation_level not in expected_levels and report.recommendation_level != "REJECTED":
                    warnings.append(f"{report.symbol}: 等级{report.recommendation_level}不在{filter_value}+范围内")
        
        # 检查标题与内容数量是否一致
        if "推荐" in title and len([r for r in reports if r.is_recommended]) == 0:
            warnings.append("标题包含'推荐'但无推荐股票")
        
        # 检查通过率
        pass_rate = len([r for r in reports if r.is_recommended]) / max(1, len(reports))
        if pass_rate > 0.3:
            warnings.append(f"推荐率过高({pass_rate:.1%})，可能需要收紧标准")
        
        return len(warnings) == 0, warnings
    
    def generate_markdown(
        self,
        reports: List[TenbaggerReportV2] = None,
        filter_type: str = "recommended",
        filter_value: str = "A",
        include_metadata: bool = True
    ) -> str:
        """
        生成Markdown格式报告
        
        Args:
            reports: 报告列表（默认使用评估器中的所有报告）
            filter_type: 过滤类型
            filter_value: 过滤值
            include_metadata: 是否包含元数据
            
        Returns:
            Markdown格式的报告
        """
        # 获取报告
        if reports is None:
            if filter_type == "recommended":
                reports = self.evaluator.get_recommendations(min_level=filter_value)
            else:
                reports = list(self.evaluator._reports.values())
        
        # 生成标题
        title = self._generate_title(reports, filter_type, filter_value)
        
        # 验证一致性
        is_valid, warnings = self._validate_consistency(title, reports, filter_type, filter_value)
        
        # 获取统计
        stats = self.evaluator.get_stats()
        consistency_report = self.evaluator.generate_consistency_report()
        
        # 构建报告
        md = []
        
        # 标题
        md.append(f"# {title}")
        md.append("")
        md.append(f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"> **版本**: V2.0")
        md.append(f"> **运行ID**: {consistency_report.run_id}")
        md.append("")
        
        # 一致性检查结果
        if not is_valid:
            md.append("## ⚠️ 一致性警告")
            md.append("")
            for warning in warnings:
                md.append(f"- {warning}")
            md.append("")
        
        # 元数据
        if include_metadata:
            md.append("## 📊 评估配置与统计")
            md.append("")
            md.append("### 过滤阈值")
            md.append("")
            md.append("| 层级 | 阈值 | 说明 |")
            md.append("|------|------|------|")
            md.append(f"| L1 | {consistency_report.thresholds_used.get('l1_threshold', 50)} | 早期结构信号阈值 |")
            md.append(f"| L2 | {consistency_report.thresholds_used.get('l2_threshold', 65)} | 十倍路径精评阈值 |")
            md.append("")
            
            md.append("### 等级映射")
            md.append("")
            md.append("| 等级 | 分数范围 | 阶段要求 | 描述 |")
            md.append("|------|----------|----------|------|")
            md.append("| S+ | ≥85 | S1-S3 | 顶级推荐 |")
            md.append("| S | ≥75 | S1-S3 | 强烈推荐 |")
            md.append("| A | ≥65 | S1-S4 | 推荐 |")
            md.append("| B | ≥50 | S0-S5 | 关注 |")
            md.append("| C | ≥35 | S0-S5 | 观察 |")
            md.append("| D | <35 | - | 暂不推荐 |")
            md.append("")
            
            md.append("### 通过率统计")
            md.append("")
            md.append(f"- **总评估数**: {stats['total_evaluated']}")
            md.append(f"- **推荐数**: {stats['recommended']}")
            md.append(f"- **推荐率**: {stats['recommended'] / max(1, stats['total_evaluated']):.1%}")
            md.append(f"- **否决数**: {stats['rejected']}")
            md.append("")
            
            md.append("### 等级分布")
            md.append("")
            md.append("| 等级 | 数量 |")
            md.append("|------|------|")
            for level in ["S+", "S", "A", "B", "C", "D", "REJECTED"]:
                count = stats["by_level"].get(level, 0)
                if count > 0:
                    md.append(f"| {level} | {count} |")
            md.append("")
            
            md.append("### 阶段分布")
            md.append("")
            md.append("| 阶段 | 数量 | 说明 |")
            md.append("|------|------|------|")
            stage_desc = {
                "S0": "观察期",
                "S1": "验证期",
                "S2": "导入期（最佳介入点）",
                "S3": "放量期",
                "S4": "加速期",
                "S5": "成熟期"
            }
            for stage in ["S0", "S1", "S2", "S3", "S4", "S5"]:
                count = stats["by_stage"].get(stage, 0)
                if count > 0:
                    md.append(f"| {stage} | {count} | {stage_desc.get(stage, '')} |")
            md.append("")
        
        # 推荐列表
        md.append("## 📋 推荐股票列表")
        md.append("")
        
        recommended = [r for r in reports if r.is_recommended]
        if recommended:
            md.append("| 序号 | 代码 | 名称 | 等级 | 分数 | 阶段 | 推荐理由 |")
            md.append("|------|------|------|------|------|------|----------|")
            
            for i, report in enumerate(recommended, 1):
                md.append(f"| {i} | {report.symbol} | {report.name} | {report.recommendation_level} | {report.final_score:.1f} | {report.stage} | {report.recommendation_reason[:30]}... |")
            md.append("")
        else:
            md.append("*本次评估无符合条件的推荐股票*")
            md.append("")
        
        # 详细报告
        md.append("## 📝 详细评估报告")
        md.append("")
        
        for report in reports[:10]:  # 限制输出数量
            md.append(f"### {report.symbol} - {report.name}")
            md.append("")
            md.append(f"- **推荐等级**: {report.recommendation_level}")
            md.append(f"- **综合评分**: {report.final_score:.1f}")
            md.append(f"- **阶段**: {report.stage} (置信度: {report.stage_confidence:.0%})")
            md.append(f"- **漏斗层级**: {report.funnel_level}")
            md.append(f"- **数据质量**: {report.quality_flag}")
            md.append("")
            
            if report.stage_evidence:
                md.append("**阶段证据**:")
                for evidence in report.stage_evidence[:3]:
                    md.append(f"- {evidence}")
                md.append("")
            
            if report.risk_warnings:
                md.append("**风险警示**:")
                for warning in report.risk_warnings[:3]:
                    md.append(f"- ⚠️ {warning}")
                md.append("")
            
            md.append(f"**推荐理由**: {report.recommendation_reason}")
            md.append("")
            md.append("---")
            md.append("")
        
        # 脚注
        md.append("## 📌 免责声明")
        md.append("")
        md.append("本报告由十倍股早期识别系统V2自动生成，仅供参考，不构成投资建议。")
        md.append("投资有风险，入市需谨慎。")
        md.append("")
        md.append(f"*报告生成时间: {datetime.now().isoformat()}*")
        
        return "\n".join(md)
    
    def generate_json(
        self,
        reports: List[TenbaggerReportV2] = None,
        filter_type: str = "recommended",
        filter_value: str = "A"
    ) -> Dict[str, Any]:
        """
        生成JSON格式报告
        
        Returns:
            JSON格式的报告
        """
        if reports is None:
            if filter_type == "recommended":
                reports = self.evaluator.get_recommendations(min_level=filter_value)
            else:
                reports = list(self.evaluator._reports.values())
        
        title = self._generate_title(reports, filter_type, filter_value)
        is_valid, warnings = self._validate_consistency(title, reports, filter_type, filter_value)
        stats = self.evaluator.get_stats()
        consistency_report = self.evaluator.generate_consistency_report()
        
        return {
            "title": title,
            "generated_at": datetime.now().isoformat(),
            "version": "v2",
            "run_id": consistency_report.run_id,
            "consistency": {
                "is_valid": is_valid,
                "warnings": warnings
            },
            "metadata": {
                "thresholds": consistency_report.thresholds_used,
                "stats": stats
            },
            "reports": [r.to_dict() for r in reports],
            "summary": {
                "total_evaluated": stats["total_evaluated"],
                "recommended": stats["recommended"],
                "pass_rate": f"{stats['recommended'] / max(1, stats['total_evaluated']):.1%}",
                "by_level": stats["by_level"],
                "by_stage": stats["by_stage"]
            }
        }
    
    def save_report(
        self,
        output_path: str,
        format: str = "markdown",
        **kwargs
    ) -> str:
        """
        保存报告到文件
        
        Args:
            output_path: 输出路径
            format: 格式 (markdown/json)
            **kwargs: 传递给生成函数的参数
            
        Returns:
            保存的文件路径
        """
        if format == "markdown":
            content = self.generate_markdown(**kwargs)
            if not output_path.endswith(".md"):
                output_path += ".md"
        else:
            content = json.dumps(self.generate_json(**kwargs), ensure_ascii=False, indent=2)
            if not output_path.endswith(".json"):
                output_path += ".json"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"报告已保存: {output_path}")
        return output_path

