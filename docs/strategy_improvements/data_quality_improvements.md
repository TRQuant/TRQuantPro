# 陈小群策略数据质量改进建议

## 📋 改进目标

基于知识库和深度分析，优化数据质量，确保回测结果的可靠性：
- **有效数据占比**: 从23.1%提升到80%以上
- **数据填充准确性**: 使用更智能的填充策略，减少对回测结果的影响
- **选股数据质量**: 提升选股数据质量，提高选股成功率

---

## 🔍 核心问题回顾

### 问题1: 历史数据获取不足

- **表现**: 65天回测期间，有效数据只有15天（23.1%）
- **根本原因**: AKShare历史数据有限，无法获取更早的历史数据

### 问题2: 数据填充策略过于简单

- **表现**: 使用固定比例（80%）填充，没有考虑市场实际情况
- **根本原因**: 填充策略过于简单，没有考虑市场实际情况和历史趋势

### 问题3: 选股数据质量问题

- **表现**: 选股成功率可能较低，封板资金数据可能不准确或缺失
- **根本原因**: 数据获取问题（历史数据限制），数据质量检查不完善

---

## 💡 改进建议

### 1. 优化数据源选择

#### 1.1 优先使用JQData获取历史数据

**当前问题**:
- 主要使用AKShare获取历史涨停数据
- AKShare历史数据有限，无法满足回测需求

**改进建议**:

1. **数据源优先级**:
   ```python
   DATA_SOURCE_PRIORITY = [
       'jqdata',      # 优先使用JQData（如果有权限）
       'akshare',     # 降级到AKShare
       'estimated'    # 最后使用估算值
   ]
   ```

2. **数据源降级策略**:
   ```python
   def fetch_market_data_with_fallback(
       date_str: str,
       data_sources: List[str] = None
   ) -> Dict:
       """
       带降级策略的数据获取
       
       规则：
       1. 优先使用JQData获取历史数据
       2. 如果JQData不可用，降级到AKShare
       3. 如果AKShare也不可用，使用估算值
       """
       if data_sources is None:
           data_sources = DATA_SOURCE_PRIORITY
       
       for source in data_sources:
           try:
               if source == 'jqdata':
                   data = fetch_jqdata_market_data(date_str)
               elif source == 'akshare':
                   data = fetch_akshare_market_data(date_str)
               elif source == 'estimated':
                   data = estimate_market_data(date_str)
               else:
                   continue
               
               # 验证数据质量
               if validate_data_quality(data):
                   return {
                       'data': data,
                       'source': source,
                       'quality': 'good'
                   }
           except Exception as e:
               logger.warning(f"{source} 数据获取失败: {e}")
               continue
       
       # 所有数据源都失败
       return {
           'data': None,
           'source': 'failed',
           'quality': 'poor'
       }
   ```

3. **增加数据获取的重试机制**:
   ```python
   def fetch_data_with_retry(
       date_str: str,
       max_retries: int = 3,
       retry_delay: float = 1.0
   ) -> Dict:
       """
       带重试机制的数据获取
       
       规则：
       1. 如果数据获取失败，重试最多3次
       2. 每次重试之间延迟1秒
       3. 如果所有重试都失败，返回None
       """
       for attempt in range(max_retries):
           try:
               data = fetch_market_data_with_fallback(date_str)
               if data['data'] is not None:
                   return data
           except Exception as e:
               logger.warning(f"数据获取失败（尝试{attempt+1}/{max_retries}）: {e}")
               if attempt < max_retries - 1:
                   time.sleep(retry_delay)
       
       return {
           'data': None,
           'source': 'failed',
           'quality': 'poor'
       }
   ```

4. **增加数据获取的缓存机制**:
   ```python
   def fetch_data_with_cache(
       date_str: str,
       cache_dir: Path = None
   ) -> Dict:
       """
       带缓存机制的数据获取
       
       规则：
       1. 如果缓存中存在数据，直接返回
       2. 如果缓存中不存在，获取数据并缓存
       3. 缓存有效期：1天
       """
       if cache_dir is None:
           cache_dir = Path('.trquant/cache/market_data')
       
       cache_file = cache_dir / f"{date_str}.json"
       
       # 检查缓存
       if cache_file.exists():
           cache_age = time.time() - cache_file.stat().st_mtime
           if cache_age < 86400:  # 1天
               try:
                   data = json.loads(cache_file.read_text())
                   return {
                       'data': data,
                       'source': 'cache',
                       'quality': 'good'
                   }
               except Exception as e:
                   logger.warning(f"缓存读取失败: {e}")
       
       # 获取新数据
       data = fetch_data_with_retry(date_str)
       
       # 缓存数据
       if data['data'] is not None:
           try:
               cache_dir.mkdir(parents=True, exist_ok=True)
               cache_file.write_text(json.dumps(data['data'], indent=2))
           except Exception as e:
               logger.warning(f"缓存写入失败: {e}")
       
       return data
   ```

