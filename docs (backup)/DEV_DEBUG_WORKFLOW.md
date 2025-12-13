# 开发与Debug工作流程

## 🔧 自动Debug流程

### 开发后必须执行的检查

每次开发新模块或修改现有代码后，**必须**运行自动debug脚本：

```bash
cd /home/taotao/.local/share/jqquant
source venv/bin/activate
python scripts/auto_debug.py [模块路径]
```

### 示例

```bash
# 检查单个文件
python scripts/auto_debug.py gui/widgets/heatmap_panel.py

# 检查整个目录
python scripts/auto_debug.py gui/widgets/

# 检查多个路径
python scripts/auto_debug.py gui/widgets/ markets/ashare/mainline/

# 默认检查常用目录
python scripts/auto_debug.py
```

---

## 📋 自动检查项目

### 1. 语法检查 (SyntaxCheck)
- 使用AST解析Python语法
- 检测语法错误和行号

### 2. 导入检查 (ImportCheck)
- 检查所有import语句
- 验证模块是否可导入

### 3. 颜色属性检查 (ColorsCheck) ⚠️ 重要
- 检查 `Colors.XXX` 的使用是否正确
- 验证Colors类中是否存在该属性
- **常见错误**: `Colors.PRIMARY_HOVER` → 应使用 `Colors.PRIMARY_LIGHT`

### 4. 模块加载测试 (ModuleLoad)
- 实际导入模块测试
- 检测运行时错误

### 5. GUI组件测试 (WidgetInit)
- 测试GUI组件能否正确初始化
- 检测UI构建错误

---

## 🎨 Colors类可用属性

```python
# 主色调
PRIMARY, PRIMARY_LIGHT, PRIMARY_DARK

# 强调色
ACCENT, ACCENT_LIGHT, ACCENT_DARK

# 背景色
BG_DARK, BG_PRIMARY, BG_SECONDARY, BG_TERTIARY, BG_CARD, BG_HOVER

# 边框色
BORDER_DARK, BORDER_PRIMARY, BORDER_LIGHT, BORDER_ACTIVE

# 文字色
TEXT_PRIMARY, TEXT_SECONDARY, TEXT_TERTIARY, TEXT_MUTED, TEXT_DISABLED

# 状态色
SUCCESS, SUCCESS_DARK
WARNING, WARNING_DARK
ERROR, ERROR_DARK
INFO, INFO_DARK
```

### ❌ 常见错误

| 错误用法 | 正确用法 |
|----------|----------|
| `Colors.PRIMARY_HOVER` | `Colors.PRIMARY_LIGHT` |
| `Colors.BORDER` | `Colors.BORDER_PRIMARY` |
| `Colors.DANGER` | `Colors.ERROR` |

---

## 🚀 开发流程

### 1. 开发新功能
```
编写代码 → 保存文件
```

### 2. 运行自动debug
```bash
python scripts/auto_debug.py [文件路径]
```

### 3. 检查结果
```
✅ 所有检查通过 → 进入测试
❌ 有错误 → 修复后重新运行
```

### 4. 手动测试
```bash
# 测试模块导入
python -c "from xxx import Xxx; print('OK')"

# 测试GUI初始化
python -c "
from PyQt6.QtWidgets import QApplication
from gui.widgets.xxx_panel import XxxPanel
app = QApplication([])
panel = XxxPanel()
print('OK')
"
```

### 5. 启动应用验证
```bash
pkill -9 -f 'python.*JQQuant' 2>/dev/null
python JQQuant.py &
```

---

## 🔍 常见问题排查

### 问题1: `type object 'Colors' has no attribute 'XXX'`
**原因**: 使用了Colors类中不存在的属性  
**解决**: 查看上面的可用属性列表，使用正确的属性名

### 问题2: `ModuleNotFoundError`
**原因**: 模块导入路径错误  
**解决**: 检查import语句，确保路径正确

### 问题3: GUI组件初始化失败
**原因**: 通常是引用了不存在的属性或方法  
**解决**: 检查错误信息中的具体行号

---

## 📝 开发规范

1. **新建文件后必须运行auto_debug.py**
2. **修改Colors相关代码后必须检查属性名**
3. **GUI组件修改后测试初始化**
4. **提交代码前运行完整检查**

```bash
# 完整检查命令
python scripts/auto_debug.py gui/ markets/
```

---

*韬睿量化平台 - 开发规范 v1.0*

