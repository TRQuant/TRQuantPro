#!/bin/bash
# 文件恢复脚本 - 尝试从ext4文件系统恢复丢失的文件

set -e

FILE_PATH="$1"
if [ -z "$FILE_PATH" ]; then
    echo "用法: $0 <文件路径>"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "错误: 文件不存在: $FILE_PATH"
    exit 1
fi

# 获取文件信息
INODE=$(stat -c %i "$FILE_PATH")
DEVICE=$(df "$FILE_PATH" | tail -1 | awk '{print $1}')
MOUNT_POINT=$(df "$FILE_PATH" | tail -1 | awk '{print $6}')

echo "=== 文件恢复信息 ==="
echo "文件路径: $FILE_PATH"
echo "Inode: $INODE"
echo "设备: $DEVICE"
echo "挂载点: $MOUNT_POINT"
echo ""

# 检查是否有debugfs
if ! command -v debugfs >/dev/null 2>&1; then
    echo "错误: 未安装debugfs，请运行: sudo apt-get install e2fsprogs"
    exit 1
fi

echo "=== 尝试恢复步骤 ==="
echo "1. 检查已删除的文件..."
echo "   sudo debugfs -R 'lsdel' $DEVICE | grep $INODE"
echo ""
echo "2. 如果找到，尝试恢复:"
echo "   sudo debugfs -R 'dump <inode> /tmp/recovered_$(basename $FILE_PATH)' $DEVICE"
echo ""
echo "3. 检查文件内容:"
echo "   cat /tmp/recovered_$(basename $FILE_PATH)"
echo ""
echo "⚠️  注意: 需要sudo权限，且文件系统必须未卸载"
