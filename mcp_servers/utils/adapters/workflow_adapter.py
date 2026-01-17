"""
工作流MCP适配器

连接MCP工具调用和业务服务，实现版本路由和格式转换。

Author: TRQuant Team
Date: 2025-12-21
"""

from typing import Dict, Any, List, Optional
import logging

from core.mcp.interfaces.workflow_interface import (
    IWorkflowService,
    WorkflowRequest,
    WorkflowResponse,
    WorkflowStep
)
from core.mcp.versioning.version_manager import get_version_manager

logger = logging.getLogger(__name__)

# 全局适配器实例
_adapter: Optional['WorkflowMCPAdapter'] = None


class WorkflowMCPAdapter:
    """
    工作流MCP适配器
    
    功能:
    1. 将MCP工具调用转换为服务接口调用
    2. 路由到对应版本的服务
    3. 转换响应格式为MCP格式
    4. 处理版本兼容性
    """
    
    def __init__(self):
        self.version_manager = get_version_manager()
        self._register_services()
    
    def _register_services(self):
        """注册服务版本"""
        try:
            # 注册V1服务
            from mcp_servers.utils.services.workflow_service_v1 import WorkflowServiceV1
            self.version_manager.register("v1", WorkflowServiceV1, is_default=True)
            logger.info("已注册工作流服务 V1")
        except ImportError as e:
            logger.warning(f"注册V1服务失败: {e}")
    
    async def handle_get_steps(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理 workflow9.get_steps 工具调用"""
        try:
            version = args.get("version", "v1")
            service: IWorkflowService = self.version_manager.get_service(version)
            steps = service.get_steps()
            
            return {
                "success": True,
                "steps": [
                    {
                        "id": step.id,
                        "name": step.name,
                        "icon": step.icon,
                        "color": step.color,
                        "description": step.description,
                        "status": step.status
                    }
                    for step in steps
                ],
                "version": version
            }
        except Exception as e:
            logger.error(f"workflow9.get_steps 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v1")}
    
    async def handle_create(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理 workflow9.create 工具调用"""
        try:
            version = args.get("version", "v1")
            service: IWorkflowService = self.version_manager.get_service(version)
            
            response = service.create_workflow(args.get("name"))
            return response.to_dict()
        except Exception as e:
            logger.error(f"workflow9.create 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v1")}
    
    async def handle_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理 workflow9.status 工具调用"""
        try:
            version = args.get("version", "v1")
            workflow_id = args.get("workflow_id")
            
            if not workflow_id:
                return {"success": False, "error": "缺少必需参数: workflow_id"}
            
            service: IWorkflowService = self.version_manager.get_service(version)
            response = service.get_status(workflow_id)
            
            return response.to_dict()
        except Exception as e:
            logger.error(f"workflow9.status 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v1")}
    
    async def handle_run_step(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理 workflow9.run_step 工具调用"""
        try:
            version = args.get("version", "v1")
            request = WorkflowRequest(
                workflow_id=args.get("workflow_id"),
                step_id=args.get("step_id"),
                args=args.get("args", {}),
                version=version
            )
            
            if not request.workflow_id or not request.step_id:
                return {"success": False, "error": "缺少必需参数: workflow_id 或 step_id"}
            
            service: IWorkflowService = self.version_manager.get_service(version)
            response = service.run_step(request)
            
            return response.to_dict()
        except Exception as e:
            logger.error(f"workflow9.run_step 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v1")}
    
    async def handle_run_all(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理 workflow9.run_all 工具调用"""
        try:
            version = args.get("version", "v1")
            workflow_id = args.get("workflow_id")
            
            if not workflow_id:
                return {"success": False, "error": "缺少必需参数: workflow_id"}
            
            service: IWorkflowService = self.version_manager.get_service(version)
            response = service.run_all(workflow_id)
            
            return response.to_dict()
        except Exception as e:
            logger.error(f"workflow9.run_all 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v1")}
    
    async def handle_get_context(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """处理 workflow9.get_context 工具调用"""
        try:
            version = args.get("version", "v1")
            workflow_id = args.get("workflow_id")
            
            if not workflow_id:
                return {"success": False, "error": "缺少必需参数: workflow_id"}
            
            service: IWorkflowService = self.version_manager.get_service(version)
            response = service.get_context(workflow_id)
            
            return response.to_dict()
        except Exception as e:
            logger.error(f"workflow9.get_context 错误: {e}", exc_info=True)
            return {"success": False, "error": str(e), "version": args.get("version", "v1")}
    
    def get_available_versions(self) -> List[str]:
        """获取可用版本列表"""
        return self.version_manager.list_versions()


def get_workflow_adapter() -> WorkflowMCPAdapter:
    """获取全局适配器实例（单例）"""
    global _adapter
    if _adapter is None:
        _adapter = WorkflowMCPAdapter()
    return _adapter

