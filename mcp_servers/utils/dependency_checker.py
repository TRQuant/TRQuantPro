#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
依赖检查器
==========

提供MCP服务器依赖检查功能，避免"代码完成但环境缺失"类失败。
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class DependencyChecker:
    """依赖检查器"""
    
    # 必需依赖配置
    REQUIRED_DEPENDENCIES = {
        "trquant-factor": ["scipy", "numpy", "pandas"],
        "trquant-strategy-optimizer": ["scipy", "numpy"],
        "trquant-workflow": ["pymongo"],
        "trquant-data-quality": ["pandas"],
        "trquant-backtest": ["pandas", "numpy"],
        "trquant-report": ["pandas"],
    }
    
    # 可选依赖配置
    OPTIONAL_DEPENDENCIES = {
        "trquant-factor": ["jqdata"],
        "trquant-workflow": ["jqdata", "akshare"],
        "trquant-data-quality": ["jqdata", "tushare"],
        "trquant-backtest": ["jqdata"],
    }
    
    def __init__(self):
        """初始化依赖检查器"""
        self._cache: Dict[str, Dict[str, bool]] = {}
    
    def check_dependencies(self, server_name: str) -> Dict[str, Any]:
        """
        检查服务器依赖
        
        Args:
            server_name: 服务器名称
        
        Returns:
            依赖检查结果
        """
        required = self.REQUIRED_DEPENDENCIES.get(server_name, [])
        optional = self.OPTIONAL_DEPENDENCIES.get(server_name, [])
        
        results = {
            "required": {},
            "optional": {},
            "all_required_available": True,
            "missing_required": [],
            "missing_optional": []
        }
        
        # 检查必需依赖
        for dep in required:
            available = self._check_module(dep)
            results["required"][dep] = available
            if not available:
                results["all_required_available"] = False
                results["missing_required"].append(dep)
        
        # 检查可选依赖
        for dep in optional:
            available = self._check_module(dep)
            results["optional"][dep] = available
            if not available:
                results["missing_optional"].append(dep)
        
        return results
    
    def _check_module(self, module_name: str) -> bool:
        """
        检查模块是否可用
        
        Args:
            module_name: 模块名称
        
        Returns:
            是否可用
        """
        # 使用缓存
        if module_name in self._cache.get("modules", {}):
            return self._cache["modules"][module_name]
        
        try:
            __import__(module_name)
            # 更新缓存
            if "modules" not in self._cache:
                self._cache["modules"] = {}
            self._cache["modules"][module_name] = True
            return True
        except ImportError:
            if "modules" not in self._cache:
                self._cache["modules"] = {}
            self._cache["modules"][module_name] = False
            return False
        except Exception as e:
            logger.warning(f"检查模块 {module_name} 时出错: {e}")
            if "modules" not in self._cache:
                self._cache["modules"] = {}
            self._cache["modules"][module_name] = False
            return False
    
    def check_all_servers(self) -> Dict[str, Dict[str, Any]]:
        """
        检查所有服务器的依赖
        
        Returns:
            所有服务器的依赖检查结果
        """
        all_results = {}
        
        all_servers = set(self.REQUIRED_DEPENDENCIES.keys()) | set(self.OPTIONAL_DEPENDENCIES.keys())
        
        for server_name in all_servers:
            all_results[server_name] = self.check_dependencies(server_name)
        
        return all_results
    
    def get_missing_dependencies_summary(self) -> Dict[str, List[str]]:
        """
        获取缺失依赖摘要
        
        Returns:
            缺失依赖摘要（按服务器分组）
        """
        summary = {}
        
        all_servers = set(self.REQUIRED_DEPENDENCIES.keys()) | set(self.OPTIONAL_DEPENDENCIES.keys())
        
        for server_name in all_servers:
            results = self.check_dependencies(server_name)
            missing = results["missing_required"] + results["missing_optional"]
            if missing:
                summary[server_name] = missing
        
        return summary
    
    def format_check_report(self, server_name: Optional[str] = None) -> str:
        """
        格式化检查报告
        
        Args:
            server_name: 服务器名称（如果为None则检查所有服务器）
        
        Returns:
            格式化的报告字符串
        """
        if server_name:
            results = self.check_dependencies(server_name)
            return self._format_single_server_report(server_name, results)
        else:
            all_results = self.check_all_servers()
            return self._format_all_servers_report(all_results)
    
    def _format_single_server_report(self, server_name: str, results: Dict[str, Any]) -> str:
        """格式化单个服务器报告"""
        lines = [f"📦 {server_name} 依赖检查报告", "=" * 60]
        
        # 必需依赖
        lines.append("\n✅ 必需依赖:")
        for dep, available in results["required"].items():
            status = "✅" if available else "❌"
            lines.append(f"  {status} {dep}")
        
        # 可选依赖
        if results["optional"]:
            lines.append("\n⚠️  可选依赖:")
            for dep, available in results["optional"].items():
                status = "✅" if available else "⚠️"
                lines.append(f"  {status} {dep}")
        
        # 总结
        if results["all_required_available"]:
            lines.append("\n✅ 所有必需依赖已安装")
        else:
            lines.append(f"\n❌ 缺少必需依赖: {', '.join(results['missing_required'])}")
        
        return "\n".join(lines)
    
    def _format_all_servers_report(self, all_results: Dict[str, Dict[str, Any]]) -> str:
        """格式化所有服务器报告"""
        lines = ["📦 所有服务器依赖检查报告", "=" * 60]
        
        for server_name, results in all_results.items():
            lines.append(f"\n{server_name}:")
            if results["all_required_available"]:
                lines.append("  ✅ 所有必需依赖已安装")
            else:
                lines.append(f"  ❌ 缺少必需依赖: {', '.join(results['missing_required'])}")
        
        return "\n".join(lines)


# 全局实例
_dependency_checker: Optional[DependencyChecker] = None


def get_dependency_checker() -> DependencyChecker:
    """获取依赖检查器实例（单例）"""
    global _dependency_checker
    if _dependency_checker is None:
        _dependency_checker = DependencyChecker()
    return _dependency_checker









