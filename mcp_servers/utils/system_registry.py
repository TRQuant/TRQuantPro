#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统状态注册表
=============

管理TRQuant系统的模块状态、依赖关系和变更记录。

功能:
    - 模块注册与状态管理
    - 系统状态快照
    - 开发变更记录
    - 依赖关系检查
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib
import subprocess

logger = logging.getLogger(__name__)

# 数据目录
REGISTRY_DIR = Path(__file__).parent.parent.parent / ".trquant" / "registry"
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

# 文件路径
MODULES_FILE = REGISTRY_DIR / "modules.json"
SNAPSHOTS_DIR = REGISTRY_DIR / "snapshots"
CHANGES_FILE = REGISTRY_DIR / "changes.json"

SNAPSHOTS_DIR.mkdir(exist_ok=True)


class ModuleStatus:
    """模块状态"""
    ACTIVE = "active"           # 活跃
    DEVELOPING = "developing"   # 开发中
    TESTING = "testing"         # 测试中
    DEPRECATED = "deprecated"   # 已废弃
    DISABLED = "disabled"       # 已禁用


class SystemRegistry:
    """系统状态注册表"""
    
    def __init__(self):
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        # 加载模块注册表
        if MODULES_FILE.exists():
            self.modules = json.loads(MODULES_FILE.read_text(encoding='utf-8'))
        else:
            self.modules = {}
        
        # 加载变更记录
        if CHANGES_FILE.exists():
            self.changes = json.loads(CHANGES_FILE.read_text(encoding='utf-8'))
        else:
            self.changes = []
    
    def _save_modules(self):
        """保存模块注册表"""
        MODULES_FILE.write_text(json.dumps(self.modules, indent=2, ensure_ascii=False), encoding='utf-8')
    
    def _save_changes(self):
        """保存变更记录"""
        CHANGES_FILE.write_text(json.dumps(self.changes, indent=2, ensure_ascii=False), encoding='utf-8')
    
    # ==================== 模块管理 ====================
    
    def register_module(
        self,
        module_id: str,
        name: str,
        version: str = "1.0",
        status: str = ModuleStatus.ACTIVE,
        mcp_server: str = None,
        tools: List[str] = None,
        dependencies: List[str] = None,
        notes: str = ""
    ) -> Dict:
        """注册模块"""
        module = {
            "module_id": module_id,
            "name": name,
            "version": version,
            "status": status,
            "mcp_server": mcp_server,
            "tools": tools or [],
            "dependencies": dependencies or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "notes": notes
        }
        self.modules[module_id] = module
        self._save_modules()
        logger.info(f"模块已注册: {module_id}")
        return module
    
    def update_module(self, module_id: str, **kwargs) -> Optional[Dict]:
        """更新模块"""
        if module_id not in self.modules:
            return None
        
        for key, value in kwargs.items():
            if key in self.modules[module_id]:
                self.modules[module_id][key] = value
        
        self.modules[module_id]["updated_at"] = datetime.now().isoformat()
        self._save_modules()
        return self.modules[module_id]
    
    def get_module(self, module_id: str) -> Optional[Dict]:
        """获取模块"""
        return self.modules.get(module_id)
    
    def list_modules(self, status: str = None) -> List[Dict]:
        """列出模块"""
        modules = list(self.modules.values())
        if status:
            modules = [m for m in modules if m.get("status") == status]
        return modules
    
    def check_dependencies(self, module_id: str) -> Dict:
        """检查模块依赖"""
        module = self.get_module(module_id)
        if not module:
            return {"error": f"模块不存在: {module_id}"}
        
        deps = module.get("dependencies", [])
        result = {
            "module_id": module_id,
            "dependencies": [],
            "missing": [],
            "all_satisfied": True
        }
        
        for dep in deps:
            if dep in self.modules:
                dep_module = self.modules[dep]
                result["dependencies"].append({
                    "id": dep,
                    "status": dep_module.get("status"),
                    "satisfied": dep_module.get("status") == ModuleStatus.ACTIVE
                })
                if dep_module.get("status") != ModuleStatus.ACTIVE:
                    result["all_satisfied"] = False
            else:
                result["missing"].append(dep)
                result["all_satisfied"] = False
        
        return result
    
    # ==================== 系统快照 ====================
    
    def create_snapshot(self, description: str = "") -> Dict:
        """创建系统状态快照"""
        snapshot_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 收集模块状态
        modules_status = {}
        for mid, module in self.modules.items():
            modules_status[mid] = {
                "status": module.get("status"),
                "version": module.get("version"),
                "tools_count": len(module.get("tools", []))
            }
        
        # 检查数据库状态
        databases = self._check_databases()
        
        # 检查服务状态
        services = self._check_services()
        
        # 获取Git信息
        git_info = self._get_git_info()
        
        snapshot = {
            "snapshot_id": snapshot_id,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "modules": modules_status,
            "databases": databases,
            "services": services,
            "git": git_info,
            "modules_count": len(self.modules),
            "active_modules": len([m for m in self.modules.values() if m.get("status") == ModuleStatus.ACTIVE])
        }
        
        # 保存快照
        snapshot_file = SNAPSHOTS_DIR / f"{snapshot_id}.json"
        snapshot_file.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding='utf-8')
        
        logger.info(f"系统快照已创建: {snapshot_id}")
        return snapshot
    
    def get_snapshot(self, snapshot_id: str) -> Optional[Dict]:
        """获取快照"""
        snapshot_file = SNAPSHOTS_DIR / f"{snapshot_id}.json"
        if snapshot_file.exists():
            return json.loads(snapshot_file.read_text(encoding='utf-8'))
        return None
    
    def list_snapshots(self, limit: int = 10) -> List[Dict]:
        """列出快照"""
        snapshots = []
        for f in sorted(SNAPSHOTS_DIR.glob("snap_*.json"), reverse=True)[:limit]:
            data = json.loads(f.read_text(encoding='utf-8'))
            snapshots.append({
                "snapshot_id": data.get("snapshot_id"),
                "timestamp": data.get("timestamp"),
                "description": data.get("description"),
                "modules_count": data.get("modules_count"),
                "active_modules": data.get("active_modules")
            })
        return snapshots
    
    def get_current_status(self) -> Dict:
        """获取当前系统状态"""
        return {
            "timestamp": datetime.now().isoformat(),
            "modules": {
                "total": len(self.modules),
                "active": len([m for m in self.modules.values() if m.get("status") == ModuleStatus.ACTIVE]),
                "developing": len([m for m in self.modules.values() if m.get("status") == ModuleStatus.DEVELOPING]),
                "list": [{"id": m["module_id"], "name": m["name"], "status": m["status"]} 
                         for m in self.modules.values()]
            },
            "databases": self._check_databases(),
            "services": self._check_services(),
            "git": self._get_git_info(),
            "recent_changes": self.changes[-5:] if self.changes else []
        }
    
    def _check_databases(self) -> Dict:
        """检查数据库状态"""
        result = {}
        
        # MongoDB
        try:
            from pymongo import MongoClient
            client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=1000)
            client.server_info()
            db = client["jqquant"]
            result["mongodb"] = {
                "status": "running",
                "collections": len(db.list_collection_names())
            }
        except:
            result["mongodb"] = {"status": "not_running"}
        
        # Chroma
        chroma_path = Path(__file__).parent.parent.parent / "data" / "kb"
        if chroma_path.exists():
            indexes = len(list(chroma_path.glob("*/chroma.sqlite3")))
            result["chroma"] = {"status": "available", "indexes": indexes}
        else:
            result["chroma"] = {"status": "not_found"}
        
        # Redis
        try:
            import redis
            r = redis.Redis(host='localhost', port=6379, socket_timeout=1)
            r.ping()
            result["redis"] = {"status": "running"}
        except:
            result["redis"] = {"status": "not_running"}
        
        return result
    
    def _check_services(self) -> Dict:
        """检查服务状态"""
        mcp_servers = list(Path(__file__).parent.parent.glob("*_server*.py"))
        return {
            "mcp_servers": len(mcp_servers),
            "mcp_server_files": [f.name for f in mcp_servers[:10]]
        }
    
    def _get_git_info(self) -> Dict:
        """获取Git信息"""
        try:
            root = Path(__file__).parent.parent.parent
            commit = subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], 
                cwd=root, stderr=subprocess.DEVNULL
            ).decode().strip()
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"], 
                cwd=root, stderr=subprocess.DEVNULL
            ).decode().strip()
            return {"commit": commit, "branch": branch}
        except:
            return {"commit": "unknown", "branch": "unknown"}
    
    # ==================== 变更记录 ====================
    
    def record_change(
        self,
        module: str,
        action: str,
        description: str,
        files_changed: List[str] = None,
        git_commit: str = None
    ) -> Dict:
        """记录开发变更"""
        change_id = f"chg_{hashlib.md5(f'{module}{datetime.now().isoformat()}'.encode()).hexdigest()[:8]}"
        
        change = {
            "change_id": change_id,
            "timestamp": datetime.now().isoformat(),
            "module": module,
            "action": action,
            "description": description,
            "files_changed": files_changed or [],
            "git_commit": git_commit or self._get_git_info().get("commit", "")
        }
        
        self.changes.append(change)
        self._save_changes()
        logger.info(f"变更已记录: {change_id}")
        return change
    
    def list_changes(self, module: str = None, limit: int = 20) -> List[Dict]:
        """列出变更记录"""
        changes = self.changes
        if module:
            changes = [c for c in changes if c.get("module") == module]
        return changes[-limit:]


# 全局实例
_registry = None

def get_registry() -> SystemRegistry:
    """获取注册表实例"""
    global _registry
    if _registry is None:
        _registry = SystemRegistry()
    return _registry
