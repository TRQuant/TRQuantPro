#!/bin/bash
# 快速回测脚本

cd /home/taotao/dev/QuantTest/TRQuant
source extension/venv/bin/activate

STRATEGY="strategies/bullettrade/TRQuant_momentum_v3_improved.py"
OUTPUT_DIR="backtest_results/quick_test_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR"

echo "运行1周回测..."
bullet-trade backtest "$STRATEGY" \
    --start 2025-09-06 \
    --end 2025-09-13 \
    --cash 1000000 \
    --benchmark 000300.XSHG \
    --output "$OUTPUT_DIR" 2>&1 | tee "$OUTPUT_DIR/backtest.log"

echo ""
echo "回测完成，结果在: $OUTPUT_DIR"
