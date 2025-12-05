---
title: "VS Code 主题与代码复制功能演示"
description: "演示VS Code主题配色和代码复制按钮功能"
lang: "zh-CN"
layout: "../layouts/HandbookLayout.astro"
book: "theory"
---

# VS Code 主题与代码复制功能演示

本页面演示了项目中集成的VS Code官方主题配色和代码复制功能。

## 🎨 主题特色

- **完整的VS Code配色方案**：使用VS Code官方的Dark Modern和Light Modern主题
- **语法高亮增强**：支持多种编程语言的精确语法高亮
- **一键复制功能**：每个代码块都有复制按钮，支持快捷键
- **响应式设计**：在移动端和桌面端都有良好的显示效果

## 📋 代码复制功能

### 功能特点
- 🖱️ **鼠标悬停显示**：鼠标悬停在代码块上时显示复制按钮
- ⌨️ **键盘快捷键**：`Ctrl+Shift+C` 复制当前焦点代码块
- ✅ **状态反馈**：复制成功后显示确认状态
- ♿ **无障碍支持**：支持键盘导航和屏幕阅读器
- 🔄 **降级处理**：如果剪贴板API不可用，自动选择文本

## 💻 多语言代码示例

### Python 示例（支持语法高亮和代码差异）
```python
# QuantConnect算法示例
class MomentumReversalAlgorithm(QCAlgorithm):
    def Initialize(self):
        """初始化算法参数"""
        self.SetStartDate(2020, 1, 1)  # [!code highlight]
        self.SetEndDate(2023, 12, 31)
        self.SetCash(100000)
        
        # 添加股票数据
        self.spy = self.AddEquity("SPY", Resolution.Daily)
        self.qqq = self.AddEquity("QQQ", Resolution.Daily)  # [!code ++]
        
        # 技术指标
        self.rsi = self.RSI("SPY", 14, Resolution.Daily)
        self.sma_short = self.SMA("SPY", 20, Resolution.Daily)  # [!code focus]
        self.sma_long = self.SMA("SPY", 50, Resolution.Daily)   # [!code focus]
        
    def OnData(self, data):
        """处理数据更新"""
        if not self.rsi.IsReady or not self.sma_long.IsReady:
            return
            
        # 动量反转策略 - 优化版本
        rsi_value = self.rsi.Current.Value  # [!code ++]
        if rsi_value < 30 and self.sma_short.Current.Value > self.sma_long.Current.Value:  # [!code --]
        if rsi_value < 25 and self.sma_short.Current.Value > self.sma_long.Current.Value:  # [!code ++]
            self.SetHoldings("SPY", 0.8)
        elif rsi_value > 70:  # [!code ++]
        elif self.rsi.Current.Value > 70:  # [!code --]
            self.Liquidate("SPY")
```

### JavaScript/TypeScript 示例
```typescript
// IBKR WebSocket连接管理
interface IBKRConfig {
  host: string;
  port: number;
  clientId: number;
  reconnectInterval: number;
}

class IBKRConnection {
  private ws: WebSocket | null = null;
  private config: IBKRConfig;
  private reconnectTimer: NodeJS.Timeout | null = null;
  
  constructor(config: IBKRConfig) {
    this.config = config;
  }
  
  async connect(): Promise<boolean> {
    try {
      const url = `ws://${this.config.host}:${this.config.port}`;
      this.ws = new WebSocket(url);
      
      this.ws.onopen = () => {
        console.log('IBKR连接已建立');
        this.authenticate();
      };
      
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.handleMessage(data);
      };
      
      this.ws.onclose = () => {
        console.log('IBKR连接已断开');
        this.scheduleReconnect();
      };
      
      return true;
    } catch (error) {
      console.error('连接失败:', error);
      return false;
    }
  }
  
  private handleMessage(data: any): void {
    switch (data.type) {
      case 'MARKET_DATA':
        this.processMarketData(data.payload);
        break;
      case 'ORDER_STATUS':
        this.processOrderStatus(data.payload);
        break;
      default:
        console.log('未知消息类型:', data.type);
    }
  }
}
```

### SQL 查询示例
```sql
-- 多因子选股查询
WITH factor_scores AS (
    SELECT 
        stock_symbol,
        -- 基本面因子
        (roe - AVG(roe) OVER()) / STDDEV(roe) OVER() AS roe_score,
        (revenue_growth - AVG(revenue_growth) OVER()) / STDDEV(revenue_growth) OVER() AS growth_score,
        -- 技术面因子
        (momentum_20d - AVG(momentum_20d) OVER()) / STDDEV(momentum_20d) OVER() AS momentum_score,
        (rsi_divergence - AVG(rsi_divergence) OVER()) / STDDEV(rsi_divergence) OVER() AS rsi_score
    FROM stock_factors
    WHERE date_updated = CURRENT_DATE
),
composite_scores AS (
    SELECT 
        stock_symbol,
        (roe_score * 0.3 + 
         growth_score * 0.25 + 
         momentum_score * 0.25 + 
         rsi_score * 0.2) AS composite_score
    FROM factor_scores
)
SELECT 
    cs.stock_symbol,
    cs.composite_score,
    sf.current_price,
    sf.market_cap,
    RANK() OVER (ORDER BY cs.composite_score DESC) as ranking
