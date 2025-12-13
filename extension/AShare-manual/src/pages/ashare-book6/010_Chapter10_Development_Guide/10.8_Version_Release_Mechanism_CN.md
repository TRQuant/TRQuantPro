---
title: "10.8 版本与发布机制"
description: "深入解析TRQuant版本管理与发布机制，包括版本号规范、版本更新流程、变更日志管理、发布流程、依赖管理等核心技术，为项目版本管理提供完整的开发指导"
lang: "zh-CN"
layout: "/src/layouts/HandbookLayout.astro"
currentBook: "ashare-book6"
updateDate: "2025-12-12"
---

# 📦 10.8 版本与发布机制

> **核心摘要：**
> 
> 本节系统介绍TRQuant版本管理与发布机制，包括版本号规范、版本更新流程、变更日志管理、发布流程、依赖管理等核心技术。通过理解版本与发布机制的完整方法，帮助开发者掌握项目的版本管理和发布流程，确保项目的可追溯性和可维护性。

版本管理是软件开发的重要环节，TRQuant采用语义化版本控制（Semantic Versioning），通过版本号、变更日志、Git标签等方式管理项目版本。

## 📋 章节概览

<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const headerOffset = 100;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
  }
}
</script>

<div class="section-overview">
  <div class="section-item" onclick="scrollToSection('section-10-8-1')">
    <h4>🔢 10.8.1 版本号规范</h4>
    <p>语义化版本、版本号格式、版本类型、版本递增规则</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-8-2')">
    <h4>🔄 10.8.2 版本更新流程</h4>
    <p>版本文件、版本更新脚本、自动版本管理、版本验证</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-8-3')">
    <h4>📝 10.8.3 变更日志管理</h4>
    <p>CHANGELOG格式、变更分类、变更记录、变更审核</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-8-4')">
    <h4>🚀 10.8.4 发布流程</h4>
    <p>发布准备、发布检查、Git标签、发布文档、发布通知</p>
  </div>
  <div class="section-item" onclick="scrollToSection('section-10-8-5')">
    <h4>📦 10.8.5 依赖管理</h4>
    <p>依赖版本、依赖更新、依赖锁定、依赖审计</p>
  </div>
</div>

## 🎯 学习目标

通过本节学习，您将能够：

- **理解版本号规范**：掌握语义化版本控制的基本规则
- **执行版本更新**：掌握版本更新的流程和工具
- **管理变更日志**：掌握变更日志的编写和维护方法
- **执行发布流程**：掌握完整的发布流程和检查清单
- **管理依赖版本**：掌握依赖版本的管理和更新方法

## 📚 核心概念

### 语义化版本（SemVer）

- **格式**：`MAJOR.MINOR.PATCH`（如 `2.0.0`）
- **MAJOR**：不兼容的API修改
- **MINOR**：向后兼容的功能新增
- **PATCH**：向后兼容的问题修复

### 版本文件

- **VERSION**：主版本文件（项目根目录）
- **package.json**：扩展版本（extension/package.json）
- **pyproject.toml**：Python包版本（如适用）

### 发布流程

- **开发阶段**：功能开发、测试、代码审查
- **发布准备**：版本更新、变更日志、文档更新
- **发布执行**：Git标签、构建、部署
- **发布后**：通知、监控、反馈收集

<h2 id="section-10-8-1">🔢 10.8.1 版本号规范</h2>

TRQuant采用语义化版本控制（Semantic Versioning），版本号格式为 `MAJOR.MINOR.PATCH`。

### 版本号格式

```
MAJOR.MINOR.PATCH
  │     │     │
  │     │     └─ 补丁版本（Bug修复，向后兼容）
  │     └─────── 次版本（新功能，向后兼容）
  └───────────── 主版本（重大变更，可能不兼容）
```

### 版本类型

#### 主版本（MAJOR）

主版本号递增的情况：

- **不兼容的API修改**：移除或修改现有API
- **架构重大变更**：系统架构的重大调整
- **数据格式变更**：数据库结构或文件格式变更

示例：`2.0.0` → `3.0.0`

#### 次版本（MINOR）

次版本号递增的情况：

- **新功能添加**：新增功能模块或API
- **功能增强**：现有功能的改进和优化
- **向后兼容**：不影响现有功能的使用

示例：`2.0.0` → `2.1.0`

#### 补丁版本（PATCH）

