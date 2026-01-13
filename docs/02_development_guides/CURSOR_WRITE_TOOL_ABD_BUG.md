# Cursor Write工具路径重定向到abd的Bug

> **更新时间**: 2026-01-13  
> **问题**: Cursor的write工具将文件路径重定向到`abd`目录，即使使用绝对路径指向`ope`目录

---

## 🔍 问题确认

### 现象

当使用Cursor的`write`工具创建文件时：
1. 即使使用绝对路径：`/home/taotao/.cursor/worktrees/TRQuant/ope/test.txt`
2. 文件实际被创建在：`/home/taotao/.cursor/worktrees/TRQuant/abd/test.txt`
3. 这是Cursor工具层面的路径重定向bug

### 证据

```bash
# 使用write工具创建文件
write("/home/taotao/.cursor/worktrees/TRQuant/ope/test.txt", "内容")

# 实际文件位置
find /home/taotao/.cursor/worktrees/TRQuant -name "test.txt"
# 结果: /home/taotao/.cursor/worktrees/TRQuant/abd/test.txt ❌

# 期望位置
# /home/taotao/.cursor/worktrees/TRQuant/ope/test.txt ✅
```

---

## 💡 解决方案

### 方案1: 使用终端命令创建文件（推荐）

**原理**：绕过Cursor的write工具，直接使用终端命令。

**实施**：
```bash
# 使用终端命令创建文件
cd /home/taotao/.cursor/worktrees/TRQuant/ope
cat > myfile.txt << 'EOF'
文件内容
EOF
```

**优点**：
- ✅ 完全绕过bug
- ✅ 文件创建在正确位置
- ✅ 不依赖Cursor的内部逻辑

---

### 方案2: 定期清理abd目录

**清理脚本** (`cleanup_abd.sh`):
```bash
#!/bin/bash
cd ~/.cursor/worktrees/TRQuant
if [ -d abd ]; then
    if [ ! -f abd/.git ] && [ ! -d abd/.git ]; then
        echo "删除abd目录..."
        rm -rf abd
        echo "✅ abd目录已删除"
    fi
fi
```

---

## ⚠️ 当前状态

- ❌ write工具：文件创建到abd（bug）
- ✅ 终端命令：文件创建到ope（正常）

**建议**：对于重要文件，使用终端命令创建，或创建后立即验证位置并移动。

---

**最后更新**: 2026-01-13  
**状态**: 问题确认，临时解决方案已实施
