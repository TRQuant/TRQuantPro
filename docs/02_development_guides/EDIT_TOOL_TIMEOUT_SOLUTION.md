# Edit Tool 超时问题分析与解决方案

## 问题描述

在使用 `search_replace` 或 `edit` 工具时，经常遇到 "Tool call errored or timed out" 错误。

## 根本原因分析

### 1. **文件大小问题**
- **现象**: 大文件（>1000行）编辑时容易超时
- **原因**: 工具需要读取、解析、替换整个文件内容
- **影响**: 文件越大，处理时间越长，超时风险越高

### 2. **操作复杂度**
- **现象**: 复杂的正则替换或多次替换操作
- **原因**: 
  - 正则表达式匹配需要遍历整个文件
  - 多次替换操作累积时间
  - 字符串匹配算法的时间复杂度

### 3. **系统负载**
- **现象**: 系统繁忙时更容易超时
- **原因**:
  - CPU/内存资源竞争
  - 磁盘I/O瓶颈
  - 网络延迟（如果涉及远程操作）

### 4. **文件锁定**
- **现象**: 文件正在被其他进程使用
- **原因**:
  - IDE正在编辑文件
  - 其他工具正在读取文件
  - 文件系统缓存问题

### 5. **工具限制**
- **现象**: 某些特定操作总是超时
- **原因**:
  - Cursor的edit工具可能有内置超时限制
  - 工具实现的性能瓶颈

## 解决方案

### 方案1: 使用 `cat heredoc` 写入大文件 ⭐ **推荐**

**适用场景**: 创建新文件或完全重写文件

```bash
cat > target_file.py << 'ENDOFFILE'
# 文件内容
...
ENDOFFILE
```

**优点**:
- 绕过edit工具的限制
- 适合大文件
- 一次性写入，速度快

**缺点**:
- 只能完全替换文件
- 不能做增量修改

### 方案2: 使用 Python 脚本批量修改 ⭐ **推荐**

**适用场景**: 需要批量修改多个文件或复杂逻辑

```python
from pathlib import Path

file_path = Path("target_file.py")
content = file_path.read_text(encoding='utf-8')

# 执行修改
content = content.replace("old", "new")

# 写入文件
file_path.write_text(content, encoding='utf-8')
```

**优点**:
- 可以处理复杂逻辑
- 可以批量操作
- 可以添加验证和错误处理

**缺点**:
- 需要编写脚本
- 需要执行额外步骤

### 方案3: 分块修改

**适用场景**: 大文件需要修改多个位置

**策略**:
1. 先读取文件，确定修改位置
2. 使用 `read_file` 的 `offset` 和 `limit` 参数分块读取
3. 对每个块分别使用 `search_replace`
4. 最后合并结果

**示例**:
```python
# 第一步：读取文件，定位修改位置
content = read_file("large_file.py", offset=100, limit=50)

# 第二步：对每个块分别修改
search_replace("large_file.py", old_string="...", new_string="...")
```

### 方案4: 使用 `run_terminal_cmd` + `sed`/`awk`

**适用场景**: 简单的文本替换

```bash
sed -i 's/old/new/g' target_file.py
```

**优点**:
- 速度快
- 适合简单替换

**缺点**:
- 功能有限
- 跨平台兼容性问题

### 方案5: 优化 search_replace 使用

**策略**:
1. **提供更多上下文**: 确保 `old_string` 唯一且包含足够上下文
2. **避免模糊匹配**: 使用更具体的匹配模式
3. **减少替换次数**: 合并多个替换为一次操作
4. **使用 replace_all**: 如果确定要替换所有出现

**示例**:
```python
# ❌ 不好：上下文太少，可能匹配多个位置
search_replace("file.py", "def func", "def new_func")

# ✅ 好：包含足够上下文，唯一匹配
search_replace("file.py", 
    "    def func(self, arg1, arg2):\n        return arg1 + arg2",
    "    def new_func(self, arg1, arg2):\n        return arg1 * arg2")
```

## 针对当前问题的解决方案

### 问题: backtest_server.py 的 main 函数缩进错误

**当前状态**:
```python
async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())
```

**解决方案**: 使用 Python 脚本修复

```python
from pathlib import Path

file_path = Path("mcp_servers/backtest_server.py")
content = file_path.read_text(encoding='utf-8')

# 修复main函数
old_main = """async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())"""

new_main = """async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())"""

content = content.replace(old_main, new_main)
file_path.write_text(content, encoding='utf-8')
```

## 最佳实践建议

### 1. **文件大小评估**
- 小文件（<500行）: 直接使用 `search_replace`
- 中等文件（500-1000行）: 使用 `search_replace`，提供足够上下文
- 大文件（>1000行）: 使用 Python 脚本或 `cat heredoc`

### 2. **操作复杂度评估**
- 简单替换（1-2处）: 使用 `search_replace`
- 多处替换（3-5处）: 考虑合并为一次操作
- 复杂逻辑（>5处或需要条件判断）: 使用 Python 脚本

### 3. **错误处理**
- 使用 `read_file` 验证文件内容
- 使用 `python3 -m py_compile` 验证语法
- 在脚本中添加 try-except 错误处理

### 4. **性能优化**
- 批量操作时，先收集所有修改，再一次性写入
- 使用 `replace_all=True` 避免多次调用
- 避免在循环中频繁调用 edit 工具

## 预防措施

### 1. **代码结构优化**
- 保持文件大小合理（<1000行）
- 使用模块化设计，拆分大文件

### 2. **开发流程优化**
- 小改动优先使用 `search_replace`
- 大改动使用 Python 脚本
- 复杂重构使用专门的工具脚本

### 3. **监控和诊断**
- 记录超时操作的模式
- 识别容易超时的文件类型
- 建立文件大小和操作复杂度的映射

## 总结

**快速决策树**:
1. 文件 < 500行 → 使用 `search_replace`
2. 文件 500-1000行 → 使用 `search_replace` + 更多上下文
3. 文件 > 1000行 → 使用 Python 脚本
4. 完全重写 → 使用 `cat heredoc`
5. 批量操作 → 使用 Python 脚本
6. 复杂逻辑 → 使用 Python 脚本

**核心原则**: 
- **小改动用小工具，大改动用大工具**
- **避免在工具限制边缘操作**
- **优先使用更可靠的方法**









