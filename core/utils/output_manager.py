#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一输出目录管理器
==================

规范：
- 所有生成的文件统一放在 `output/` 目录下
- 按总任务/模块设立子文件夹管理
- 支持自动创建目录、时间戳、版本管理

目录结构：
output/
├── advisor_v4/          # Investment Advisor V4.0
│   ├── reports/         # HTML报告
│   ├── backtest/        # 回测结果
│   ├── models/          # 模型文件
│   ├── recommendations/ # 推荐结果
│   ├── optimization/    # 优化结果
│   └── logs/            # 日志文件
├── market_trend/        # 市场趋势分析
│   ├── reports/
│   ├── signals/
│   └── backtest/
├── tenbagger/           # 十倍股策略
│   ├── reports/
│   ├── screening/
│   └── backtest/
├── workflow/            # 工作流结果
│   ├── reports/
│   └── strategies/
└── shared/              # 共享文件
    ├── data/
    └── cache/
"""

from __future__ import annotations

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Union
from enum import Enum

logger = logging.getLogger(__name__)


class OutputCategory(Enum):
    """输出类别枚举"""
    ADVISOR_V4 = "advisor_v4"
    MARKET_TREND = "market_trend"
    TENBAGGER = "tenbagger"
    WORKFLOW = "workflow"
    SHARED = "shared"


class OutputType(Enum):
    """输出类型枚举"""
    REPORTS = "reports"
    BACKTEST = "backtest"
    MODELS = "models"
    RECOMMENDATIONS = "recommendations"
    OPTIMIZATION = "optimization"
    LOGS = "logs"
    DATA = "data"
    CACHE = "cache"
    SIGNALS = "signals"
    SCREENING = "screening"
    STRATEGIES = "strategies"


class OutputManager:
    """统一输出目录管理器"""

    def __init__(
        self,
        project_root: Optional[Path] = None,
        base_output_dir: str = "output",
    ):
        """
        初始化输出管理器

        Args:
            project_root: 项目根目录（默认自动检测）
            base_output_dir: 基础输出目录名（默认: output）
        """
        if project_root is None:
            # 自动检测项目根目录
            current_file = Path(__file__).resolve()
            # 从 core/utils/ 向上找到项目根目录
            project_root = current_file.parent.parent.parent

        self.project_root = Path(project_root)
        self.base_output_dir = self.project_root / base_output_dir
        self.base_output_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"OutputManager 初始化: 基础目录 = {self.base_output_dir}")

    def get_path(
        self,
        category: Union[OutputCategory, str],
        output_type: Union[OutputType, str],
        filename: Optional[str] = None,
        create_dirs: bool = True,
        add_timestamp: bool = False,
    ) -> Path:
        """
        获取输出路径

        Args:
            category: 输出类别（如 advisor_v4, market_trend）
            output_type: 输出类型（如 reports, backtest）
            filename: 文件名（可选）
            create_dirs: 是否自动创建目录
            add_timestamp: 是否添加时间戳到文件名

        Returns:
            输出路径（Path对象）

        Examples:
            >>> manager = OutputManager()
            >>> # 获取报告目录
            >>> report_dir = manager.get_path("advisor_v4", "reports")
            >>> # 获取带时间戳的文件路径
            >>> report_file = manager.get_path("advisor_v4", "reports", "weekly_layout.html", add_timestamp=True)
        """
        # 转换枚举为字符串
        if isinstance(category, OutputCategory):
            category = category.value
        if isinstance(output_type, OutputType):
            output_type = output_type.value

        # 构建路径
        path = self.base_output_dir / category / output_type

        # 创建目录
        if create_dirs:
            path.mkdir(parents=True, exist_ok=True)

        # 如果有文件名，添加到路径
        if filename:
            if add_timestamp:
                # 添加时间戳到文件名
                file_path = Path(filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            path = path / filename

        return path

    def get_report_path(
        self,
        category: Union[OutputCategory, str],
        filename: str,
        add_timestamp: bool = False,
    ) -> Path:
        """获取报告文件路径（快捷方法）"""
        return self.get_path(category, OutputType.REPORTS, filename, add_timestamp=add_timestamp)

    def get_backtest_path(
        self,
        category: Union[OutputCategory, str],
        filename: str,
        add_timestamp: bool = False,
    ) -> Path:
        """获取回测结果路径（快捷方法）"""
        return self.get_path(category, OutputType.BACKTEST, filename, add_timestamp=add_timestamp)

    def get_model_path(
        self,
        category: Union[OutputCategory, str],
        filename: str,
        add_timestamp: bool = False,
    ) -> Path:
        """获取模型文件路径（快捷方法）"""
        return self.get_path(category, OutputType.MODELS, filename, add_timestamp=add_timestamp)

    def get_recommendation_path(
        self,
        category: Union[OutputCategory, str],
        filename: str,
        add_timestamp: bool = False,
    ) -> Path:
        """获取推荐结果路径（快捷方法）"""
        return self.get_path(
            category, OutputType.RECOMMENDATIONS, filename, add_timestamp=add_timestamp
        )

    def get_optimization_path(
        self,
        category: Union[OutputCategory, str],
        filename: str,
        add_timestamp: bool = False,
    ) -> Path:
        """获取优化结果路径（快捷方法）"""
        return self.get_path(
            category, OutputType.OPTIMIZATION, filename, add_timestamp=add_timestamp
        )

    def get_log_path(
        self,
        category: Union[OutputCategory, str],
        filename: str,
        add_timestamp: bool = False,
    ) -> Path:
        """获取日志文件路径（快捷方法）"""
        return self.get_path(category, OutputType.LOGS, filename, add_timestamp=add_timestamp)

    def list_files(
        self,
        category: Union[OutputCategory, str],
        output_type: Union[OutputType, str],
        pattern: str = "*",
    ) -> list[Path]:
        """
        列出指定目录下的文件

        Args:
            category: 输出类别
            output_type: 输出类型
            pattern: 文件名模式（支持glob）

        Returns:
            文件路径列表
        """
        dir_path = self.get_path(category, output_type, create_dirs=False)
        if not dir_path.exists():
            return []
        return list(dir_path.glob(pattern))

    def cleanup_old_files(
        self,
        category: Union[OutputCategory, str],
        output_type: Union[OutputType, str],
        keep_days: int = 30,
        pattern: str = "*",
    ) -> int:
        """
        清理旧文件

        Args:
            category: 输出类别
            output_type: 输出类型
            keep_days: 保留天数
            pattern: 文件名模式

        Returns:
            删除的文件数量
        """
        import time

        files = self.list_files(category, output_type, pattern)
        cutoff_time = time.time() - (keep_days * 24 * 3600)

        deleted = 0
        for file_path in files:
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    deleted += 1
                except Exception as e:
                    logger.warning(f"删除文件失败 {file_path}: {e}")

        if deleted > 0:
            logger.info(f"清理了 {deleted} 个旧文件（保留 {keep_days} 天）")

        return deleted


# 全局单例
_global_output_manager: Optional[OutputManager] = None


def get_output_manager(project_root: Optional[Path] = None) -> OutputManager:
    """
    获取全局输出管理器（单例模式）

    Args:
        project_root: 项目根目录（仅在首次调用时生效）

    Returns:
        OutputManager 实例
    """
    global _global_output_manager
    if _global_output_manager is None:
        _global_output_manager = OutputManager(project_root=project_root)
    return _global_output_manager


# 便捷函数
def get_output_path(
    category: Union[OutputCategory, str],
    output_type: Union[OutputType, str],
    filename: Optional[str] = None,
    add_timestamp: bool = False,
) -> Path:
    """
    获取输出路径（便捷函数）

    Args:
        category: 输出类别
        output_type: 输出类型
        filename: 文件名
        add_timestamp: 是否添加时间戳

    Returns:
        输出路径
    """
    manager = get_output_manager()
    return manager.get_path(category, output_type, filename, add_timestamp=add_timestamp)
