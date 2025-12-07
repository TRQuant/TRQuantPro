# Cursor Agent 框架 - 基于 Cursor 内置 AI 能力

## 📋 概述

在 Cursor 开发环境中，我们**不需要集成外部 LLM 客户端**。Cursor 本身就是一个强大的 AI 开发环境，内置了 Claude 等模型。我们应该充分利用 Cursor 的内置能力，通过规则和 Prompt 系统实现多 Agent 协作。

---

## 🎯 设计理念

### 为什么不需要外部客户端？

1. **Cursor 已内置 AI**：Cursor 内置了 Claude Sonnet/Opus 等模型
2. **上下文感知**：Cursor 能理解整个项目代码结构
3. **交互式开发**：实时对话、迭代优化
4. **无缝集成**：在开发环境中完成全部工作

### Agent 在 Cursor 中的实现方式

- **通过 `.cursorrules` 定义 Agent 角色和行为**
- **通过 Prompt 模板实现多 Agent 协作**
- **通过代码检查工具实现规范智能体**
- **通过 Cursor 的命令和上下文实现开发智能体**

---

## 🏗️ Agent 架构（Cursor 原生实现）

### 三层智能体体系

```
┌─────────────────────────────────────────────────────────┐
│          Cursor AI 环境（内置 Claude）                   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Agent 协调层（.cursorrules）             │   │
│  │  - 角色定义                                        │   │
│  │  - 工作流管理                                      │   │
│  │  - 任务分解                                        │   │
│  └──────────────────────────────────────────────────┘   │
│                        │                                  │
│        ┌───────────────┼───────────────┐                 │
│        │               │               │                 │
│  ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐          │
│  │ 架构设计   │  │ 代码生成   │  │ 规范检查   │          │
│  │ Agent     │  │ Agent     │  │ Agent     │          │
│  │           │  │           │  │           │          │
│  │ Prompt    │  │ Prompt    │  │ 工具链    │          │
│  │ 模板      │  │ 模板      │  │ (ruff/    │          │
│  │           │  │           │  │  mypy)    │          │
│  └───────────┘  └───────────┘  └───────────┘          │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent 角色定义（在 Cursor 中实现）

### 1. 架构设计 Agent

**实现方式**：通过 `.cursorrules` 中的 Prompt 模板

**角色定义**：
```markdown
## 架构设计 Agent

当你需要设计新模块或系统架构时，请遵循以下流程：

1. **需求分析**
   - 理解用户需求
   - 分析现有代码结构
   - 识别依赖关系

2. **架构设计**
   - 设计模块结构
   - 定义接口和数据结构
   - 制定开发计划

3. **任务分解**
   - 将大任务分解为小任务
   - 确定优先级
   - 识别依赖关系

**输出格式**：
- 模块结构（目录树）
- 核心类和方法定义
- 接口设计（类型定义）
- 开发任务列表（按优先级）
```

### 2. 代码生成 Agent

**实现方式**：通过 `.cursorrules` 中的代码生成规范

**角色定义**：
```markdown
## 代码生成 Agent

生成代码时，请遵循以下规范：

1. **代码规范**
   - 严格遵循 PEP 8
   - 所有函数必须有类型注解
   - 所有公共函数必须有 docstring（Google 风格）
   - 行长度不超过 100 字符

2. **质量要求**
   - 单一职责原则
   - 函数长度不超过 50 行
   - 完整的错误处理
   - 避免使用 any 类型（TypeScript）

3. **生成流程**
   - 先生成接口定义
   - 再生成实现代码
   - 最后生成测试代码
   - 每步完成后自检
```

### 3. 规范检查 Agent

**实现方式**：通过代码检查工具 + Cursor 规则

**角色定义**：
```markdown
## 规范检查 Agent

在提交代码前，请执行以下检查：

1. **语法检查**：确保代码可以编译/解析
2. **风格检查**：运行 `ruff check .`
3. **类型检查**：运行 `mypy .`
4. **安全扫描**：检查危险函数
5. **性能分析**：检查明显的性能问题

**检查清单**：
- [ ] 语法正确
- [ ] 代码风格符合规范
- [ ] 类型注解完整
- [ ] 无安全风险
- [ ] 性能合理
```

---

## 📝 Cursor 规则集成

### 更新 `.cursorrules`

在 `.cursorrules` 中添加 Agent 工作流：

```markdown
# TRQuant 代码规范化规则
# 基于 Compound Engineering 理念 + AI Agent 协作框架

## 🤖 AI Agent 工作流

### 开发新功能时的 Agent 协作流程

#### 阶段一：架构设计（Architect Agent）

当用户提出新功能需求时：

1. **分析需求**
   - 理解功能目标
   - 分析现有代码结构
   - 识别可复用的模块

2. **设计架构**
   - 设计模块结构（目录树）
   - 定义核心类和接口
   - 确定依赖关系

3. **任务分解**
   - 将功能分解为多个任务
   - 确定任务优先级
   - 识别任务依赖关系