补丁版本号递增的情况：

- **Bug修复**：修复已知问题
- **性能优化**：性能改进（不影响功能）
- **文档更新**：文档修正和补充

示例：`2.0.0` → `2.0.1`

### 版本递增规则

```python
# core/version.py
def increment_version(part="patch"):
    """
    递增版本号
    
    Args:
        part: 版本部分（"major", "minor", "patch"）
    
    Returns:
        新版本号
    """
    version_file = Path(__file__).parent.parent / "VERSION"
    
    if not version_file.exists():
        current_version = "2.0.0"
    else:
        current_version = version_file.read_text().strip()
    
    major, minor, patch = map(int, current_version.split('.'))
    
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"无效的版本部分: {part}")
    
    new_version = f"{major}.{minor}.{patch}"
    
    # 更新版本文件
    version_file.write_text(new_version + "\n")
    
    return new_version
```

<h2 id="section-10-8-2">🔄 10.8.2 版本更新流程</h2>

版本更新流程包括版本文件管理、版本更新脚本、自动版本管理等。

### 版本文件

版本号存储在 `VERSION` 文件中：

```bash
# 查看当前版本
cat VERSION
# 输出: 2.0.0
```

### 版本更新脚本

#### Python脚本

```python
# scripts/version_bump.py
#!/usr/bin/env python3
"""版本号更新脚本"""
import sys
from pathlib import Path
from core.version import increment_version

def main():
    if len(sys.argv) < 2:
        print("用法: python version_bump.py [major|minor|patch]")
        sys.exit(1)
    
    part = sys.argv[1]
    if part not in ["major", "minor", "patch"]:
        print(f"无效的版本部分: {part}")
        sys.exit(1)
    
    old_version = Path("VERSION").read_text().strip()
    new_version = increment_version(part)
    
    print(f"版本更新: {old_version} → {new_version}")
    
    # 更新package.json（如适用）
    import json
    package_json = Path("extension/package.json")
    if package_json.exists():
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['version'] = new_version
        with open(package_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 已更新 extension/package.json")

if __name__ == "__main__":
    main()
```

#### Shell脚本

```bash
# scripts/version_bump.sh
#!/bin/bash
# 版本号更新脚本

VERSION_FILE="VERSION"
PART=${1:-patch}  # 默认patch

if [ ! -f "$VERSION_FILE" ]; then
    echo "2.0.0" > "$VERSION_FILE"
fi

CURRENT_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')
IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

case $PART in
    major)
        MAJOR=$((MAJOR + 1))
        MINOR=0
        PATCH=0
        ;;
    minor)
        MINOR=$((MINOR + 1))
        PATCH=0
        ;;
    patch)
        PATCH=$((PATCH + 1))
        ;;
    *)
        echo "无效的版本部分: $PART"
        exit 1
        ;;
esac

NEW_VERSION="$MAJOR.$MINOR.$PATCH"
echo "$NEW_VERSION" > "$VERSION_FILE"

echo "版本更新: $CURRENT_VERSION → $NEW_VERSION"
```

### 自动版本管理

#### Git Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
# 检查VERSION文件是否已更新

VERSION_FILE="VERSION"
STAGED_VERSION=$(git diff --cached -- "$VERSION_FILE" | grep "^+" | grep -v "^+++" | sed 's/^+//')

if [ -n "$STAGED_VERSION" ]; then
    echo "✅ 检测到版本更新: $STAGED_VERSION"
    
    # 验证版本格式
    if ! echo "$STAGED_VERSION" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+$'; then
        echo "❌ 版本格式错误: $STAGED_VERSION"
        exit 1
    fi
fi
```

### 版本验证

```python
# core/version.py
import re
from pathlib import Path

def validate_version(version: str) -> bool:
    """验证版本号格式"""
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version))

def get_version() -> str:
    """获取当前版本号"""
    version_file = Path(__file__).parent.parent / "VERSION"
    
    if version_file.exists():
        version = version_file.read_text().strip()
        if validate_version(version):
            return version
    
    return "2.0.0"  # 默认版本
```

<h2 id="section-10-8-3">📝 10.8.3 变更日志管理</h2>

变更日志（CHANGELOG）记录每个版本的变更内容，帮助用户了解版本更新。

### CHANGELOG格式

```markdown
# 变更日志

所有重要的变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 新增功能A
- 新增功能B

