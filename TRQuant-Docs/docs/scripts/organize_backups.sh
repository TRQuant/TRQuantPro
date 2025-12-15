#!/bin/bash
# 整理备份文件夹

DOCS_DIR="/home/taotao/dev/QuantTest/TRQuant/docs"
cd "$DOCS_DIR"

echo "整理备份文件夹..."
echo ""

# 创建统一的备份目录
BACKUP_ROOT="09_legacy/backups"
mkdir -p "$BACKUP_ROOT"

# 处理第一个备份文件夹（有内容的）
if [ -d "_backup_20251209_160959" ] && [ "$(ls -A _backup_20251209_160959 2>/dev/null)" ]; then
    echo "处理 _backup_20251209_160959 (12个备份文件)..."
    
    # 移动备份文件到legacy/backups，按时间戳分类
    BACKUP_DEST="$BACKUP_ROOT/20251209_160959"
    mkdir -p "$BACKUP_DEST"
    mv _backup_20251209_160959/* "$BACKUP_DEST/" 2>/dev/null
    rmdir "_backup_20251209_160959" 2>/dev/null
    echo "✓ 备份文件已移动到: $BACKUP_DEST/"
fi

# 删除空的备份文件夹
if [ -d "_backup_20251209_161009" ]; then
    if [ -z "$(ls -A _backup_20251209_161009 2>/dev/null)" ]; then
        echo "删除空的备份文件夹: _backup_20251209_161009"
        rmdir "_backup_20251209_161009"
    else
        BACKUP_DEST="$BACKUP_ROOT/20251209_161009"
        mkdir -p "$BACKUP_DEST"
        mv _backup_20251209_161009/* "$BACKUP_DEST/" 2>/dev/null
        rmdir "_backup_20251209_161009" 2>/dev/null
        echo "✓ 备份文件已移动到: $BACKUP_DEST/"
    fi
fi

# 创建备份说明文件
cat > "$BACKUP_ROOT/README.md" << 'README_EOF'
# 文档整理备份

本目录包含文档整理过程中创建的备份文件。

## 备份说明

这些备份文件是在文档整理过程中，当目标文件已存在时自动创建的备份。备份文件保留了整理前的原始版本，以防需要恢复。

## 备份目录结构

```
backups/
├── 20251209_160959/    # 第一次整理的备份（12个文件）
└── README.md           # 本说明文件
```

## 备份文件列表

### 20251209_160959
这些文件在整理时目标位置已存在，因此创建了备份：
- astro-plan.md
- CONFIG_VERIFICATION.md
- DEV_DEBUG_WORKFLOW.md
- DEVELOPMENT_LOG.md
- markdown-import-rules.md
- PROJECT_ANALYSIS_SUMMARY.md
- PROJECT_DIRECTORY_EXPLANATION.md
- PROJECT_SYNC_GUIDE.md
- QUICK_SYNC_GUIDE.md
- REVIEW_CHECKLIST.md
- TODO_CLEANUP_SUMMARY.md
- token_optimization_rule.md

## 注意事项

- 这些备份文件可以安全删除，因为目标位置已有对应文件
- 如果需要恢复某个文件，可以从备份中复制
- 建议在确认整理无误后，可以删除这些备份以节省空间

## 清理建议

如果确认整理无误，可以运行以下命令删除备份：

```bash
rm -rf 09_legacy/backups/
```

README_EOF

echo "✓ 创建备份说明文件: $BACKUP_ROOT/README.md"
echo ""
echo "完成！备份文件已整理到: $BACKUP_ROOT/"