4. **输出架构设计**
   - 模块结构图
   - 接口定义
   - 开发计划

**Prompt 模板**：
```
你是 TRQuant 系统的架构设计师。

## 需求
{用户需求}

## 现有代码结构
{相关代码和模块}

## 任务
请设计架构并分解任务：
1. 模块结构
2. 接口定义
3. 开发计划（按优先级）
```

#### 阶段二：代码生成（Code Generator Agent）

根据架构设计生成代码时：

1. **生成接口定义**
   - 类型定义
   - 接口声明
   - 数据结构

2. **生成实现代码**
   - 遵循代码规范
   - 添加类型注解
   - 添加文档字符串
   - 处理错误情况

3. **生成测试代码**
   - 单元测试
   - 集成测试
   - 边界条件测试

4. **自检代码质量**
   - 检查类型注解
   - 检查文档字符串
   - 检查代码风格
   - 检查逻辑正确性

**Prompt 模板**：
```
你是 TRQuant 系统的代码生成专家。

## 架构设计
{架构设计}

## 任务
实现以下模块：
{模块名称和描述}

## 要求
1. 严格遵循代码规范（见下文）
2. 所有函数必须有类型注解和 docstring
3. 函数长度不超过 50 行
4. 完整的错误处理
5. 生成对应的单元测试

## 代码规范
{代码规范内容}
```

#### 阶段三：规范检查（Quality Checker Agent）

代码生成后，执行规范检查：

1. **语法检查**
   - 确保代码可以解析
   - 检查语法错误

2. **风格检查**
   - 运行 `ruff check .`
   - 修复风格问题

3. **类型检查**
   - 运行 `mypy .`
   - 修复类型错误

4. **安全检查**
   - 检查危险函数（eval, exec 等）
   - 检查安全漏洞

5. **性能检查**
   - 检查明显的性能问题
   - 优化建议

**检查清单**：
```
在提交代码前，请确认：
- [ ] 代码语法正确（可以编译/解析）
- [ ] 运行 `ruff check .` 无错误
- [ ] 运行 `mypy .` 无类型错误
- [ ] 无安全风险（无 eval, exec 等）
- [ ] 性能合理（无明显的性能瓶颈）
- [ ] 所有测试通过
```

### 多 Agent 协作流程

```
用户需求
  ↓
[Architect Agent] 分析需求 → 架构设计 → 任务分解
  ↓
[Code Generator Agent] 生成代码 → 自检质量
  ↓
[Quality Checker Agent] 规范检查 → 修复问题
  ↓
高质量代码
```

---

## 🛠️ 实现细节

### 1. Agent 角色切换

在 Cursor 中，通过不同的 Prompt 前缀来切换 Agent 角色：

```markdown
## 使用 Architect Agent
@architect 请设计 BulletTrade 回测模块的架构

## 使用 Code Generator Agent
@codegen 请实现 BulletTrade 引擎封装

## 使用 Quality Checker Agent
@quality 请检查以下代码的质量
```

### 2. 工作流自动化

在 `.cursorrules` 中定义自动化工作流：

```markdown
## 自动化工作流

当用户说"开发新功能"时：

1. 自动切换到 Architect Agent
2. 分析需求并设计架构
3. 自动切换到 Code Generator Agent
4. 生成代码
5. 自动切换到 Quality Checker Agent
6. 检查代码质量
7. 如果发现问题，返回步骤 4 修复
8. 输出最终代码
```

### 3. 规范智能体（工具链集成）

规范检查通过工具链实现：

```python
# scripts/quality_check.py
"""规范检查脚本

在 Cursor 中可以通过命令调用
"""

import subprocess
import sys

def check_quality():
    """执行全面质量检查"""
    checks = [
        ("语法检查", "python -m py_compile"),
        ("风格检查", "ruff check ."),
        ("类型检查", "mypy ."),
    ]
    
    results = []
    for name, command in checks:
        result = subprocess.run(command.split(), capture_output=True)
        results.append({
            "name": name,
            "passed": result.returncode == 0,
            "output": result.stdout.decode()
        })
    
    return results

if __name__ == "__main__":
    results = check_quality()
    for r in results:
        print(f"{r['name']}: {'✓' if r['passed'] else '✗'}")
    
    if not all(r["passed"] for r in results):
        sys.exit(1)
```

### 4. 开发智能体（Prompt 模板）

开发智能体通过 Prompt 模板实现：

```markdown
## 开发智能体 Prompt 模板

### 架构设计模板
```
你是 TRQuant 系统的架构设计师（Architect Agent）。

## 当前任务
{任务描述}

## 现有代码
{相关代码}

## 要求
1. 分析需求
2. 设计架构
3. 分解任务

请提供详细的架构设计。
```

### 代码生成模板
```
你是 TRQuant 系统的代码生成专家（Code Generator Agent）。

## 架构设计
{架构设计}

