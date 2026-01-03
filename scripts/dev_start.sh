#!/bin/bash
# TRQuant 开发启动检查脚本
# 每次开发前运行此脚本

echo "=============================================="
echo "   TRQuant 开发启动检查"
echo "=============================================="
echo ""

# 1. 确认工作目录
cd /home/taotao/dev/QuantTest/TRQuant
if [ "$PWD" != "/home/taotao/dev/QuantTest/TRQuant" ]; then
    echo "❌ 工作目录错误！"
    exit 1
fi
echo "✅ 工作目录: $PWD"

# 2. 激活虚拟环境
source venv/bin/activate
echo "✅ 虚拟环境已激活"

# 3. 执行状态检查
echo ""
python scripts/dev_workflow.py check

echo ""
echo "=============================================="
echo "  开发准备就绪！"
echo "=============================================="
echo ""
echo "快捷命令:"
echo "  开始任务: python scripts/dev_workflow.py start '任务名' '描述'"
echo "  添加日志: python scripts/dev_workflow.py log '内容' --tags development"
echo "  完成任务: python scripts/dev_workflow.py complete 'task_id'"
echo "  搜索经验: python scripts/dev_workflow.py search '关键词'"
echo ""
