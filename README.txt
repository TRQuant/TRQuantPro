TRQuant 主工作区
===============

工作区说明
----------
这是 TRQuant 核心代码开发工作区，用于核心代码的开发、维护和优化。

工作区用途
----------
- 核心代码开发
- MCP 服务器开发
- GUI 开发
- VS Code 扩展开发
- 策略和回测系统开发

重要规则
--------

Composer 使用规则
-----------------
✅ 可用，但仅用于小改（<50行变更）

可以使用 Composer：
- ✅ 分析已有代码（只读）
- ✅ 小范围修改（<50行变更）
- ✅ 重构已有函数（<100行）
- ✅ 修复 bug（<30行）

禁止使用 Composer：
- ❌ 生成新文件
- ❌ 大范围修改（>100行变更）
- ❌ 批量生成代码
- ❌ 处理 Markdown 文档
- ❌ 处理大文件（>1000行）

工作流程
--------
代码开发流程：
1. 使用 Composer 分析代码
2. 使用 Composer 小范围修改（<50行变更）
3. 使用 Chat + 手动保存（大范围修改）
4. ❌ 不使用 Composer 生成新文件

目录结构
--------
TRQuant/
├── core/              # 核心代码
├── mcp_servers/       # MCP 服务器
├── gui/               # GUI 代码
├── extension/         # VS Code 扩展
├── .cursor/           # Cursor 配置
└── README.txt         # 本文件

配置说明
--------
Cursor 配置：
在 .cursor/workflow_guidelines.md 中明确：
- Composer: 可用（只做小改 <50行）
- Chat: 可用（生成新文件、大范围修改）
- 文件大小限制: 建议 < 1000行

最佳实践
--------
1. 保持文件大小合理（<1000行）
2. 使用模块化设计，拆分大文件
3. 小改动优先使用 Composer
4. 大改动使用 Chat + 手动保存

相关工作区
----------
- TRQuant-Docs（文档维护）：/home/taotao/dev/QuantTest/TRQuant-Docs/
- TRQuant-Scripts（脚本生成）：/home/taotao/dev/QuantTest/TRQuant-Scripts/

创建时间: 2025-12-15
目的: 核心代码开发，避免 Composer 性能问题
