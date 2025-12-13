# 金融术语API扩展功能使用指南

## 🎯 功能概述

金融术语API扩展功能允许系统从多个外部数据源获取金融术语的详细解释，大大扩展了术语库的覆盖范围。

## 🏗️ 支持的API

### 1. Wikipedia API
- **状态**: ✅ 已集成
- **功能**: 获取术语的Wikipedia解释
- **优势**: 内容丰富，多语言支持
- **限制**: 需要网络连接

### 2. Investopedia
- **状态**: ✅ 已集成
- **功能**: 获取专业金融术语解释
- **优势**: 专业性强，金融领域权威
- **限制**: 需要网络连接，可能有访问限制

### 3. Alpha Vantage
- **状态**: 🔧 预留接口
- **功能**: 获取股票相关术语
- **优势**: 实时数据，专业API
- **限制**: 需要API key

## 🚀 使用方法

### 1. 基本使用

```javascript
import { getTermDefinition } from '../utils/finance-glossary.js';

// 获取术语解释（自动选择最佳数据源）
const definition = await getTermDefinition('EBITDA');
console.log(definition);
```

### 2. 指定数据源

```javascript
// 只从Wikipedia获取
const wikiResult = await getWikipediaTerm('CAGR');

// 只从Investopedia获取
const investopediaResult = await getInvestopediaTerm('PEG');

// 并行获取多个源
const [wiki, investopedia] = await Promise.allSettled([
  getWikipediaTerm('ROE'),
  getInvestopediaTerm('ROE')
]);
```

### 3. 批量处理

```javascript
import { getMultipleTerms } from '../utils/finance-glossary.js';

const terms = ['CAGR', 'TAM', 'ROE', 'PEG'];
const results = await getMultipleTerms(terms, {
  preferLocal: false,
  includeWikipedia: true,
  includeInvestopedia: true
});
```

### 4. 搜索功能

```javascript
import { searchTerms } from '../utils/finance-glossary.js';

// 搜索相关术语
const results = await searchTerms('growth', {
  maxResults: 10,
  includeExternal: true
});
```

## 🔧 配置选项

### API配置

```javascript
const API_CONFIG = {
  wikipedia: {
    baseUrl: 'https://en.wikipedia.org/api/rest_v1/page/summary/',
    timeout: 5000
  },
  investopedia: {
    baseUrl: 'https://www.investopedia.com/terms/',
    timeout: 5000
  }
};
```

### 缓存配置

```javascript
const API_CACHE_DURATION = 24 * 60 * 60 * 1000; // 24小时
```

## 📊 缓存管理

### 查看缓存状态

```javascript
import { getCacheStats } from '../utils/finance-glossary.js';

const stats = getCacheStats();
console.log(stats);
// 输出: { total: 15, valid: 12, expired: 3, sources: {...} }
```

### 清理缓存

```javascript
import { clearExpiredCache } from '../utils/finance-glossary.js';

const cleared = clearExpiredCache();
console.log(`清理了 ${cleared} 个过期缓存项`);
```

## 🎨 在组件中使用

### 1. 在Astro组件中

```astro
---
import { getWikipediaTerm } from '../utils/finance-glossary.js';

const term = 'EBITDA';
const definition = await getWikipediaTerm(term);
---

<div class="term-definition">
  <h3>{definition.fullName}</h3>
  <p>{definition.description}</p>
  <small>来源: {definition.source}</small>
</div>
```

### 2. 动态加载

```astro
<script>
  import { getTermDefinition } from '../utils/finance-glossary.js';

  async function loadTermDefinition(term) {
    try {
      const definition = await getTermDefinition(term);
      if (definition) {
        showTooltip(definition);
      }
    } catch (error) {
      console.error('加载术语失败:', error);
    }
  }
</script>
```

## 🔍 错误处理

### 网络错误

```javascript
try {
  const result = await getWikipediaTerm('CAGR');
  if (result) {
    // 处理结果
  } else {
    // 回退到本地词典
    const localResult = getLocalTerm('CAGR');
  }
} catch (error) {
  console.warn('API请求失败，使用本地数据');
  // 使用本地数据作为回退
}
```

### 超时处理

```javascript
// 设置较短的超时时间
const quickResult = await getTermDefinition('CAGR', {
  timeout: 2000 // 2秒超时
});
```

## 📈 性能优化

### 1. 缓存策略

- **本地缓存**: 24小时有效期
- **智能回退**: API失败时使用本地数据
- **批量处理**: 减少API调用次数

### 2. 网络优化

- **超时控制**: 避免长时间等待
- **并行请求**: 同时查询多个API
- **错误重试**: 自动重试失败的请求

### 3. 用户体验

- **加载状态**: 显示加载指示器
- **渐进增强**: 先显示本地数据，再加载外部数据
- **离线支持**: 网络不可用时使用本地数据

## 🛠️ 扩展开发

### 添加新的API

```javascript
// 在finance-glossary.js中添加新API
export async function getCustomAPITerm(term) {
  const cacheKey = `custom_${term.toLowerCase()}`;
  
  if (isCacheValid(cacheKey)) {
    return getCache(cacheKey);
  }

  try {
    const response = await fetch(`https://api.example.com/terms/${term}`);
    const data = await response.json();
    
    const result = {
      term: term,
      fullName: data.title,
      description: data.description,
      category: 'Custom API',
      source: 'custom'
    };
    
    setCache(cacheKey, result);
    return result;
  } catch (error) {
    console.warn(`Failed to fetch term "${term}" from Custom API:`, error);
    return null;
  }
}
```

### 自定义缓存策略

```javascript
// 为特定API设置不同的缓存时间
const CUSTOM_CACHE_DURATION = 60 * 60 * 1000; // 1小时

function setCustomCache(cacheKey, data) {
  GLOSSARY_CACHE.set(cacheKey, {
    data,
    timestamp: Date.now(),
    duration: CUSTOM_CACHE_DURATION
  });
}
```

## 📋 最佳实践

### 1. 数据源选择

- **本地优先**: 核心术语使用本地数据
- **外部补充**: 扩展术语使用外部API
- **智能回退**: API失败时自动回退

### 2. 错误处理

- **优雅降级**: 网络错误不影响基本功能
- **用户提示**: 告知用户数据来源
- **重试机制**: 自动重试失败的请求

### 3. 性能考虑

- **懒加载**: 按需加载外部数据
- **预加载**: 预加载常用术语
- **缓存优化**: 合理设置缓存时间

## 🔮 未来计划

### 短期目标
- [ ] 添加更多金融数据源
- [ ] 实现智能术语推荐
- [ ] 支持多语言术语

### 长期目标
- [ ] 机器学习术语识别
- [ ] 个性化术语库
- [ ] 实时术语更新

---

**最后更新**: 2025-01-03
**版本**: v1.0
**维护者**: AI Assistant 
 