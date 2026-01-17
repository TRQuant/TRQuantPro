# 试用账户权限范围动态计算指南

> **更新时间**: 2025-12-19 22:50  
> **状态**: ✅ 已实现动态日期计算

---

## 📋 概述

试用账户的权限范围是**相对日期**，每天都会往前推1天。系统已实现**自动动态计算**，确保每天都能获取到最新可用数据。

---

## ✅ 实现原理

### 权限范围计算

**试用账户权限范围**:
- **开始日期** = 今天 - 约464天（约15.5个月）
- **结束日期** = 今天 - 约92天（约3个月）

**示例**:
- **今天** (2025-12-19): 2024-09-11 至 2025-09-18
- **明天** (2025-12-20): 2024-09-12 至 2025-09-19
- **后天** (2025-12-21): 2024-09-13 至 2025-09-20

---

## 🔧 技术实现

### 1. DataPermission类增强

**新增字段**:
```python
self.start_days_offset: Optional[int] = None  # 开始日期相对天数
self.end_days_offset: Optional[int] = None   # 结束日期相对天数
```

**新增方法**:
```python
def _get_current_start_date(self) -> date:
    """获取当前计算出的开始日期（动态）"""
    if self.start_days_offset is not None:
        return date.today() - timedelta(days=self.start_days_offset)
    # ...

def _get_current_end_date(self) -> date:
    """获取当前计算出的结束日期（动态）"""
    if self.end_days_offset is not None:
        return date.today() - timedelta(days=self.end_days_offset)
    # ...
```

---

### 2. 权限检测时计算相对天数

**检测到权限范围后**:
```python
# 计算相对天数（用于动态计算）
today = date.today()
start_dt = datetime.strptime(dates[0], '%Y-%m-%d').date()
end_dt = datetime.strptime(dates[1], '%Y-%m-%d').date()

self.permission.start_days_offset = (today - start_dt).days
self.permission.end_days_offset = (today - end_dt).days
```

---

### 3. 所有日期方法使用动态计算

**is_date_in_range()**:
```python
start_dt = self._get_current_start_date()  # 动态计算
end_dt = self._get_current_end_date()      # 动态计算
```

**get_valid_date_range()**:
```python
perm_start = self._get_current_start_date()  # 动态计算
perm_end = self._get_current_end_date()      # 动态计算
```

**get_latest_available_date()**:
```python
end_dt = self._get_current_end_date()  # 动态计算
return end_dt.strftime('%Y-%m-%d')
```

---

## 📊 使用示例

### 检查权限范围

```python
from jqdata.client import JQDataClient

jq_client = JQDataClient()
jq_client.authenticate(username, password)

perm = jq_client.get_permission()
print(f"当前权限范围: {perm}")
# 输出: 数据模式: 历史, 范围: 2024-09-11 至 2025-09-18

# 明天会自动更新
# 输出: 数据模式: 历史, 范围: 2024-09-12 至 2025-09-19
```

### 获取最新可用日期

```python
latest = jq_client.get_available_end_date()
print(f"最新可用日期: {latest}")
# 输出: 2025-09-18（今天）
# 明天输出: 2025-09-19（自动更新）
```

### 数据获取（自动使用动态权限范围）

```python
from mcp_servers.utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher

fetcher = TenbaggerDataFetcher(jq_client=jq_client)

# 所有数据获取自动使用动态权限范围
data = fetcher.fetch_complete_data('000001.XSHE')
# 自动使用权限范围内的最新日期
```

---

## ✅ 验证

### 测试结果

```
当前权限范围: 数据模式: 历史, 范围: 2024-09-11 至 2025-09-18
今天日期: 2025-12-19
明天的权限范围: 2024-09-12 至 2025-09-19
最新可用日期: 2025-09-18
✅ 权限范围动态计算正常
```

---

## 🔄 自动更新机制

### 每天自动更新

1. **权限检测**: 首次检测时计算相对天数
2. **日期计算**: 每次调用时使用`date.today()`动态计算
3. **自动适配**: 无需手动更新，每天自动往前推1天

### 无需手动操作

- ✅ 无需每天修改代码
- ✅ 无需手动更新日期
- ✅ 系统自动处理

---

## 📚 相关文档

- `docs/TENBAGGER_V2_TRIAL_ACCOUNT_GUIDE.md` - 试用账户处理指南
- `jqdata/client.py` - JQDataClient实现（权限检测和动态日期计算）

---

## ✅ 检查清单

- [x] DataPermission类支持相对日期计算
- [x] 权限检测时计算相对天数
- [x] 所有日期方法使用动态计算
- [x] 数据获取自动使用动态权限范围
- [x] 测试验证通过

---

*文档版本: 1.0 | 创建时间: 2025-12-19 22:50*

