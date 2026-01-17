---
name: "验证代码"
description: "运行Core模块的单元测试，验证代码质量"
command: |
  cd /home/taotao/.cursor/worktrees/TRQuant/ope && \
  python -m pytest tests/test_core/ -v --tb=short
---

# 验证代码命令

运行Core模块的单元测试，验证代码质量和功能正确性。

## 使用方式

在Cursor Chat中：
```
@validate-code
```

## 说明

- 运行所有Core模块的测试
- 显示详细输出（-v）
- 简短错误追踪（--tb=short）
