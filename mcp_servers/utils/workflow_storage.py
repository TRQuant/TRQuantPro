#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工作流状态持久化存储
==================

提供工作流状态的持久化存储、查询和恢复功能。
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class WorkflowStorage:
    """工作流状态持久化存储"""
    
    def __init__(self, storage_path: Path):
        """
        初始化工作流存储
        
        Args:
            storage_path: 存储目录路径
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"工作流存储目录: {self.storage_path}")
    
    def save_workflow_status(self, workflow_id: str, status: Dict[str, Any]) -> None:
        """
        保存工作流状态
        
        Args:
            workflow_id: 工作流ID
            status: 状态数据
        """
        file_path = self.storage_path / f"{workflow_id}.json"
        
        # 添加保存时间戳
        status_data = status.copy()
        status_data["_saved_at"] = datetime.now().isoformat()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False, default=str)
            logger.debug(f"工作流状态已保存: {workflow_id}")
        except Exception as e:
            logger.error(f"保存工作流状态失败: {workflow_id}, 错误: {e}")
            raise
    
    def load_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """
        加载工作流状态
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            状态数据，如果不存在则返回None
        """
        file_path = self.storage_path / f"{workflow_id}.json"
        
        if not file_path.exists():
            logger.debug(f"工作流状态不存在: {workflow_id}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                status = json.load(f)
            logger.debug(f"工作流状态已加载: {workflow_id}")
            return status
        except Exception as e:
            logger.error(f"加载工作流状态失败: {workflow_id}, 错误: {e}")
            return None
    
    def list_workflows(
        self,
        limit: int = 100,
        offset: int = 0,
        status_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        列出所有工作流（按时间倒序）
        
        Args:
            limit: 返回数量限制
            offset: 偏移量
            status_filter: 状态过滤（completed, failed, running, all）
        
        Returns:
            工作流列表
        """
        workflows = []
        
        # 获取所有工作流文件
        workflow_files = sorted(
            self.storage_path.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        for file_path in workflow_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    workflow = json.load(f)
                
                # 状态过滤
                if status_filter and status_filter != "all":
                    workflow_status = workflow.get("status", "")
                    if workflow_status != status_filter:
                        continue
                
                # 添加文件信息
                workflow["_file_path"] = str(file_path)
                workflow["_file_mtime"] = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                
                workflows.append(workflow)
            except Exception as e:
                logger.warning(f"加载工作流文件失败: {file_path}, 错误: {e}")
                continue
        
        # 分页
        return workflows[offset:offset+limit]
    
    def delete_workflow(self, workflow_id: str) -> bool:
        """
        删除工作流状态
        
        Args:
            workflow_id: 工作流ID
        
        Returns:
            是否删除成功
        """
        file_path = self.storage_path / f"{workflow_id}.json"
        
        if not file_path.exists():
            logger.warning(f"工作流状态不存在，无法删除: {workflow_id}")
            return False
        
        try:
            file_path.unlink()
            logger.info(f"工作流状态已删除: {workflow_id}")
            return True
        except Exception as e:
            logger.error(f"删除工作流状态失败: {workflow_id}, 错误: {e}")
            return False
    
    def get_workflow_count(self, status_filter: Optional[str] = None) -> int:
        """
        获取工作流数量
        
        Args:
            status_filter: 状态过滤
        
        Returns:
            工作流数量
        """
        if status_filter and status_filter != "all":
            workflows = self.list_workflows(limit=10000, status_filter=status_filter)
            return len(workflows)
        else:
            return len(list(self.storage_path.glob("*.json")))
    
    def cleanup_old_workflows(self, days: int = 30) -> int:
        """
        清理旧的工作流（超过指定天数）
        
        Args:
            days: 保留天数
        
        Returns:
            清理的数量
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(days=days)
        cleaned_count = 0
        
        for file_path in self.storage_path.glob("*.json"):
            try:
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_mtime < cutoff_time:
                    file_path.unlink()
                    cleaned_count += 1
                    logger.debug(f"清理旧工作流: {file_path.name}")
            except Exception as e:
                logger.warning(f"清理工作流失败: {file_path}, 错误: {e}")
        
        if cleaned_count > 0:
            logger.info(f"清理了 {cleaned_count} 个旧工作流（超过 {days} 天）")
        
        return cleaned_count









