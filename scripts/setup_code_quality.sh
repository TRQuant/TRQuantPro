#!/bin/bash
# TRQuant 代码质量工具安装脚本

set -e

echo "=========================================="
echo "TRQuant 代码质量工具安装"
echo "=========================================="
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查 Node.js 环境
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "项目根目录: $PROJECT_ROOT"
echo ""

# 检查并激活虚拟环境
if [ -d "venv" ]; then
    echo "发现虚拟环境，激活中..."
    source venv/bin/activate
    echo "✓ 虚拟环境已激活"
elif [ -d ".venv" ]; then
    echo "发现虚拟环境，激活中..."
    source .venv/bin/activate
    echo "✓ 虚拟环境已激活"
else
    echo "未找到虚拟环境，创建中..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虚拟环境已创建并激活"
fi

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Python 工具安装
echo ""
echo "安装 Python 代码质量工具..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
else
    pip install black ruff mypy pytest pytest-cov
    echo "创建 requirements-dev.txt..."
    pip freeze | grep -E "(black|ruff|mypy|pytest)" > requirements-dev.txt || true
fi

# TypeScript 工具安装
echo ""
echo "安装 TypeScript 代码质量工具..."
cd extension
if [ -f "package.json" ]; then
    npm install --save-dev prettier eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
else
    echo "警告: extension/package.json 不存在"
fi

cd "$PROJECT_ROOT"

# 创建配置文件
echo ""
echo "创建配置文件..."

# Black 配置
cat > pyproject.toml << 'EOF'
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP"]
ignore = ["E501"]  # 行长度由 black 处理

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
EOF

# Prettier 配置
cat > extension/.prettierrc << 'EOF'
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
EOF

# ESLint 配置
cat > extension/.eslintrc.json << 'EOF'
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module"
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "warn",
    "@typescript-eslint/explicit-function-return-type": "off",
    "no-console": "off"
  }
}
EOF

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "使用方法："
echo ""
echo "Python 代码格式化："
echo "  black ."
echo ""
echo "Python 代码检查："
echo "  ruff check ."
echo ""
echo "Python 类型检查："
echo "  mypy ."
echo ""
echo "TypeScript 代码格式化："
echo "  cd extension && npx prettier --write ."
echo ""
echo "TypeScript 代码检查："
echo "  cd extension && npx eslint ."
echo ""

