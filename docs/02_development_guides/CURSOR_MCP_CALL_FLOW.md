# Cursor扩展中MCP调用流程规范

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: TRQuant Cursor扩展

---

## 📋 概述

本文档定义了Cursor扩展中MCP工具调用的标准流程，确保调用过程规范、可追溯、可监控。

## 🎯 设计目标

1. **标准化**: 统一的MCP调用流程
2. **可追溯性**: 完整的调用链追踪
3. **可监控性**: 调用过程可监控
4. **错误处理**: 完善的错误处理机制

---

## 📝 调用流程

### 基本流程

```
用户请求
    ↓
参数验证（trace_id生成）
    ↓
MCP工具调用（传递trace_id）
    ↓
结果处理（包含trace_id）
    ↓
日志记录（关联trace_id）
    ↓
返回结果
```

### 详细步骤

1. **调用前准备**
   - 生成或获取trace_id
   - 验证参数（使用parameter_validator）
   - 记录调用日志

2. **调用过程**
   - 通过MCP协议调用工具
   - 传递trace_id
   - 监控调用状态

3. **调用后处理**
   - 验证返回结果
   - 记录结果日志
   - 处理错误情况

---

## 🔧 实现方案

### 1. MCP调用包装器

```typescript
// extension/src/services/mcpWrapper.ts
export class MCPWrapper {
    /**
     * 调用MCP工具（标准流程）
     */
    static async callTool(
        toolName: string,
        arguments: Record<string, any>,
        options?: MCPCallOptions
    ): Promise<MCPCallResult> {
        // 1. 生成trace_id
        const traceId = generateTraceId();
        
        // 2. 验证参数
        const validatedArgs = await validateParameters(toolName, arguments);
        
        // 3. 添加trace_id
        validatedArgs.trace_id = traceId;
        
        // 4. 记录调用日志
        logger.info(`[trace_id=${traceId}] 调用MCP工具: ${toolName}`);
        
        // 5. 调用工具
        try {
            const result = await mcpClient.callTool(toolName, validatedArgs);
            
            // 6. 记录结果日志
            logger.info(`[trace_id=${traceId}] 工具调用成功`);
            
            return {
                success: true,
                result: result,
                trace_id: traceId
            };
        } catch (error) {
            // 7. 错误处理
            logger.error(`[trace_id=${traceId}] 工具调用失败: ${error}`);
            
            return {
                success: false,
                error: error,
                trace_id: traceId
            };
        }
    }
}
```

### 2. 参数验证

```typescript
async function validateParameters(
    toolName: string,
    arguments: Record<string, any>
): Promise<Record<string, any>> {
    // 获取工具schema
    const schema = await getToolSchema(toolName);
    
    // 验证参数
    const validator = new ParameterValidator(schema);
    return validator.validate(arguments);
}
```

### 3. trace_id生成

```typescript
function generateTraceId(): string {
    return uuid.v4();
}
```

---

## 📊 调用示例

### 示例1: 基本调用

```typescript
const result = await MCPWrapper.callTool(
    'kb.query',
    {
        query: '如何配置数据源',
        scope: 'manual',
        top_k: 10
    }
);

if (result.success) {
    console.log('查询结果:', result.result);
    console.log('追踪ID:', result.trace_id);
} else {
    console.error('调用失败:', result.error);
}
```

### 示例2: 带选项的调用

```typescript
const result = await MCPWrapper.callTool(
    'backtest.run',
    {
        strategy_id: 'strategy_001',
        start_date: '2024-01-01',
        end_date: '2024-12-31'
    },
    {
        timeout: 60000,  // 60秒超时
        retry: 3,        // 重试3次
        onProgress: (progress) => {
            console.log('进度:', progress);
        }
    }
);
```

---

## 🔍 错误处理

### 错误类型

1. **参数验证错误**: 参数不符合schema
2. **调用超时**: 工具调用超时
3. **工具错误**: 工具执行失败
4. **网络错误**: MCP连接失败

### 错误处理流程

```typescript
try {
    const result = await MCPWrapper.callTool(...);
} catch (error) {
    if (error instanceof ParameterValidationError) {
        // 参数验证错误
        handleParameterError(error);
    } else if (error instanceof TimeoutError) {
        // 超时错误
        handleTimeoutError(error);
    } else if (error instanceof MCPError) {
        // MCP工具错误
        handleMCPError(error);
    } else {
        // 其他错误
        handleUnknownError(error);
    }
}
```

---

## 📖 相关文档

- [MCP工具命名规范](./MCP_NAMING_CONVENTIONS.md)
- [MCP参数结构规范](./MCP_PARAMETER_SCHEMA.md)
- [trace_id追踪机制](./TRACE_ID_DESIGN.md)
- [MCP错误码体系](./ERROR_CODE_SYSTEM.md)

---

**最后更新**: 2025-12-14
