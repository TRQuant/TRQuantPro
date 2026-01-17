# QuantConnect + IBKR Bridge 指南

## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。







## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。





## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。


## 1. 目录约定

```
strategies/quantconnect/        # Lean/QuantConnect 策略文件（py/ipynb/cs）
data/quantconnect/
  ├── backtest_results/        # `lean backtest` 导出的 JSON
  └── trades/                  # 订单/成交/IBKR 执行日志（JSON）
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m quantconnect_bridge.server
# 默认监听 http://127.0.0.1:8200
```

## 3. CLI 样例

```bash
python scripts/quantconnect_cli.py strategies
python scripts/quantconnect_cli.py backtests --strategy alpha_factor
python scripts/quantconnect_cli.py trades --strategy alpha_factor
```

## 4. 集成流程建议

1. 使用 `lean backtest <project>` 生成 `backtest-*.json`，复制到 `data/quantconnect/backtest_results`.
2. 若使用 IBKR 实盘，可将 IB Gateway/TWS 订单日志解析成 JSON，置于 `data/quantconnect/trades`.
3. 由 `quantconnect_bridge` 对外暴露统一的 REST API，供仪表盘/GUI/CLI 调用。
4. 后续可结合 Git/Lean CLI 实现策略版本管理与自动部署。














