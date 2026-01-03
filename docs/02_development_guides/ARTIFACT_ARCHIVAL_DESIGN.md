# Artifact归档设计

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中artifact（MCP调用产出物）的归档策略，用于统一管理和检索所有MCP工具的产出物。

## 🎯 设计目标

1. **统一归档**: 所有MCP产出物统一归档
2. **可追溯性**: 与trace_id、工具名关联
3. **可检索性**: 支持多维度检索
4. **版本管理**: 支持版本标签
5. **自动清理**: 过期artifact自动清理

---

## 📝 归档方案

### 存储位置

1. **文件系统**: `.taorui/artifacts/` (本地存储)
2. **对象存储**: MinIO/S3 (可选，用于生产环境)
3. **元数据**: PostgreSQL (artifact元数据)

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

PostgreSQL表：`artifact_archives`

```sql
CREATE TABLE artifact_archives (
    id SERIAL PRIMARY KEY,
    hash VARCHAR(64) UNIQUE NOT NULL,
    file_path TEXT NOT NULL,
    storage_type VARCHAR(20) DEFAULT 'filesystem',  -- filesystem, s3, minio
    tool_name VARCHAR(100) NOT NULL,
    description TEXT,
    file_size BIGINT,
    mime_type VARCHAR(100),
    trace_id VARCHAR(36),
    version_tag VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    metadata JSONB,
    INDEX idx_tool_name (tool_name),
    INDEX idx_trace_id (trace_id),
    INDEX idx_created_at (created_at)
);
```

---

## 🔧 实现方案

### 1. Artifact归档管理器

```python
class ArtifactArchival:
    """Artifact归档管理器"""
    
    def archive_artifact(
        self,
        artifact_info: Dict[str, Any],
        tool_name: str,
        trace_id: str = None,
        version_tag: str = None,
        description: str = ""
    ) -> str:
        """
        归档artifact
        
        Args:
            artifact_info: artifact信息（包含hash、路径等）
            tool_name: 工具名称
            trace_id: 追踪ID
            version_tag: 版本标签
            description: 描述
        
        Returns:
            artifact归档ID
        """
        pass
    
    def query_artifacts(
        self,
        tool_name: str = None,
        trace_id: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        version_tag: str = None
    ) -> List[Dict[str, Any]]:
        """查询artifact"""
        pass
    
    def get_artifact_by_hash(self, hash: str) -> Optional[Dict[str, Any]]:
        """根据hash获取artifact"""
        pass
    
    def cleanup_expired(self) -> int:
        """清理过期artifact"""
        pass
```

---

## 📊 使用场景

### 场景1: 自动归档

```python
# MCP工具调用后自动归档
result = await mcp_tool.call(...)
if should_archive(result):
    artifact_info = artifact_manager.save_artifact(result)
    archival.archive_artifact(
        artifact_info=artifact_info,
        tool_name="backtest.run",
        trace_id=trace_id,
        description="回测报告"
    )
```

### 场景2: 版本管理

```python
# 带版本标签的归档
archival.archive_artifact(
    artifact_info=artifact_info,
    tool_name="strategy.generate",
    trace_id=trace_id,
    version_tag="v1.0.0",
    description="策略生成结果"
)
```

---

## 🔍 检索接口

### 按工具名检索

```python
artifacts = archival.query_artifacts(tool_name="backtest.run")
```

### 按trace_id检索

```python
artifacts = archival.query_artifacts(trace_id=trace_id)
```

### 按时间范围检索

```python
artifacts = archival.query_artifacts(
    start_date=datetime(2025, 12, 1),
    end_date=datetime(2025, 12, 14)
)
```

### 按版本检索

```python
artifacts = archival.query_artifacts(version_tag="v1.0.0")
```

---

## 🗑️ 清理策略

### 自动清理

1. **基于过期时间**: 超过expires_at的artifact自动删除
2. **基于大小**: 总大小超过限制时，删除最旧的artifact
3. **定期清理**: 每天自动清理一次

### 清理配置

```python
CLEANUP_CONFIG = {
    "expires_in_days": 30,
    "max_total_size": 10 * 1024 * 1024 * 1024,  # 10GB
    "cleanup_interval_hours": 24
}
```

---

## 📖 相关文档

- [Artifact存储设计](./ARTIFACT_STORAGE_DESIGN.md)
- [trace_id追踪机制](./TRACE_ID_DESIGN.md)

---

**最后更新**: 2025-12-14