#### 1.2 增加数据质量检查机制

**改进建议**:

1. **数据完整性检查**:
   ```python
   def validate_data_completeness(
       data: Dict,
       required_fields: List[str] = ['limit_up_count', 'zhaban_rate', 'max_height']
   ) -> bool:
       """
       检查数据完整性
       
       检查：
       1. 是否有缺失字段
       2. 字段值是否为None或NaN
       3. 字段值是否在合理范围内
       """
       for field in required_fields:
           if field not in data:
               logger.warning(f"缺少字段: {field}")
               return False
           
           value = data[field]
           if value is None or (isinstance(value, float) and np.isnan(value)):
               logger.warning(f"字段值为空: {field}")
               return False
       
       return True
   ```

2. **数据合理性检查**:
   ```python
   def validate_data_reasonableness(
       data: Dict
   ) -> bool:
       """
       检查数据合理性
       
       检查：
       1. 涨停家数是否在合理范围内（0-500）
       2. 炸板率是否在合理范围内（0-100%）
       3. 连板高度是否在合理范围内（0-20）
       """
       limit_up_count = data.get('limit_up_count', 0)
       zhaban_rate = data.get('zhaban_rate', 0)
       max_height = data.get('max_height', 0)
       
       if not (0 <= limit_up_count <= 500):
           logger.warning(f"涨停家数不合理: {limit_up_count}")
           return False
       
       if not (0 <= zhaban_rate <= 100):
           logger.warning(f"炸板率不合理: {zhaban_rate}")
           return False
       
       if not (0 <= max_height <= 20):
           logger.warning(f"连板高度不合理: {max_height}")
           return False
       
       return True
   ```

3. **数据一致性检查**:
   ```python
   def validate_data_consistency(
       data: Dict,
       historical_data: List[Dict]
   ) -> bool:
       """
       检查数据一致性
       
       检查：
       1. 与历史数据是否一致（是否有异常波动）
       2. 不同数据源的数据是否一致
       """
       if not historical_data:
           return True
       
       # 计算历史数据的统计值
       historical_limit_ups = [d['limit_up_count'] for d in historical_data]
       historical_avg = np.mean(historical_limit_ups)
       historical_std = np.std(historical_limit_ups)
       
       # 检查当前数据是否异常
       current_limit_up = data['limit_up_count']
       if abs(current_limit_up - historical_avg) > 3 * historical_std:
           logger.warning(f"数据异常波动: {current_limit_up} vs {historical_avg:.1f}±{historical_std:.1f}")
           return False
       
       return True
   ```

#### 1.3 增加数据缺失的报警机制

**改进建议**:

1. **数据缺失报警**:
   ```python
   def check_data_missing(
       trade_days: List[str],
       market_data_history: Dict
   ) -> Dict:
       """
       检查数据缺失情况
       
       返回：
       - 缺失数据列表
       - 缺失数据占比
       - 报警信息
       """
       missing_days = []
       for day in trade_days:
           if day not in market_data_history:
               missing_days.append(day)
           elif market_data_history[day].get('limit_up_count', 0) == 0:
               missing_days.append(day)
       
       missing_ratio = len(missing_days) / len(trade_days) if trade_days else 0
       
       # 报警
       if missing_ratio > 0.2:  # 缺失超过20%
           logger.error(f"数据缺失严重: {missing_ratio:.1%} ({len(missing_days)}/{len(trade_days)})")
       elif missing_ratio > 0.1:  # 缺失超过10%
           logger.warning(f"数据缺失较多: {missing_ratio:.1%} ({len(missing_days)}/{len(trade_days)})")
       
       return {
           'missing_days': missing_days,
           'missing_ratio': missing_ratio,
           'total_days': len(trade_days),
           'missing_count': len(missing_days)
       }
   ```

