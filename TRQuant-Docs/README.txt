TRQuant-Docs 工作区
==================

工作区说明
----------
这是 TRQuant 文档维护工作区，专门用于文档的创建、编辑和维护。

工作区用途
----------
- 文档创建和维护
- Markdown 文档编辑
- 用户手册编写
- API 文档生成
- 开发指南编写

重要规则
--------

Composer 使用规则
-----------------
完全禁用 Composer

原因：
- 文档文件通常很大（>1000行）
- Markdown 文件的 diff 渲染复杂
- Composer 处理大文档容易超时

工作流程
--------
使用 Chat 模式：
1. 使用 Chat 生成文档内容
2. 手动创建/覆盖文件
3. 保存文件
4. 使用 Git 管理版本

禁止使用 Composer：
- 不要用 Composer 生成文档
- 不要用 Composer 编辑大文档
- 不要用 Composer 批量修改文档

目录结构
--------
TRQuant-Docs/
├── docs/                    # 所有文档
│   ├── 02_development_guides/  # 开发指南
│   ├── 09_legacy/              # 历史文档
│   └── ...
├── extension/
│   └── AShare-manual/      # A股手册
├── .cursor/                 # Cursor 配置
└── README.txt              # 本文件

配置说明
--------
Cursor 配置：
在 .cursor/workflow_guidelines.txt 中明确：
- Composer: 禁用
- Chat: 可用
- 文件大小限制: 无（但建议拆分大文件）

最佳实践
--------
1. 文档拆分：大文档（>1000行）拆分为多个小文档
2. 版本管理：使用 Git 管理文档版本
3. 手动保存：生成型内容手动落盘，不使用 Composer
4. 定期清理：删除过时文档，保持文档库整洁

相关工作区
----------
- TRQuant（代码开发）：/home/taotao/dev/QuantTest/TRQuant/
- TRQuant-Scripts（脚本生成）：/home/taotao/dev/QuantTest/TRQuant-Scripts/

创建时间: 2025-12-15
目的: 物理隔离文档，避免 Composer 性能问题
