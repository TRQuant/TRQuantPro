# 📚 PDF语言版本生成指南

## 🎯 问题背景

当前项目结构中，中文版(`_CN.md`)和英文版(`_EN.md`)文件存在于同一文件夹中。传统的PDF生成会包含所有文件，无法按语言分别生成PDF。

## 🔧 解决方案

### 1. 新增语言过滤PDF生成器

**文件位置**: `scripts/astro-pdf-generator-lang.mjs`

**核心功能**:
- 根据文件名后缀(`_CN.md` 或 `_EN.md`)过滤文件
- 按章节顺序自动排序
- 支持单页、章节、整册PDF生成
- 自动合并多个PDF文件

### 2. PowerShell便捷脚本

**文件位置**: `scripts/generate-pdf-by-language.ps1`

**功能特点**:
- 简化的命令行接口
- 自动环境检查
- 自动启动开发服务器
- 彩色输出和进度显示

## 📋 使用方法

### 方法一：PowerShell脚本（推荐）

```powershell
# 生成所有书籍的中文版PDF
.\scripts\generate-pdf-by-language.ps1 -Language CN -Type all

# 生成book1的英文版PDF
.\scripts\generate-pdf-by-language.ps1 -Language EN -Type book -Path book1

# 生成第一章的中文版PDF
.\scripts\generate-pdf-by-language.ps1 -Language CN -Type chapter -Path book1/001_Chapter1

# 生成单个页面的英文版PDF
.\scripts\generate-pdf-by-language.ps1 -Language EN -Type single -URL /book1/001_Chapter1/1.1_xxx_EN
```

### 方法二：npm脚本

```bash
# 生成所有书籍的中文版PDF
npm run pdf:lang:all CN

# 生成book1的英文版PDF
npm run pdf:lang:book book1 EN

# 生成第一章的中文版PDF
npm run pdf:lang:chapter book1/001_Chapter1 CN

# 生成单个页面的英文版PDF
npm run pdf:lang:single /book1/001_Chapter1/1.1_xxx_EN EN
```

### 方法三：直接调用Node.js脚本

```bash
# 生成所有书籍的中文版PDF
node scripts/astro-pdf-generator-lang.mjs all CN

# 生成book1的英文版PDF
node scripts/astro-pdf-generator-lang.mjs book book1 EN

# 生成第一章的中文版PDF
node scripts/astro-pdf-generator-lang.mjs chapter book1/001_Chapter1 CN

# 生成单个页面的英文版PDF
node scripts/astro-pdf-generator-lang.mjs single /book1/001_Chapter1/1.1_xxx_EN EN
```

## 📁 输出文件结构

```
dist/pdf/
├── book1_CN_Complete.pdf          # book1中文完整版
├── book1_EN_Complete.pdf          # book1英文完整版
├── book2_CN_Complete.pdf          # book2中文完整版
├── book2_EN_Complete.pdf          # book2英文完整版
├── 001_Chapter1_CN_Complete.pdf   # 第一章中文版
├── 001_Chapter1_EN_Complete.pdf   # 第一章英文版
└── 1.1_xxx_CN.pdf                # 单个页面PDF
```

## 🔍 文件过滤逻辑

### 语言识别规则

1. **中文文件**: 文件名包含 `_CN.md`
   - `1.1_Self_Awareness_and_Investment_Wisdom_CN.md`
   - `001_Chapter1_Know_Yourself_and_the_World_CN.md`

2. **英文文件**: 文件名包含 `_EN.md`
   - `1.1_Self_Awareness_and_Investment_Wisdom_EN.md`
   - `001_Chapter1_Know_Yourself_and_the_World_EN.md`

### 排序规则

1. **章节排序**: 按数字顺序排序
   - `1.1_xxx_CN.md` → `1.2_xxx_CN.md` → `1.3_xxx_CN.md`
   - `001_Chapter1_CN.md` → `002_Chapter2_CN.md`

2. **小节排序**: 按小数点数字排序
   - `1.1_xxx_CN.md` → `1.2_xxx_CN.md` → `1.10_xxx_CN.md`

## ⚙️ 环境要求

### 必需软件
- Node.js (v16+)
- npm 或 yarn
- PowerShell (Windows) 或 bash (Linux/Mac)

### 必需依赖
```json
{
  "puppeteer": "^24.16.0",
  "pdf-lib": "^1.17.1",
  "glob": "^10.3.0"
}
```

### 开发服务器
- 确保Astro开发服务器运行在 `http://localhost:4321`
- PowerShell脚本会自动启动开发服务器

## 🚀 快速开始

### 1. 安装依赖
```bash
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```

### 3. 生成PDF
```powershell
# 生成中文版PDF
.\scripts\generate-pdf-by-language.ps1 -Language CN -Type all

# 生成英文版PDF
.\scripts\generate-pdf-by-language.ps1 -Language EN -Type all
```

## 🔧 故障排除

### 常见问题

#### 1. "开发服务器未运行"
**解决方案**:
```bash
npm run dev
```

#### 2. "未找到指定语言的文件"
**检查项**:
- 确认文件名包含正确的语言后缀(`_CN.md` 或 `_EN.md`)
- 检查文件路径是否正确

#### 3. "PDF生成失败"
**检查项**:
- 确认Node.js版本 >= 16
- 确认所有依赖已安装
- 检查开发服务器是否正常运行

#### 4. "内存不足"
**解决方案**:
- 减少并发数（修改脚本中的 `concurrency` 参数）
- 分批生成PDF

### 调试模式

启用详细日志输出：
```bash
# 设置环境变量
$env:DEBUG = "true"

# 运行脚本
.\scripts\generate-pdf-by-language.ps1 -Language CN -Type all
```

## 📊 性能优化

### 并发控制
- 默认并发数: 3
- 可根据系统性能调整

### 内存优化
- 自动清理临时文件
- 分批处理大文件
- 优化图片加载

### 网络优化
- 本地开发服务器
- 减少网络请求
- 缓存静态资源

## 🔄 未来扩展

### 计划功能
1. **多语言支持**: 支持更多语言版本
2. **自定义样式**: 支持自定义PDF样式
3. **批量处理**: 支持批量生成多个版本
4. **自动化**: 集成到CI/CD流程

### 配置选项
```javascript
// 可配置选项
const options = {
  language: 'CN',           // 语言版本
  concurrency: 3,          // 并发数
  outputDir: './dist/pdf',  // 输出目录
  baseURL: 'http://localhost:4321' // 开发服务器URL
};
```

## 📞 技术支持

### 日志文件
- 详细日志保存在 `logs/` 目录
- 错误信息包含完整的堆栈跟踪

### 联系方式
- 项目Issues: GitHub Issues
- 文档更新: 提交Pull Request

---

**注意**: 此解决方案保持了现有的文件夹结构，无需重新组织文件，只需通过命令行参数即可区分语言版本生成PDF。 