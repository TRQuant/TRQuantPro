#!/bin/bash
# 移动重复文件到专门文件夹（不删除）

DOCS_DIR="/home/taotao/dev/QuantTest/TRQuant/docs"
cd "$DOCS_DIR"

echo "移动重复文件到专门文件夹..."
echo ""

# 创建重复文件存放目录
DUPLICATES_DIR="09_legacy/duplicates"
mkdir -p "$DUPLICATES_DIR"

# 统计变量
moved_count=0
skipped_count=0

# 查找所有 *_ROOT.md 文件
find . -name "*_ROOT.md" -type f ! -path "./09_legacy/*" ! -path "./scripts/*" | while read file; do
    # 获取相对路径
    rel_path="${file#./}"
    dir_path=$(dirname "$rel_path")
    filename=$(basename "$rel_path")
    
    # 创建对应的目录结构
    target_dir="$DUPLICATES_DIR/$dir_path"
    mkdir -p "$target_dir"
    
    # 移动文件
    mv "$file" "$target_dir/$filename"
    echo "✓ 移动: $rel_path -> $target_dir/$filename"
    moved_count=$((moved_count + 1))
done

# 创建说明文件
cat > "$DUPLICATES_DIR/README.md" << 'README_EOF'
# 重复文件归档

本目录包含文档整理过程中发现的重复文件。

## 说明

这些 `*_ROOT.md` 文件是在文档整理过程中，当目标位置已存在同名文件时自动创建的备份文件。为了安全起见，这些文件被移动到此目录而不是删除。

## 文件来源

这些文件主要来自以下情况：
- 文档整理时，目标位置已有同名文件
- 整理脚本自动创建了 `*_ROOT.md` 作为备份
- 原文件已存在于目标位置

## 目录结构

重复文件保持了原有的目录结构，便于查找和对比。

```
duplicates/
├── 02_development_guides/
│   ├── COMPLETE_DEVELOPMENT_WORKFLOW_ROOT.md
│   └── ...
├── 03_modules/
│   ├── DATA_SOURCE_DEVELOPMENT_ROOT.md
│   └── ...
└── ...
```

## 处理建议

### 1. 对比文件内容
如果需要，可以对比 `*_ROOT.md` 和对应的原文件，确认内容是否一致。

### 2. 保留策略
- 如果内容相同：可以安全删除
- 如果内容不同：需要人工审查后决定
- 如果不确定：建议保留

### 3. 清理时机
建议在以下情况下再考虑清理：
- 确认整理无误后
- 文档使用一段时间后
- 需要释放空间时

## 注意事项

⚠️ **重要**: 删除前请务必：
1. 对比原文件和重复文件的内容
2. 确认原文件完整无误
3. 备份重要内容

## 统计信息

- 重复文件总数: 约 61 个
- 归档时间: 2025-12-09
- 归档原因: 文档整理过程中的备份文件

README_EOF

echo ""
echo "✓ 创建说明文件: $DUPLICATES_DIR/README.md"
echo ""
echo "完成！"
echo "移动的文件数: $moved_count"
