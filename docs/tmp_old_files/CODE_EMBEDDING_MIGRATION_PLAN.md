# 代码嵌入迁移计划

## 📋 概述

将所有文档中的代码块迁移为使用Astro组件嵌入，实现代码与文档分离。

## 🎯 目标

1. **代码独立存储**：所有代码存储在 `code_library/` 目录
2. **文档使用组件**：文档中使用 `<CodeBlockFromFile />` 组件引用代码
3. **自动更新**：代码更新后文档自动显示最新版本
4. **按章节顺序**：按章节顺序系统迁移

## 📝 迁移步骤

### 阶段1：准备代码库结构

```bash
# 创建代码库目录结构
mkdir -p code_library/{001..013}_Chapter*/

# 为每个章节创建小节目录
for chapter in {001..013}_Chapter*; do
    # 根据章节概览创建小节目录
    # 例如：001_Chapter1_System_Overview/1.1/, 1.2/, ...
done
```

### 阶段2：提取代码到文件

使用代码管理工具批量提取：

```bash
python scripts/code_manager.py \
    --action extract \
    --docs-dir extension/AShare-manual/src/pages/ashare-book6 \
    --code-lib-dir code_library \
    --db-config config/database_code_library.json
```

### 阶段3：更新文档使用组件

按章节顺序更新文档：

#### 第1章：系统概述（1.1-1.9）
- [ ] 1.1 项目背景与目标
- [ ] 1.2 系统架构总览
- [ ] 1.3 技术栈选型
- [ ] 1.4 开发历程
- [ ] 1.5 系统开发状态
- [ ] 1.6 系统功能模块
- [ ] 1.7 系统工作流
- [ ] 1.8 系统技术架构
- [ ] 1.9 数据库架构设计

#### 第2章：数据源（2.1-2.4）
- [ ] 2.1 数据源管理
- [ ] 2.2 数据质量检查
- [ ] 2.3 数据更新机制
- [ ] 2.4 数据缓存策略

#### 第3章：市场分析（3.1-3.4）
- [x] 3.1 趋势分析
- [x] 3.2 市场状态判断（部分完成）
- [ ] 3.3 五维评分系统
- [ ] 3.4 MCP工具集成

#### 第4章：主线识别（4.1-4.4）
- [ ] 4.1 主线评分
- [ ] 4.2 主线筛选
- [ ] 4.3 主线引擎
- [ ] 4.4 MCP工具集成

#### 第5章：候选池构建（5.1-5.4）
- [ ] 5.1 股票池管理
- [ ] 5.2 筛选规则
- [ ] 5.3 股票评分
- [ ] 5.4 MCP工具集成

#### 第6章：因子库（6.1-6.5）
- [ ] 6.1 因子计算
- [ ] 6.2 因子管理
- [ ] 6.3 因子优化
- [ ] 6.4 因子流水线
- [ ] 6.5 因子池集成

#### 第7章：策略开发（7.1-7.7）
- [ ] 7.1 策略模板
- [ ] 7.2 策略生成
- [ ] 7.3 策略优化
- [ ] 7.4 策略标准化
- [ ] 7.5 策略测试
- [ ] 7.6 策略部署
- [ ] 7.7 MCP工具集成

#### 第8章：回测验证（8.1-8.8）
- [ ] 8.1 回测框架
- [ ] 8.2 回测分析器
- [ ] 8.3 收益分析
- [ ] 8.4 风险分析
- [ ] 8.5 交易分析
- [ ] 8.6 回测报告
- [ ] 8.7 滚动窗口分析
- [ ] 8.8 优化建议

#### 第9章：平台集成（9.1-9.6）
- [ ] 9.1 PTrade集成
- [ ] 9.2 QMT集成
- [ ] 9.3 策略转换
- [ ] 9.4 实盘部署
- [ ] 9.5 监控管理
- [ ] 9.6 实盘交易管理

#### 第10章：开发指南（10.1-10.13）
- [ ] 10.1 环境搭建
- [ ] 10.2 开发原则
- [ ] 10.3 开发流程
- [ ] 10.4 桌面系统开发
- [ ] 10.5 Cursor扩展开发
- [ ] 10.6 前端开发
- [ ] 10.7 MCP Server开发
- [ ] 10.8 版本发布机制
- [ ] 10.9 MCP Cursor工作流
- [ ] 10.10 RAG知识库开发
- [ ] 10.11 开发方法论
- [ ] 10.12 GUI开发指南
- [ ] 10.13 爬虫开发指南

#### 第11章：用户手册（11.1-11.3）
- [ ] 11.1 快速开始
- [ ] 11.2 GUI指南
- [ ] 11.3 工作流指南

#### 第12章：API参考（12.1-12.3）
- [ ] 12.1 模块API
- [ ] 12.2 数据源API
- [ ] 12.3 配置参考

#### 第13章：附录（A.1-A.4）
- [ ] A.1 术语表
- [ ] A.2 更新日志
- [ ] A.3 贡献指南
- [ ] A.4 参考资料

## 🔧 迁移工具

### 自动迁移脚本

```python
# scripts/migrate_code_to_component.py
"""
自动将文档中的代码块迁移为组件引用
"""
import re
from pathlib import Path

def migrate_doc(md_file: Path, code_library_dir: Path):
    """迁移单个文档"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配代码块
    pattern = r'```python\n(.*?)```'
    
    def replace_code(match):
        code_content = match.group(1).strip()
        
        # 提取函数/类名
        func_match = re.search(r'def\s+(\w+)|class\s+(\w+)', code_content)
        func_name = func_match.group(1) if func_match and func_match.group(1) else \
                   (func_match.group(2) if func_match and func_match.group(2) else None)
        
        if not func_name:
            return match.group(0)  # 无法识别，保留原样
        
        # 生成代码文件路径
        chapter = md_file.parent.name
        section = extract_section(md_file)
        safe_code_id = f"{section}.{func_name}".replace('.', '_')
        code_file = code_library_dir / chapter / section / f"code_{safe_code_id}.py"
        
        # 保存代码文件
        code_file.parent.mkdir(parents=True, exist_ok=True)
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code_content)
        
        # 生成组件引用
        relative_path = code_file.relative_to(Path.cwd())
        return f"""---
import CodeBlockFromFile from '../../../components/CodeBlockFromFile.astro';
---

<CodeBlockFromFile 
  filePath="{relative_path}"
  language="python"
  showDesignPrinciples={{true}}
/>

<!-- 原始代码（保留作为备份）：
```python
{code_content}
```
-->"""
    
    new_content = re.sub(pattern, replace_code, content, flags=re.DOTALL)
    
    # 保存更新后的文档
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
```

## ✅ 验证清单

迁移后需要验证：

- [ ] 代码文件已创建
- [ ] 文档中代码块已替换为组件
- [ ] 组件能正确读取代码文件
- [ ] 设计原理正确显示
- [ ] 代码高亮正常
- [ ] 构建无错误

## 📊 进度跟踪

- **总章节数**：13章
- **总小节数**：约60个小节
- **已完成**：3.2（部分）
- **进行中**：第3章
- **待完成**：其余章节

## 🎯 下一步

1. 完成第3章所有小节的代码迁移
2. 按章节顺序继续迁移
3. 建立代码更新流程
4. 建立代码审查机制

