# docs目录整理方案

## 问题分析

### 1. 主要问题
- **docs/docs/ 目录 (180M)** - 重复嵌套结构，与docs根目录内容重复
- **根目录散乱文件 (404个)** - 大量文件未分类，应该归类到相应子目录
- **ExtentionDev目录** - 应该合并到 `02_development_guides/ExtentionDev/`
- **09_legacy目录 (14M)** - 包含备份和过时文件，需要审查清理
- **Ptrade_coding目录 (11M)** - 应该合并到 `04_platform_integration/`
- **大量重复文件名** - 同一文件名出现在多个目录

### 2. 目录结构目标

```
docs/
├── 01_architecture/          # 架构设计文档
├── 02_development_guides/    # 开发指南（包含ExtentionDev子目录）
├── 03_modules/               # 模块文档
├── 04_platform_integration/  # 平台集成（包含Ptrade_coding内容）
├── 05_reference_books/       # 参考书籍
├── 06_testing_reports/       # 测试报告
├── 07_workflow/              # 工作流程
├── 08_ai_tools/              # AI工具
├── 09_legacy/                # 遗留文件（清理后的精简版）
├── MUST_READ/                # 必读文档
├── knowledge_base/           # 知识库
├── joinquant_kb_comprehensive/  # JoinQuant知识库
├── joinquant_crawled/        # JoinQuant爬取数据
├── jqdata_crawled/           # JQData爬取数据
├── HMM/                      # HMM相关
├── strategy_kb/              # 策略知识库
└── README.md                 # 文档索引

删除：
- docs/docs/ (重复目录)
- ExtentionDev/ (合并到02_development_guides/)
- Ptrade_coding/ (合并到04_platform_integration/)
```

## 整理步骤

### 阶段1: 备份和准备
1. 确认docs (backup)已清理
2. 创建当前状态快照

### 阶段2: 处理重复目录
1. **删除 docs/docs/ 目录** (180M，完全重复)
   - 如果docs/docs/中有更新版本的文件，需要先对比
   
2. **合并 ExtentionDev/ → 02_development_guides/ExtentionDev/**
   - 如果目标位置已存在，对比保留最新版本
   
3. **合并 Ptrade_coding/ → 04_platform_integration/Ptrade_coding/**
   - 如果目标位置已存在，对比保留最新版本

### 阶段3: 整理根目录散乱文件
将根目录下的文件按内容分类移动到相应目录：

- **架构相关** → `01_architecture/`
  - ARCHITECTURE*.md, DATA_ANALYSIS_ARCHITECTURE.md, DESIGN.md 等
  
- **开发指南相关** → `02_development_guides/`
  - INSTALLATION.md, DEVELOPMENT*.md, PROJECT*.md, CURSOR*.md, mcp_setup_guide.md 等
  
- **模块相关** → `03_modules/`
  - CANDIDATE_POOL*.md, FACTOR*.md, MARKET_TREND*.md, DATA_SOURCE*.md 等
  
- **平台集成相关** → `04_platform_integration/`
  - PTRADE*.md, QMT*.md, QUANTCONNECT*.md, ALLTICK*.md, AKSHARE*.md 等
  
- **JQData相关** → 根目录或新建 `jqdata/` 目录
  - JQDATA*.md, JOINQUANT*.md 等
  
- **知识库相关** → 相应知识库目录
  - KB_*.md → knowledge_base/ 或相关目录
  
- **工作流程相关** → `07_workflow/`
  - WORKFLOW*.md, MCP_WORKFLOW*.md, STANDARD*.md 等
  
- **AI工具相关** → `08_ai_tools/`
  - AI_MODEL*.md, AUTO_COMMIT_GUIDE.md, chat_history_backup.md 等
  
- **Git相关** → `02_development_guides/` 或新建 `git/` 子目录
  - GIT_*.md, GIT_SETUP*.md 等
  
- **过时/临时文件** → `09_legacy/`
  - 多次重复的CODE_EMBEDDING*.md (很多版本), 过时的状态报告等

### 阶段4: 清理09_legacy
1. 审查09_legacy/backups/中的备份文件
2. 保留有价值的备份，删除过时的
3. 整理duplicates目录（如果存在）

### 阶段5: 处理重复文件
对于同名文件，保留最新版本或最完整版本：
- 优先保留分类目录中的版本（如02_development_guides/中的版本）
- 删除根目录中的重复版本
- 如有冲突，手动审查决定

### 阶段6: 统一命名和索引
1. 更新README.md作为文档索引
2. 统一文件命名规范
3. 清理空目录

## 注意事项

1. **执行前确认**: 每个步骤都需要确认后再执行
2. **保留有价值内容**: 不要删除可能有用的文档
3. **版本对比**: 合并时对比文件内容，保留最新/最完整版本
4. **Git状态**: 整理后需要重新git add，确认更改

## 预期结果

- docs目录结构清晰，文件分类明确
- 删除重复文件，减少存储占用
- 提高文档查找效率
- 统一的文档组织结构

