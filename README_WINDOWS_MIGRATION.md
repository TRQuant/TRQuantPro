# TRQuant Windows迁移 - 快速指南

> **项目目录**: `/home/taotao/.cursor/worktrees/TRQuant/ope`  
> **Windows安装路径**: `C:\TRQuantPro\ope`  
> **更新**: 2026-01-11

---

## 🚀 快速开始

### 步骤1: 在Linux上打包

```bash
# 进入ope目录（唯一项目目录）
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 运行打包脚本
./scripts/package_for_windows.sh

# 会生成: TRQuant_Windows_YYYYMMDD_HHMMSS.tar.gz
```

### 步骤2: 传输到Windows

将生成的压缩包传输到Windows电脑

### 步骤3: 在Windows上安装

```powershell
# 解压文件到临时目录
# 然后运行安装脚本
cd <解压目录>\TRQuant
.\install_windows.ps1

# 会自动安装到: C:\TRQuantPro\ope
```

---

## ⚠️ 重要提示

1. **项目目录**: 只有 `ope/` 目录，`abd/` 已删除并合并
2. **Python版本**: QMT需要Python 3.11或3.10（3.12以下）
3. **安装路径**: Windows上固定为 `C:\TRQuantPro\ope`
4. **知识库**: 已包含在打包中（`.trquant/dev/knowledge/`）

---

## 📋 详细文档

- **完整迁移指南**: `docs/02_development_guides/WINDOWS_MIGRATION_GUIDE.md`
- **合并报告**: `docs/02_development_guides/ABD_MERGE_COMPLETE.md`

---

**最后更新**: 2026-01-11
