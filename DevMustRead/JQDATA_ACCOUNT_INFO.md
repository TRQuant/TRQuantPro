# JQData get_account_info() 账号权限详情

> **测试时间**: 2025-12-19  
> **API**: `get_account_info()`

---

## 📋 API说明

**功能**: 查看账号功能权限详情

**调用方式**:
```python
from jqdatasdk import auth, get_account_info

# 先认证
auth('username', 'password')

# 获取账号信息
account_info = get_account_info()
```

---

## 📊 返回结果

### 实际返回示例

```json
{
  "mob": "18072069583",
  "query_count_limit": 1000000,
  "license": 1,
  "expire_time": "2026-02-07 00:00:00",
  "date_range_start": "2024-09-11 00:00:00",
  "date_range_end": "2025-09-18 00:00:00"
}
```

---

## 🔍 字段说明

### 1. mob

**类型**: String  
**说明**: 手机号（账号标识）  
**示例**: `"18072069583"`

---

### 2. query_count_limit

**类型**: Integer  
**说明**: 每日查询次数限制

| 账号类型 | 限制值 | 说明 |
|---------|--------|------|
| 试用账户 | 1000000 | 100万条/天 |
| 正式账户 | 200000000 | 2亿条/天 |

**示例**: `1000000`

---

### 3. license

**类型**: Integer  
**说明**: 账号类型标识

| 值 | 说明 |
|---|------|
| 1 | 可能是试用账户 |
| 其他 | 可能是正式账户或其他类型 |

**示例**: `1`

---

### 4. expire_time

**类型**: String  
**格式**: `"YYYY-MM-DD HH:MM:SS"`  
**说明**: 账号有效期

| 账号类型 | 有效期 |
|---------|--------|
| 试用账户 | 通常3个月 |
| 正式账户 | 通常12个月 |

**示例**: `"2026-02-07 00:00:00"`

---

### 5. date_range_start

**类型**: String  
**格式**: `"YYYY-MM-DD HH:MM:SS"`  
**说明**: 数据开始日期（可查询的最早日期）

| 账号类型 | 说明 |
|---------|------|
| 试用账户 | 前15个月（距今15个月前） |
| 正式账户 | 不限制 |

**示例**: `"2024-09-11 00:00:00"`

---

### 6. date_range_end

**类型**: String  
**格式**: `"YYYY-MM-DD HH:MM:SS"`  
**说明**: 数据结束日期（可查询的最晚日期）

| 账号类型 | 说明 |
|---------|------|
| 试用账户 | 前3个月（距今最近3个月，不包含最近3个月） |
| 正式账户 | 不限制 |

**示例**: `"2025-09-18 00:00:00"`

---

## 🔐 权限判断

### 试用账户特征

1. `query_count_limit = 1000000`（100万条/天）
2. `date_range_start`和`date_range_end`存在（数据范围受限）
3. `license = 1`（可能是试用账户标识）
4. `expire_time`距离当前时间约3个月

### 正式账户特征

1. `query_count_limit = 200000000`（2亿条/天）
2. `date_range_start`和`date_range_end`可能不存在或范围更大
3. `license`可能为其他值
4. `expire_time`距离当前时间约12个月

---

## 💡 使用建议

### 1. 检查账号权限

```python
from jqdatasdk import auth, get_account_info

auth('username', 'password')
account_info = get_account_info()

# 判断账号类型
if account_info['query_count_limit'] == 1000000:
    print("试用账户")
else:
    print("正式账户")
```

### 2. 根据数据范围调整查询

```python
# 获取数据范围
start_date = account_info['date_range_start'][:10]  # 提取日期部分
end_date = account_info['date_range_end'][:10]

# 确保查询日期在范围内
if query_date < start_date or query_date > end_date:
    print(f"查询日期超出范围: {start_date} 至 {end_date}")
```

### 3. 监控每日查询量

```python
from jqdatasdk import get_query_count

# 获取剩余查询次数
query_count = get_query_count()
spare = query_count.get('spare', 0)
limit = account_info['query_count_limit']

print(f"剩余查询次数: {spare}/{limit}")
```

---

## 📊 实际测试结果

**测试账号信息**:
- 手机号: 18072069583
- 每日流量限制: 1000000（100万条）
- 账号类型: license=1（试用账户）
- 有效期: 2026-02-07
- 数据范围: 2024-09-11 至 2025-09-18

**权限判断**:
- ✅ 试用账户（query_count_limit=1000000）
- ✅ 数据范围受限（前15个月~前3个月）
- ✅ 有效期约3个月（从2025-12-19到2026-02-07）

---

## 🔄 与官方说明的对比

| 项目 | 官方说明 | get_account_info()返回 |
|------|---------|----------------------|
| 账号有效期 | 3个月 | expire_time: 2026-02-07（约3个月） |
| 历史数据范围 | 前15个月~前3个月 | date_range_start: 2024-09-11<br>date_range_end: 2025-09-18 |
| 每日流量 | 100万条 | query_count_limit: 1000000 |
| 连接数 | 1个 | 未在返回结果中 |

---

## 📚 相关文档

- JQData官方文档: https://www.joinquant.com/help/api/help?name=api
- 账号权限说明: `docs/JQDATA_BASIC_DATA_SCOPE.md`
- 数据范围说明: `docs/TRIAL_ACCOUNT_DYNAMIC_DATE_GUIDE.md`

---

*文档版本: 1.0 | 创建时间: 2025-12-19*

