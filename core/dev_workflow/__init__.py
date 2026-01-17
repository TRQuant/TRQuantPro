#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 开发工作流模块
=====================

提供标准化开发流程支持：
- 开发前调研
- 代码复用检查
- 增量测试验证
- 测试结果存储
- 知识库记录
"""

from .test_result_storage import (
    TestResult,
    TestSession,
    TestResultStorage,
    get_test_storage,
    record_test_result,
    query_tests,
    get_module_stats
)

__all__ = [
    "TestResult",
    "TestSession", 
    "TestResultStorage",
    "get_test_storage",
    "record_test_result",
    "query_tests",
    "get_module_stats"
]
