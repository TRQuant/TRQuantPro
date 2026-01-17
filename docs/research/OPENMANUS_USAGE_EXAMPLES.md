# OpenManus 使用示例

> **创建时间**: 2026-01-11  
> **目的**: 提供OpenManus在Cursor Chat中的实际使用示例

---

## 🎯 在Cursor Chat中使用OpenManus

### 前提条件

✅ OpenManus已安装  
✅ MCP服务器已配置到Cursor  
✅ Cursor已重启  

---

## 📊 使用示例

### 示例1: 访问网页 🌐

**在Cursor Chat中**:
```
"使用openmanus的browser工具访问 https://www.eastmoney.com"
```

**结果**: 浏览器会自动打开东方财富网站

---

### 示例2: 搜索股票并获取价格 📈

**任务**: 访问东方财富，搜索000001，获取当前价格

**注意**: 这是一个多步操作，需要分步执行：

**步骤1**: 访问网站
```
"使用openmanus的browser工具，action参数为go_to_url，url为https://www.eastmoney.com"
```

**步骤2**: 搜索股票
```
"使用openmanus的browser工具，action参数为input_text，在搜索框中输入000001"
```

**步骤3**: 点击搜索
```
"使用openmanus的browser工具，action参数为click_element，点击搜索按钮"
```

**步骤4**: 提取价格
```
"使用openmanus的browser工具，action参数为extract_content，goal参数为获取股票当前价格"
```

---

### 示例3: 提取页面内容 📄

**在Cursor Chat中**:
```
"使用openmanus的browser工具，先访问 https://www.eastmoney.com，然后提取页面标题和主要新闻标题"
```

**注意**: 这需要两步：
1. 访问URL (`go_to_url`)
2. 提取内容 (`extract_content`)

---

### 示例4: 使用Bash工具执行命令 💻

**在Cursor Chat中**:
```
"使用openmanus的bash工具，执行命令 ls -la /home/taotao/.cursor/worktrees/TRQuant/ope/strategies"
```

---

### 示例5: 使用Editor工具编辑文件 📝

**在Cursor Chat中**:
```
"使用openmanus的editor工具，读取文件 /home/taotao/.cursor/worktrees/TRQuant/ope/strategies/test.py"
```

---

## 🔧 工具参数说明

### Browser工具参数

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 操作类型（go_to_url, click_element, extract_content等） |
| `url` | string | 部分必需 | URL（用于go_to_url, open_tab操作） |
| `index` | integer | 部分必需 | 元素索引（用于click_element, input_text等） |
| `text` | string | 部分必需 | 文本内容（用于input_text, scroll_to_text等） |
| `goal` | string | 部分必需 | 提取目标（用于extract_content操作） |
| `query` | string | 部分必需 | 搜索查询（用于web_search操作） |

### 常用操作

#### 1. 访问URL
```json
{
  "action": "go_to_url",
  "url": "https://www.eastmoney.com"
}
```

#### 2. 点击元素
```json
{
  "action": "click_element",
  "index": 0
}
```

#### 3. 输入文本
```json
{
  "action": "input_text",
  "index": 0,
  "text": "000001"
}
```

#### 4. 提取内容
```json
{
  "action": "extract_content",
  "goal": "获取股票当前价格"
}
```

#### 5. 网页搜索
```json
{
  "action": "web_search",
  "query": "000001 股票"
}
```

---

## 💡 实际应用场景

### 场景1: 财经数据抓取

**完整流程**:
1. 访问财经网站
2. 搜索股票代码
3. 提取价格信息
4. 保存到数据库

**在Cursor Chat中**:
```
"使用openmanus工具完成以下任务：
1. 使用browser工具访问 https://www.eastmoney.com
2. 搜索000001
3. 提取当前价格
4. 使用bash工具将价格保存到文件"
```

---

### 场景2: 新闻收集

**在Cursor Chat中**:
```
"使用openmanus的browser工具访问东方财富新闻页面，提取最新10条财经新闻标题和摘要"
```

---

### 场景3: 数据下载

**在Cursor Chat中**:
```
"使用openmanus的browser工具访问数据下载页面，下载CSV格式的历史行情数据"
```

---

## ⚠️ 注意事项

1. **多步操作**:
   - 复杂的操作需要多步执行
   - 每步调用一次browser工具
   - 需要保持浏览器会话状态

2. **元素识别**:
   - 基础操作不需要LLM API
   - 智能元素识别需要LLM API（可选）
   - 可以手动指定元素索引

3. **错误处理**:
   - 如果操作失败，检查参数是否正确
   - 验证网页是否加载完成
   - 检查元素索引是否正确

4. **性能**:
   - 浏览器操作需要时间
   - 建议分步执行，不要一次执行太多操作
   - 可以设置等待时间（wait操作）

---

## 🎓 最佳实践

1. **分步执行**: 将复杂任务分解为多个简单步骤
2. **验证结果**: 每步操作后验证结果
3. **错误处理**: 处理可能的错误情况
4. **性能优化**: 避免不必要的操作
5. **数据保存**: 及时保存提取的数据

---

## 📝 总结

OpenManus提供了强大的浏览器自动化工具，可以在Cursor Chat中使用。

**主要能力**:
- ✅ 访问网页
- ✅ 交互操作（点击、输入等）
- ✅ 内容提取
- ✅ 数据抓取

**使用方式**:
- 在Cursor Chat中通过自然语言指令
- Cursor通过MCP协议调用OpenManus工具
- 工具执行操作并返回结果

---

**更多信息**: 
- 快速开始: `docs/research/OPENMANUS_QUICK_START.md`
- 功能指南: `docs/research/OPENMANUS_CAPABILITIES_GUIDE.md`
- MCP配置: `docs/research/OPENMANUS_MCP_SETUP.md`
