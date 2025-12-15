# -*- coding: utf-8 -*-
"""
数据库备份管理器
================

管理MongoDB数据库的备份和恢复

功能:
- 定时备份
- 增量备份
- 压缩存储
- 备份清理
- 恢复验证
"""

import logging
import os
import json
import gzip
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False


@dataclass
class BackupInfo:
    """备份信息"""
    backup_id: str
    created_at: datetime
    database: str
    collections: List[str]
    size_bytes: int
    compressed: bool
    path: str
    status: str  # completed, failed, partial


class BackupManager:
    """备份管理器"""
    
    def __init__(self, 
                 connection_string: str = None,
                 database_name: str = "trquant",
                 backup_dir: str = None):
        self.connection_string = connection_string or os.getenv(
            "MONGODB_URI", "mongodb://localhost:27017"
        )
        self.database_name = database_name
        self.backup_dir = Path(backup_dir or "backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self._client = None
        self._db = None
    
    def connect(self):
        """连接数据库"""
        if not PYMONGO_AVAILABLE:
            raise ImportError("pymongo未安装")
        
        if self._client is None:
            self._client = MongoClient(self.connection_string)
            self._db = self._client[self.database_name]
        return self._db
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
    
    def create_backup(self, 
                      collections: List[str] = None,
                      compress: bool = True,
                      description: str = "") -> BackupInfo:
        """
        创建备份
        
        Args:
            collections: 要备份的集合列表，为None时备份所有
            compress: 是否压缩
            description: 备份描述
            
        Returns:
            BackupInfo
        """
        db = self.connect()
        
        # 生成备份ID
        backup_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # 获取要备份的集合
        if collections is None:
            collections = db.list_collection_names()
        
        # 排除系统集合
        collections = [c for c in collections if not c.startswith("system.")]
        
        total_size = 0
        backed_up = []
        failed = []
        
        for collection_name in collections:
            try:
                collection = db[collection_name]
                documents = list(collection.find())
                
                # 转换特殊类型
                for doc in documents:
                    for key, value in doc.items():
                        if key == '_id':
                            doc[key] = str(value)
                        elif isinstance(value, datetime):
                            doc[key] = value.isoformat()
                
                # 写入文件
                output_file = backup_path / f"{collection_name}.json"
                
                if compress:
                    output_file = backup_path / f"{collection_name}.json.gz"
                    with gzip.open(output_file, 'wt', encoding='utf-8') as f:
                        json.dump(documents, f, ensure_ascii=False)
                else:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(documents, f, ensure_ascii=False, indent=2)
                
                file_size = output_file.stat().st_size
                total_size += file_size
                backed_up.append(collection_name)
                
                logger.info(f"已备份 {collection_name}: {len(documents)} 条, {file_size} 字节")
                
            except Exception as e:
                logger.error(f"备份 {collection_name} 失败: {e}")
                failed.append(collection_name)
        
        # 保存元数据
        metadata = {
            "backup_id": backup_id,
            "created_at": datetime.utcnow().isoformat(),
            "database": self.database_name,
            "collections": backed_up,
            "failed_collections": failed,
            "total_size": total_size,
            "compressed": compress,
            "description": description
        }
        
        with open(backup_path / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        status = "completed" if not failed else ("partial" if backed_up else "failed")
        
        backup_info = BackupInfo(
            backup_id=backup_id,
            created_at=datetime.utcnow(),
            database=self.database_name,
            collections=backed_up,
            size_bytes=total_size,
            compressed=compress,
            path=str(backup_path),
            status=status
        )
        
        logger.info(f"备份完成: {backup_id}, 状态: {status}")
        return backup_info
    
    def restore_backup(self,
                       backup_id: str,
                       collections: List[str] = None,
                       drop_existing: bool = False) -> Dict[str, int]:
        """
        恢复备份
        
        Args:
            backup_id: 备份ID
            collections: 要恢复的集合，为None时恢复所有
            drop_existing: 是否先删除现有数据
            
        Returns:
            恢复统计 {collection: count}
        """
        db = self.connect()
        backup_path = self.backup_dir / backup_id
        
        if not backup_path.exists():
            raise FileNotFoundError(f"备份不存在: {backup_id}")
        
        # 读取元数据
        with open(backup_path / "metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        compressed = metadata.get("compressed", False)
        available_collections = metadata.get("collections", [])
        
        if collections is None:
            collections = available_collections
        else:
            collections = [c for c in collections if c in available_collections]
        
        result = {}
        
        for collection_name in collections:
            try:
                # 读取备份文件
                if compressed:
                    input_file = backup_path / f"{collection_name}.json.gz"
                    with gzip.open(input_file, 'rt', encoding='utf-8') as f:
                        documents = json.load(f)
                else:
                    input_file = backup_path / f"{collection_name}.json"
                    with open(input_file, 'r', encoding='utf-8') as f:
                        documents = json.load(f)
                
                collection = db[collection_name]
                
                if drop_existing:
                    collection.delete_many({})
                
                # 移除_id避免冲突
                for doc in documents:
                    doc.pop('_id', None)
                
                if documents:
                    collection.insert_many(documents)
                
                result[collection_name] = len(documents)
                logger.info(f"已恢复 {collection_name}: {len(documents)} 条")
                
            except Exception as e:
                logger.error(f"恢复 {collection_name} 失败: {e}")
                result[collection_name] = -1
        
        return result
    
    def list_backups(self) -> List[BackupInfo]:
        """列出所有备份"""
        backups = []
        
        for backup_dir in sorted(self.backup_dir.iterdir(), reverse=True):
            if not backup_dir.is_dir():
                continue
            
            metadata_file = backup_dir / "metadata.json"
            if not metadata_file.exists():
                continue
            
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                backup_info = BackupInfo(
                    backup_id=metadata["backup_id"],
                    created_at=datetime.fromisoformat(metadata["created_at"]),
                    database=metadata["database"],
                    collections=metadata["collections"],
                    size_bytes=metadata["total_size"],
                    compressed=metadata.get("compressed", False),
                    path=str(backup_dir),
                    status="completed"
                )
                backups.append(backup_info)
            except Exception as e:
                logger.warning(f"读取备份元数据失败 {backup_dir}: {e}")
        
        return backups
    
    def delete_backup(self, backup_id: str) -> bool:
        """删除备份"""
        backup_path = self.backup_dir / backup_id
        
        if not backup_path.exists():
            return False
        
        shutil.rmtree(backup_path)
        logger.info(f"已删除备份: {backup_id}")
        return True
    
    def cleanup_old_backups(self, keep_days: int = 30, keep_count: int = 5) -> List[str]:
        """
        清理旧备份
        
        Args:
            keep_days: 保留天数
            keep_count: 最少保留数量
            
        Returns:
            删除的备份ID列表
        """
        backups = self.list_backups()
        cutoff_date = datetime.utcnow() - timedelta(days=keep_days)
        
        # 按时间排序，保留最新的keep_count个
        backups_to_keep = set()
        for backup in backups[:keep_count]:
            backups_to_keep.add(backup.backup_id)
        
        deleted = []
        for backup in backups:
            if backup.backup_id in backups_to_keep:
                continue
            
            if backup.created_at < cutoff_date:
                if self.delete_backup(backup.backup_id):
                    deleted.append(backup.backup_id)
        
        return deleted
    
    def get_backup_info(self, backup_id: str) -> Optional[BackupInfo]:
        """获取备份信息"""
        backup_path = self.backup_dir / backup_id
        
        if not backup_path.exists():
            return None
        
        metadata_file = backup_path / "metadata.json"
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        return BackupInfo(
            backup_id=metadata["backup_id"],
            created_at=datetime.fromisoformat(metadata["created_at"]),
            database=metadata["database"],
            collections=metadata["collections"],
            size_bytes=metadata["total_size"],
            compressed=metadata.get("compressed", False),
            path=str(backup_path),
            status="completed"
        )


def get_backup_manager(backup_dir: str = None) -> BackupManager:
    """获取备份管理器"""
    return BackupManager(backup_dir=backup_dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    manager = get_backup_manager("backups")
    
    print("TRQuant 备份管理器")
    print("=" * 50)
    
    # 列出备份
    backups = manager.list_backups()
    print(f"\n已有备份: {len(backups)} 个")
    
    for backup in backups[:5]:
        print(f"  - {backup.backup_id}: {len(backup.collections)} 集合, {backup.size_bytes} 字节")
