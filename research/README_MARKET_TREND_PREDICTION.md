# 市场趋势预测算法研究

## 📋 研究计划文档

详细研究计划请查看：`research/market_trend_prediction_research_plan.md`

## 🚀 快速开始

### 1. 使用Jupyter Notebook进行研究

```bash
# 打开研究notebook（待创建）
cd /home/taotao/dev/QuantTest/TRQuant
jupyter lab research/market_trend_prediction.ipynb
```

### 2. 研究阶段

#### 阶段1: 文献调研 ✅
- [x] 搜索权威网站和学术论文
- [x] 分析开源项目实现方式
- [x] 总结技术方法

#### 阶段2: 数据准备
- [ ] 获取聚宽3年历史数据
- [ ] 数据清洗和预处理
- [ ] 特征工程

#### 阶段3: 模型训练
- [ ] 短期预测模型（1-7天）
- [ ] 中期预测模型（1-3月）
- [ ] 长期预测模型（6月+）

#### 阶段4: 验证与优化
- [ ] Walk-Forward验证
- [ ] 聚宽回测验证
- [ ] 模型优化

## 📚 参考资源

### 学术研究

1. **Stockformer** (arXiv:2401.06139)
   - 小波变换+多任务自注意力网络
   - 价格-成交量因子选股模型

2. **Tsururu** (arXiv:2509.15843)
   - Python时间序列预测策略库
   - 支持全局和多变量方法

3. **TFB基准** (arXiv:2403.20150)
   - 全面且公平的时间序列预测基准
   - 涵盖股票市场数据集

4. **HIST** (arXiv:2110.13716)
   - 基于图神经网络的股票趋势预测
   - 挖掘概念导向共享信息

### 开源项目

- PyAlgoTrade: 算法交易框架
- zipline: 量化交易回测框架
- backtrader: Python回测库

## 🔧 技术栈

- **数据**: JQData (聚宽)
- **机器学习**: scikit-learn, XGBoost, LightGBM
- **深度学习**: PyTorch (可选)
- **时间序列**: Prophet, statsmodels
- **回测**: 聚宽回测引擎
- **可视化**: Matplotlib, Plotly

## 📊 预期成果

1. **短期预测模型**: 1-7天趋势预测，准确率>55%
2. **中期预测模型**: 1-3月趋势预测，准确率>60%
3. **长期预测模型**: 6月+环境判断，准确率>65%

---

*研究项目启动日期: 2025-01-01*

