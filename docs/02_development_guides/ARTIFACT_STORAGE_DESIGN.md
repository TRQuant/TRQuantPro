# Artifact存储设计

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中artifact（大输出）的存储方案，遵循"大输出artifact化"原则，避免在响应中返回过大的内容。

## 🎯 设计原则

1. **大输出artifact化**: 超过阈值的大输出自动保存为artifact
2. **可追溯性**: artifact与trace_id关联
3. **可检索性**: 支持基于trace_id、工具名、时间等检索
4. **版本管理**: 支持artifact版本管理
5. **清理策略**: 自动清理过期artifact

---

## 📝 存储方案

### 存储目录

```
.taorui/artifacts/
├── {YYYY-MM-DD}/
│   ├── {工具名}_{描述}_{hash}.{扩展名}
│   └── metadata/
│       └── {hash}.json
```

### 命名规则

```
{日期}_{工具名}_{描述}_{hash}.{扩展名}
```

示例：
```
2025-12-14_backtest_report_strategy_001_a1b2c3d4.json
2025-12-14_kb_query_results_how_to_config_e5f6g7h8.md
```

### 元数据存储

PostgreSQL表：`artifacts`

```sql
CREATE TABLE artifacts (
    id SERIAL PRIMARY KEY,
    hash VARCHAR(64) UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    tool_name VARCHAR(100) NOT NULL,
    description TEXT,
    file_size BIGINT,
    mime_type VARCHAR(100),
    trace_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    metadata JSONB
);
```

---

## 🔧 实现方案

### 1. Artifact管理器

```python
class ArtifactManager:
    """Artifact管理器"""
    
    def save_artifact(
        self,
        content: str | bytes,
        tool_name: str,
        description: str = "",
        trace_id: str = None,
        mime_type: str = None,
        expires_in_days: int = 30
    ) -> ArtifactInfo:
        """
        保存artifact
        
        Returns:
            ArtifactInfo对象，包含hash、路径等信息
        """
        pass
    
    def get_artifact(self, hash: str) -> Optional[ArtifactInfo]:
        """获取artifact信息"""
        pass
    
    def list_artifacts(
        self,
        tool_name: str = None,
        trace_id: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ) -> List[ArtifactInfo]:
        """列出artifact"""
        pass
    
    def delete_artifact(self, hash: str) -> bool:
        """删除artifact"""
        pass
    
    def cleanup_expired(self) -> int:
        """清理过期artifact"""
        pass
```

### 2. 自动artifact化

```python
def auto_artifactize_if_large(
    content: str | bytes,
    tool_name: str,
    threshold: int = 10000  # 10KB
) -> str | ArtifactInfo:
    """
    如果内容超过阈值，自动保存为artifact
    
    Returns:
        如果超过阈值，返回ArtifactInfo；否则返回原始内容
    """
    if len(content) > threshold:
        return artifact_manager.save_artifact(
            content=content,
            tool_name=tool_name
        )
    return content
```

---

## 📊 使用场景

### 场景1: 回测报告

```python
# 回测结果很大，自动保存为artifact
result = backtest.run(...)
if len(json.dumps(result)) > 10000:
    artifact = artifact_manager.save_artifact(
        content=json.dumps(result),
        tool_name="backtest.run",
        description=f"回测报告_{strategy_id}",
        trace_id=trace_id
    )
    return {
        "artifact": artifact.hash,
        "artifact_path": artifact.file_path,
        "summary": result.get("summary")
    }
```

### 场景2: 知识库查询结果

```python
# 查询结果很多，保存为artifact
results = kb.query(...)
if len(results) > 50:
    artifact = artifact_manager.save_artifact(
        content=json.dumps(results),
        tool_name="kb.query",
        description=f"查询结果_{query[:20]}",
        trace_id=trace_id
    )
    return {
        "artifact": artifact.hash,
        "count": len(results),
        "top_5": results[:5]  # 返回前5条作为预览
    }
```

---

## 🔍 检索和访问

### 基于trace_id检索

```python
# 获取某个调用链的所有artifact
artifacts = artifact_manager.list_artifacts(trace_id=trace_id)
```

### 基于工具名检索

```python
# 获取某个工具的所有artifact
artifacts = artifact_manager.list_artifacts(tool_name="backtest.run")
```

### 访问artifact内容

```python
# 通过hash获取artifact
artifact = artifact_manager.get_artifact(hash)
with open(artifact.file_path, 'r') as f:
    content = f.read()
```

---

## 🗑️ 清理策略

### 自动清理

1. **基于过期时间**: 超过expires_at的artifact自动删除
2. **基于大小**: 总大小超过限制时，删除最旧的artifact
3. **手动清理**: 提供清理命令

### 清理配置

```python
CLEANUP_CONFIG = {
    "expires_in_days": 30,  # 30天后过期
    "max_total_size": 10 * 1024 * 1024 * 1024,  # 10GB
    "cleanup_interval_hours": 24  # 每24小时清理一次
}
```

---

## 📖 相关文档

- [MCP工具命名规范](./MCP_NAMING_CONVENTIONS.md)
- [trace_id追踪机制](./TRACE_ID_DESIGN.md)
- [MCP错误码体系](./ERROR_CODE_SYSTEM.md)

---

**最后更新**: 2025-12-14
