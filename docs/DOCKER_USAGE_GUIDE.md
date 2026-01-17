# TRQuant 系统 - Docker使用指南

> **版本**: v1.0  
> **更新**: 2026-01-16  
> **目的**: Docker在TRQuant系统中的作用、本机系统状态和Windows使用指南

---

## 📋 目录

1. [Docker在TRQuant系统中的作用](#docker在trquant系统中的作用)
2. [本机系统状态](#本机系统状态)
3. [Windows系统使用Docker](#windows系统使用docker)
4. [Docker服务管理](#docker服务管理)
5. [故障排除](#故障排除)

---

## 🐳 Docker在TRQuant系统中的作用

### 核心作用

Docker在TRQuant系统中主要用于：

1. **数据库服务容器化**
   - MongoDB - 文档存储，研究材料、信号、回测结果
   - PostgreSQL - 主数据库（强事务/审计）
   - ClickHouse/TimescaleDB - 时序分析库
   - Redis - 缓存/队列
   - Chroma - 向量数据库（知识库向量索引）

2. **GUI应用容器化**
   - PyQt6桌面GUI应用
   - 统一的运行环境

3. **MCP服务器容器化**
   - 官方MCP服务器（time, memory, git, filesystem等）
   - 第三方MCP服务器（OpenManus等）

4. **开发环境隔离**
   - 统一的开发环境
   - 依赖管理
   - 跨平台一致性

### 架构中的位置

根据TRQuant系统7层架构，Docker主要服务于：

**第6层：数据与知识平台层**
```
┌─────────────────────────────────────────┐
│ 数据与知识平台层 (Docker容器)            │
├─────────────────────────────────────────┤
│ - PostgreSQL (主数据库)                 │
│ - ClickHouse/TimescaleDB (时序分析)      │
│ - MinIO/S3 (对象存储)                   │
│ - Redis (缓存/队列)                     │
│ - Chroma (向量数据库)                    │
│ - MongoDB (文档存储)                     │
└─────────────────────────────────────────┘
```

**第1层：表现层（GUI容器化）**
```
┌─────────────────────────────────────────┐
│ 表现层 (Docker容器)                      │
├─────────────────────────────────────────┤
│ - PyQt6 GUI应用                          │
│ - 统一的运行环境                          │
└─────────────────────────────────────────┘
```

---

## 💻 本机系统状态

### Ubuntu端（当前状态）

#### Docker服务状态

```bash
# 检查Docker是否安装
docker --version

# 检查Docker服务状态
sudo systemctl status docker

# 检查运行的容器
docker ps

# 检查所有容器（包括停止的）
docker ps -a

# 检查Docker Compose服务
docker-compose ps
```

#### 当前Docker配置

**配置文件位置**:
- `docker-compose.yml` - 主配置文件
- `docker-compose.gui.yml` - GUI应用配置
- `packaging/docker/Dockerfile` - 主应用镜像
- `packaging/docker/Dockerfile.gui` - GUI应用镜像

**管理脚本**:
- `scripts/docker_manager.sh` - Docker服务管理脚本
- `docker/run_gui_container.sh` - GUI容器运行脚本
- `docker/install_docker_shortcut.sh` - Docker快捷方式安装

#### 数据存储位置

Docker容器数据通常存储在：
- **卷挂载**: `/var/lib/docker/volumes/`
- **绑定挂载**: 项目目录下的 `data/` 或 `.data/`
- **配置文件**: `docker-compose.yml` 中定义的volumes

---

## 🪟 Windows系统使用Docker

### 步骤1: 安装Docker Desktop

1. **下载Docker Desktop for Windows**
   - 访问: https://www.docker.com/products/docker-desktop/
   - 下载: Docker Desktop for Windows
   - 要求: Windows 10/11 64位，支持WSL 2

2. **安装WSL 2（如果还没有）**
   ```powershell
   # 以管理员身份运行PowerShell
   wsl --install
   
   # 或更新WSL
   wsl --update
   ```

3. **安装Docker Desktop**
   - 运行安装程序
   - 安装完成后重启电脑
   - 启动Docker Desktop

4. **验证安装**
   ```powershell
   docker --version
   # 应该显示: Docker version 24.x.x
   
   docker-compose --version
   # 应该显示: docker-compose version 2.x.x
   ```

### 步骤2: 配置Docker

#### 基本配置

1. **打开Docker Desktop设置**
   - 右键点击系统托盘中的Docker图标
   - 选择 "Settings"

2. **配置资源**
   - General → 启用 "Use WSL 2 based engine"
   - Resources → 分配足够的内存（推荐8GB+）
   - Resources → 分配足够的CPU（推荐4核+）

3. **配置卷挂载**
   - Settings → Resources → File Sharing
   - 添加项目目录: `C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope`

### 步骤3: 使用Docker Compose

#### 启动服务

```powershell
# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 停止服务

```powershell
# 停止所有服务
docker-compose down

# 停止并删除卷（谨慎使用）
docker-compose down -v
```

#### 重启服务

```powershell
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart mongodb
```

### 步骤4: 运行GUI应用（可选）

```powershell
# 使用GUI配置启动
docker-compose -f docker-compose.gui.yml up -d

# 或使用脚本
.\docker\run_gui_container.ps1
```

---

## 🔧 Docker服务管理

### 常用命令

#### 查看服务状态

```powershell
# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 查看Docker Compose服务
docker-compose ps

# 查看服务日志
docker-compose logs [服务名]
docker-compose logs -f [服务名]  # 实时日志
```

#### 启动/停止服务

```powershell
# 启动所有服务
docker-compose up -d

# 启动特定服务
docker-compose up -d mongodb

# 停止所有服务
docker-compose down

# 停止特定服务
docker-compose stop mongodb

# 重启服务
docker-compose restart mongodb
```

#### 数据管理

```powershell
# 查看卷
docker volume ls

# 查看卷详情
docker volume inspect [卷名]

# 备份数据
docker run --rm -v [卷名]:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /data

# 恢复数据
docker run --rm -v [卷名]:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
```

### 服务说明

#### MongoDB服务

**用途**: 存储信号、回测结果、版本管理

**连接信息**:
- 主机: `localhost` 或 `127.0.0.1`
- 端口: `27017` (默认)
- 数据库: `trquant`

**使用示例**:
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['trquant']
```

#### PostgreSQL服务（如果配置）

**用途**: 主数据库，强事务/审计

**连接信息**:
- 主机: `localhost`
- 端口: `5432` (默认)
- 数据库: `trquant`

#### Redis服务（如果配置）

**用途**: 缓存/队列

**连接信息**:
- 主机: `localhost`
- 端口: `6379` (默认)

#### Chroma服务（如果配置）

**用途**: 向量数据库，知识库向量索引

**连接信息**:
- 主机: `localhost`
- 端口: `8000` (默认)

---

## 🔍 本机系统状态检查

### Ubuntu端检查脚本

```bash
#!/bin/bash
# 检查Docker服务状态

echo "=========================================="
echo "Docker服务状态检查"
echo "=========================================="

# 检查Docker是否安装
if command -v docker &> /dev/null; then
    echo "✅ Docker已安装: $(docker --version)"
else
    echo "❌ Docker未安装"
    exit 1
fi

# 检查Docker服务状态
if systemctl is-active --quiet docker; then
    echo "✅ Docker服务运行中"
else
    echo "❌ Docker服务未运行"
    echo "启动命令: sudo systemctl start docker"
fi

# 检查运行的容器
echo ""
echo "运行的容器:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 检查Docker Compose服务
if [ -f "docker-compose.yml" ]; then
    echo ""
    echo "Docker Compose服务:"
    docker-compose ps
fi

# 检查卷
echo ""
echo "Docker卷:"
docker volume ls

echo ""
echo "=========================================="
```

### Windows端检查脚本

```powershell
# 检查Docker服务状态

Write-Host "=========================================="
Write-Host "Docker服务状态检查"
Write-Host "=========================================="

# 检查Docker是否安装
if (Get-Command docker -ErrorAction SilentlyContinue) {
    $dockerVersion = docker --version
    Write-Host "✅ Docker已安装: $dockerVersion"
} else {
    Write-Host "❌ Docker未安装"
    exit 1
}

# 检查Docker Desktop是否运行
$dockerInfo = docker info 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker Desktop运行中"
} else {
    Write-Host "❌ Docker Desktop未运行"
    Write-Host "请启动Docker Desktop"
    exit 1
}

# 检查运行的容器
Write-Host ""
Write-Host "运行的容器:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 检查Docker Compose服务
if (Test-Path "docker-compose.yml") {
    Write-Host ""
    Write-Host "Docker Compose服务:"
    docker-compose ps
}

# 检查卷
Write-Host ""
Write-Host "Docker卷:"
docker volume ls

Write-Host ""
Write-Host "=========================================="
```

---

## 🚀 Windows系统Docker使用流程

### 完整安装和配置流程

#### 步骤1: 安装Docker Desktop

```powershell
# 1. 下载Docker Desktop for Windows
# https://www.docker.com/products/docker-desktop/

# 2. 安装WSL 2（如果还没有）
wsl --install

# 3. 安装Docker Desktop
# 运行下载的安装程序

# 4. 重启电脑

# 5. 启动Docker Desktop
# 从开始菜单启动Docker Desktop
```

#### 步骤2: 配置Docker

```powershell
# 1. 打开Docker Desktop设置
# 右键系统托盘Docker图标 → Settings

# 2. 配置资源
# General → 启用 "Use WSL 2 based engine"
# Resources → 内存: 8GB+
# Resources → CPU: 4核+

# 3. 配置文件共享
# Resources → File Sharing
# 添加: C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope
```

#### 步骤3: 启动Docker服务

```powershell
# 进入项目目录
cd C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope

# 启动所有服务
docker-compose up -d

# 验证服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 步骤4: 验证连接

```powershell
# 测试MongoDB连接
docker exec -it trquant-mongodb mongosh --eval "db.version()"

# 测试Redis连接
docker exec -it trquant-redis redis-cli ping

# 查看服务健康状态
docker-compose ps
```

---

## 🔧 故障排除

### 问题1: Docker Desktop无法启动

**错误**: Docker Desktop启动失败

**解决方案**:
1. 确保WSL 2已安装并更新
   ```powershell
   wsl --update
   wsl --set-default-version 2
   ```

2. 检查Windows功能
   - 启用 "Virtual Machine Platform"
   - 启用 "Windows Subsystem for Linux"

3. 重启电脑

### 问题2: 端口冲突

**错误**: 端口已被占用

**解决方案**:
```powershell
# 查看端口占用
netstat -ano | findstr :27017

# 修改docker-compose.yml中的端口映射
# 例如: "27017:27017" 改为 "27018:27017"
```

### 问题3: 卷挂载失败

**错误**: 卷挂载权限问题

**解决方案**:
1. 在Docker Desktop设置中添加文件共享路径
2. 确保路径使用正斜杠或双反斜杠
   ```yaml
   volumes:
     - C:/Users/Administrator/.cursor/worktrees/TRQuantPro/ope/data:/data
   ```

### 问题4: 容器无法连接

**错误**: 容器间无法通信

**解决方案**:
```powershell
# 检查网络
docker network ls

# 检查容器网络
docker inspect [容器名] | findstr NetworkMode

# 确保使用相同的网络
# 在docker-compose.yml中使用networks配置
```

### 问题5: 数据丢失

**错误**: 容器删除后数据丢失

**解决方案**:
1. 使用命名卷而不是绑定挂载
2. 定期备份数据
   ```powershell
   # 备份MongoDB数据
   docker exec trquant-mongodb mongodump --out /backup
   docker cp trquant-mongodb:/backup ./backup
   ```

---

## 📝 最佳实践

### 1. 数据持久化

- ✅ 使用命名卷存储数据库数据
- ✅ 定期备份重要数据
- ❌ 不要将数据存储在容器内

### 2. 资源管理

- ✅ 合理分配Docker资源（内存、CPU）
- ✅ 定期清理未使用的镜像和容器
  ```powershell
  docker system prune -a
  ```

### 3. 安全配置

- ✅ 使用环境变量管理敏感信息
- ✅ 限制容器网络访问
- ✅ 定期更新Docker镜像

### 4. 开发工作流

- ✅ 开发时使用 `docker-compose up` 启动服务
- ✅ 生产环境使用 `docker-compose up -d` 后台运行
- ✅ 使用 `docker-compose logs` 查看日志

---

## 🎯 快速参考

### Ubuntu端常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 检查状态
docker-compose ps
```

### Windows端常用命令

```powershell
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 检查状态
docker-compose ps
```

---

## 📚 相关文档

- `docs/02_development_guides/MONGODB_SETUP.md` - MongoDB设置指南
- `docs/02_development_guides/DOCKER_GUIDE.md` - Docker详细指南
- `docker-compose.yml` - Docker Compose配置文件
- `packaging/docker/Dockerfile` - Docker镜像定义

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