2. **数据质量报告**:
   ```python
   def generate_data_quality_report(
       market_data_history: Dict,
       trade_days: List[str]
   ) -> Dict:
       """
       生成数据质量报告
       
       返回：
       - 数据完整性统计
       - 数据质量评分
       - 改进建议
       """
       report = {
           'total_days': len(trade_days),
           'valid_days': 0,
           'invalid_days': 0,
           'estimated_days': 0,
           'data_sources': {},
           'quality_score': 0.0,
           'suggestions': []
       }
       
       for day in trade_days:
           if day not in market_data_history:
               report['invalid_days'] += 1
               continue
           
           data = market_data_history[day]
           source = data.get('source', 'unknown')
           
           if data.get('limit_up_count', 0) > 0:
               report['valid_days'] += 1
           else:
               report['invalid_days'] += 1
           
           if source == 'estimated':
               report['estimated_days'] += 1
           
           report['data_sources'][source] = report['data_sources'].get(source, 0) + 1
       
       # 计算质量评分
       report['quality_score'] = report['valid_days'] / report['total_days'] if report['total_days'] > 0 else 0.0
       
       # 生成改进建议
       if report['quality_score'] < 0.8:
           report['suggestions'].append("数据质量不足，建议优先使用JQData获取历史数据")
       
       if report['estimated_days'] > report['total_days'] * 0.3:
           report['suggestions'].append("估算数据过多，建议优化数据获取策略")
       
       return report
   ```

---

### 2. 优化数据填充策略

#### 2.1 使用更智能的填充策略

**当前问题**:
- 使用固定比例（80%）填充，没有考虑市场实际情况
- 填充值可能不准确，影响情绪周期判断

**改进建议**:

1. **基于相邻日期填充**:
   ```python
   def fill_data_from_adjacent_days(
       date_str: str,
       market_data_history: Dict,
       trade_days: List[str]
   ) -> Dict:
       """
       基于相邻日期填充数据
       
       规则：
       1. 优先使用前一个交易日的数据
       2. 如果前一个交易日也没有数据，使用后一个交易日的数据
       3. 如果都没有，使用最近的有效数据
       """
       date_idx = trade_days.index(date_str) if date_str in trade_days else -1
       
       # 尝试前一个交易日
       if date_idx > 0:
           prev_day = trade_days[date_idx - 1]
           if prev_day in market_data_history:
               prev_data = market_data_history[prev_day]
               if prev_data.get('limit_up_count', 0) > 0:
                   return {
                       'limit_up_count': prev_data['limit_up_count'],
                       'zhaban_rate': prev_data['zhaban_rate'],
                       'max_height': prev_data['max_height'],
                       'source': 'adjacent_previous',
                       'quality': 'medium'
                   }
       
       # 尝试后一个交易日
       if date_idx >= 0 and date_idx < len(trade_days) - 1:
           next_day = trade_days[date_idx + 1]
           if next_day in market_data_history:
               next_data = market_data_history[next_day]
               if next_data.get('limit_up_count', 0) > 0:
                   return {
                       'limit_up_count': next_data['limit_up_count'],
                       'zhaban_rate': next_data['zhaban_rate'],
                       'max_height': next_data['max_height'],
                       'source': 'adjacent_next',
                       'quality': 'medium'
                   }
       
       # 使用最近的有效数据
       valid_data = {k: v for k, v in market_data_history.items() 
                     if v.get('limit_up_count', 0) > 0}
       if valid_data:
           latest_date = max(valid_data.keys())
           latest_data = valid_data[latest_date]
           return {
               'limit_up_count': latest_data['limit_up_count'],
               'zhaban_rate': latest_data['zhaban_rate'],
               'max_height': latest_data['max_height'],
               'source': 'latest_valid',
               'quality': 'low'
           }
       
       return None
   ```

