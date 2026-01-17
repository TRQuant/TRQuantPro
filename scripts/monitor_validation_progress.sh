#!/bin/bash
# 监控模型验证进度

LOG_FILE="/home/taotao/.cursor/worktrees/TRQuant/ope/logs/validation/validate_individual_models.log"
OUTPUT_DIR="/home/taotao/.cursor/worktrees/TRQuant/ope/output/model_validation"

echo "=== 模型验证进度监控 ==="
echo ""

# 检查进程是否运行
if pgrep -f "validate_individual_models.py" > /dev/null; then
    echo "✅ 验证进程正在运行"
    echo ""
    
    # 显示最新日志
    if [ -f "$LOG_FILE" ]; then
        echo "📋 最新日志（最后10行）:"
        tail -10 "$LOG_FILE"
        echo ""
    fi
    
    # 检查输出文件
    if [ -d "$OUTPUT_DIR" ]; then
        REPORT_COUNT=$(find "$OUTPUT_DIR" -name "individual_models_validation_*.md" | wc -l)
        echo "📊 已生成报告数量: $REPORT_COUNT"
        
        if [ $REPORT_COUNT -gt 0 ]; then
            echo ""
            echo "📄 最新报告:"
            ls -lt "$OUTPUT_DIR"/*.md 2>/dev/null | head -1 | awk '{print $NF}'
        fi
    fi
else
    echo "❌ 验证进程未运行"
    echo ""
    echo "检查日志文件:"
    if [ -f "$LOG_FILE" ]; then
        echo "最后20行日志:"
        tail -20 "$LOG_FILE"
    else
        echo "日志文件不存在"
    fi
fi

echo ""
echo "=== 进程信息 ==="
ps aux | grep "validate_individual_models.py" | grep -v grep | awk '{print "PID:", $2, "| CPU:", $3"%", "| 内存:", $4"%", "| 运行时间:", $10}'