### 变更
- 优化功能C的性能

### 修复
- 修复Bug X
- 修复Bug Y

## [2.1.0] - 2025-12-12

### 新增
- 新增市场状态分析功能
- 新增投资主线识别模块

### 变更
- 优化因子计算性能
- 改进策略生成逻辑

### 修复
- 修复数据源连接问题
- 修复回测结果展示错误

## [2.0.0] - 2025-11-30

### 新增
- 初始版本发布
- 核心功能模块
```

### 变更分类

#### 新增（Added）

- 新功能、新模块、新API
- 新增配置选项
- 新增依赖项

#### 变更（Changed）

- 现有功能的改进
- API的向后兼容变更
- 性能优化

#### 废弃（Deprecated）

- 即将移除的功能
- 不推荐使用的API

#### 移除（Removed）

- 已移除的功能
- 已废弃的API

#### 修复（Fixed）

- Bug修复
- 安全问题修复

#### 安全（Security）

- 安全漏洞修复

### 变更记录工具

```python
# scripts/changelog_helper.py
#!/usr/bin/env python3
"""变更日志辅助工具"""
from pathlib import Path
from datetime import datetime
from core.version import get_version

def add_changelog_entry(category: str, description: str):
    """添加变更日志条目"""
    changelog_file = Path("CHANGELOG.md")
    
    if not changelog_file.exists():
        # 创建初始CHANGELOG
        changelog_file.write_text("""# 变更日志

所有重要的变更都会记录在此文件中。

## [未发布]

""")
    
    content = changelog_file.read_text(encoding='utf-8')
    
    # 在"## [未发布]"部分添加条目
    if "## [未发布]" in content:
        entry = f"- {description}\n"
        category_section = f"### {category}\n"
        
        if category_section in content:
            # 在现有分类下添加
            idx = content.find(category_section) + len(category_section)
            content = content[:idx] + entry + content[idx:]
        else:
            # 添加新分类
            idx = content.find("## [未发布]") + len("## [未发布]")
            content = content[:idx] + "\n\n" + category_section + entry + content[idx:]
    
    changelog_file.write_text(content, encoding='utf-8')
    print(f"✅ 已添加变更日志: [{category}] {description}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        add_changelog_entry(sys.argv[1], sys.argv[2])
    else:
        print("用法: python changelog_helper.py [类别] [描述]")
        print("类别: Added, Changed, Deprecated, Removed, Fixed, Security")
```

<h2 id="section-10-8-4">🚀 10.8.4 发布流程</h2>

发布流程包括发布准备、发布检查、Git标签、发布文档等步骤。

### 发布准备

#### 发布检查清单

```markdown
## 发布检查清单

### 代码质量
- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 无已知严重Bug
- [ ] 代码风格检查通过

### 文档
- [ ] README更新
- [ ] CHANGELOG更新
- [ ] API文档更新
- [ ] 用户手册更新

### 版本管理
- [ ] 版本号已更新
- [ ] 版本号格式正确
- [ ] 所有相关文件版本号已同步

### 构建与测试
- [ ] 构建成功
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 性能测试通过
```

### 发布脚本

```bash
#!/bin/bash
# scripts/release.sh
# 发布脚本

set -e

VERSION_FILE="VERSION"
CURRENT_VERSION=$(cat "$VERSION_FILE" | tr -d '[:space:]')

echo "🚀 准备发布版本: v$CURRENT_VERSION"

# 1. 检查工作区是否干净
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ 工作区不干净，请先提交或暂存所有变更"
    exit 1
fi

# 2. 运行测试
echo "🧪 运行测试..."
python -m pytest tests/ || {
    echo "❌ 测试失败"
    exit 1
}

# 3. 构建
echo "🔨 构建项目..."
npm run build || {
    echo "❌ 构建失败"
    exit 1
}

# 4. 创建Git标签
echo "🏷️  创建Git标签: v$CURRENT_VERSION"
git tag -a "v$CURRENT_VERSION" -m "Release v$CURRENT_VERSION"

# 5. 推送标签
echo "📤 推送标签..."
git push origin "v$CURRENT_VERSION"

# 6. 更新CHANGELOG
echo "📝 更新CHANGELOG..."
# 将"## [未发布]"改为"## [$CURRENT_VERSION] - $(date +%Y-%m-%d)"
sed -i "s/## \[未发布\]/## [$CURRENT_VERSION] - $(date +%Y-%m-%d)/" CHANGELOG.md

# 7. 提交CHANGELOG更新
git add CHANGELOG.md
git commit -m "chore: release v$CURRENT_VERSION"
git push origin main

echo "✅ 发布完成: v$CURRENT_VERSION"
```

### Git标签

```bash
# 创建带注释的标签
git tag -a v2.1.0 -m "Release v2.1.0: 新增市场状态分析功能"

# 推送标签
git push origin v2.1.0

# 查看所有标签
git tag -l

# 查看标签详情
git show v2.1.0
```

### 发布文档

```markdown
# 发布说明 v2.1.0

## 发布日期
2025-12-12

## 主要变更

### 新增功能
- 市场状态分析：支持risk_on/risk_off/neutral判断
- 投资主线识别：自动识别当前市场投资主线
- 因子推荐：基于市场状态推荐量化因子

### 功能改进
- 优化因子计算性能，提升50%
- 改进策略生成逻辑，支持更多策略风格

### Bug修复
- 修复数据源连接超时问题
- 修复回测结果展示错误

## 升级指南

1. 更新代码：`git pull origin main`
2. 更新依赖：`pip install -r requirements.txt`
3. 重启服务：`python TRQuant.py`

## 已知问题

- 暂无

## 致谢

感谢所有贡献者的支持！
```

<h2 id="section-10-8-5">📦 10.8.5 依赖管理</h2>

依赖管理包括依赖版本锁定、依赖更新、依赖审计等。

### 依赖版本

#### Python依赖

```txt
# requirements.txt
pandas==2.1.4
numpy==1.26.2
langchain==0.1.0
chromadb==0.4.18
rank-bm25==0.2.2
sentence-transformers==2.2.2
```

#### Node.js依赖

```json
{
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/node": "^20.x",
    "@types/vscode": "^1.85.0",
    "typescript": "^5.x",
    "webpack": "^5.x"
  }
}
```

### 依赖更新

#### 检查过时依赖

```bash
# Python
pip list --outdated