FROM composite_scores cs
JOIN stock_factors sf ON cs.stock_symbol = sf.stock_symbol
WHERE cs.composite_score > 1.5  -- 只选择得分超过1.5标准差的股票
ORDER BY cs.composite_score DESC
LIMIT 20;
```

### CSS 样式示例
```css
/* VS Code主题变量 */
:root {
  --vscode-editor-background: #1e1e1e;
  --vscode-editor-foreground: #d4d4d4;
  --vscode-keyword-color: #569cd6;
  --vscode-string-color: #ce9178;
  --vscode-comment-color: #6a9955;
  --vscode-function-color: #dcdcaa;
}

/* 代码块样式 */
.code-container {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.copy-button {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: var(--vscode-editor-foreground);
  padding: 8px 12px;
  font-size: 13px;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.code-container:hover .copy-button {
  opacity: 1;
  transform: translateY(0);
}

.copy-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}
```

### Bash/Shell 脚本示例
```bash
#!/bin/bash
# 自动化交易系统部署脚本

# 配置变量
APP_NAME="quantconnect-ibkr-bridge"
DEPLOY_DIR="/opt/trading-system"
LOG_DIR="/var/log/trading"
SERVICE_NAME="trading-bridge"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查系统依赖..."
    
    command -v docker >/dev/null 2>&1 || {
        log_error "Docker未安装，请先安装Docker"
        exit 1
    }
    
    command -v python3 >/dev/null 2>&1 || {
        log_error "Python3未安装，请先安装Python3"
        exit 1
    }
    
    log_info "依赖检查通过"
}

