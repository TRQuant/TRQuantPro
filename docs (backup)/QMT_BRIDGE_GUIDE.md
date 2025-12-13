# QMT Bridge 使用指南

> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。







> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。





> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。


> 目标：为国金 QMT（xtquant）策略提供与韬睿量化仪表盘/CLI 的统一桥接能力。

## 1. 目录结构

```
strategies/qmt/                 # QMT 策略脚本
data/qmt/
  ├── backtest_results/        # xtquant 回测导出的 JSON/CSV（建议统一 JSON）
  └── trades/                  # 实盘/模拟交易记录 JSON
```

## 2. 服务启动

```bash
source venv/bin/activate
python -m qmt_bridge.server
# 默认监听 http://127.0.0.1:8100
```

## 3. CLI

```bash
python scripts/qmt_cli.py strategies
python scripts/qmt_cli.py backtests --strategy my_strategy
python scripts/qmt_cli.py trades --strategy my_strategy
```

## 4. 后续扩展建议

1. **xtquant SDK 集成**：通过 Python API 直接获取回测/实盘数据，落地到 `data/qmt/...`。
2. **版本管理**：在 `strategies/qmt/.versions` 保存策略快照，配合 `core/strategy_manager`.
3. **自动化**：借助 CLI 触发 xtquant 回测脚本，将结果 JSON 自动拷贝到 `backtest_results`。