2. **基于市场整体情况填充**:
   ```python
   def fill_data_from_market_context(
       date_str: str,
       market_data_history: Dict,
       trade_days: List[str]
   ) -> Dict:
       """
       基于市场整体情况填充数据
       
       规则：
       1. 计算有效数据的统计值（均值、中位数、标准差）
       2. 根据市场趋势（上涨/下跌/震荡）调整填充值
       3. 考虑季节性因素（如果有历史数据）
       """
       valid_data = {k: v for k, v in market_data_history.items() 
                     if v.get('limit_up_count', 0) > 0}
       
       if not valid_data:
           return None
       
       # 计算统计值
       limit_ups = [v['limit_up_count'] for v in valid_data.values()]
       zhaban_rates = [v['zhaban_rate'] for v in valid_data.values()]
       max_heights = [v['max_height'] for v in valid_data.values()]
       
       # 使用中位数（更稳健）
       median_limit_up = np.median(limit_ups)
       median_zhaban = np.median(zhaban_rates)
       median_height = np.median(max_heights)
       
       # 根据市场趋势调整（如果有基准指数数据）
       # ... 可以添加更多逻辑
       
       return {
           'limit_up_count': int(median_limit_up),
           'zhaban_rate': float(median_zhaban),
           'max_height': int(median_height),
           'source': 'market_context',
           'quality': 'medium'
       }
   ```

3. **基于历史同期数据填充**（如果有历史数据）:
   ```python
   def fill_data_from_historical_period(
       date_str: str,
       historical_data: Dict
   ) -> Dict:
       """
       基于历史同期数据填充
       
       规则：
       1. 查找历史同期（如去年同月）的数据
       2. 使用历史同期数据的统计值
       3. 考虑市场环境变化（如整体情绪提升）
       """
       # 解析日期
       date_obj = datetime.strptime(date_str, '%Y-%m-%d')
       month = date_obj.month
       day = date_obj.day
       
       # 查找历史同期数据
       historical_period_data = []
       for hist_date, hist_data in historical_data.items():
           hist_date_obj = datetime.strptime(hist_date, '%Y-%m-%d')
           if hist_date_obj.month == month and abs(hist_date_obj.day - day) <= 3:
               if hist_data.get('limit_up_count', 0) > 0:
                   historical_period_data.append(hist_data)
       
       if historical_period_data:
           # 使用历史同期数据的统计值
           limit_ups = [d['limit_up_count'] for d in historical_period_data]
           zhaban_rates = [d['zhaban_rate'] for d in historical_period_data]
           max_heights = [d['max_height'] for d in historical_period_data]
           
           return {
               'limit_up_count': int(np.median(limit_ups)),
               'zhaban_rate': float(np.median(zhaban_rates)),
               'max_height': int(np.median(max_heights)),
               'source': 'historical_period',
               'quality': 'medium'
           }
       
       return None
   ```

#### 2.2 增加数据填充的置信度标记

**改进建议**:

1. **填充数据标记**:
   ```python
   def mark_filled_data(
       data: Dict,
       fill_method: str,
       confidence: float = 0.5
   ) -> Dict:
       """
       标记填充数据
       
       参数：
       - fill_method: 填充方法（'adjacent', 'market_context', 'historical_period', 'estimated'）
       - confidence: 置信度（0-1）
       """
       data['is_filled'] = True
       data['fill_method'] = fill_method
       data['fill_confidence'] = confidence
       data['fill_timestamp'] = datetime.now().isoformat()
       
       return data
   ```

2. **在回测结果中显示数据质量信息**:
   ```python
   def generate_backtest_report_with_data_quality(
       backtest_results: Dict,
       market_data_history: Dict
   ) -> Dict:
       """
       生成包含数据质量信息的回测报告
       
       返回：
       - 回测结果
       - 数据质量统计
       - 数据质量对回测结果的影响评估
       """
       # 统计数据质量
       total_days = len(market_data_history)
       filled_days = sum(1 for d in market_data_history.values() if d.get('is_filled', False))
       filled_ratio = filled_days / total_days if total_days > 0 else 0
       
       # 评估数据质量对回测结果的影响
       # ... 可以添加更多分析
       
       return {
           'backtest_results': backtest_results,
           'data_quality': {
               'total_days': total_days,
               'filled_days': filled_days,
               'filled_ratio': filled_ratio,
               'quality_score': 1.0 - filled_ratio * 0.3  # 填充数据降低质量评分
           },
           'impact_assessment': {
               'data_quality_impact': 'medium',  # low/medium/high
               'recommendation': '建议优先使用JQData获取历史数据，减少数据填充'
           }
       }
   ```

---

### 3. 增加实时数据获取能力

#### 3.1 实时数据获取（用于实盘交易）

**改进建议**:

