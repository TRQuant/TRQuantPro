# 8步骤工作流点击测试指南

**更新时间**: 2025-12-07

---

## ✅ 命令注册状态

### 1. 侧边栏树视图

**位置**: VS Code 左侧活动栏 → TRQuant → 🔄 投资工作流

**状态**: ✅ 已注册
- **视图ID**: `trquant-workflow`
- **注册位置**: `extension/src/providers/workflowProvider.ts` (行 337)
- **配置位置**: `extension/package.json` (行 375-376)

**测试方法**:
1. 打开 VS Code
2. 点击左侧活动栏的 TRQuant 图标
3. 找到 "🔄 投资工作流" 视图
4. 应该能看到 8 个步骤的树形结构
5. 点击任意步骤，应该能打开对应的面板

---

### 2. 命令面板

**状态**: ✅ 已注册

**测试方法**:
1. 按 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. 输入 `TRQuant:`
3. 应该能看到所有 8 个步骤的命令：
   - `TRQuant: 📡 数据中心 (步骤1)`
   - `TRQuant: 📈 市场分析 (步骤2)`
   - `TRQuant: 🔥 投资主线 (步骤3)`
   - `TRQuant: 📦 候选池 (步骤4)`
   - `TRQuant: 📊 因子中心 (步骤5)`
   - `TRQuant: 🛠️ 策略开发 (步骤6)`
   - `TRQuant: 🔄 回测中心 (步骤7)`
   - `TRQuant: 🚀 交易中心 (步骤8)`

---

### 3. 主控制台

**状态**: ✅ 已注册
- **命令**: `trquant.openDashboard`
- **文件**: `extension/src/views/mainDashboard.ts`

**测试方法**:
1. 命令面板: `Ctrl+Shift+P` → `TRQuant: 量化工作台`
2. 在主控制台中应该能看到 8 步骤工作流的快捷入口

---

## 🔐 聚宽账号配置状态

### 配置文件位置

**路径**: `config/jqdata_config.json`

### 当前配置

```json
{
  "username": "18072069583",
  "password": "%5Diamond",
  "api_endpoint": "https://dataapi.joinquant.com",
  "timeout": 30,
  "retry_times": 3,
  "data_mode": "historical"
}
```

**状态**: ✅ 已配置
- **用户名**: `18072069583`
- **密码**: 已设置（URL编码格式）
- **API端点**: `https://dataapi.joinquant.com`
- **数据模式**: `historical` (历史数据，免费版)

---

## 🧪 测试步骤

### 测试1: 验证命令注册

```bash
# 在 VS Code 中打开命令面板
Ctrl+Shift+P

# 输入以下命令之一
TRQuant: 📡 数据中心 (步骤1)
TRQuant: 📈 市场分析 (步骤2)
```

**预期结果**: 应该能打开对应的面板

---

### 测试2: 验证侧边栏树视图

1. 打开 VS Code
2. 点击左侧活动栏的 TRQuant 图标
3. 找到 "🔄 投资工作流" 视图
4. 展开任意步骤
5. 点击步骤名称

**预期结果**: 应该能打开对应的面板

---

### 测试3: 验证聚宽配置

```bash
cd /home/taotao/dev/QuantTest/TRQuant
python3 -c "
from config.config_manager import get_config_manager
cm = get_config_manager()
jq_config = cm.get_jqdata_config()
print('用户名:', jq_config.get('username'))
print('密码已设置:', bool(jq_config.get('password')))
"
```

**预期结果**: 应该显示用户名和密码已设置

---

### 测试4: 验证聚宽认证

在数据中心面板中：
1. 打开步骤1: 数据中心
2. 点击 "🔐 测试聚宽认证" 按钮
3. 查看认证结果

**预期结果**: 应该显示认证成功或失败

---

## ⚠️ 常见问题

### 问题1: 点击步骤没有反应

**可能原因**:
1. 扩展未激活
2. 命令未注册
3. Python Bridge 未启动

**解决方法**:
1. 检查扩展是否已安装并激活
2. 重新加载窗口: `Ctrl+Shift+P` → `Developer: Reload Window`
3. 检查 `extension/python/bridge.py` 是否存在

---

### 问题2: 聚宽认证失败

**可能原因**:
1. 账号密码错误
2. 网络连接问题
3. `jqdatasdk` 未安装

**解决方法**:
1. 检查配置文件中的账号密码是否正确
2. 安装 `jqdatasdk`: `pip install jqdatasdk`
3. 测试网络连接: `ping dataapi.joinquant.com`

---

### 问题3: 侧边栏不显示

**可能原因**:
1. `package.json` 中的视图配置错误
2. 扩展未正确加载

**解决方法**:
1. 检查 `extension/package.json` 中的 `views` 配置
2. 重新编译扩展: `cd extension && npm run compile`
3. 重新加载窗口

---

## 📝 总结

### ✅ 已完成的配置

1. **命令注册**: 所有 8 个步骤的命令已注册
2. **侧边栏视图**: 工作流树视图已配置
3. **聚宽账号**: 已配置用户名和密码
4. **Python Bridge**: `extension/python/bridge.py` 存在

### 🔄 需要验证的功能

1. **点击打开**: 需要在实际使用中验证点击是否真的能打开面板
2. **聚宽认证**: 需要在数据中心面板中测试认证功能
3. **数据获取**: 需要测试是否能正常获取数据

---

**下一步**: 在实际使用中测试点击打开功能，并验证聚宽账号是否能正常认证。