# Node.js
npm outdated
```

#### 更新依赖

```bash
# Python - 更新单个包
pip install --upgrade pandas

# Python - 更新所有包
pip install --upgrade -r requirements.txt

# Node.js - 更新单个包
npm update axios

# Node.js - 更新所有包
npm update
```

### 依赖锁定

#### Python

```bash
# 生成锁定文件
pip freeze > requirements.lock

# 使用锁定文件安装
pip install -r requirements.lock
```

#### Node.js

```bash
# 生成package-lock.json
npm install

# 使用锁定文件安装
npm ci
```

### 依赖审计

```bash
# Python - 安全检查
pip-audit

# Node.js - 安全检查
npm audit

# Node.js - 自动修复
npm audit fix
```

## 🔗 相关章节

- **10.1 环境搭建**：了解依赖安装和环境配置
- **10.3 开发工作流**：了解开发流程和代码提交
- **第1章：系统概述**：了解系统整体架构

## 💡 关键要点

1. **版本号规范**：采用语义化版本控制，格式为MAJOR.MINOR.PATCH
2. **版本更新**：使用脚本自动化版本更新流程
3. **变更日志**：遵循Keep a Changelog格式，分类记录变更
4. **发布流程**：完整的发布检查清单和发布脚本
5. **依赖管理**：锁定依赖版本，定期更新和审计

## 🔮 总结与展望

<div class="summary-outlook">
  <h3>本节回顾</h3>
  <p>本节系统介绍了版本与发布机制，包括版本号规范、版本更新流程、变更日志管理、发布流程、依赖管理等核心技术。通过理解版本与发布机制的完整方法，帮助开发者掌握项目的版本管理和发布流程。</p>
  
  <h3>下节预告</h3>
  <p>掌握了版本与发布机制后，下一节将介绍MCP × Cursor × 工具链联用规范，包括MCP与Cursor的集成、工具链配置、工作流设计等。通过理解工具链联用规范，帮助开发者掌握MCP、Cursor和工具链的协同使用方法。</p>
  
  <a href="/ashare-book6/010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN" class="next-section">
    继续学习：10.9 MCP × Cursor × 工具链联用规范 →
  </a>
</div>

> **适用版本**: v1.0.0+  
> **最后更新**: 2025-12-12

