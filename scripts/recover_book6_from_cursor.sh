#!/bin/bash
# 从Cursor历史批量恢复第六册所有文件

set -e

CURSOR_HISTORY_DIR="$HOME/.config/Cursor/User/History"
TARGET_DATE="2025-12-13"
TARGET_HOUR_START=6
TARGET_HOUR_END=9
BOOK6_DIR="extension/AShare-manual/src/pages/ashare-book6"

echo "=== 从Cursor历史恢复第六册文件 ==="
echo "目标日期: $TARGET_DATE"
echo "目标时间: ${TARGET_HOUR_START}:00 - ${TARGET_HOUR_END}:59"
echo ""

# 创建备份目录
BACKUP_DIR=".backups/book6_recovery_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "✅ 备份目录: $BACKUP_DIR"
echo ""

# 统计
recovered=0
not_found=0
skipped=0

# 遍历所有第六册文件
for file in $(find "$BOOK6_DIR" -type f -name "*.md" | sort); do
    file_uri="file://$(realpath "$file")"
    file_name=$(basename "$file")
    
    # 查找对应的History目录
    history_dir=$(find "$CURSOR_HISTORY_DIR" -name "entries.json" -exec grep -l "$file_uri" {} \; 2>/dev/null | head -1 | xargs dirname)
    
    if [ -z "$history_dir" ] || [ ! -d "$history_dir" ]; then
        echo "⚠️  未找到历史: $file_name"
        not_found=$((not_found + 1))
        continue
    fi
    
    # 查找目标时间范围内的最新版本
    target_file=""
    target_time=""
    
    for hist_file in "$history_dir"/*.md "$history_dir"/*.astro 2>/dev/null; do
        if [ ! -f "$hist_file" ]; then
            continue
        fi
        
        file_time=$(stat -c %y "$hist_file" | cut -d'.' -f1)
        date_part=$(echo "$file_time" | cut -d' ' -f1)
        hour=$(echo "$file_time" | cut -d' ' -f2 | cut -d':' -f1 | sed 's/^0//')
        if [ -z "$hour" ]; then
            hour=0
        fi
        
        if [ "$date_part" = "$TARGET_DATE" ] && [ "$hour" -ge "$TARGET_HOUR_START" ] && [ "$hour" -le "$TARGET_HOUR_END" ]; then
            # 检查是否比当前目标文件更新
            if [ -z "$target_file" ] || [ "$hist_file" -nt "$target_file" ]; then
                target_file="$hist_file"
                target_time="$file_time"
            fi
        fi
    done
    
    if [ -z "$target_file" ]; then
        # 如果没有找到目标时间范围内的，尝试找最接近的
        closest_file=$(ls -t "$history_dir"/*.md "$history_dir"/*.astro 2>/dev/null | head -1)
        if [ -f "$closest_file" ]; then
            file_time=$(stat -c %y "$closest_file" | cut -d'.' -f1)
            date_part=$(echo "$file_time" | cut -d' ' -f1)
            if [ "$date_part" = "$TARGET_DATE" ]; then
                target_file="$closest_file"
                target_time="$file_time"
                echo "ℹ️  使用最接近的版本: $file_name ($target_time)"
            else
                echo "⚠️  跳过（不在目标日期）: $file_name"
                skipped=$((skipped + 1))
                continue
            fi
        else
            echo "⚠️  未找到历史文件: $file_name"
            not_found=$((not_found + 1))
            continue
        fi
    fi
    
    # 创建备份
    backup_file="$BACKUP_DIR/$(echo "$file" | sed 's|/|_|g')"
    mkdir -p "$(dirname "$backup_file")"
    cp "$file" "$backup_file" 2>/dev/null || touch "$backup_file"
    
    # 恢复文件
    cp "$target_file" "$file"
    echo "✅ 已恢复: $file_name ($target_time)"
    recovered=$((recovered + 1))
done

echo ""
echo "=== 恢复完成 ==="
echo "✅ 已恢复: $recovered 个文件"
echo "⚠️  未找到: $not_found 个文件"
echo "ℹ️  跳过: $skipped 个文件"
echo "📋 备份位置: $BACKUP_DIR"
