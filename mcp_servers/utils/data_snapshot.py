#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DataSnapshot - 数据快照管理
==========================

M1里程碑核心组件：确保研究可复现

功能：
1. 数据版本快照
2. 数据校验与一致性检查
3. 快照对比
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)


@dataclass
class DataSnapshot:
    """
    数据快照
    
    记录数据的版本信息，确保可复现性
    """
    snapshot_id: str
    name: str
    description: str = ""
    
    # 数据源信息
    data_source: str = ""  # jqdata, akshare, mock
    data_type: str = ""    # market, factor, candidate_pool, etc.
    
    # 数据范围
    symbols: List[str] = field(default_factory=list)
    start_date: str = ""
    end_date: str = ""
    
    # 数据校验
    row_count: int = 0
    column_count: int = 0
    data_hash: str = ""
    schema_hash: str = ""
    
    # 元数据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    created_by: str = "system"
    tags: List[str] = field(default_factory=list)
    
    # 存储位置
    storage_path: str = ""
    storage_type: str = "file"  # file, mongodb, redis
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataSnapshot":
        return cls(**data)


class SnapshotManager:
    """
    数据快照管理器
    
    提供快照的创建、查询、对比功能
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "snapshots"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._index_file = self.storage_path / "snapshot_index.json"
        self._index: Dict[str, Dict] = self._load_index()
        self._mongo_db = None
        self._init_mongo()
    
    def _init_mongo(self):
        """初始化MongoDB连接"""
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            self._mongo_db = client.get_database("trquant")
        except:
            pass
    
    def _load_index(self) -> Dict[str, Dict]:
        """加载快照索引"""
        if self._index_file.exists():
            try:
                with open(self._index_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_index(self):
        """保存快照索引"""
        with open(self._index_file, 'w') as f:
            json.dump(self._index, f, indent=2, ensure_ascii=False)
    
    def create_snapshot(
        self,
        name: str,
        data: Any,
        data_source: str = "unknown",
        data_type: str = "generic",
        symbols: List[str] = None,
        start_date: str = "",
        end_date: str = "",
        description: str = "",
        tags: List[str] = None
    ) -> DataSnapshot:
        """
        创建数据快照
        
        Args:
            name: 快照名称
            data: 要快照的数据（DataFrame, dict, list等）
            data_source: 数据源
            data_type: 数据类型
            symbols: 涉及的股票代码
            start_date: 数据开始日期
            end_date: 数据结束日期
            description: 描述
            tags: 标签
        
        Returns:
            DataSnapshot对象
        """
        import uuid
        
        snapshot_id = f"snap_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # 计算数据统计和哈希
        row_count, column_count, data_hash, schema_hash = self._compute_data_stats(data)
        
        # 保存数据
        data_file = self.storage_path / f"{snapshot_id}_data.json"
        self._save_data(data, data_file)
        
        snapshot = DataSnapshot(
            snapshot_id=snapshot_id,
            name=name,
            description=description,
            data_source=data_source,
            data_type=data_type,
            symbols=symbols or [],
            start_date=start_date,
            end_date=end_date,
            row_count=row_count,
            column_count=column_count,
            data_hash=data_hash,
            schema_hash=schema_hash,
            storage_path=str(data_file),
            tags=tags or []
        )
        
        # 保存快照元数据
        meta_file = self.storage_path / f"{snapshot_id}_meta.json"
        with open(meta_file, 'w') as f:
            json.dump(snapshot.to_dict(), f, indent=2, ensure_ascii=False)
        
        # 更新索引
        self._index[snapshot_id] = {
            "name": name,
            "data_type": data_type,
            "data_source": data_source,
            "created_at": snapshot.created_at,
            "data_hash": data_hash,
            "tags": tags or []
        }
        self._save_index()
        
        # 同步到MongoDB
        if self._mongo_db is not None:
            try:
                self._mongo_db.data_snapshots.insert_one(snapshot.to_dict())
            except:
                pass
        
        logger.info(f"[Snapshot] 创建快照: {snapshot_id} ({name})")
        return snapshot
    
    def _compute_data_stats(self, data: Any) -> tuple:
        """计算数据统计信息"""
        row_count = 0
        column_count = 0
        schema_hash = ""
        
        try:
            # 尝试处理pandas DataFrame
            if hasattr(data, 'shape'):
                row_count, column_count = data.shape[0], data.shape[1] if len(data.shape) > 1 else 1
                schema_hash = hashlib.md5(str(list(data.columns)).encode()).hexdigest()[:8] if hasattr(data, 'columns') else ""
            elif isinstance(data, list):
                row_count = len(data)
                if data and isinstance(data[0], dict):
                    column_count = len(data[0])
                    schema_hash = hashlib.md5(str(sorted(data[0].keys())).encode()).hexdigest()[:8]
            elif isinstance(data, dict):
                row_count = 1
                column_count = len(data)
                schema_hash = hashlib.md5(str(sorted(data.keys())).encode()).hexdigest()[:8]
        except:
            pass
        
        # 计算数据哈希
        try:
            content = json.dumps(data, sort_keys=True, default=str)
            data_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        except:
            data_hash = hashlib.md5(str(data).encode()).hexdigest()[:16]
        
        return row_count, column_count, data_hash, schema_hash
    
    def _save_data(self, data: Any, file_path: Path):
        """保存数据到文件"""
        try:
            # 尝试转换DataFrame
            if hasattr(data, 'to_dict'):
                data = data.to_dict(orient='records')
            
            with open(file_path, 'w') as f:
                json.dump(data, f, default=str, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存数据失败: {e}")
    
    def get_snapshot(self, snapshot_id: str) -> Optional[DataSnapshot]:
        """获取快照元数据"""
        meta_file = self.storage_path / f"{snapshot_id}_meta.json"
        if not meta_file.exists():
            return None
        
        with open(meta_file, 'r') as f:
            return DataSnapshot.from_dict(json.load(f))
    
    def get_snapshot_data(self, snapshot_id: str) -> Optional[Any]:
        """获取快照数据"""
        data_file = self.storage_path / f"{snapshot_id}_data.json"
        if not data_file.exists():
            return None
        
        with open(data_file, 'r') as f:
            return json.load(f)
    
    def list_snapshots(
        self,
        data_type: str = None,
        data_source: str = None,
        tags: List[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """列出快照"""
        results = []
        
        for sid, info in self._index.items():
            if data_type and info.get("data_type") != data_type:
                continue
            if data_source and info.get("data_source") != data_source:
                continue
            if tags and not set(tags).issubset(set(info.get("tags", []))):
                continue
            
            results.append({"snapshot_id": sid, **info})
            
            if len(results) >= limit:
                break
        
        return sorted(results, key=lambda x: x.get("created_at", ""), reverse=True)
    
    def compare_snapshots(self, snapshot_id_1: str, snapshot_id_2: str) -> Dict[str, Any]:
        """对比两个快照"""
        snap1 = self.get_snapshot(snapshot_id_1)
        snap2 = self.get_snapshot(snapshot_id_2)
        
        if not snap1 or not snap2:
            return {"error": "快照不存在"}
        
        comparison = {
            "snapshot_1": snapshot_id_1,
            "snapshot_2": snapshot_id_2,
            "same_data": snap1.data_hash == snap2.data_hash,
            "same_schema": snap1.schema_hash == snap2.schema_hash,
            "row_diff": snap2.row_count - snap1.row_count,
            "column_diff": snap2.column_count - snap1.column_count,
            "time_diff": {
                "start_date": (snap1.start_date, snap2.start_date),
                "end_date": (snap1.end_date, snap2.end_date)
            }
        }
        
        return comparison
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """删除快照"""
        try:
            meta_file = self.storage_path / f"{snapshot_id}_meta.json"
            data_file = self.storage_path / f"{snapshot_id}_data.json"
            
            if meta_file.exists():
                meta_file.unlink()
            if data_file.exists():
                data_file.unlink()
            
            if snapshot_id in self._index:
                del self._index[snapshot_id]
                self._save_index()
            
            logger.info(f"[Snapshot] 删除快照: {snapshot_id}")
            return True
        except Exception as e:
            logger.error(f"删除快照失败: {e}")
            return False


# 全局管理器
_manager: Optional[SnapshotManager] = None

def get_snapshot_manager() -> SnapshotManager:
    """获取快照管理器"""
    global _manager
    if _manager is None:
        _manager = SnapshotManager()
    return _manager
