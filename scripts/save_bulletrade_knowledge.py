#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将BulletTrade环境变量问题的经验存入RAG知识库
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add, error_pattern_add, practice_add

print('='*70)
print('将经验教训存入RAG知识库')
print('='*70)

# 1. 添加错误模式
print('\n1. 添加错误模式...')
error_result = error_pattern_add(
    error_type='BulletTrade数据权限错误',
    pattern='BulletTrade回测时报错：账号权限仅能获取xxx日期范围的数据。原因：BulletTrade引擎内部使用环境变量认证（JQDATA_USERNAME/JQDATA_PASSWORD），而不是脚本中的jq.auth()认证',
    solution='在回测脚本开头设置JQData环境变量：os.environ["JQDATA_USERNAME"] = username; os.environ["JQDATA_PASSWORD"] = password',
    prevention='在所有使用BulletTrade的脚本中，必须先设置JQData环境变量再运行回测',
    tags=['BulletTrade', 'JQData', '环境变量', '数据权限']
)
print(f'  结果: {error_result.get("success")}')
if error_result.get('success'):
    print(f'  模式ID: {error_result.get("pattern_id")}')

# 2. 添加最佳实践
print('\n2. 添加最佳实践...')
practice_result = practice_add(
    title='BulletTrade回测前必须设置JQData环境变量',
    description='BulletTrade引擎内部使用环境变量JQDATA_USERNAME和JQDATA_PASSWORD来认证JQData，而不是使用脚本中的jq.auth()。因此在任何使用BulletTrade回测的脚本中，必须在回测前设置这些环境变量。',
    code_example='''import os
from config.config_manager import get_config_manager

# 读取配置
config_manager = get_config_manager()
jq_config = config_manager.get_jqdata_config()
username = jq_config.get('username')
password = jq_config.get('password')

# 必须！设置环境变量供BulletTrade使用
os.environ['JQDATA_USERNAME'] = username
os.environ['JQDATA_USER'] = username
os.environ['JQDATA_PASSWORD'] = password
os.environ['JQDATA_PWD'] = password

# 然后才能运行BulletTrade回测
from core.advisor_v4.bullettrade_backtest import BulletTradeBacktest
backtest = BulletTradeBacktest(...)
result = backtest.run_backtest(...)''',
    category='BulletTrade',
    tags=['BulletTrade', 'JQData', '环境变量', '回测', '必须步骤']
)
print(f'  结果: {practice_result.get("success")}')
if practice_result.get('success'):
    print(f'  实践ID: {practice_result.get("practice_id")}')

# 3. 添加知识条目
print('\n3. 添加知识条目...')
knowledge_content = '''## 问题背景
在使用BulletTrade回测引擎时，即使脚本开头使用jq.auth()认证了JQData正式账号，回测时仍然报错"账号权限仅能获取xxx日期范围的数据"。

## 根本原因
BulletTrade引擎内部的数据提供者（bullet_trade/data/providers/jqdata.py）使用**环境变量**来认证JQData，而不是使用脚本中的jq.auth()认证。

关键环境变量：
- JQDATA_USERNAME / JQDATA_USER
- JQDATA_PASSWORD / JQDATA_PWD

## 解决方案
在回测脚本开头，除了jq.auth()外，还必须设置这些环境变量：
```python
import os
os.environ['JQDATA_USERNAME'] = username
os.environ['JQDATA_PASSWORD'] = password
```

## 预防措施
1. 在所有使用BulletTrade的脚本中，必须先设置JQData环境变量
2. 建议封装一个init_jqdata_for_bullettrade()函数，统一处理认证和环境变量设置
3. 在check_jqdata_permission()函数中同时设置环境变量

## 相关文件
- core/advisor_v4/bullettrade_backtest.py
- scripts/run_bull_market_optimization_v3.py
- bullet_trade/data/providers/jqdata.py (第三方库)

## 教训
第三方库可能有自己的认证机制，不能假设脚本中的认证会自动传递。需要仔细阅读第三方库的文档和源码，了解其数据获取机制。
'''

knowledge_result = knowledge_add(
    title='BulletTrade与JQData认证机制详解',
    content=knowledge_content,
    type='lesson',
    tags=['BulletTrade', 'JQData', '环境变量', '认证', '第三方库', '数据权限'],
    source='bull_market_optimization_v3_debug_20260111'
)
print(f'  结果: {knowledge_result.get("success")}')
if knowledge_result.get('success'):
    print(f'  知识ID: {knowledge_result.get("knowledge_id")}')

print('\n' + '='*70)
print('✅ 知识已存入RAG知识库')
print('='*70)
