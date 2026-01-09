# 如何将策略文件复制到QMT（避免编码问题）

## ⚠️ 重要提示

**推荐使用**: `TRQuant_V4_QMT_Research_SAFE_UTF8.py`
- 完全纯ASCII字符
- 无中文注释
- 避免所有编码问题

## 📋 复制步骤

### 方法1: 直接复制（推荐）

1. **在Linux/Mac上**:
   ```bash
   # 复制SAFE版本到Windows共享目录或使用scp
   cp strategies/qmt/TRQuant_V4_QMT_Research_SAFE_UTF8.py /path/to/windows/share/
   ```

2. **在Windows上**:
   - 从共享目录复制到QMT策略目录
   - 或使用文件管理器直接复制
   - **不要用记事本打开编辑**（可能改变编码）

### 方法2: 使用编码转换工具

如果文件在复制过程中编码改变了：

```bash
# 在Linux/Mac上转换并复制
python scripts/convert_to_qmt_safe_encoding.py \
    strategies/qmt/TRQuant_V4_QMT_Research_SAFE_UTF8.py \
    /path/to/windows/share/策略文件.py
```

### 方法3: 在Windows上修复

如果文件已经在Windows上但出现编码问题：

1. **使用Notepad++**:
   - 打开文件
   - 菜单：编码 → 转为UTF-8编码
   - 保存文件

2. **使用Python脚本**:
   ```python
   # fix_encoding.py
   with open('策略文件.py', 'rb') as f:
       content = f.read()
   
   # 尝试UTF-8解码
   try:
       text = content.decode('utf-8')
   except UnicodeDecodeError:
       # 尝试GBK解码
       text = content.decode('gbk')
   
   # 保存为UTF-8
   with open('策略文件.py', 'w', encoding='utf-8') as f:
       f.write(text)
   ```

## 🔍 验证文件编码

复制到Windows后，验证文件编码：

```python
# verify_encoding.py
with open('策略文件.py', 'rb') as f:
    content = f.read()
    
# 检查位置8的字节
if len(content) > 8:
    byte_at_8 = content[8:9]
    print(f"位置8的字节: 0x{byte_at_8[0]:02x}")
    
    # 应该是ASCII字符（0x20-0x7e）或UTF-8多字节序列
    if 0x81 <= byte_at_8[0] <= 0xfe:
        print("⚠️  警告: 位置8的字节可能是GBK编码特征")
        print("   建议: 将文件转换为UTF-8编码")

# 尝试UTF-8解码
try:
    text = content.decode('utf-8')
    print("✅ UTF-8编码正确")
except UnicodeDecodeError as e:
    print(f"❌ UTF-8编码错误: {e}")
    print("   建议: 使用编码转换工具修复")
```

## 💡 最佳实践

1. **使用SAFE版本**: `TRQuant_V4_QMT_Research_SAFE_UTF8.py`
2. **直接复制**: 不要用编辑器打开（可能改变编码）
3. **验证编码**: 复制后验证文件编码
4. **避免编辑**: 如果必须编辑，使用UTF-8编码的编辑器

## 🚀 一键复制脚本

```bash
#!/bin/bash
# copy_to_qmt.sh

SOURCE_FILE="strategies/qmt/TRQuant_V4_QMT_Research_SAFE_UTF8.py"
TARGET_DIR="/mnt/windows/QMT/python"  # 修改为实际路径

# 复制文件
cp "$SOURCE_FILE" "$TARGET_DIR/TRQuant_V4_QMT_Research.py"

# 验证编码
python3 -c "
with open('$TARGET_DIR/TRQuant_V4_QMT_Research.py', 'rb') as f:
    content = f.read()
    try:
        text = content.decode('utf-8')
        print('✅ 文件编码验证通过（UTF-8）')
    except UnicodeDecodeError as e:
        print(f'❌ 文件编码错误: {e}')
"
```
