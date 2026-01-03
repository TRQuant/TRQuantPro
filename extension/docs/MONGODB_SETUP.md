# MongoDB 安装指南

## 📦 已安装的组件

✅ **jqdatasdk** (1.9.7) - 聚宽数据SDK  
✅ **pymongo** (4.15.5) - MongoDB Python客户端  
✅ **JQData认证** - 已成功配置并测试通过

## 🔧 MongoDB 服务器安装

MongoDB 用于数据缓存和存储。如果需要使用缓存功能，请安装 MongoDB 服务器。

### Ubuntu/Debian 安装

```bash
# 1. 导入 MongoDB 公钥
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# 2. 添加 MongoDB 仓库
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# 3. 更新包列表
sudo apt update

# 4. 安装 MongoDB
sudo apt install -y mongodb-org

# 5. 启动 MongoDB 服务
sudo systemctl start mongod
sudo systemctl enable mongod

# 6. 验证安装
sudo systemctl status mongod
```

### 使用 Docker 安装（推荐）

```bash
# 拉取 MongoDB 镜像
docker pull mongo:latest

# 运行 MongoDB 容器
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# 验证运行
docker ps | grep mongodb
```

### 验证连接

```bash
# 测试 MongoDB 连接
python3 -c "from pymongo import MongoClient; client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000); client.admin.command('ping'); print('✓ MongoDB 连接成功')"
```

## 📝 注意事项

1. **MongoDB 是可选的**：如果不需要数据缓存功能，可以不安装 MongoDB。数据源管理器会使用其他数据源（如 JQData、AKShare）。

2. **当前状态**：
   - ✅ JQData 已配置并可用
   - ✅ MongoDB 已安装并运行（Docker 容器：taorui-mongodb）

3. **数据更新功能**：即使没有 MongoDB，数据更新功能仍然可以正常工作，只是无法使用本地缓存。

## 🔍 测试数据更新

在 Cursor 中：

1. 打开 **🔄 投资工作流** → **📡 1. 数据中心**
2. 点击 **🔐 测试聚宽认证** - 应该显示成功
3. 点击 **📈 更新行情数据** - 应该可以正常更新

---

**最后更新**：2025-12-05


