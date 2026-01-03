#!/bin/bash
# Docker运行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac



set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant Docker 运行脚本"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker-compose是否安装
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    USE_COMPOSE=true
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
    USE_COMPOSE=true
else
    echo "⚠️  docker-compose未安装，将使用docker build和run"
    USE_COMPOSE=false
fi

# 解析参数
ACTION=${1:-build}
shift || true

case $ACTION in
    build)
        echo "1. 构建Docker镜像..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD build
        else
            docker build -t jqquant:latest .
        fi
        echo "✅ 构建完成"
        ;;
    
    run)
        echo "2. 运行Docker容器..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant "$@"
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest "$@"
        fi
        ;;
    
    test)
        echo "3. 运行测试回测..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python test_backtest.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python test_backtest.py
        fi
        ;;
    
    shell)
        echo "4. 进入容器Shell..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant /bin/bash
        else
            docker run --rm -it \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest /bin/bash
        fi
        ;;
    
    verify)
        echo "5. 验证配置..."
        if [ "$USE_COMPOSE" = true ]; then
            $DOCKER_COMPOSE_CMD run --rm jqquant python verify_config.py
        else
            docker run --rm \
                -v "$SCRIPT_DIR/config:/app/config:ro" \
                -v "$SCRIPT_DIR/results:/app/results" \
                -v "$SCRIPT_DIR/data:/app/data" \
                -v "$SCRIPT_DIR/logs:/app/logs" \
                jqquant:latest python verify_config.py
        fi
        ;;
    
    *)
        echo "用法: $0 {build|run|test|shell|verify} [参数...]"
        echo ""
        echo "命令:"
        echo "  build   - 构建Docker镜像"
        echo "  run     - 运行容器（可传递参数给main.py）"
        echo "  test    - 运行测试回测"
        echo "  shell   - 进入容器Shell"
        echo "  verify  - 验证配置"
        echo ""
        echo "示例:"
        echo "  $0 build"
        echo "  $0 verify"
        echo "  $0 test"
        echo "  $0 run --strategy ma_cross --start 2024-08-01 --end 2024-10-31 --securities 000001.XSHE 600000.XSHG"
        exit 1
        ;;
esac

