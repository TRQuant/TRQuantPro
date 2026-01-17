#!/bin/bash
# HMM验证进度实时显示

LOG_FILE="/tmp/hmm_validation.log"
TOTAL_PERIODS=10

while true; do
    clear
    echo "=========================================="
    echo "  HMM验证进度实时监控"
    echo "=========================================="
    echo ""
    
    # 检查进程
    PID=$(ps aux | grep validate_hmm_trend_accuracy | grep -v grep | awk '{print $2}')
    if [ -z "$PID" ]; then
        echo "⚠️  进程未运行（可能已完成）"
    else
        CPU=$(ps aux | grep validate_hmm_trend_accuracy | grep -v grep | awk '{print $3}')
        MEM=$(ps aux | grep validate_hmm_trend_accuracy | grep -v grep | awk '{print $4}')
        echo "✅ 进程运行中 | PID: $PID | CPU: ${CPU}% | 内存: ${MEM}%"
    fi
    
    echo ""
    echo "----------------------------------------"
    echo "进度统计:"
    echo "----------------------------------------"
    
    # 统计已完成的时期
    COMPLETED=$(grep -c "验证时期:" "$LOG_FILE" 2>/dev/null || echo "0")
    PROGRESS=$(echo "scale=1; $COMPLETED * 100 / $TOTAL_PERIODS" | bc 2>/dev/null || echo "0")
    
    echo "已完成: $COMPLETED / $TOTAL_PERIODS 个时期 ($PROGRESS%)"
    echo ""
    
    # 显示当前处理的时期
    CURRENT=$(grep "验证时期:" "$LOG_FILE" 2>/dev/null | tail -1 | sed 's/.*验证时期: //' | sed 's/ \[.*//')
    if [ -n "$CURRENT" ]; then
        echo "当前处理: $CURRENT"
    fi
    
    echo ""
    echo "----------------------------------------"
    echo "最新日志 (最后5行):"
    echo "----------------------------------------"
    tail -5 "$LOG_FILE" 2>/dev/null | sed 's/^/  /'
    
    echo ""
    echo "----------------------------------------"
    echo "按 Ctrl+C 退出监控"
    echo "=========================================="
    
    sleep 3
done
