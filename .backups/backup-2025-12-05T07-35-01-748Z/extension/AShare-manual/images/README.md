# 第一章图片使用指南

## 图片列表及使用建议

### 1. 哲学与自我认知类图片

#### `socrates_philosophy.jpg`
- **使用位置**: 1.1.1 认识你自己 - 古希腊哲学部分
- **说明**: 苏格拉底哲学思想，体现"认识你自己"的智慧
- **Markdown使用**: `![苏格拉底哲学](socrates_philosophy.jpg)`

#### `meditation_mindfulness.jpg`
- **使用位置**: 1.1.2 如何突破自我 - 冥想与正念部分
- **说明**: 冥想练习，体现正念训练的重要性
- **Markdown使用**: `![冥想正念](meditation_mindfulness.jpg)`

#### `brain_neuroscience.jpg`
- **使用位置**: 1.1.1 认识你自己 - 现代神经科学部分
- **说明**: 大脑科学，展示前额叶与杏仁核的决策机制
- **Markdown使用**: `![大脑神经科学](brain_neuroscience.jpg)`

### 2. 投资与决策类图片

#### `investment_charts.jpg`
- **使用位置**: 1.2 看懂世界 - 投资分析框架
- **说明**: 投资图表分析，体现技术分析的重要性
- **Markdown使用**: `![投资图表](investment_charts.jpg)`

#### `decision_making.jpg`
- **使用位置**: 1.1.2 如何突破自我 - 认知行为疗法部分
- **说明**: 决策过程，体现理性决策的重要性
- **Markdown使用**: `![决策制定](decision_making.jpg)`

#### `emotional_control.jpg`
- **使用位置**: 1.1.2 如何突破自我 - 情绪管理部分
- **说明**: 情绪控制，体现投资中的情绪管理
- **Markdown使用**: `![情绪控制](emotional_control.jpg)`

### 3. 全球视野类图片

#### `global_economy.jpg`
- **使用位置**: 1.2.1 理论学习框架 - 宏观经济分析
- **说明**: 全球经济，体现宏观分析的重要性
- **Markdown使用**: `![全球经济](global_economy.jpg)`

#### `world_map.jpg`
- **使用位置**: 1.2 看懂世界 - 建立投资的全局视野
- **说明**: 世界地图，体现全球投资视野
- **Markdown使用**: `![世界地图](world_map.jpg)`

### 4. 认知心理学类图片

#### `cognitive_psychology.jpg`
- **使用位置**: 1.1.1 认识你自己 - 认知科学部分
- **说明**: 认知心理学，体现认知偏差的研究
- **Markdown使用**: `![认知心理学](cognitive_psychology.jpg)`

#### `critical_thinking.jpg`
- **使用位置**: 1.1.2 如何突破自我 - 批判性思维训练
- **说明**: 批判性思维，体现理性分析能力
- **Markdown使用**: `![批判性思维](critical_thinking.jpg)`

#### `self_awareness.jpg`
- **使用位置**: 1.1.1 认识你自己 - 自我觉察部分
- **说明**: 自我觉察，体现内在认知的重要性
- **Markdown使用**: `![自我觉察](self_awareness.jpg)`

### 5. 投资框架类图片

#### `investment_framework.jpg`
- **使用位置**: 1.2.1 理论学习框架
- **说明**: 投资框架，体现系统化分析方法
- **Markdown使用**: `![投资框架](investment_framework.jpg)`

#### `risk_management.jpg`
- **使用位置**: 1.1.2 如何突破自我 - 风险管理部分
- **说明**: 风险管理，体现投资中的风险控制
- **Markdown使用**: `![风险管理](risk_management.jpg)`

#### `portfolio_diversification.jpg`
- **使用位置**: 1.2.1 理论学习框架 - 投资组合理论
- **说明**: 投资组合，体现分散投资的重要性
- **Markdown使用**: `![投资组合](portfolio_diversification.jpg)`

## 在Astro页面中使用图片

### 方法1: 相对路径引用
```markdown
![图片描述](../images/图片名称.jpg)
```

### 方法2: 绝对路径引用
```markdown
![图片描述](/images/图片名称.jpg)
```

### 方法3: 在Astro组件中使用
```astro
---
// 在Astro组件中
---
<img src="/images/图片名称.jpg" alt="图片描述" class="chapter-image" />
```

## 图片优化建议

1. **尺寸**: 所有图片已优化为800x600像素，适合网页显示
2. **格式**: 使用JPG格式，文件大小适中
3. **加载**: 建议添加懒加载属性 `loading="lazy"`
4. **响应式**: 建议添加CSS类实现响应式显示

## CSS样式建议

```css
.chapter-image {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 20px 0;
}

.chapter-image:hover {
    transform: scale(1.02);
    transition: transform 0.3s ease;
}
```

## 版权说明

所有图片均来自Unsplash，遵循Unsplash许可证，可免费用于商业和非商业用途。 