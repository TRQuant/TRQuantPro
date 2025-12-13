# 数据源配置指南

## 📡 聚宽 (JQData) 配置

### 1. 安装依赖

首先确保已安装 `jqdatasdk`：

```bash
pip install jqdatasdk>=1.9.0
```

或者安装完整依赖：

```bash
cd /home/taotao/dev/QuantTest/TRQuant/extension/python
pip install -r requirements.txt
```

### 2. 配置账号密码

配置文件位置：`/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json`

配置文件格式：

```json
{
  "username": "your_phone_number",
  "password": "your_password",
  "api_endpoint": "https://dataapi.joinquant.com",
  "timeout": 30,
  "retry_times": 3,
  "data_mode": "historical",
  "permission": {
    "auto_detect": true,
    "start_date": null,
    "end_date": null
  }
}
```

**当前配置状态**：
- ✅ 配置文件已存在
- ✅ 账号：`18072069583`
- ✅ 密码：已配置

### 3. 测试认证

在 Cursor 中：

1. 打开 **🔄 投资工作流** → **📡 1. 数据中心**
2. 点击 **🔐 测试聚宽认证** 按钮
3. 查看认证结果

或者使用命令行测试：

```bash
cd /home/taotao/dev/QuantTest/TRQuant
python3 -c "from jqdata.auth import authenticate; from config.config_manager import get_config_manager; cm = get_config_manager(); jq_config = cm.get_jqdata_config(); result = authenticate(jq_config.get('username'), jq_config.get('password')); print('认证结果:', '成功' if result else '失败')"
```

### 4. 数据更新

在数据中心面板中，您可以：

- **📈 更新行情数据**：更新日线、分钟线等行情数据
- **📋 更新财务数据**：更新财务报表、估值等数据
- **🔐 测试聚宽认证**：验证账号密码是否正确

### 5. 常见问题

#### 问题1：ModuleNotFoundError: No module named 'jqdatasdk'

**解决方案**：
```bash
pip install jqdatasdk
```

#### 问题2：认证失败

**检查项**：
1. 账号密码是否正确
2. 网络连接是否正常
3. 账号是否有效（未过期）
4. 配置文件路径是否正确

**修复步骤**：
1. 打开配置文件：`/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json`
2. 确认 `username` 和 `password` 字段正确
3. 保存文件
4. 重新测试认证

#### 问题3：数据获取失败

**可能原因**：
- 免费账户有数据权限限制
- 请求的数据超出权限范围
- 网络问题

**解决方案**：
- 检查账号权限范围
- 使用 `data_mode: "historical"` 模式（免费版）
- 检查网络连接

### 6. 配置路径说明

系统会按以下顺序查找配置：

1. **项目配置**（优先）：`/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json`
2. **用户配置**（备用）：`~/.local/share/trquant/config/jqdata_config.json`

### 7. 其他数据源

#### AKShare（免费，推荐）

无需配置，直接使用：

```bash
pip install akshare
```

#### TuShare

需要 Token，配置方式类似：

```json
{
  "token": "your_tushare_token"
}
```

---

**最后更新**：2025-12-05








