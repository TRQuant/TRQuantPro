"""
工作流服务实现 V1

实现IWorkflowService接口，封装9步工作流系统的功能。

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

logger = logging.getLogger(__name__)


class WorkflowServiceV1(IWorkflowService):
    """
    工作流服务实现 V1
    
    封装9步工作流系统的功能，实现IWorkflowService接口。
    """
    
    def __init__(self):
        self._workflow_storage = None
    
    def _get_workflow_storage(self):
        """延迟加载工作流存储"""
        if self._workflow_storage is None:
            try:
                from mcp_servers.utils.workflow_storage import WorkflowStorage
                self._workflow_storage = WorkflowStorage()
            except ImportError:
                logger.warning("WorkflowStorage不可用")
                self._workflow_storage = None
        return self._workflow_storage
    
    def get_version(self) -> str:
        """获取服务版本"""
        return "v1"
    
    def get_steps(self) -> List[WorkflowStep]:
        """获取所有步骤定义"""
        from mcp_servers.workflow_9steps_server import WORKFLOW_9STEPS
        
        return [
            WorkflowStep(
                id=step["id"],
                name=step["name"],
                icon=step["icon"],
                color=step["color"],
                description=step["description"]
            )
            for step in WORKFLOW_9STEPS
        ]
    
    def create_workflow(self, name: Optional[str] = None) -> WorkflowResponse:
        """创建新的工作流会话"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 创建工作流
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.create",
                            {"name": name or "9步投资工作流"}
                        ))
                    )
                    result = future.result(timeout=10)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.create",
                    {"name": name or "9步投资工作流"}
                ))
            
            if result.get("success"):
                return WorkflowResponse(
                    success=True,
                    workflow_id=result.get("workflow_id"),
                    version="v1"
                )
            else:
                return WorkflowResponse(
                    success=False,
                    error=result.get("error", "创建工作流失败"),
                    version="v1"
                )
        except Exception as e:
            logger.error(f"创建工作流失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                error=str(e),
                version="v1"
            )
    
    def get_status(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流状态"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 获取状态
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.status",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=10)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.status",
                    {"workflow_id": workflow_id}
                ))
            
            if result.get("success"):
                return WorkflowResponse(
                    success=True,
                    workflow_id=workflow_id,
                    result=result,
                    version="v1"
                )
            else:
                return WorkflowResponse(
                    success=False,
                    error=result.get("error", "获取工作流状态失败"),
                    version="v1"
                )
        except Exception as e:
            logger.error(f"获取工作流状态失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                error=str(e),
                version="v1"
            )
    
    def run_step(self, request: WorkflowRequest) -> WorkflowResponse:
        """执行指定步骤"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用原始处理函数（异步函数需要await）
            # 检查是否已有事件循环
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.run_step",
                            {
                                "workflow_id": request.workflow_id,
                                "step_id": request.step_id,
                                "args": request.args or {}
                            }
                        ))
                    )
                    result = future.result(timeout=60)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.run_step",
                    {
                        "workflow_id": request.workflow_id,
                        "step_id": request.step_id,
                        "args": request.args or {}
                    }
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                error=str(e),
                version="v1"
            )
    
    def run_all(self, workflow_id: str) -> WorkflowResponse:
        """一键执行所有步骤"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 执行所有步骤
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.run_all",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=300)  # 5分钟超时
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.run_all",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行所有步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )
    
    def get_context(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流上下文"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 获取上下文
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.get_context",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=10)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.get_context",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"获取工作流上下文失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )


                    }
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                error=str(e),
                version="v1"
            )
    
    def run_all(self, workflow_id: str) -> WorkflowResponse:
        """一键执行所有步骤"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 执行所有步骤
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.run_all",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=300)  # 5分钟超时
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.run_all",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行所有步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )
    
    def get_context(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流上下文"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 获取上下文
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.get_context",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=10)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.get_context",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"获取工作流上下文失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )


                    }
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                error=str(e),
                version="v1"
            )
    
    def run_all(self, workflow_id: str) -> WorkflowResponse:
        """一键执行所有步骤"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 执行所有步骤
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.run_all",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=300)  # 5分钟超时
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.run_all",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行所有步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )
    
    def get_context(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流上下文"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 获取上下文
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.get_context",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=10)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.get_context",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"获取工作流上下文失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )


                    }
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=request.workflow_id,
                step_id=request.step_id,
                error=str(e),
                version="v1"
            )
    
    def run_all(self, workflow_id: str) -> WorkflowResponse:
        """一键执行所有步骤"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 执行所有步骤
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.run_all",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=300)  # 5分钟超时
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.run_all",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"执行所有步骤失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )
    
    def get_context(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流上下文"""
        import asyncio
        try:
            from mcp_servers.workflow_9steps_server import _handle_tool
            
            # 调用 _handle_tool 获取上下文
            try:
                loop = asyncio.get_running_loop()
                # 如果已有循环，使用线程池执行
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(_handle_tool(
                            "workflow9.get_context",
                            {"workflow_id": workflow_id}
                        ))
                    )
                    result = future.result(timeout=10)
            except RuntimeError:
                # 没有运行中的循环，直接使用asyncio.run
                result = asyncio.run(_handle_tool(
                    "workflow9.get_context",
                    {"workflow_id": workflow_id}
                ))
            
            return WorkflowResponse(
                success=result.get("success", False),
                workflow_id=workflow_id,
                result=result,
                error=result.get("error"),
                version="v1"
            )
        except Exception as e:
            logger.error(f"获取工作流上下文失败: {e}", exc_info=True)
            return WorkflowResponse(
                success=False,
                workflow_id=workflow_id,
                error=str(e),
                version="v1"
            )

