# 在Cursor中运行Jupyter Notebook指南

## 方法一：直接在Cursor中打开Notebook（推荐）

Cursor内置了Jupyter Notebook支持，可以直接打开`.ipynb`文件：

### 步骤：

1. **打开Notebook文件**
   - 在Cursor中按 `Ctrl+P` (或 `Cmd+P` on Mac)
   - 输入 `01_market_analysis.ipynb`
   - 选择文件打开

2. **选择Python解释器**
   - 打开Notebook后，Cursor会在顶部提示选择Kernel
   - 点击 "Select Kernel" 按钮
   - 选择：`/home/taotao/dev/QuantTest/TRQuant/venv/bin/python`

3. **运行代码单元**
   - 点击代码单元格左侧的 "Run" 按钮
   - 或使用快捷键：`Shift + Enter` (运行并移到下一行)
   - `Ctrl + Enter` (运行但不移动)

4. **使用LLM辅助**
   - 选中代码，按 `Ctrl+K` 让AI解释或修改代码
   - 使用 `Ctrl+L` 打开Chat面板讨论代码
   - 在代码单元格中添加 `# TODO:` 注释，AI会自动建议实现

## 方法二：使用Cursor的Python交互式环境

如果Notebook支持有问题，可以使用Cursor的交互式Python：

1. **创建临时Python脚本**
   ```python
   # test_market_analysis.py
   # 复制notebook中的代码到脚本
   ```

2. **在Cursor终端中运行**
   ```bash
   cd /home/taotao/dev/QuantTest/TRQuant
   /home/taotao/dev/QuantTest/TRQuant/venv/bin/python test_market_analysis.py
   ```

3. **使用Cursor的AI功能**
   - 选中输出结果，按 `Ctrl+K` 让AI分析
   - 在Chat中讨论结果

## 方法三：JupyterLab（如果需要完整Notebook体验）

如果需要完整的JupyterLab体验（多文件、交互式可视化）：

```bash
# 启动JupyterLab
cd /home/taotao/dev/QuantTest/TRQuant
/home/taotao/dev/QuantTest/TRQuant/venv/bin/jupyter lab --notebook-dir=notebooks

# 然后在浏览器中打开显示的URL（通常是 http://localhost:8888）
```

**注意**：在JupyterLab中运行后，可以：
- 复制结果回到Cursor
- 使用Cursor的AI功能分析结果
- 在Cursor中编辑和优化代码，再复制回JupyterLab

## 推荐工作流

**最佳实践**：结合Cursor和JupyterLab的优势

1. **在Cursor中编写和优化代码**
   - 利用AI辅助编写
   - 代码补全和错误检查
   - 版本控制集成

2. **在JupyterLab中运行和调试**
   - 交互式执行
   - 可视化输出
   - 逐步调试

3. **在Cursor中分析结果**
   - 使用AI分析输出
   - 生成报告
   - 保存到知识库

## 快速启动脚本

创建 `/home/taotao/dev/QuantTest/TRQuant/scripts/open_notebook.sh`:

```bash
#!/bin/bash
cd /home/taotao/dev/QuantTest/TRQuant
/home/taotao/dev/QuantTest/TRQuant/venv/bin/jupyter lab notebooks/templates/01_market_analysis.ipynb
```

然后运行：
```bash
chmod +x scripts/open_notebook.sh
./scripts/open_notebook.sh
```

## 故障排除

### 问题1：Cursor找不到Kernel
**解决**：
- 确保venv已激活
- 在Cursor设置中指定Python解释器路径：`/home/taotao/dev/QuantTest/TRQuant/venv/bin/python`

### 问题2：导入模块失败
**解决**：
- 确保在代码开头添加：`sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')`
- 检查venv中是否安装了所需包

### 问题3：Notebook显示为JSON
**解决**：
- 安装Jupyter扩展：`Ctrl+Shift+X`，搜索 "Jupyter"
- 或使用 `.py` 脚本格式代替

