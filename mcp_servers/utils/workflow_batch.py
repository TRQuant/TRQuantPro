#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工作流批量执行工具
==================

用于减少Max模式下的MCP工具调用次数，自动执行流程直到需要用户输入。

功能：
- workflow.batch: 批量执行多个工具调用
- workflow.auto: 自动执行流程直到需要用户输入
- 智能检测用户输入需求
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Callable
from enum import Enum

logger = logging.getLogger(__name__)


class ExecutionStatus(str, Enum):
    """执行状态"""
    SUCCESS = "success"
    NEED_INPUT = "need_input"
    ERROR = "error"
    SKIPPED = "skipped"


class BatchResult:
    """批量执行结果"""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.status: ExecutionStatus = ExecutionStatus.SUCCESS
        self.stopped_at: Optional[int] = None
        self.error: Optional[str] = None
        self.total_calls: int = 0
        self.successful_calls: int = 0
    
    def add_result(self, index: int, tool_name: str, result: Dict[str, Any], 
                   status: ExecutionStatus, error: Optional[str] = None):
        """添加执行结果"""
        self.results.append({
            "index": index,
            "tool_name": tool_name,
            "result": result,
            "status": status.value,
            "error": error
        })
        self.total_calls += 1
        if status == ExecutionStatus.SUCCESS:
            self.successful_calls += 1
        elif status == ExecutionStatus.NEED_INPUT:
            self.status = ExecutionStatus.NEED_INPUT
            self.stopped_at = index
        elif status == ExecutionStatus.ERROR:
            self.status = ExecutionStatus.ERROR
            self.stopped_at = index
            self.error = error
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status.value,
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "stopped_at": self.stopped_at,
            "error": self.error,
            "results": self.results
        }


class WorkflowBatchExecutor:
    """工作流批量执行器"""
    
    def __init__(self, tool_caller: Optional[Callable] = None):
        """
        初始化执行器
        
        Args:
            tool_caller: 工具调用函数，签名: async def call_tool(name: str, args: Dict) -> Dict
        """
        self.tool_caller = tool_caller
        self._context: Dict[str, Any] = {}
    
    def _needs_input(self, result: Dict[str, Any]) -> bool:
        """
        检测结果是否需要用户输入
        
        判断标准：
        1. 结果中包含 "need_input": true
        2. 结果中包含 "requires_user_decision": true
        3. 错误信息包含 "需要用户" 或 "请选择" 等关键词
        4. 状态为 "pending_user_input"
        """
        if not isinstance(result, dict):
            return False
        
        # 检查显式标记
        if result.get("need_input") is True:
            return True
        if result.get("requires_user_decision") is True:
            return True
        if result.get("status") == "pending_user_input":
            return True
        
        # 检查错误信息
        error = result.get("error", "")
        if isinstance(error, str):
            keywords = ["需要用户", "请选择", "请确认", "需要输入", "等待用户", "user input required"]
            if any(kw in error.lower() for kw in keywords):
                return True
        
        return False
    
    async def execute_batch(
        self,
        tools: List[Dict[str, Any]],
        stop_on_input: bool = True,
        stop_on_error: bool = False,
        max_calls: int = 50
    ) -> BatchResult:
        """
        批量执行工具调用
        
        Args:
            tools: 工具列表，每个元素格式: {"name": "tool.name", "args": {...}}
            stop_on_input: 遇到需要用户输入时是否停止
            stop_on_error: 遇到错误时是否停止
            max_calls: 最大调用次数（防止无限循环）
        
        Returns:
            BatchResult: 批量执行结果
        """
        if not self.tool_caller:
            raise ValueError("tool_caller未设置")
        
        result = BatchResult()
        
        for i, tool_config in enumerate(tools):
            if i >= max_calls:
                logger.warning(f"达到最大调用次数限制: {max_calls}")
                break
            
            tool_name = tool_config.get("name")
            tool_args = tool_config.get("args", {})
            
            if not tool_name:
                result.add_result(i, "unknown", {}, ExecutionStatus.ERROR, "工具名缺失")
                if stop_on_error:
                    break
                continue
            
            try:
                logger.info(f"[批量执行 {i+1}/{len(tools)}] 调用工具: {tool_name}")
                
                # 调用工具
                tool_result = await self.tool_caller(tool_name, tool_args)
                
                # 检查是否需要用户输入
                if self._needs_input(tool_result):
                    logger.info(f"工具 {tool_name} 需要用户输入，停止执行")
                    result.add_result(i, tool_name, tool_result, ExecutionStatus.NEED_INPUT)
                    if stop_on_input:
                        break
                else:
                    # 成功执行
                    result.add_result(i, tool_name, tool_result, ExecutionStatus.SUCCESS)
                    # 更新上下文（如果结果包含上下文数据）
                    if isinstance(tool_result, dict) and "context" in tool_result:
                        self._context.update(tool_result["context"])
            
            except Exception as e:
                error_msg = str(e)
                logger.error(f"工具 {tool_name} 执行失败: {error_msg}")
                result.add_result(i, tool_name, {}, ExecutionStatus.ERROR, error_msg)
                if stop_on_error:
                    break
        
        return result
    
    async def execute_auto(
        self,
        workflow_steps: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> BatchResult:
        """
        自动执行工作流直到需要用户输入
        
        Args:
            workflow_steps: 工作流步骤定义，每个步骤格式:
                {
                    "step_id": "step1",
                    "tool": "tool.name",
                    "args": {...} 或 "args_builder": "function_name",
                    "condition": "function_name"  # 可选，条件检查函数
                }
            context: 初始上下文
        
        Returns:
            BatchResult: 执行结果
        """
        if context:
            self._context.update(context)
        
        # 构建工具调用列表
        tools = []
        for step in workflow_steps:
            # 检查条件
            if "condition" in step:
                # TODO: 实现条件检查
                pass
            
            # 构建参数
            if "args_builder" in step:
                # TODO: 实现参数构建器
                args = step.get("args", {})
            else:
                args = step.get("args", {})
                # 从上下文填充参数
                args = self._fill_context(args, self._context)
            
            tools.append({
                "name": step["tool"],
                "args": args
            })
        
        # 执行批量调用
        return await self.execute_batch(tools, stop_on_input=True, stop_on_error=False)
    
    def _fill_context(self, args: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """从上下文填充参数"""
        filled = {}
        for key, value in args.items():
            if isinstance(value, str) and value.startswith("$"):
                # 从上下文获取值，例如 "$step1.result"
                context_key = value[1:]
                filled[key] = context.get(context_key, value)
            else:
                filled[key] = value
        return filled
    
    def get_context(self) -> Dict[str, Any]:
        """获取当前上下文"""
        return self._context.copy()
    
    def set_context(self, context: Dict[str, Any]):
        """设置上下文"""
        self._context.update(context)

