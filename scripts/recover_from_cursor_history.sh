#!/bin/bash
# 从Cursor历史恢复文件的脚本

set -e

CURSOR_HISTORY_DIR="$HOME/.config/Cursor/User/History"
FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    echo "用法: $0 <文件路径>"
    echo "示例: $0 extension/AShare-manual/src/pages/index.astro"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "错误: 文件不存在: $FILE_PATH"
    exit 1
fi

# 将文件路径转换为URI格式
FILE_URI="file://$(realpath "$FILE_PATH")"

echo "=== 从Cursor历史恢复文件 ==="
echo "文件路径: $FILE_PATH"
echo "文件URI: $FILE_URI"
echo ""

# 查找对应的History目录
HISTORY_DIR=$(find "$CURSOR_HISTORY_DIR" -name "entries.json" -exec grep -l "$FILE_URI" {} \; 2>/dev/null | head -1 | xargs dirname)

if [ -z "$HISTORY_DIR" ]; then
    echo "❌ 未找到该文件的历史记录"
    exit 1
fi

echo "✅ 找到历史目录: $HISTORY_DIR"
echo ""

# 读取entries.json获取最新版本
LATEST_ENTRY=$(cat "$HISTORY_DIR/entries.json" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'entries' in data and len(data['entries']) > 0:
    # 按timestamp排序，获取最新的
    entries = sorted(data['entries'], key=lambda x: x.get('timestamp', 0), reverse=True)
    print(entries[0]['id'])
" 2>/dev/null)

if [ -z "$LATEST_ENTRY" ]; then
    echo "❌ 无法从entries.json获取最新版本"
    # 尝试使用文件系统时间戳
    LATEST_FILE=$(ls -t "$HISTORY_DIR"/*.astro "$HISTORY_DIR"/*.md "$HISTORY_DIR"/*.ts "$HISTORY_DIR"/*.js 2>/dev/null | head -1)
    if [ -z "$LATEST_FILE" ]; then
        echo "❌ 未找到历史文件"
        exit 1
    fi
    LATEST_ENTRY=$(basename "$LATEST_FILE")
    echo "使用文件系统时间戳找到: $LATEST_ENTRY"
fi

HISTORY_FILE="$HISTORY_DIR/$LATEST_ENTRY"

if [ ! -f "$HISTORY_FILE" ]; then
    echo "❌ 历史文件不存在: $HISTORY_FILE"
    exit 1
fi

echo "✅ 找到最新历史版本: $LATEST_ENTRY"
echo "   时间: $(stat -c %y "$HISTORY_FILE" | cut -d'.' -f1)"
echo ""

# 创建备份
BACKUP_FILE="${FILE_PATH}.backup_$(date +%Y%m%d_%H%M%S)"
cp "$FILE_PATH" "$BACKUP_FILE"
echo "✅ 已创建当前文件备份: $BACKUP_FILE"
echo ""

# 恢复文件
cp "$HISTORY_FILE" "$FILE_PATH"
echo "✅ 已从Cursor历史恢复文件！"
echo ""
echo "恢复的文件: $FILE_PATH"
echo "备份位置: $BACKUP_FILE"
echo "历史版本: $HISTORY_FILE"
