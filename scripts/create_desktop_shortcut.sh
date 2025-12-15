#!/bin/bash
# 创建桌面快捷方式脚本

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DESKTOP_FILE="$HOME/Desktop/TRQuant回测.desktop"

# 检查图标文件
if [ -f "$PROJECT_DIR/assets/icons/trquant-backtest.png" ]; then
    ICON_PATH="$PROJECT_DIR/assets/icons/trquant-backtest.png"
elif [ -f "$PROJECT_DIR/assets/icons/trquant-backtest.svg" ]; then
    ICON_PATH="$PROJECT_DIR/assets/icons/trquant-backtest.svg"
else
    ICON_PATH=""
fi

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=TRQuant回测
Name[zh_CN]=TRQuant回测
Comment=TRQuant量化回测系统 - 工程型GUI
Comment[zh_CN]=TRQuant量化回测系统 - 工程型GUI
Exec=$PROJECT_DIR/scripts/launch_backtest_gui.sh
Icon=$ICON_PATH
Path=$PROJECT_DIR
Terminal=false
Categories=Finance;Development;Science;
Keywords=quant;trading;backtest;strategy;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"
echo "✅ 桌面快捷方式已创建: $DESKTOP_FILE"
