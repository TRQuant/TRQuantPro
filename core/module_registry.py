#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块注册表 - 快速查找和验证模块导入
===================================
解决重复开发、错误导入问题
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


class ModuleRegistry:
    """模块注册表 - 确保正确导入"""
    
    # 核心模块映射 (类名 -> 正确导入路径)
    MODULES = {
        # JQData相关
        "JQDataClient": "jqdata.client",
        "JQDataProvider": "core.data.jqdata_provider",
        "DataPermission": "jqdata.client",
        
        # 主线扫描
        "MainlineBasedScanner": "core.mainline_scanner",
        "MainlineMapper": "core.mainline_mapper",
        
        # 候选池
        "CandidatePoolBuilder": "core.candidate_pool_builder",
        "CandidateStock": "core.candidate_pool_builder",
        "CandidatePool": "core.candidate_pool_builder",
        
        # 动量分析
        "MomentumGrowthScanner": "core.momentum_growth_scanner",
        "MomentumGrowthStock": "core.momentum_growth_scanner",
        
        # 评分
        "FiveDimensionScorer": "core.five_dimension_scorer",
        
        # 策略
        "StrategyGenerator": "core.strategy_generator",
        "StrategyManager": "core.strategy_manager",
        
        # 回测
        "BacktestEngine": "core.backtest_engine",
        
        # 配置
        "ConfigManager": "config.config_manager",
        "get_config_manager": "config.config_manager",
    }
    
    # 常见错误导入 -> 正确导入
    IMPORT_FIXES = {
        "core.data.jqdata_provider.JQDataClient": "jqdata.client.JQDataClient",
        "core.mainline_scanner.MainlineScanner": "core.mainline_scanner.MainlineBasedScanner",
    }
    
    @classmethod
    def get_import_path(cls, class_name: str) -> Optional[str]:
        """获取类的正确导入路径"""
        return cls.MODULES.get(class_name)
    
    @classmethod
    def get_import_statement(cls, class_name: str) -> Optional[str]:
        """获取完整导入语句"""
        path = cls.get_import_path(class_name)
        if path:
            return f"from {path} import {class_name}"
        return None
    
    @classmethod
    def validate_import(cls, import_statement: str) -> Dict[str, Any]:
        """验证导入语句是否正确"""
        # 检查是否是已知错误
        for wrong, correct in cls.IMPORT_FIXES.items():
            if wrong in import_statement:
                return {
                    "valid": False,
                    "error": f"错误导入: {wrong}",
                    "suggestion": f"应使用: from {correct.rsplit('.', 1)[0]} import {correct.rsplit('.', 1)[1]}"
                }
        return {"valid": True}
    
    @classmethod
    def quick_import(cls, class_name: str) -> Any:
        """快速导入类（用于动态加载）"""
        path = cls.get_import_path(class_name)
        if not path:
            raise ImportError(f"未知类: {class_name}")
        
        try:
            module = __import__(path, fromlist=[class_name])
            return getattr(module, class_name)
        except Exception as e:
            raise ImportError(f"导入失败 {class_name} from {path}: {e}")
    
    @classmethod
    def get_jqdata_client(cls) -> Any:
        """快速获取已认证的JQData客户端"""
        JQDataClient = cls.quick_import("JQDataClient")
        get_config_manager = cls.quick_import("get_config_manager")
        
        client = JQDataClient()
        if not client.is_authenticated():
            config = get_config_manager().get_jqdata_config()
            if config.get("username") and config.get("password"):
                client.authenticate(config["username"], config["password"])
        
        return client
    
    @classmethod
    def get_mainline_scanner(cls) -> Any:
        """快速获取主线扫描器（已配置JQData）"""
        MainlineBasedScanner = cls.quick_import("MainlineBasedScanner")
        jq_client = cls.get_jqdata_client()
        return MainlineBasedScanner(jq_client=jq_client)
    
    @classmethod
    def get_candidate_pool_builder(cls) -> Any:
        """快速获取候选池构建器（已配置JQData）"""
        CandidatePoolBuilder = cls.quick_import("CandidatePoolBuilder")
        jq_client = cls.get_jqdata_client()
        return CandidatePoolBuilder(jq_client=jq_client)
    
    @classmethod
    def print_all_modules(cls):
        """打印所有注册的模块"""
        print("\n📦 TRQuant 模块注册表")
        print("=" * 60)
        for name, path in sorted(cls.MODULES.items()):
            print(f"  from {path} import {name}")
        print("=" * 60)


# 便捷函数
def get_jqdata_client():
    """获取JQData客户端"""
    return ModuleRegistry.get_jqdata_client()

def get_mainline_scanner():
    """获取主线扫描器"""
    return ModuleRegistry.get_mainline_scanner()

def get_candidate_pool_builder():
    """获取候选池构建器"""
    return ModuleRegistry.get_candidate_pool_builder()


if __name__ == "__main__":
    ModuleRegistry.print_all_modules()
