---
title: "代码嵌入功能测试"
description: "测试代码嵌入和代码高亮功能"
layout: "/src/layouts/HandbookLayout.astro"
---

# 代码嵌入功能测试

## 测试1：基本代码嵌入

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_price_dimension.py"
  language="python"
  showDesignPrinciples="true"
/>

## 测试2：不带设计原理

<CodeFromFile 
  filePath="code_library/003_Chapter3_Market_Analysis/3.2/code_3_2_2_analyze_volume_dimension.py"
  language="python"
  showDesignPrinciples="false"
/>

## 测试3：对比 - 普通Markdown代码块

```python
def test_function():
    """这是一个测试函数"""
    return "Hello, World!"
```

## 说明

- 测试1应该显示设计原理和代码高亮
- 测试2应该只显示代码高亮
- 测试3是普通Markdown代码块，用于对比

