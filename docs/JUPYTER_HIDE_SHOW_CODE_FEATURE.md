# Jupyter Notebook Hide/Show Code 功能

## 📋 功能说明

在 Jupyter Notebook 中添加 Hide/Show Code 按钮，可以一键隐藏/显示所有代码编辑器，让 notebook 更简洁易读。

## 🎯 使用场景

- ✅ **推荐使用**：在**浏览器中打开的 Jupyter Notebook**（使用 miniconda 环境）
- ❌ **不支持**：Cursor 界面的 notebook（无法实现此功能）

## ⚠️ 重要限制

### 仅支持浏览器版本的 Jupyter Notebook

- ✅ **浏览器 Jupyter Notebook**：功能完全正常
  - 通过 `http://localhost:8888` 访问
  - 使用 miniconda 环境的 Python kernel
  - JavaScript 代码可以正常执行
  
- ❌ **Cursor 内置 Notebook**：功能不可用
  - Cursor 的 notebook 界面不支持 `%%javascript` 魔法命令
  - JavaScript 代码无法在 Cursor 界面中执行
  - 需要使用浏览器版本的 Jupyter Notebook

## 📝 代码内容

```javascript
%%javascript
(() => {
  // 只隐藏编辑器，不隐藏 cell 的 toolbar / prompt
  const selectors = ['.jp-InputArea-editor', '.cm-editor', '.CodeMirror'];

  // 找到当前 Notebook 使用的编辑器 DOM（优先匹配第一个存在的 selector）
  function getEditors() {
    for (const s of selectors) {
      const nodes = document.querySelectorAll(s);
      if (nodes.length) return { sel: s, nodes };
    }
    return { sel: null, nodes: [] };
  }

  // 切换显示/隐藏
  function toggle() {
    const { sel, nodes } = getEditors();
    if (!nodes.length) return alert('没找到编辑器区域：' + selectors.join(' / '));

    const hide = nodes[0].style.display !== 'none';
    nodes.forEach(n => n.style.display = hide ? 'none' : '');

    // 仅用于调试：输出当前使用的 selector
    console.log("toggle selector:", sel);
  }

  // 创建右上角按钮（避免重复创建）
  let btn = document.getElementById('toggleCodeBtn');
  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'toggleCodeBtn';
    btn.textContent = 'Hide/Show Code';
    btn.style.cssText =
      'position:fixed;top:12px;right:12px;z-index:99999;padding:6px 12px;border-radius:6px;';
    btn.addEventListener('click', toggle);
    document.body.appendChild(btn);
  }

  // 默认隐藏编辑器（只隐藏代码，不影响按钮/工具栏/输出）
  const { nodes } = getEditors();
  nodes.forEach(n => n.style.display = 'none');
})();
```

## 🚀 使用方法

### 1. 启动 Jupyter Notebook（浏览器版本）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
./start_jupyter_notebook.sh
```

或者：

```bash
conda activate base
jupyter notebook
```

浏览器会自动打开 `http://localhost:8888`

### 2. 打开任意 Notebook

- 在浏览器中打开任意 `.ipynb` 文件
- 例如：`notebooks/research/00_system_architecture_workflow.ipynb`

### 3. 运行第一个 Cell

- 第一个 cell 包含 `%%javascript` 代码
- 点击运行（或按 Shift+Enter）
- 右上角会出现 "Hide/Show Code" 按钮

### 4. 使用 Hide/Show Code 功能

- 点击右上角的 "Hide/Show Code" 按钮
- 可以切换显示/隐藏所有代码编辑器
- 默认隐藏代码，只显示输出和 markdown

## 📦 已应用的文件

所有 notebook 文件都已自动添加此功能：

- ✅ `notebooks/research/` 目录下的所有 notebook
- ✅ `notebooks/templates/` 目录下的所有 notebook
- ✅ `notebooks/lib/` 目录下的所有 notebook

## 🔧 技术实现

### 工作原理

1. **JavaScript 魔法命令**：使用 `%%javascript` 在 notebook 中执行 JavaScript
2. **DOM 操作**：通过 `querySelectorAll` 找到所有代码编辑器元素
3. **样式控制**：使用 `display: none` 隐藏代码编辑器
4. **按钮创建**：在页面右上角创建固定位置的切换按钮

### 兼容性

- ✅ Jupyter Notebook (经典界面)
- ✅ JupyterLab
- ✅ 支持 `.jp-InputArea-editor`, `.cm-editor`, `.CodeMirror` 三种编辑器类型
- ❌ Cursor 内置 Notebook（不支持 JavaScript 魔法命令）

### 代码位置

- 代码位置：每个 notebook 的第一个 cell
- 代码类型：JavaScript（使用 `%%javascript` 魔法命令）
- 执行方式：运行 cell 时自动执行

## 🔄 更新方法

如果需要更新所有 notebook 的代码，运行：

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
python3 update_toggle_code_all_notebooks.py
```

## 📋 注意事项

1. **必须使用浏览器版本**：此功能仅在浏览器版本的 Jupyter Notebook 中有效
2. **每次打开需要运行**：每次打开 notebook 需要运行第一个 cell 才能启用功能
3. **不影响输出**：隐藏代码不会影响 cell 的输出和 markdown 显示
4. **不影响工具栏**：不会隐藏 cell 的 toolbar 和 prompt 区域

## 🎯 使用建议

1. **研究展示**：隐藏代码，只展示结果和图表
2. **代码审查**：需要时显示代码进行审查
3. **报告生成**：生成简洁的报告，隐藏代码细节
4. **演示演示**：在演示时隐藏代码，突出结果

## 📚 相关文档

- [Jupyter Notebook 启动指南](JUPYTER_KERNEL_GUIDE.md)
- [Conda 环境设置指南](CONDA_ENV_SETUP.md)
- [Jupyter Kernel 选择指南](JUPYTER_KERNEL_GUIDE.md)

## 🔗 相关脚本

- `start_jupyter_notebook.sh` - 启动浏览器版本的 Jupyter Notebook
- `update_toggle_code_all_notebooks.py` - 更新所有 notebook 的 toggle code 代码

