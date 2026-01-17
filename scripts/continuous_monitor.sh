#!/bin/bash
# 持续监控HMM验证进度

LOG_FILE="/tmp/hmm_validation.log"
TOTAL_PERIODS=10

while true; do
    clear
    echo "=========================================="
    echo "  HMM验证进度实时监控"
    echo "  更新时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="
    echo ""
    
    # 检查进程
    PID=$(ps aux | grep validate_hmm_trend_accuracy | grep -v grep | awk '{print $2}')
    if [ -z "$PID" ]; then
        echo "⚠️  进程未运行（可能已完成）"
        echo ""
        # 检查是否有完成标记
        if grep -q "验证完成\|生成报告" "$LOG_FILE" 2>/dev/null; then
            echo "✅ 验证已完成！"
            echo ""
            echo "报告位置:"
            grep "生成报告\|保存报告" "$LOG_FILE" 2>/dev/null | tail -1
            break
        fi
    else
        CPU=$(ps aux | grep validate_hmm_trend_accuracy | grep -v grep | awk '{print $3}')
        MEM=$(ps aux | grep validate_hmm_trend_accuracy | grep -v grep | awk '{print $4}')
        RUNTIME=$(ps -p $PID -o etime= 2>/dev/null | tr -d ' ')
        echo "✅ 进程运行中"
        echo "   PID: $PID"
        echo "   CPU: ${CPU}%"
        echo "   内存: ${MEM}%"
        echo "   运行时间: $RUNTIME"
    fi
    
    echo ""
    echo "----------------------------------------"
    echo "进度统计:"
    echo "----------------------------------------"
    
    # 统计已完成的时期
    COMPLETED=$(grep -c "验证时期:" "$LOG_FILE" 2>/dev/null || echo "0")
    PROGRESS=$(echo "scale=1; $COMPLETED * 100 / $TOTAL_PERIODS" | bc 2>/dev/null || echo "0")
    
    echo "已完成: $COMPLETED / $TOTAL_PERIODS 个时期"
    echo "进度: ${PROGRESS}%"
    echo ""
    
    # 显示已完成的时期列表
    if [ "$COMPLETED" -gt 0 ]; then
        echo "已完成的时期:"
        grep "验证时期:" "$LOG_FILE" 2>/dev/null | sed 's/.*验证时期: /  ✓ /' | tail -$COMPLETED
    fi
    
    echo ""
    echo "----------------------------------------"
    echo "当前状态:"
    echo "----------------------------------------"
    
    # 显示当前处理的时期
    CURRENT=$(grep "验证时期:" "$LOG_FILE" 2>/dev/null | tail -1 | sed 's/.*验证时期: //' | sed 's/ \[.*//')
    if [ -n "$CURRENT" ]; then
        echo "当前处理: $CURRENT"
    fi
    
    # 显示最新状态
    LATEST_STATUS=$(tail -3 "$LOG_FILE" 2>/dev/null | grep -E "(状态解释完成|批量分析|Walk-forward)" | tail -1)
    if [ -n "$LATEST_STATUS" ]; then
        echo "最新状态: $(echo "$LATEST_STATUS" | sed 's/.*INFO - //')"
    fi
    
    echo ""
    echo "----------------------------------------"
    echo "最新日志 (最后5行):"
    echo "----------------------------------------"
    tail -5 "$LOG_FILE" 2>/dev/null | sed 's/^/  /' | sed 's/.*INFO - /  /'
    
    echo ""
    echo "----------------------------------------"
    echo "按 Ctrl+C 退出监控"
    echo "=========================================="
    
    sleep 5
done
