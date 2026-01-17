"""
版本管理器

管理不同版本的服务实现，支持多版本并存和独立升级。

Author: TRQuant Team
Date: 2025-12-21
"""

from typing import Dict, Type, List, Optional
import logging

logger = logging.getLogger(__name__)

# 全局版本管理器实例
_version_manager: Optional['VersionManager'] = None


class VersionManager:
    """
    版本管理器
    
    功能:
    1. 注册不同版本的服务实现
    2. 根据版本标识路由到对应服务
    3. 支持版本降级（如果请求的版本不存在，使用最新版本）
    4. 支持版本列表查询
    """
    
    def __init__(self):
        self._services: Dict[str, Type] = {}  # version -> service_class
        self._instances: Dict[str, object] = {}  # version -> service_instance (单例)
        self._default_version: Optional[str] = None
    
    def register(
        self,
        version: str,
        service_class: Type,
        is_default: bool = False,
        singleton: bool = True
    ):
        """
        注册服务版本
        
        Args:
            version: 版本标识（如 "v2", "v3"）
            service_class: 服务类（必须实现对应接口）
            is_default: 是否设为默认版本
            singleton: 是否使用单例模式
        """
        self._services[version] = service_class
        
        if is_default or self._default_version is None:
            self._default_version = version
        
        if singleton:
            # 预创建单例实例
            try:
                self._instances[version] = service_class()
            except Exception as e:
                logger.warning(f"预创建 {version} 服务实例失败: {e}")
        
        logger.info(f"已注册服务版本: {version} (默认: {is_default})")
    
    def get_service(self, version: Optional[str] = None, create_new: bool = False):
        """
        获取指定版本的服务实例
        
        Args:
            version: 版本标识，如果为None则使用默认版本
            create_new: 是否创建新实例（忽略单例）
            
        Returns:
            服务实例
        """
        # 确定版本
        if version is None:
            version = self._default_version
        
        if version is None:
            raise ValueError("没有可用的服务版本，请先注册服务")
        
        # 检查版本是否存在
        if version not in self._services:
            logger.warning(f"版本 {version} 不存在，降级到默认版本 {self._default_version}")
            version = self._default_version
        
        # 获取实例
        if create_new:
            return self._services[version]()
        
        # 使用单例
        if version not in self._instances:
            self._instances[version] = self._services[version]()
        
        return self._instances[version]
    
    def list_versions(self) -> List[str]:
        """列出所有可用版本"""
        return sorted(self._services.keys())
    
    def get_default_version(self) -> Optional[str]:
        """获取默认版本"""
        return self._default_version
    
    def set_default_version(self, version: str):
        """设置默认版本"""
        if version not in self._services:
            raise ValueError(f"版本 {version} 未注册")
        self._default_version = version
        logger.info(f"默认版本已设置为: {version}")
    
    def unregister(self, version: str):
        """注销服务版本"""
        if version in self._services:
            del self._services[version]
        if version in self._instances:
            del self._instances[version]
        if self._default_version == version:
            # 重新选择默认版本
            if self._services:
                self._default_version = max(self._services.keys())
            else:
                self._default_version = None
        logger.info(f"已注销服务版本: {version}")


def get_version_manager() -> VersionManager:
    """获取全局版本管理器实例（单例）"""
    global _version_manager
    if _version_manager is None:
        _version_manager = VersionManager()
    return _version_manager