# 部署应用
deploy_app() {
    log_info "开始部署应用..."
    
    # 创建目录
    sudo mkdir -p $DEPLOY_DIR $LOG_DIR
    
    # 复制文件
    sudo cp -r ./src/* $DEPLOY_DIR/
    sudo cp ./config/production.yml $DEPLOY_DIR/config.yml
    
    # 设置权限
    sudo chown -R trading:trading $DEPLOY_DIR
    sudo chmod +x $DEPLOY_DIR/start.sh
    
    log_info "应用部署完成"
}

# 启动服务
start_service() {
    log_info "启动交易服务..."
    
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl start $SERVICE_NAME
    
    if systemctl is-active --quiet $SERVICE_NAME; then
        log_info "服务启动成功"
    else
        log_error "服务启动失败"
        exit 1
    fi
}

# 主函数
main() {
    log_info "开始部署交易系统..."
    
    check_dependencies
    deploy_app
    start_service
    
    log_info "部署完成！"
    log_info "监控日志: tail -f $LOG_DIR/trading.log"
    log_info "服务状态: systemctl status $SERVICE_NAME"
}

# 执行主函数
main "$@"
```

## 🚀 高级语法高亮功能

### 代码差异和高亮演示
```typescript {1,3-5}
// IBKR风险管理系统 - 版本对比
interface RiskConfig {
    maxPosition: number;        // [!code highlight]
    stopLoss: number;          // [!code --]
    stopLossPercent: number;   // [!code ++]
    maxDrawdown: number;       // [!code focus]
    alertThreshold: number;    // [!code focus]
}

class RiskManager {
    private config: RiskConfig;
    
    constructor(config: RiskConfig) {
        this.config = config;
        this.validateConfig();     // [!code ++]
    }
    
    validatePosition(position: number): boolean {
        // 检查持仓限制
        if (position > this.config.maxPosition) {  // [!code highlight]
            return false;
        }
        
        // 计算风险指标
        const risk = this.calculateRisk(position);  // [!code focus]
        return risk <= this.config.maxDrawdown;     // [!code focus]
    }
    
    private calculateRisk(position: number): number {  // [!code ++]
        return position * 0.02; // 2% 风险率                // [!code ++]
    }                                                      // [!code ++]
}
```

### 语法高亮功能说明
- **`// [!code highlight]`** - 高亮显示重要代码行（黄色背景）
- **`// [!code focus]`** - 聚焦显示关键代码行（蓝色边框）  
- **`// [!code ++]`** - 显示新增的代码行（绿色背景）
- **`// [!code --]`** - 显示删除的代码行（红色背景）
- **`{1,3-5}`** - 在代码块标题中指定高亮行号

### 多语言增强示例

#### SQL 查询优化
```sql
-- 投资组合性能分析查询
WITH portfolio_returns AS (
    SELECT 
        symbol,
        date,
        price,
        LAG(price) OVER (PARTITION BY symbol ORDER BY date) as prev_price,  -- [!code highlight]
        (price - LAG(price) OVER (PARTITION BY symbol ORDER BY date)) / 
         LAG(price) OVER (PARTITION BY symbol ORDER BY date) as daily_return  -- [!code focus]
    FROM stock_prices 
    WHERE date >= '2024-01-01'
),
risk_metrics AS (
    SELECT 
        symbol,
        AVG(daily_return) as avg_return,        -- [!code ++]
        STDDEV(daily_return) as volatility,     -- [!code ++]
        MAX(daily_return) as max_return,        -- [!code highlight]
        MIN(daily_return) as max_drawdown       -- [!code highlight]
    FROM portfolio_returns 
    WHERE daily_return IS NOT NULL
    GROUP BY symbol
)
SELECT 
    symbol,
    avg_return * 252 as annualized_return,      -- [!code focus]
    volatility * SQRT(252) as annualized_vol,   -- [!code focus]
    avg_return / volatility as sharpe_ratio     -- [!code highlight]
FROM risk_metrics
ORDER BY sharpe_ratio DESC;
```

#### Bash 脚本自动化
```bash {2,8-10}
#!/bin/bash
# 交易系统健康检查脚本

API_ENDPOINT="https://api.ibkr.com/health"     # [!code highlight]
LOG_FILE="/var/log/trading/health.log"
MAX_RESPONSE_TIME=5000  # 毫秒

# 检查API连接状态
check_api_connection() {                        # [!code focus]
    local response_time=$(curl -w "%{time_total}" -s -o /dev/null $API_ENDPOINT)  # [!code focus]
    echo "API响应时间: ${response_time}ms"        # [!code focus]
    
    if (( $(echo "$response_time > $MAX_RESPONSE_TIME" | bc -l) )); then
        echo "警告: API响应时间过长" >> $LOG_FILE   # [!code ++]
        send_alert "API响应缓慢"                   # [!code ++]
        return 1
    fi
    return 0
}

# 发送告警通知
send_alert() {                                  # [!code ++]
    local message="$1"                          # [!code ++]
    echo "$(date): $message" >> $LOG_FILE       # [!code ++]
    # 这里可以集成邮件或Slack通知                   # [!code ++]
}                                               # [!code ++]

# 主执行流程
main() {
    echo "开始健康检查..."
    if check_api_connection; then
        echo "系统状态正常" | tee -a $LOG_FILE     # [!code highlight]
    else
        echo "系统异常，请检查" | tee -a $LOG_FILE  # [!code highlight]
        exit 1
    fi
}

main "$@"
```

## 🔧 使用说明

### 复制代码
1. **鼠标操作**：将鼠标悬停在任何代码块上，右上角会出现复制按钮
2. **键盘快捷键**：使用 `Ctrl+Shift+C` 复制当前焦点的代码块
3. **无障碍支持**：使用 `Tab` 键导航到复制按钮，按 `Enter` 或 `Space` 执行复制

### 主题切换
- 使用页面右上角的主题切换按钮在亮色/暗色模式间切换
- 代码块会自动适应当前主题，显示相应的配色方案

### 浏览器兼容性
- **现代浏览器**：Chrome 66+、Firefox 63+、Safari 13.1+、Edge 79+
- **降级支持**：在不支持剪贴板API的浏览器中，会自动选择代码文本

## 📱 响应式设计

代码块和复制按钮在不同设备上都有优化：

- **桌面端**：完整功能，最佳体验
- **平板端**：适中的字体大小和按钮尺寸
- **移动端**：紧凑布局，易于触摸操作

## 🎯 技术实现

本功能基于以下技术实现：

- **Astro组件**：模块化的代码复制组件
- **TypeScript**：类型安全的脚本编写
- **CSS变量**：灵活的主题切换支持
- **Web APIs**：现代浏览器的剪贴板API
- **无障碍标准**：WCAG 2.1 AA级别支持

## 🎨 VS Code 主题完整配色

### 支持的语言和特性
- **20+ 编程语言**：Python, JavaScript, TypeScript, SQL, Bash, CSS, HTML, JSON, YAML, Markdown 等
- **完整语法高亮**：关键字、字符串、注释、函数、类型、变量等
- **智能缩进保持**：保持原始代码的缩进格式
- **代码差异显示**：支持添加、删除、高亮、聚焦等标记
- **行号和元数据**：可选的行号显示和代码元信息

### 主题切换效果
代码块会根据当前主题自动切换配色方案：
- **亮色模式**：使用 VS Code Light Plus 主题
- **暗色模式**：使用 VS Code Dark Plus 主题
- **自动切换**：根据系统偏好自动适应

---

**提示**：试试复制上面的任何代码块，体验一下这个功能！切换页面主题看看代码块的配色变化！ 