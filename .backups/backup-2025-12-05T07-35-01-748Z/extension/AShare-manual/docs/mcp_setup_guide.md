# Cursor中配置Interactive-Feedback-MCP指南

## 🎯 目标
在Cursor中配置interactive-feedback-mcp，实现AI助手与用户的实时交互反馈，提升开发效率和对话连续性。

## 📋 配置步骤

### 1. 安装MCP服务器

#### 推荐方法：使用社区实现
```bash
# 克隆社区实现的Interactive-Feedback MCP
git clone https://github.com/noopstudios/interactive-feedback-mcp
cd interactive-feedback-mcp

# 安装uv包管理器（如果未安装）
pip install uv

# 安装依赖
python -m uv sync

# 测试运行服务器
python -m uv run server.py
```

#### 备用方法：直接使用源码
```bash
# 如果uv有问题，可以直接使用pip
git clone https://github.com/noopstudios/interactive-feedback-mcp
cd interactive-feedback-mcp
pip install -r requirements.txt
```

### 2. 配置Cursor设置

#### 打开Cursor设置
1. 按 `Ctrl+,` (Windows) 或 `Cmd+,` (Mac)
2. 搜索 "MCP" 或 "Model Context Protocol"
3. 找到 "MCP Servers" 配置项

#### 添加MCP服务器配置
```json
{
  "mcpServers": {
    "interactive-feedback-mcp": {
      "command": "python",
      "args": [
        "-m",
        "uv",
        "--directory",
        "C:\\path\\to\\interactive-feedback-mcp",
        "run",
        "server.py"
      ],
      "timeout": 600,
      "autoApprove": [
        "interactive_feedback"
      ]
    }
  }
}
```

#### 使用相对路径配置（推荐）
```json
{
  "mcpServers": {
    "interactive-feedback-mcp": {
      "command": "python",
      "args": [
        "-m",
        "uv",
        "--directory",
        "./interactive-feedback-mcp",
        "run",
        "server.py"
      ],
      "timeout": 600,
      "autoApprove": [
        "interactive_feedback"
      ]
    }
  }
}
```

### 3. 高级配置选项

#### 自定义反馈类型
```json
{
  "mcpServers": {
    "interactive-feedback": {
      "command": "node",
      "args": ["./interactive-feedback-mcp/dist/index.js"],
      "env": {
        "NODE_ENV": "development",
        "FEEDBACK_TYPES": "code_review,error_correction,style_guide",
        "RESPONSE_DELAY": "1000"
      }
    }
  }
}
```

#### 项目特定配置
在项目根目录创建 `.cursor/mcp-config.json`：
```json
{
  "interactive-feedback": {
    "projectRules": [
      "VS Code Dark主题标准",
      "HTML零空行规则",
      "组件化重构原则"
    ],
    "autoFeedback": true,
    "feedbackDelay": 2000
  }
}
```

### 4. 验证配置

#### 检查MCP服务器状态
1. 打开Cursor开发者工具 (`Ctrl+Shift+I`)
2. 查看控制台是否有MCP相关日志
3. 确认interactive-feedback服务器已启动

#### 测试交互功能
在聊天中输入：
```
请检查当前代码是否符合项目规范
```

应该能看到实时反馈和建议。

## 🔧 功能特性

### 实时代码检查
- **语法检查**：自动检测代码语法错误
- **风格检查**：确保符合项目编码规范
- **最佳实践**：提供改进建议

### 上下文感知反馈
- **项目规则**：基于`.cursorrules`提供反馈
- **历史对话**：参考之前的讨论内容
- **文件结构**：了解项目整体架构

### 智能建议
- **代码优化**：提供性能改进建议
- **组件复用**：识别可复用的代码片段
- **Token优化**：建议减少token消耗的方法

## 📊 使用场景

### 1. 代码生成时
```
用户：生成一个React组件
AI：生成代码...
MCP：检测到组件缺少TypeScript类型定义，建议添加Props接口
```

### 2. 代码审查时
```
用户：请检查这段代码
AI：代码分析...
MCP：发现HTML标签间有空行，违反项目规则
```

