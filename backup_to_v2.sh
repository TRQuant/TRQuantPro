#!/bin/bash
# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v






# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v




# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v

# -*- coding: utf-8 -*-
# JQQuant_V2 备份脚本
# 用于将当前代码备份到JQQuant_V2仓库

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "JQQuant_V2 备份脚本"
echo "=========================================="
echo ""

# 检查git状态
echo "1. 检查git状态..."
git status --short

# 询问是否提交更改
read -p "是否提交所有更改到git? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 添加所有更改
    echo "2. 添加所有更改..."
    git add -A
    
    # 提交
    read -p "请输入提交信息 (默认: 备份更新): " commit_msg
    commit_msg=${commit_msg:-备份更新}
    echo "3. 提交更改: $commit_msg"
    git commit -m "$commit_msg"
else
    echo "跳过提交，直接推送现有提交..."
fi

# 推送到origin
echo ""
echo "4. 推送到origin仓库..."
if git push origin master; then
    echo "✅ 推送到origin成功"
else
    echo "❌ 推送到origin失败"
    exit 1
fi

# 推送到backup (JQQuant_V2)
echo ""
echo "5. 推送到backup仓库 (JQQuant_V2)..."
if git push backup master; then
    echo "✅ 推送到JQQuant_V2成功"
else
    echo "❌ 推送到JQQuant_V2失败"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ 备份完成！"
echo "=========================================="
echo ""
echo "远程仓库:"
git remote -v














