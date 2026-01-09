# 轩辕剑灵GUI面板集成说明

> **创建时间**: 2026-01-03  
> **说明**: 轩辕剑灵开发助手GUI面板集成到主窗口的说明文档

---

## ✅ 集成完成

轩辕剑灵GUI面板已成功集成到 `gui/main_window_v2.py` 主窗口中。

---

## 📋 集成内容

### 1. 导入模块

在 `gui/main_window_v2.py` 中添加：

```python
from gui.widgets.xuanyuan_assistant_panel import XuanyuanAssistantPanel
```

### 2. 导航按钮

在侧边栏导航中添加了新的导航项：

```python
nav_items = [
    ("dashboard", "📊", "仪表盘"),
    ("strategy", "📋", "策略管理"),
    ("backtest", "▶️", "回测运行"),
    ("results", "📈", "结果分析"),
    ("reports", "📄", "报告中心"),
    ("xuanyuan", "🐉", "轩辕剑灵"),  # 新增
    ("settings", "⚙️", "系统设置"),
]
```

### 3. 页面创建

添加了 `_create_xuanyuan_page()` 方法：

```python
def _create_xuanyuan_page(self):
    """创建轩辕剑灵开发助手页面"""
    self.xuanyuan_panel = XuanyuanAssistantPanel()
    self.page_stack.addWidget(self.xuanyuan_panel)
```

### 4. 页面映射

更新了 `_on_nav_clicked()` 方法中的页面映射：

```python
page_map = {
    "dashboard": 0,
    "strategy": 1,
    "backtest": 2,
    "results": 3,
    "reports": 4,
    "xuanyuan": 5,  # 新增
    "settings": 6,
}
```

### 5. 标题映射

更新了页面标题映射：

```python
titles = {
    "dashboard": "仪表盘",
    "strategy": "策略管理",
    "backtest": "回测运行",
    "results": "结果分析",
    "reports": "报告中心",
    "xuanyuan": "轩辕剑灵开发助手",  # 新增
    "settings": "系统设置",
}
```

---

## 🎯 使用方式

### 启动GUI

```bash
# 方式1: 直接运行主窗口
python gui/main_window_v2.py

# 方式2: 通过主程序启动（如果已集成）
python main.py  # 或其他启动脚本
```

### 访问面板

1. 启动GUI后，在左侧边栏找到 **🐉 轩辕剑灵** 按钮
2. 点击按钮切换到轩辕剑灵面板
3. 使用4个功能标签页：
   - **提示词管理**: 管理提示词模板
   - **错误处理**: 分析错误和获取修复建议
   - **命令助手**: 命令建议和解释
   - **记忆管理**: 保存和回忆上下文

---

## 📊 功能模块

### 1. 提示词管理

- **列出模板**: 查看所有保存的提示词模板
- **创建模板**: 创建新的提示词模板
- **模板详情**: 查看和编辑模板内容

### 2. 错误处理

- **分析错误**: 输入错误信息，获取错误分析
- **修复建议**: 获取针对性的修复方案
- **调试步骤**: 生成调试步骤指南

### 3. 命令助手

- **命令建议**: 输入意图，获取Linux命令建议
- **命令解释**: 解释命令的作用和参数
- **安全检查**: 检查命令的安全性

### 4. 记忆管理

- **保存上下文**: 保存重要的项目配置和约定
- **回忆历史**: 根据键值回忆保存的上下文
- **搜索记忆**: 搜索相关的记忆内容

---

## ⚠️ 注意事项

1. **MCP客户端依赖**: GUI面板需要通过 `core.mcp.MCPClient` 调用MCP服务器
2. **服务器配置**: 确保MCP服务器已正确配置（见 `docs/XUANYUAN_MCP_SETUP.md`）
3. **数据目录**: 数据保存在 `data/xuanyuan/` 目录下
4. **异步调用**: 所有MCP调用都在单独的线程中执行，不会阻塞UI

---

## 🔧 技术细节

### 架构

```
主窗口 (MainWindowV2)
  └── 轩辕剑灵面板 (XuanyuanAssistantPanel)
        ├── 提示词管理标签页
        ├── 错误处理标签页
        ├── 命令助手标签页
        └── 记忆管理标签页
              └── MCP调用 (XuanyuanWorker线程)
                    └── MCPClient
                          └── xuanyuan_server.py (MCP服务器)
```

### 数据流

1. **用户操作**: 用户在GUI面板中点击按钮或输入内容
2. **信号触发**: PyQt6信号触发对应的槽函数
3. **MCP调用**: 创建 `XuanyuanWorker` 线程执行MCP调用
4. **结果返回**: 通过信号将结果返回UI线程
5. **界面更新**: 更新显示区域的内容

---

## 📝 相关文件

- **面板代码**: `gui/widgets/xuanyuan_assistant_panel.py`
- **主窗口**: `gui/main_window_v2.py`
- **MCP服务器**: `mcp_servers/xuanyuan_server.py`
- **配置文档**: `docs/XUANYUAN_MCP_SETUP.md`
- **快速开始**: `docs/XUANYUAN_QUICK_START.md`

---

*创建时间: 2026-01-03*





