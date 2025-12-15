# 工作流状态持久化设计

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: TRQuant工作流编排系统

---

## 📋 概述

本文档定义了TRQuant系统中工作流状态的持久化方案，确保工作流可以恢复和继续执行。

## 🎯 设计目标

1. **可恢复性**: 工作流中断后可以恢复
2. **可追溯性**: 完整记录工作流执行历史
3. **可审计性**: 支持工作流执行审计
4. **高性能**: 状态持久化不影响性能

---

## 📝 持久化方案

### 存储位置

1. **PostgreSQL**: 工作流元数据和状态
2. **Redis**: 工作流运行时状态（可选，用于快速恢复）
3. **文件系统**: 工作流配置和结果

### 数据表设计

```sql
CREATE TABLE workflow_instances (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(100) NOT NULL,
    workflow_name VARCHAR(200),
    status VARCHAR(50) NOT NULL,  -- pending, running, completed, failed, paused
    current_step INTEGER DEFAULT 0,
    config JSONB,
    state_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    trace_id VARCHAR(36),
    INDEX idx_workflow_id (workflow_id),
    INDEX idx_status (status),
    INDEX idx_trace_id (trace_id)
);

CREATE TABLE workflow_steps (
    id SERIAL PRIMARY KEY,
    workflow_instance_id INTEGER REFERENCES workflow_instances(id),
    step_index INTEGER NOT NULL,
    step_name VARCHAR(100),
    tool_name VARCHAR(100),
    status VARCHAR(50),  -- pending, running, completed, failed, skipped
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_ms INTEGER,
    INDEX idx_workflow_instance (workflow_instance_id),
    INDEX idx_step_index (workflow_instance_id, step_index)
);
```

---

## 🔧 实现方案

### 1. 状态管理器

```python
class WorkflowStateManager:
    """工作流状态管理器"""
    
    def save_state(self, workflow_id: str, state: Dict[str, Any]):
        """保存工作流状态"""
        pass
    
    def load_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """加载工作流状态"""
        pass
    
    def update_step_status(
        self,
        workflow_id: str,
        step_index: int,
        status: str,
        output: Any = None,
        error: str = None
    ):
        """更新步骤状态"""
        pass
```

### 2. 状态恢复

```python
def resume_workflow(workflow_id: str):
    """恢复工作流"""
    state = state_manager.load_state(workflow_id)
    if state:
        # 从断点继续执行
        workflow = create_workflow_from_state(state)
        workflow.resume()
```

---

## 📖 相关文档

- [工作流错误处理设计](./ERROR_PROPAGATION_DESIGN.md)

---

**最后更新**: 2025-12-14
