# Git工作目录切换指南

> **更新时间**: 2025-01-03  
> **目的**: 将Git工作目录从主项目目录切换到worktrees目录

## 📊 当前状态

### Worktrees目录
- **路径**: `~/.cursor/worktrees/TRQuant/`
- **状态**: ✅ 完整的Git仓库（.git是目录）
- **分支**: main
- **Remote**: origin, trquantpro, upstream
- **状态**: 可以直接作为Git工作目录使用

### 主项目目录
- **路径**: `/home/taotao/dev/QuantTest/TRQuant`
- **状态**: Git主仓库
- **关系**: 与worktrees目录通过remote同步

## ✅ 结论：worktrees目录已经是Git工作目录

**无需切换**，worktrees目录已经是完整的Git仓库，可以直接使用：

```bash
cd ~/.cursor/worktrees/TRQuant
git status      # ✅ 正常工作
git add .       # ✅ 正常工作
git commit      # ✅ 正常工作
git push        # ✅ 正常工作
```

## 🔄 两个目录的关系

两个目录都是独立的Git仓库，通过remote同步：

```bash
# 在worktrees目录工作
cd ~/.cursor/worktrees/TRQuant
git add .
git commit -m "更改"
git push trquantpro main

# 在主目录同步（如果需要）
cd /home/taotao/dev/QuantTest/TRQuant
git pull trquantpro main
```

## 💡 建议

**推荐：在worktrees目录工作**
- ✅ 已经是完整的Git仓库
- ✅ Cursor默认在此工作
- ✅ 文件完整，包含运行时环境
- ✅ 可以直接使用Git命令

*最后更新: 2025-01-03*
