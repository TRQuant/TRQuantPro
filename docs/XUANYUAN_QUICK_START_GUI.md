# 轩辕剑灵GUI快速启动指南

## 🚀 启动方式

### 方式1: 桌面快捷方式
双击桌面上的 **"轩辕剑灵开发助手"** 图标

### 方式2: 命令行启动
```bash
# 在项目根目录
venv/bin/python gui/xuanyuan_main_window.py

# 或使用启动脚本
bash scripts/xuanyuan_start.sh
```

### 方式3: Cursor/VSCode任务
1. 按 `Ctrl+Shift+P` (或 `Cmd+Shift+P` on Mac)
2. 输入以下任一命令：
   - `召唤剑灵`
   - `轩辕剑灵`
   - `启动轩辕剑灵GUI`
3. 选择对应任务并执行

### 方式4: 终端命令（快捷别名）
在 `~/.bashrc` 或 `~/.zshrc` 中添加：
```bash
alias 召唤剑灵='cd /home/taotao/.cursor/worktrees/TRQuant/ope && venv/bin/python gui/xuanyuan_main_window.py'
alias 轩辕剑灵='cd /home/taotao/.cursor/worktrees/TRQuant/ope && venv/bin/python gui/xuanyuan_main_window.py'
```

然后运行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
召唤剑灵  # 或 轩辕剑灵
```

## 📋 功能说明

### 提示词管理
- **创建模板**: 点击"创建模板"按钮，填写信息保存
- **查看列表**: 点击"刷新列表"查看所有模板
- **编辑模板**: 双击模板行或点击"编辑"按钮
- **复制内容**: 选中模板后点击"复制内容"按钮
- **分类筛选**: 使用下拉框筛选不同分类的模板

### 错误处理
- 输入错误信息，点击"分析"按钮

### 命令助手
- 输入Linux命令，点击"解释"按钮

### 记忆功能
- 保存和搜索上下文（功能开发中）

## 🔧 故障排除

### GUI无法启动
1. 检查venv是否激活
2. 检查Python版本: `venv/bin/python --version`
3. 检查依赖: `pip list | grep PyQt6`

### MCP调用失败
1. 检查环境变量: `echo $TRQUANT_ROOT`
2. 检查MCP服务器配置: `~/.cursor/mcp.json`

## 📝 更新日志

- 2026-01-03: 初始版本，支持提示词管理基础功能