## 实现要求
1. 严格遵循代码规范
2. 添加类型注解和文档字符串
3. 处理错误情况
4. 生成单元测试

请生成高质量代码。
```

### 规范检查模板
```
你是 TRQuant 系统的规范检查专家（Quality Checker Agent）。

## 代码
{代码内容}

## 检查要求
1. 语法检查
2. 风格检查
3. 类型检查
4. 安全检查
5. 性能检查

请提供检查报告和改进建议。
```
```

---

## 📋 使用指南

### 在 Cursor 中使用 Agent

#### 1. 开发新功能

```
用户：请开发 BulletTrade 回测模块

Cursor（Architect Agent）：
1. 分析需求
2. 设计架构
3. 输出开发计划

Cursor（Code Generator Agent）：
1. 根据架构生成代码
2. 自检代码质量
3. 生成测试代码

Cursor（Quality Checker Agent）：
1. 检查代码规范
2. 运行工具链检查
3. 提供改进建议
```

#### 2. 代码审查

```
用户：@quality 请检查以下代码

Cursor（Quality Checker Agent）：
1. 运行 ruff check
2. 运行 mypy
3. 检查安全问题
4. 提供改进建议
```

#### 3. 架构设计

```
用户：@architect 请设计多券商接口架构

Cursor（Architect Agent）：
1. 分析需求
2. 设计统一接口
3. 设计适配器模式
4. 输出架构设计
```

---

## 🔧 工具链集成

### 规范检查工具

在 `scripts/` 目录下创建工具脚本：

```python
# scripts/cursor_quality_check.py
"""Cursor 规范检查工具

在 Cursor 中可以通过命令调用
"""

import subprocess
import sys
from pathlib import Path

def run_check(name: str, command: list) -> bool:
    """运行检查命令"""
    print(f"🔍 {name}...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ {name} 通过")
        return True
    else:
        print(f"✗ {name} 失败")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return False

def main():
    """主函数"""
    checks = [
        ("语法检查", ["python", "-m", "py_compile", "core/agents/*.py"]),
        ("风格检查", ["ruff", "check", "core/agents/"]),
        ("类型检查", ["mypy", "core/agents/"]),
    ]
    
    results = []
    for name, command in checks:
        # 跳过不存在的工具
        if command[0] == "ruff" and not Path("/usr/bin/ruff").exists():
            print(f"⚠ {name} 跳过（工具未安装）")
            continue
        
        passed = run_check(name, command)
        results.append(passed)
    
    if not all(results):
        print("\n❌ 部分检查失败，请修复后重试")
        sys.exit(1)
    else:
        print("\n✅ 所有检查通过")

if __name__ == "__main__":
    main()
```

---

## 📊 Agent 协作示例

### 示例：开发 BulletTrade 回测模块

```
用户：请开发 BulletTrade 回测执行模块（bt_run.py）

[Architect Agent]
分析需求 → 设计架构：
- 模块：core/backtest/bt_run.py
- 依赖：BulletTrade, pandas
- 接口：run_backtest(strategy_path, config) -> BacktestResult
- 任务：
  1. 封装 BulletTrade CLI
  2. 实现 Python API
  3. 结果处理

[Code Generator Agent]
生成代码：
```python
# core/backtest/bt_run.py
from typing import Optional, Dict, Any
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_backtest(
    strategy_path: str,
    config: Dict[str, Any],
    output_dir: Optional[str] = None
) -> Dict[str, Any]:
    """执行 BulletTrade 回测
    
    Args:
        strategy_path: 策略文件路径
        config: 回测配置
        output_dir: 输出目录
        
    Returns:
        回测结果
    """
    # 实现...
```

[Quality Checker Agent]
检查代码：
- ✓ 语法正确
- ✓ 类型注解完整
- ✓ 文档字符串完整
- ⚠ 需要添加错误处理
- ⚠ 需要添加单元测试

[Code Generator Agent]
修复问题：
- 添加错误处理
- 生成单元测试

[Quality Checker Agent]
再次检查：
- ✓ 所有检查通过
```

---

## 🎯 优势

### 1. 无需外部依赖
- 直接使用 Cursor 内置 AI
- 无需配置 API 密钥
- 无需管理外部客户端

### 2. 上下文感知
- Cursor 能理解整个项目
- 自动识别代码模式
- 智能建议和补全

### 3. 交互式开发
- 实时对话
- 迭代优化
- 即时反馈

### 4. 工具链集成
- 直接调用 ruff, mypy 等工具
- 自动化质量检查
- 无缝集成到开发流程

---

## 📝 更新现有规则文件

需要更新以下文件以集成 Agent 框架：

1. `.cursorrules` - 添加 Agent 工作流
2. `.cursor-rules-trquant.md` - 添加 Agent 角色定义
3. `scripts/cursor_quality_check.py` - 创建规范检查工具

---

**文档版本**: v1.0  
**创建日期**: 2025-12-07  
**最后更新**: 2025-12-07


