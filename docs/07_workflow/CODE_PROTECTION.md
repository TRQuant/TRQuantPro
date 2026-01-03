# 代码保护与防倒退策略

## 问题背景

AI辅助开发时可能出现：
- **重复造轮子**：修改已经正常工作的代码
- **代码倒退**：不小心破坏已有功能
- **上下文丢失**：AI忘记之前的开发状态

## 防护措施

### 1. 修改前必须执行的检查

```bash
# 运行检查脚本
./scripts/pre_change_check.sh

# 或手动执行
cd /home/taotao/dev/QuantTest/TRQuant
source venv/bin/activate
pytest tests/test_workflow_server.py -v  # 测试工作流
pytest tests/test_mcp_data_source.py -v  # 测试数据源
cd extension && npm run compile           # 编译TypeScript
```

### 2. 遵循的原则

| 原则 | 说明 |
|------|------|
| **测试先行** | 修改前运行测试，确认当前状态 |
| **最小改动** | 只改动必要的代码，不重构"正常工作"的部分 |
| **分支开发** | 大改动使用Git分支 |
| **即时提交** | 每完成一个功能就提交 |

### 3. AI辅助开发规则

在 `.cursorrules` 中强制：

```markdown
## 修改代码前的强制检查

1. **询问现有功能状态**
   - "这个功能现在能正常工作吗？"
   - "有测试覆盖吗？"

2. **运行相关测试**
   - pytest tests/test_xxx.py -v

3. **不要重写已有代码**
   - 如果功能正常，只做增量修改
   - 如需重构，先创建备份

4. **使用MCP记录变更**
   - devlog.add 记录每次改动
   - task.update 更新任务状态
```

### 4. 关键文件保护列表

这些文件已经过测试，除非有明确需求，不要修改：

```
extension/src/views/workflowPanel.ts  # 9步工作流面板
mcp_servers/workflow_9steps_server.py # 工作流MCP服务器
core/mcp/client.py                    # MCP客户端
```

### 5. 测试覆盖

| 模块 | 测试文件 | 测试数 |
|------|----------|--------|
| 工作流 | test_workflow_server.py | 7 |
| 数据源 | test_mcp_data_source.py | - |
| 因子 | test_mcp_factor.py | - |
| 策略 | test_mcp_strategy.py | - |
| 集成 | test_workflow_integration.py | - |

### 6. 恢复方法

```bash
# 查看最近提交
git log --oneline -10

# 恢复单个文件
git checkout <commit-hash> -- path/to/file

# 恢复整个分支
git reset --hard <commit-hash>

# 恢复stash
git stash pop
```

## 总结

**核心原则：如果代码能正常工作，不要动它！**

修改前问自己：
1. 这个功能现在能用吗？→ 能用就不要改
2. 有测试吗？→ 先运行测试
3. 需要改哪里？→ 只改必要的部分

