---
name: "筛选投资标的"
description: "基于投资主线筛选投资标的股票"
command: |
  cd notebooks/research && \
  python -c "
  import sys
  from pathlib import Path
  project_root = Path(__file__).parent.parent.parent
  sys.path.insert(0, str(project_root))
  
  from core.candidate_pool_builder import CandidatePoolBuilder
  from core.module_registry import get_candidate_pool_builder
  
  builder = get_candidate_pool_builder()
  pool = builder.build_from_mainline(
      mainline_name='人工智能',
      mainline_type='concept',
      use_cache=True
  )
  
  print(f'筛选出 {len(pool.stocks)} 只投资标的')
  for i, stock in enumerate(pool.stocks[:10], 1):
      print(f'{i}. {stock.name} ({stock.code}) - 得分: {stock.composite_score:.2f}')
  "
---

# 筛选投资标的命令

基于投资主线筛选投资标的股票。

## 使用方式

在Cursor Chat中：
```
@screen-investment-targets
```

## 参数

可以通过修改命令中的 `mainline_name` 参数来指定不同的投资主线：
- '人工智能'
- '半导体芯片'
- '新能源'
- '固态电池'
- 等

## 输出

- 筛选出的股票列表
- 每只股票的得分
- 股票代码和名称
