---
name: "运行回测"
description: "运行Phase 1和Phase 2回测，验证市场趋势分析信号"
command: |
  cd notebooks/research && \
  jupyter nbconvert --to notebook --execute 01_市场趋势判断回测验证.ipynb --inplace
---

# 运行回测命令

执行市场趋势判断回测验证，包括Phase 1和Phase 2回测。

## 使用方式

在Cursor Chat中：
```
@run-backtest
```

## 说明

- 运行完整的回测流程
- 结果保存到MongoDB
- 支持版本管理和缓存