1. **实时数据获取接口**:
   ```python
   def fetch_realtime_market_data(
       date_str: str = None
   ) -> Dict:
       """
       获取实时市场数据
       
       规则：
       1. 优先使用实时数据源（如JQData实时接口）
       2. 如果实时数据不可用，使用最新缓存数据
       3. 增加数据更新机制
       """
       if date_str is None:
           date_str = datetime.now().strftime('%Y-%m-%d')
       
       # 尝试实时数据源
       try:
           data = fetch_jqdata_realtime(date_str)
           if data and validate_data_quality(data):
               return {
                   'data': data,
                   'source': 'realtime',
                   'quality': 'good',
                   'timestamp': datetime.now().isoformat()
               }
       except Exception as e:
           logger.warning(f"实时数据获取失败: {e}")
       
       # 降级到缓存数据
       cached_data = fetch_data_with_cache(date_str)
       if cached_data['data']:
           return {
               'data': cached_data['data'],
               'source': 'cache',
               'quality': 'medium',
               'timestamp': datetime.now().isoformat()
           }
       
       return {
           'data': None,
           'source': 'failed',
           'quality': 'poor'
       }
   ```

2. **数据更新机制**:
   ```python
   def update_market_data_cache(
       date_str: str,
       new_data: Dict
   ) -> bool:
       """
       更新市场数据缓存
       
       规则：
       1. 如果新数据质量更好，更新缓存
       2. 如果新数据是实时数据，优先更新
       3. 记录数据更新时间
       """
       cache_file = Path('.trquant/cache/market_data') / f"{date_str}.json"
       
       # 检查现有缓存
       if cache_file.exists():
           try:
               cached_data = json.loads(cache_file.read_text())
               cached_quality = cached_data.get('quality', 'poor')
               new_quality = new_data.get('quality', 'poor')
               
               # 质量评分
               quality_scores = {'good': 3, 'medium': 2, 'poor': 1}
               
               if quality_scores.get(new_quality, 0) > quality_scores.get(cached_quality, 0):
                   # 新数据质量更好，更新缓存
                   cache_file.write_text(json.dumps(new_data, indent=2))
                   return True
               else:
                   # 缓存数据质量更好，不更新
                   return False
           except Exception as e:
               logger.warning(f"缓存更新失败: {e}")
               return False
       else:
           # 没有缓存，直接写入
           try:
               cache_file.parent.mkdir(parents=True, exist_ok=True)
               cache_file.write_text(json.dumps(new_data, indent=2))
               return True
           except Exception as e:
               logger.warning(f"缓存写入失败: {e}")
               return False
   ```

---

## 📊 预期改进效果

### 改进前 vs 改进后

| 指标 | 改进前 | 改进后（预期） |
|------|--------|---------------|
| 有效数据占比 | 23.1% | 80%+ |
| 数据填充占比 | 76.9% | <20% |
| 数据质量评分 | 低 | 高 |
| 选股数据质量 | 低 | 高 |
| 回测结果可靠性 | 低 | 高 |

---

## 🎯 实施优先级

### 高优先级（立即实施）

1. **优先使用JQData获取历史数据**
2. **增加数据质量检查机制**
3. **使用更智能的填充策略**（基于相邻日期、市场整体情况）

### 中优先级（1-2周内实施）

1. **增加数据获取的重试机制和缓存机制**
2. **增加数据缺失的报警机制**
3. **增加数据填充的置信度标记**

### 低优先级（1个月内实施）

1. **增加实时数据获取能力**
2. **增加数据更新机制**
3. **优化数据质量报告**

---

## 📝 结论

通过以上改进，预期可以：
- **有效数据占比提升**: 从23.1%提升到80%以上
- **数据填充准确性提升**: 使用更智能的填充策略，减少对回测结果的影响
- **选股数据质量提升**: 提升选股数据质量，提高选股成功率

**关键改进点**:
1. **优化数据源选择**：优先使用JQData获取历史数据
2. **优化数据填充策略**：使用更智能的填充策略，增加置信度标记
3. **增加数据质量检查**：检查数据完整性、合理性、一致性

---

**报告生成时间**: 2026-01-14  
**改进建议来源**: 
- 知识库：`.trquant/dev/knowledge/strategy_knowledge/chen_xiaoqun_kb.json`
- 分析报告：`docs/strategy_analysis/data_quality_analysis.md`