### 3. 项目规范遵循
```
用户：创建新的章节文件
AI：生成文件...
MCP：提醒添加必要的Front-matter字段
```

## 🚀 高级用法

### 自定义反馈规则
在项目根目录创建 `.cursor/feedback-rules.json`：
```json
{
  "rules": [
    {
      "name": "HTML零空行检查",
      "pattern": "</div>\\s*\\n\\s*\\n\\s*<",
      "message": "HTML标签间不允许空行",
      "severity": "error"
    },
    {
      "name": "组件化检查",
      "pattern": "class=\"overview-grid\"",
      "message": "建议使用ChapterOverview组件",
      "severity": "warning"
    }
  ]
}
```

### 集成项目规则
```json
{
  "projectIntegration": {
    "rulesFile": ".cursorrules",
    "componentsDir": "src/components/",
    "autoImport": true
  }
}
```

## 🔍 故障排除

### 常见问题

#### 1. MCP服务器未启动
**症状**：没有看到交互反馈
**解决**：
```bash
# 检查项目是否正确克隆
ls -la interactive-feedback-mcp/

# 检查依赖是否正确安装
cd interactive-feedback-mcp
npm list

# 重新安装依赖
npm install
```

#### 2. 路径配置错误
**症状**：Cursor报错或无法启动
**解决**：
- 检查路径是否正确
- 使用绝对路径或相对路径
- 确认文件存在且有执行权限

#### 3. 构建问题
**症状**：dist目录不存在
**解决**：
```bash
cd interactive-feedback-mcp
npm run build

# 如果构建失败，直接使用源码
# 修改配置使用 src/index.js 而不是 dist/index.js
```

### 调试模式
在Cursor设置中启用调试模式：
```json
{
  "mcpServers": {
    "interactive-feedback": {
      "command": "node",
      "args": ["./interactive-feedback-mcp/dist/index.js", "--debug"],
      "env": {
        "DEBUG": "mcp:*",
        "NODE_ENV": "development"
      }
    }
  }
}
```

## 📈 性能优化

### 减少延迟
```json
{
  "mcpServers": {
    "interactive-feedback": {
      "command": "node",
      "args": ["./interactive-feedback-mcp/dist/index.js"],
      "env": {
        "RESPONSE_DELAY": "500",
        "BATCH_SIZE": "10"
      }
    }
  }
}
```

### 缓存配置
```json
{
  "cache": {
    "enabled": true,
    "ttl": 3600,
    "maxSize": 100
  }
}
```

## 🎯 最佳实践

### 1. 渐进式配置
- 先使用基础配置
- 逐步添加自定义规则
- 根据项目需求调整

### 2. 规则优先级
- 错误级别规则优先
- 项目特定规则优先于通用规则
- 定期更新规则库

### 3. 团队协作
- 共享配置文件
- 统一反馈标准
- 定期review规则有效性

## 📚 相关资源

### 官方文档
- [MCP官方文档](https://modelcontextprotocol.io/)
- [Interactive Feedback MCP](https://github.com/noopstudios/interactive-feedback-mcp)
- [Cursor MCP配置](https://cursor.sh/docs/mcp)

### 社区资源
- [MCP Discord](https://discord.gg/modelcontextprotocol)
- [Cursor社区](https://community.cursor.sh/)
- [GitHub Issues](https://github.com/noopstudios/interactive-feedback-mcp/issues)

---

## 🔄 与项目集成

### 更新项目状态快照
在 `docs/project_status_snapshot.md` 中添加：
```markdown
### 🔧 技术基础设施
- **MCP集成**：
  - Interactive-Feedback-MCP 配置完成
  - 实时代码检查启用
  - 项目规则自动验证
```

### 更新恢复脚本
在 `scripts/quick_restore.py` 中添加MCP检查：
```python
def check_mcp_config():
    """检查MCP配置状态"""
    mcp_files = [
        ".cursor/mcp-config.json",
        ".cursor/feedback-rules.json",
        "interactive-feedback-mcp/"
    ]
    
    for file in mcp_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (缺失)")
```

---

*此配置将显著提升Cursor的智能反馈能力，帮助保持项目规范一致性* 