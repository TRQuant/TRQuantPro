# 聚宽（JQData）配置完整指南

## 📋 目录

1. [安装依赖](#1-安装依赖)
2. [创建配置文件](#2-创建配置文件)
3. [配置路径优先级](#3-配置路径优先级)
4. [使用方式](#4-使用方式)
5. [测试认证](#5-测试认证)
6. [常用数据获取示例](#6-常用数据获取示例)
7. [常见问题](#7-常见问题)
8. [安全提示](#8-安全提示)
9. [更新配置](#9-更新配置)
10. [项目中的实际使用示例](#10-项目中的实际使用示例)

---

## 1. 安装依赖

### 1.1 安装 jqdatasdk

```bash
pip install jqdatasdk>=1.9.0
```

### 1.2 安装项目完整依赖

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
pip install -r requirements.txt
```

### 1.3 验证安装

```bash
python3 -c "import jqdatasdk; print('jqdatasdk版本:', jqdatasdk.__version__)"
```

---

## 2. 创建配置文件

### 2.1 配置文件位置

**主配置文件**：`config/jqdata_config.json`

**备用配置文件**：`~/.local/share/trquant/config/jqdata_config.json`

### 2.2 配置文件格式

创建 `config/jqdata_config.json` 文件：

```json
{
  "username": "your_phone_number",
  "password": "your_password",
  "api_endpoint": "https://dataapi.joinquant.com",
  "timeout": 30,
  "retry_times": 3,
  "data_mode": "historical",
  "data_mode_comment": "historical: 使用历史数据(免费版), realtime: 使用实时数据(付费版)",
  "permission": {
    "auto_detect": true,
    "auto_detect_comment": "自动检测账号权限范围",
    "start_date": null,
    "end_date": null,
    "start_date_comment": "如果auto_detect为false，手动指定开始日期",
    "end_date_comment": "如果auto_detect为false，手动指定结束日期"
  }
}
```

### 2.3 配置项说明

| 配置项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `username` | string | ✅ | 聚宽账号（手机号） |
| `password` | string | ✅ | 聚宽密码 |
| `api_endpoint` | string | ❌ | API端点地址，默认：`https://dataapi.joinquant.com` |
| `timeout` | integer | ❌ | 请求超时时间（秒），默认：30 |
| `retry_times` | integer | ❌ | 重试次数，默认：3 |
| `data_mode` | string | ❌ | 数据模式：`"historical"`（历史数据，免费版）或 `"realtime"`（实时数据，付费版） |
| `permission.auto_detect` | boolean | ❌ | 是否自动检测账号权限范围，推荐：`true` |
| `permission.start_date` | string | ❌ | 手动指定开始日期（格式：`"YYYY-MM-DD"`），仅在 `auto_detect` 为 `false` 时使用 |
| `permission.end_date` | string | ❌ | 手动指定结束日期（格式：`"YYYY-MM-DD"`），仅在 `auto_detect` 为 `false` 时使用 |

### 2.4 从模板创建配置文件

```bash
# 复制模板文件
cp config/jqdata_config.example.json config/jqdata_config.json

# 编辑配置文件
vim config/jqdata_config.json
# 或
nano config/jqdata_config.json
```

---

## 3. 配置路径优先级

系统按以下顺序查找配置：

1. **项目配置（优先）**：`config/jqdata_config.json`
2. **用户配置（备用）**：`~/.local/share/trquant/config/jqdata_config.json`

如果项目配置不存在，系统会自动尝试加载用户配置。

---

## 4. 使用方式

### 4.1 方式1：使用配置管理器（推荐）

```python
from config.config_manager import get_config_manager
import jqdatasdk as jq

# 获取配置管理器
config_manager = get_config_manager()

# 获取聚宽配置
jq_config = config_manager.get_jqdata_config()
username = jq_config['username']
password = jq_config['password']

# 认证
jq.auth(username, password)

# 验证认证状态
if jq.is_auth():
    print("✅ 认证成功！")
    
    # 检查剩余查询次数
    query_count = jq.get_query_count()
    print(f"剩余查询次数: {query_count.get('spare', 'N/A')}")
else:
    print("❌ 认证失败！")
```

### 4.2 方式2：使用项目封装的工具函数

```python
from research.short_mid_term_signal_selector.jqdata_io import ensure_jqdata, get_price_panel

# 自动认证并获取最近交易日
info = ensure_jqdata()
if info.authed:
    print(f"✅ 认证成功")
    print(f"最近交易日: {info.as_of_date}")
    print(f"剩余查询次数: {info.spare_queries}")
    
    # 获取价格数据
    price_data = get_price_panel(
        code='000001.XSHE',
        start_date='2024-01-01',
        end_date=info.as_of_date,
        fields=['open', 'high', 'low', 'close', 'volume', 'money']
    )
    print(price_data.head())
else:
    print("❌ 认证失败")
```

### 4.3 方式3：直接读取JSON文件

```python
import json
from pathlib import Path
import jqdatasdk as jq

# 读取配置文件
config_path = Path(__file__).parent / "config" / "jqdata_config.json"
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 认证
jq.auth(config['username'], config['password'])

# 验证
if jq.is_auth():
    print("✅ 认证成功")
else:
    print("❌ 认证失败")
```

### 4.4 方式4：在Notebook中使用

```python
# 在Jupyter Notebook中
import sys
sys.path.insert(0, '/home/taotao/.cursor/worktrees/TRQuant/ope')

from config.config_manager import get_config_manager
import jqdatasdk as jq

# 获取配置并认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 验证
print("认证状态:", "成功" if jq.is_auth() else "失败")
```

---

## 5. 测试认证

### 5.1 命令行测试

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

python3 -c "
from config.config_manager import get_config_manager
import jqdatasdk as jq

cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))
print('认证结果:', '✅ 成功' if jq.is_auth() else '❌ 失败')
"
```

### 5.2 Python脚本测试

创建 `test_jqdata_auth.py`：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试聚宽认证
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

import jqdatasdk as jq
from config.config_manager import get_config_manager

def test_auth():
    """测试聚宽认证"""
    try:
        # 获取配置
        cm = get_config_manager()
        jq_config = cm.get_jqdata_config()
        
        if not jq_config:
            print("❌ 配置文件不存在或为空")
            return False
        
        username = jq_config.get('username')
        password = jq_config.get('password')
        
        if not username or not password:
            print("❌ 用户名或密码未配置")
            return False
        
        # 认证
        print(f"正在认证用户: {username}...")
        jq.auth(username, password)
        
        # 验证
        if jq.is_auth():
            print("✅ 认证成功！")
            
            # 检查查询次数
            try:
                query_count = jq.get_query_count()
                print(f"剩余查询次数: {query_count.get('spare', 'N/A')}")
                print(f"总查询次数: {query_count.get('total', 'N/A')}")
            except Exception as e:
                print(f"⚠️  无法获取查询次数: {e}")
            
            return True
        else:
            print("❌ 认证失败")
            return False
            
    except Exception as e:
        print(f"❌ 认证异常: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_auth()
    sys.exit(0 if success else 1)
```

运行测试：

```bash
python3 test_jqdata_auth.py
```

### 5.3 在Cursor中测试

1. 打开 **🔄 投资工作流** → **📡 1. 数据中心**
2. 点击 **🔐 测试聚宽认证** 按钮
3. 查看认证结果

---

## 6. 常用数据获取示例

### 6.1 获取股票列表

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 获取所有股票
stocks = jq.get_all_securities(types=['stock'], date='2025-01-05')
print(f"股票数量: {len(stocks)}")
print(stocks.head())

# 获取ETF列表
etfs = jq.get_all_securities(types=['etf'], date='2025-01-05')
print(f"ETF数量: {len(etfs)}")
```

### 6.2 获取价格数据

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 获取单只股票价格数据
price = jq.get_price(
    '000001.XSHE',  # 平安银行
    start_date='2024-01-01',
    end_date='2025-01-05',
    frequency='daily',
    fields=['open', 'high', 'low', 'close', 'volume', 'money']
)
print(price.head())

# 获取多只股票价格数据
codes = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
price_panel = jq.get_price(
    codes,
    start_date='2024-01-01',
    end_date='2025-01-05',
    frequency='daily',
    fields=['close']
)
print(price_panel.head())
```

### 6.3 获取财务数据

```python
import jqdatasdk as jq
from jqdatasdk import query, valuation, indicator
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 查询单只股票的财务指标
q = query(
    valuation.code,
    valuation.market_cap,      # 市值
    valuation.pe_ratio,        # PE
    valuation.pb_ratio,        # PB
    indicator.roe,             # ROE
    indicator.gross_profit_margin,  # 毛利率
    indicator.inc_revenue_year_on_year,  # 营收YoY
    indicator.inc_net_profit_year_on_year  # 净利YoY
).filter(valuation.code == '000001.XSHE')

fin = jq.get_fundamentals(q, date='2025-01-05')
print(fin)

# 查询多只股票的财务指标
codes = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
q = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio,
    indicator.roe
).filter(valuation.code.in_(codes))

fin_multi = jq.get_fundamentals(q, date='2025-01-05')
print(fin_multi)
```

### 6.4 获取概念代码

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 获取所有概念
concepts = jq.get_concept()
print(f"概念数量: {len(concepts)}")
print(concepts.head())

# 获取特定概念下的股票
concept_code = 'SC0020'  # 汽车电子
stocks_in_concept = jq.get_concept_stocks(concept_code, date='2025-01-05')
print(f"概念 {concept_code} 下的股票数量: {len(stocks_in_concept)}")
print(stocks_in_concept[:10])
```

### 6.5 获取交易日历

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 获取指定日期范围的交易日
trade_days = jq.get_trade_days(start_date='2024-01-01', end_date='2025-01-05')
print(f"交易日数量: {len(trade_days)}")
print(f"第一个交易日: {trade_days[0]}")
print(f"最后一个交易日: {trade_days[-1]}")

# 获取最近N个交易日
recent_trade_days = jq.get_trade_days(end_date='2025-01-05', count=10)
print(f"最近10个交易日: {recent_trade_days}")
```

### 6.6 获取指数数据

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 获取指数价格数据
index_code = '000300.XSHG'  # 沪深300
index_price = jq.get_price(
    index_code,
    start_date='2024-01-01',
    end_date='2025-01-05',
    frequency='daily',
    fields=['close']
)
print(index_price.head())

# 获取指数成分股
index_stocks = jq.get_index_stocks(index_code, date='2025-01-05')
print(f"沪深300成分股数量: {len(index_stocks)}")
print(index_stocks[:10])
```

### 6.7 获取行业分类

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 获取申万行业分类
industries = jq.get_industries(name='sw_l1', date='2025-01-05')
print(f"申万一级行业数量: {len(industries)}")
print(industries.head())

# 获取特定行业下的股票
industry_code = '801010'  # 农林牧渔
stocks_in_industry = jq.get_industry_stocks(industry_code, date='2025-01-05')
print(f"行业 {industry_code} 下的股票数量: {len(stocks_in_industry)}")
```

### 6.8 完整示例：获取股票基本信息并计算指标

```python
import jqdatasdk as jq
import pandas as pd
from jqdatasdk import query, valuation, indicator
from config.config_manager import get_config_manager

# 认证
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 1. 获取股票列表
stocks = jq.get_all_securities(types=['stock'], date='2025-01-05')
print(f"股票总数: {len(stocks)}")

# 2. 选择几只股票进行分析
target_codes = ['000001.XSHE', '000002.XSHE', '600000.XSHG', '600519.XSHG']

# 3. 获取价格数据
price_data = jq.get_price(
    target_codes,
    start_date='2024-01-01',
    end_date='2025-01-05',
    frequency='daily',
    fields=['close', 'volume']
)

# 4. 计算收益率
returns = price_data['close'].pct_change()
print("收益率统计:")
print(returns.describe())

# 5. 获取财务数据
q = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio,
    valuation.pb_ratio,
    indicator.roe,
    indicator.gross_profit_margin
).filter(valuation.code.in_(target_codes))

fin_data = jq.get_fundamentals(q, date='2025-01-05')
print("\n财务数据:")
print(fin_data)

# 6. 综合展示
print("\n综合信息:")
for code in target_codes:
    stock_name = stocks.loc[code, 'display_name'] if code in stocks.index else 'N/A'
    latest_price = price_data['close'].loc[code].iloc[-1] if code in price_data['close'].columns else 'N/A'
    ret_60d = (price_data['close'].loc[code].iloc[-1] / price_data['close'].loc[code].iloc[-61] - 1) * 100 if len(price_data['close'].loc[code]) >= 61 else 'N/A'
    
    fin_row = fin_data[fin_data['code'] == code]
    pe = fin_row['pe_ratio'].iloc[0] if not fin_row.empty else 'N/A'
    roe = fin_row['roe'].iloc[0] if not fin_row.empty else 'N/A'
    
    print(f"\n{code} ({stock_name}):")
    print(f"  最新价格: {latest_price:.2f}" if isinstance(latest_price, (int, float)) else f"  最新价格: {latest_price}")
    print(f"  60日收益: {ret_60d:.2f}%" if isinstance(ret_60d, (int, float)) else f"  60日收益: {ret_60d}")
    print(f"  PE: {pe:.2f}" if isinstance(pe, (int, float)) else f"  PE: {pe}")
    print(f"  ROE: {roe:.2f}%" if isinstance(roe, (int, float)) else f"  ROE: {roe}")
```

---

## 7. 常见问题

### 7.1 ModuleNotFoundError: No module named 'jqdatasdk'

**问题描述**：找不到 `jqdatasdk` 模块

**解决方案**：

```bash
pip install jqdatasdk>=1.9.0
```

如果使用虚拟环境，确保激活虚拟环境后再安装：

```bash
# 激活虚拟环境（如果使用）
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装
pip install jqdatasdk>=1.9.0
```

### 7.2 认证失败

**问题描述**：调用 `jq.auth()` 后，`jq.is_auth()` 返回 `False`

**检查项**：

1. **账号密码是否正确**
   ```python
   # 检查配置
   from config.config_manager import get_config_manager
   cm = get_config_manager()
   jq_config = cm.get_jqdata_config()
   print(f"用户名: {jq_config.get('username')}")
   print(f"密码: {'已配置' if jq_config.get('password') else '未配置'}")
   ```

2. **网络连接是否正常**
   ```bash
   # 测试网络连接
   ping dataapi.joinquant.com
   ```

3. **账号是否有效（未过期）**
   - 登录聚宽官网检查账号状态
   - 确认账号未过期或被禁用

4. **配置文件路径是否正确**
   ```python
   from pathlib import Path
   config_path = Path(__file__).parent / "config" / "jqdata_config.json"
   print(f"配置文件路径: {config_path}")
   print(f"文件是否存在: {config_path.exists()}")
   ```

**修复步骤**：

1. 打开配置文件：`config/jqdata_config.json`
2. 确认 `username` 和 `password` 字段正确
3. 保存文件
4. 重新测试认证

### 7.3 数据获取失败

**问题描述**：调用数据获取函数时返回空数据或报错

**可能原因**：

1. **免费账户有数据权限限制**
   - 免费账户只能获取历史数据
   - 某些数据可能需要付费权限

2. **请求的数据超出权限范围**
   ```python
   # 检查账号权限范围
   import jqdatasdk as jq
   query_count = jq.get_query_count()
   print(f"剩余查询次数: {query_count.get('spare', 'N/A')}")
   ```

3. **网络问题**
   - 检查网络连接
   - 检查防火墙设置

4. **日期范围问题**
   - 确保请求的日期在账号权限范围内
   - 确保日期格式正确（`YYYY-MM-DD`）

**解决方案**：

```python
# 1. 检查账号权限
import jqdatasdk as jq
from config.config_manager import get_config_manager

cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

# 检查查询次数
query_count = jq.get_query_count()
print(f"剩余查询次数: {query_count.get('spare', 'N/A')}")

# 2. 使用历史数据模式
# 在配置文件中设置: "data_mode": "historical"

# 3. 检查网络连接
import requests
try:
    response = requests.get('https://dataapi.joinquant.com', timeout=5)
    print(f"网络连接正常: {response.status_code}")
except Exception as e:
    print(f"网络连接异常: {e}")

# 4. 使用有效的日期范围
from datetime import datetime, timedelta
today = datetime.now()
valid_end_date = today.strftime('%Y-%m-%d')
valid_start_date = (today - timedelta(days=365)).strftime('%Y-%m-%d')
print(f"有效日期范围: {valid_start_date} ~ {valid_end_date}")
```

### 7.4 查询次数限制

**问题描述**：达到每日查询次数限制

**检查剩余查询次数**：

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager

cm = get_config_manager()
jq_config = cm.get_jqdata_config()
jq.auth(jq_config.get('username'), jq_config.get('password'))

query_count = jq.get_query_count()
print(f"剩余查询次数: {query_count.get('spare', 'N/A')}")
print(f"总查询次数: {query_count.get('total', 'N/A')}")
print(f"已使用查询次数: {query_count.get('total', 0) - query_count.get('spare', 0)}")
```

**解决方案**：

1. **优化查询频率**：减少不必要的查询
2. **批量查询**：使用批量接口减少查询次数
3. **缓存数据**：对不经常变化的数据进行缓存
4. **升级账号**：考虑升级到付费账号

### 7.5 配置文件不存在

**问题描述**：`FileNotFoundError` 或配置为空

**解决方案**：

```bash
# 1. 从模板创建配置文件
cp config/jqdata_config.example.json config/jqdata_config.json

# 2. 编辑配置文件
vim config/jqdata_config.json
# 或
nano config/jqdata_config.json

# 3. 填写账号密码
# {
#   "username": "your_phone_number",
#   "password": "your_password",
#   ...
# }
```

### 7.6 日期格式错误

**问题描述**：日期参数格式不正确导致查询失败

**正确格式**：

```python
# ✅ 正确格式
date_str = '2025-01-05'  # YYYY-MM-DD

# ❌ 错误格式
date_str = '2025/01/05'  # 不支持斜杠
date_str = '01-05-2025'   # 不支持MM-DD-YYYY
date_str = '20250105'     # 不支持无分隔符
```

**日期转换示例**：

```python
from datetime import datetime

# 从datetime对象转换为字符串
dt = datetime(2025, 1, 5)
date_str = dt.strftime('%Y-%m-%d')  # '2025-01-05'

# 从字符串转换为datetime对象
date_str = '2025-01-05'
dt = datetime.strptime(date_str, '%Y-%m-%d')
```

---

## 8. 安全提示

⚠️ **重要安全提示**：

1. **不要提交配置文件到Git仓库**
   - 配置文件包含敏感信息（账号密码）
   - 已在 `.gitignore` 中排除 `config/jqdata_config.json`
   - 确保不会意外提交

2. **定期更新密码**
   - 建议每3-6个月更新一次密码
   - 使用强密码（包含大小写字母、数字、特殊字符）

3. **使用环境变量（生产环境推荐）**
   ```python
   import os
   import jqdatasdk as jq
   
   # 从环境变量读取
   username = os.getenv('JQDATA_USERNAME')
   password = os.getenv('JQDATA_PASSWORD')
   
   if username and password:
       jq.auth(username, password)
   ```

4. **使用密钥管理工具**
   - AWS Secrets Manager
   - HashiCorp Vault
   - Azure Key Vault

5. **限制配置文件权限**
   ```bash
   # Linux/Mac
   chmod 600 config/jqdata_config.json
   
   # 确保只有所有者可以读写
   ```

6. **不要在代码中硬编码密码**
   ```python
   # ❌ 错误做法
   jq.auth('18072069583', 'your_password')
   
   # ✅ 正确做法
   from config.config_manager import get_config_manager
   cm = get_config_manager()
   jq_config = cm.get_jqdata_config()
   jq.auth(jq_config.get('username'), jq_config.get('password'))
   ```

---

## 9. 更新配置

### 9.1 使用配置管理器更新

```python
from config.config_manager import get_config_manager

config_manager = get_config_manager()

# 更新聚宽配置
config_manager.update_jqdata_config(
    username='新用户名',
    password='新密码',
    timeout=60,      # 可选：更新超时时间
    retry_times=5    # 可选：更新重试次数
)

# 验证更新
jq_config = config_manager.get_jqdata_config()
print(f"新用户名: {jq_config.get('username')}")
```

### 9.2 直接编辑JSON文件

```bash
# 编辑配置文件
vim config/jqdata_config.json

# 或使用Python脚本
python3 << EOF
import json
from pathlib import Path

config_path = Path('config/jqdata_config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 更新配置
config['username'] = '新用户名'
config['password'] = '新密码'
config['timeout'] = 60

# 保存
with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("配置已更新")
EOF
```

---

## 10. 项目中的实际使用示例

### 10.1 封装的工具函数

参考文件：`research/short_mid_term_signal_selector/jqdata_io.py`

```python
from research.short_mid_term_signal_selector.jqdata_io import (
    ensure_jqdata,
    get_all_stocks,
    get_all_etfs,
    get_price_panel,
    calc_start_date
)

# 自动认证并获取最近交易日
info = ensure_jqdata()
if info.authed:
    as_of_date = info.as_of_date
    
    # 获取所有股票
    stocks = get_all_stocks(as_of_date)
    print(f"股票数量: {len(stocks)}")
    
    # 获取价格数据
    price = get_price_panel(
        code='000001.XSHE',
        start_date=calc_start_date(as_of_date, 60),
        end_date=as_of_date,
        fields=['open', 'high', 'low', 'close', 'volume', 'money']
    )
    print(price.head())
```

### 10.2 在报告生成脚本中使用

参考文件：`scripts/reports/junsheng_full_analysis_report.py`

```python
import jqdatasdk as jq
from config.config_manager import get_config_manager
from datetime import datetime

# 认证
cm = get_config_manager()
cfg = cm.get_config('jqdata')
jq.auth(cfg['username'], cfg['password'])

# 获取数据
code = '600699.XSHG'
as_of = '2026-01-05'

# 获取价格数据
price = jq.get_price(
    code,
    start_date='2020-01-01',
    end_date=as_of,
    fields=['open', 'high', 'low', 'close', 'volume', 'money']
)

# 获取财务数据
from jqdatasdk import query, valuation, indicator
q = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio,
    valuation.pb_ratio,
    indicator.roe,
    indicator.gross_profit_margin,
    indicator.inc_net_profit_year_on_year,
    indicator.inc_revenue_year_on_year
).filter(valuation.code == code)

fin = jq.get_fundamentals(q, date=as_of)
print(fin)
```

### 10.3 在数据源封装中使用

参考文件：`data_sources/jqdata_source.py`

```python
from data_sources.jqdata_source import JQDataSource

# 创建数据源实例
jq_source = JQDataSource()

# 连接
if jq_source.connect():
    print("✅ JQData连接成功")
    
    # 使用数据源获取数据
    # ... 具体使用方式参考 data_sources/jqdata_source.py
else:
    print("❌ JQData连接失败")
```

---

## 11. 快速参考

### 11.1 常用命令

```bash
# 测试认证
python3 -c "from config.config_manager import get_config_manager; import jqdatasdk as jq; cm = get_config_manager(); cfg = cm.get_jqdata_config(); jq.auth(cfg['username'], cfg['password']); print('✅ 成功' if jq.is_auth() else '❌ 失败')"

# 检查配置
cat config/jqdata_config.json

# 从模板创建配置
cp config/jqdata_config.example.json config/jqdata_config.json
```

### 11.2 常用代码片段

```python
# 快速认证
import jqdatasdk as jq
from config.config_manager import get_config_manager
cm = get_config_manager()
jq.auth(*cm.get_jqdata_config().values())

# 检查认证状态
if jq.is_auth():
    print("已认证")
```

---

## 12. 相关文档

- [数据源配置指南](docs/03_modules/DATA_SOURCE_SETUP.md)
- [配置文件说明](config/README.md)
- [聚宽官方文档](https://www.joinquant.com/help/api/help?name=JQData)

---

## 13. 更新日志

- **2026-01-06**: 创建完整配置指南文档
- **2025-12-05**: 初始配置文档

---

**最后更新**：2026-01-06

**维护者**：TRQuant Team
