#!/usr/bin/env python3
"""
十倍股早期识别系统V2 - 端到端测试

符合JQData聚宽数据规范的完整测试

测试内容:
1. 数据源连接（JQData/AKShare）
2. 获取真实候选股票
3. 三层漏斗筛选
4. 规则引擎一票否决
5. 三轴阶段判定
6. 评分引擎V2
7. 生成推荐报告

Author: TRQuant Team
Date: 2025-12-19
Version: 2.0 (符合JQData规范)
"""

import sys
import os
import traceback
from datetime import datetime, timedelta
import logging

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 错误统计
error_stats = {
    'jqdata_errors': [],
    'akshare_errors': [],
    'data_fetch_errors': [],
    'evaluation_errors': []
}

def log_error(category: str, error: Exception, context: str = ""):
    """记录错误"""
    error_msg = f"{context}: {str(error)}"
    error_stats[category].append(error_msg)
    logger.error(error_msg)
    if logger.level <= logging.DEBUG:
        traceback.print_exc()

print("=" * 70)
print("十倍股早期识别系统 V2 - 端到端测试（符合JQData规范）")
print("=" * 70)
print()

# ==================== Step 1: 数据源连接 ====================
print("📡 Step 1: 检查数据源连接...")
print("-" * 50)

jq_status = False
jq_client = None
jq_account_info = None

try:
    from jqdata.client import JQDataClient
    from config.config_manager import get_config_manager
    from jqdatasdk import auth, get_account_info, is_auth
    
    jq_client = JQDataClient()
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if not jq_config:
        raise ValueError("未找到JQData配置")
    
    # 认证JQData
    if not jq_client.is_authenticated():
        jq_client.authenticate(jq_config['username'], jq_config['password'])
    
    # 同时使用jqdatasdk认证（用于get_account_info）
    auth(jq_config['username'], jq_config['password'])
    
    if not jq_client.is_authenticated() or not is_auth():
        raise ValueError("JQData认证失败")
    
    # 获取权限信息
    perm = jq_client.get_permission()
    print(f"  ✅ JQData: 已连接并认证")
    print(f"     数据范围: {perm.start_date} 至 {perm.end_date}")
    print(f"     最新可用日期: {jq_client.get_available_end_date()}")
    
    # 获取账号信息
    try:
        jq_account_info = get_account_info()
        if jq_account_info:
            print(f"     每日流量限制: {jq_account_info.get('query_count_limit', 'N/A'):,} 条")
            print(f"     账号有效期: {jq_account_info.get('expire_time', 'N/A')}")
    except Exception as e:
        log_error('jqdata_errors', e, "获取账号信息")
    
    jq_status = True
    
except Exception as e:
    log_error('jqdata_errors', e, "JQData连接")
    print(f"  ❌ JQData: 连接失败 - {e}")

# 检查AKShare
ak_status = False
try:
    import akshare as ak
    test_df = ak.stock_fund_flow_concept(symbol="即时")
    if test_df is not None and len(test_df) > 0:
        print(f"  ✅ AKShare: 已连接 (概念资金流 {len(test_df)} 条)")
        ak_status = True
    else:
        print("  ⚠️ AKShare: 连接但无数据")
except Exception as e:
    log_error('akshare_errors', e, "AKShare连接")
    print(f"  ❌ AKShare: 连接失败 - {e}")

if not jq_status:
    print("\n❌ JQData连接失败，无法继续测试")
    sys.exit(1)

print()

# ==================== Step 2: 获取候选股票 ====================
print("📊 Step 2: 获取候选股票...")
print("-" * 50)

candidate_stocks = []

try:
    # 优先从指数获取（更可靠）
    if jq_client:
        test_symbols = []
        
        # 获取权限范围内的最新日期
        available_date = jq_client.get_available_end_date()
        print(f"  使用权限范围内的日期: {available_date}")
        
        # 获取沪深300成分股
        try:
            hs300 = jq_client.get_index_stocks("000300.XSHG", date=available_date)
            if hs300 and len(hs300) > 0:
                test_symbols.extend(hs300[:8])
                print(f"  ✅ 从沪深300获取: {len(hs300[:8])} 只")
            else:
                print(f"  ⚠️ 沪深300未返回数据")
        except Exception as e:
            log_error('jqdata_errors', e, "获取沪深300")
            print(f"  ⚠️ 获取沪深300失败: {str(e)[:50]}")
        
        # 获取创业板指成分股
        try:
            cyb = jq_client.get_index_stocks("399006.XSHE", date=available_date)
            if cyb and len(cyb) > 0:
                test_symbols.extend(cyb[:8])
                print(f"  ✅ 从创业板指获取: {len(cyb[:8])} 只")
            else:
                print(f"  ⚠️ 创业板指未返回数据")
        except Exception as e:
            log_error('jqdata_errors', e, "获取创业板指")
            print(f"  ⚠️ 获取创业板指失败: {str(e)[:50]}")
        
        # 去重并限制数量
        test_symbols = list(set(test_symbols))[:15]
        
        if test_symbols:
            # 获取股票信息
            try:
                all_secs = jq_client.get_all_securities(['stock'], date=available_date)
                
                for symbol in test_symbols:
                    try:
                        if all_secs is not None and symbol in all_secs.index:
                            name = all_secs.loc[symbol, 'display_name']
                        else:
                            name = symbol
                        candidate_stocks.append({
                            "symbol": symbol,
                            "name": name,
                            "data": {}
                        })
                    except Exception as e:
                        log_error('jqdata_errors', e, f"获取股票信息 {symbol}")
                        candidate_stocks.append({
                            "symbol": symbol,
                            "name": symbol,
                            "data": {}
                        })
            except Exception as e:
                log_error('jqdata_errors', e, "获取所有证券信息")
                # 使用股票代码作为名称
                for symbol in test_symbols:
                    candidate_stocks.append({
                        "symbol": symbol,
                        "name": symbol,
                        "data": {}
                    })
        else:
            raise ValueError("未获取到候选股票")
            
except Exception as e:
    log_error('jqdata_errors', e, "获取候选股票")
    print(f"  ❌ 获取候选股票失败: {e}")

# 如果没有获取到，使用测试数据
if not candidate_stocks:
    print("  ⚠️ 使用测试候选股票...")
    candidate_stocks = [
        {"symbol": "000001.XSHE", "name": "平安银行", "data": {}},
        {"symbol": "600519.XSHG", "name": "贵州茅台", "data": {}},
        {"symbol": "300750.XSHE", "name": "宁德时代", "data": {}},
    ]

print(f"  ✅ 候选股票: {len(candidate_stocks)} 只")
for s in candidate_stocks[:5]:
    print(f"    - {s['symbol']} {s['name']}")
if len(candidate_stocks) > 5:
    print(f"    ... 等共 {len(candidate_stocks)} 只")
print()

# ==================== Step 3: 获取财务和市场数据 ====================
print("📈 Step 3: 获取财务和市场数据...")
print("-" * 50)

def fetch_stock_data(symbol: str, jq: JQDataClient = None) -> dict:
    """
    获取单只股票的完整评估数据
    
    符合JQData聚宽数据规范：
    - 使用indicator表的标准字段（snake_case）
    - 使用valuation表的标准字段
    - 使用get_price获取价格数据
    - 完善的错误处理
    """
    try:
        from mcp_servers.utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher
        
        if not jq or not jq.is_authenticated():
            raise ValueError("JQData未认证")
        
        fetcher = TenbaggerDataFetcher(jq_client=jq)
        data = fetcher.fetch_complete_data(symbol)
        
        # 验证数据完整性
        required_fields = ['roe', 'revenue_growth', 'profit_growth', 'pe_ratio', 'latest_close']
        filled_count = sum(1 for field in required_fields if data.get(field) is not None and data.get(field) != 0)
        data_quality = filled_count / len(required_fields)
        
        if data_quality < 0.3:
            logger.warning(f"{symbol}: 数据完整度较低 ({data_quality:.1%})")
        
        return data
        
    except Exception as e:
        log_error('data_fetch_errors', e, f"获取数据 {symbol}")
        logger.warning(f"{symbol}: 数据获取失败，使用默认数据 - {str(e)[:50]}")
        return _get_default_data()

def _get_default_data() -> dict:
    """获取默认数据（当真实数据获取失败时使用）"""
    return {
        # L0 硬过滤默认值
        "is_st": False,
        "delisting_risk": False,
        "major_violation": False,
        "trading_days_ratio": 0.95,
        "financial_report_count": 4,
        "avg_turnover": 0.02,
        "missing_ratio": 0.2,
        # 财务数据（默认值）
        "revenue_growth": 0,
        "profit_growth": 0,
        "revenue_growth_qoq_change": 0,
        "profit_growth_change": 0,
        "gross_margin": 0,
        "gross_margin_change": 0,
        "roe": 0,
        "roa": 0,
        "net_profit_margin": 0,
        "eps": 0,
        "debt_ratio": 50,
        "current_ratio": 1.5,
        "cash_flow_improvement": False,
        "cash_flow_ratio": 0,
        "consecutive_improvement_quarters": 0,
        "cash_flow_negative_years": 0,
        # 估值数据（默认值）
        "pe_ratio": 20,
        "pb_ratio": 2,
        "ps_ratio": 2,
        "pcf_ratio": 10,
        "market_cap": 100,
        "circulating_market_cap": 80,
        "turnover_ratio": 1,
        # 市场数据（默认值）
        "latest_close": 0,
        "latest_volume": 0,
        "price_change_pct": 0,
        "volume_ratio": 1.0,
        "ma_trend": "neutral",
        "relative_strength": 50,
        "breakout_signal": False,
        # 其他默认值
        "event_count": 0,
        "market_cap_percentile": 0.5,
        "pe_percentile": 0.5,
        "analyst_coverage": 0,
        "research_report_count": 0,
        "announcement_count_3m": 0,
        "research_coverage_change": 0,
        "analyst_rating_upgrade": False,
        "industry_event_count": 0,
        "pe_rerating_signal": False,
        "institutional_ownership": 0,
        "short_debt_ratio": 0.5,
        "goodwill_ratio": 0.1,
        "non_recurring_ratio": 0.1,
        "pledge_ratio": 0.05,
        "near_pledge_liquidation": False,
        "receivable_revenue_ratio": 0.2,
        "inventory_revenue_ratio": 0.2,
        "audit_opinion": "standard",
        "has_major_lawsuit": False,
        "continuous_loss_years": 0,
        "data_quality": 0.0,
    }

# 为每只股票获取数据
print(f"  获取 {len(candidate_stocks)} 只股票数据...")
print("  使用JQData标准字段（indicator + valuation + get_price）...")

success_count = 0
fail_count = 0

for stock in candidate_stocks:
    try:
        stock["data"] = fetch_stock_data(stock["symbol"], jq_client)
        
        # 检查数据质量
        data_quality = stock["data"].get("data_quality", 0)
        if data_quality > 0.3:
            success_count += 1
            filled_fields = [k for k in ['roe', 'revenue_growth', 'profit_growth', 'pe_ratio', 'latest_close'] 
                           if stock["data"].get(k) and stock["data"].get(k) != 0]
            print(f"    {stock['symbol']}: ✅ 数据获取成功 (完整度: {data_quality:.0%}, 字段: {len(filled_fields)}/5)")
        else:
            fail_count += 1
            print(f"    {stock['symbol']}: ⚠️ 数据获取成功但完整度较低 ({data_quality:.0%})")
    except Exception as e:
        fail_count += 1
        log_error('data_fetch_errors', e, f"获取数据 {stock['symbol']}")
        print(f"    {stock['symbol']}: ❌ 数据获取失败 - {str(e)[:50]}")

print(f"  ✅ 数据获取完成 (成功: {success_count}, 失败/低质量: {fail_count})")
print()

# ==================== Step 4: V2系统评估 ====================
print("🔍 Step 4: V2系统评估...")
print("-" * 50)

try:
    from mcp_servers.utils.tenbagger_v2 import (
        get_evaluator_v2,
        get_candidate_funnel,
        get_rule_engine,
        get_scoring_engine_v2,
        get_tri_axis_stage_machine,
        get_pass_rate_controller,
        ReportGenerator
    )
    
    # 获取评估器（重置状态）
    evaluator = get_evaluator_v2()
    evaluator.reset()
    
    # 批量评估
    print("  执行批量评估...")
    reports = evaluator.batch_evaluate(candidate_stocks)
    
    print()
    print("  📋 评估结果:")
    print("-" * 50)
    
    for report in reports:
        try:
            status = "✅ 推荐" if report.is_recommended else "❌ 不推荐"
            vetoed = "🚫 已否决" if report.is_vetoed else ""
            
            print(f"  {report.symbol} {report.name}")
            print(f"    状态: {status} {vetoed}")
            print(f"    等级: {report.recommendation_level} | 分数: {report.final_score:.1f}")
            print(f"    阶段: {report.stage} | 漏斗: {report.funnel_level}")
            print(f"    质量: {report.quality_flag} | 置信度: {report.data_quality:.0%}")
            
            if report.is_vetoed and report.veto_reasons:
                print(f"    否决原因: {report.veto_reasons[0][:50]}...")
            elif report.stage_evidence:
                print(f"    阶段证据: {report.stage_evidence[0][:50]}...")
            
            print()
        except Exception as e:
            log_error('evaluation_errors', e, f"处理评估结果 {report.symbol if hasattr(report, 'symbol') else 'unknown'}")
            print(f"  ⚠️ 处理评估结果失败: {str(e)[:50]}")
            print()
    
except Exception as e:
    log_error('evaluation_errors', e, "V2系统评估")
    print(f"  ❌ V2系统评估失败: {e}")
    traceback.print_exc()
    sys.exit(1)

# ==================== Step 5: 统计和通过率 ====================
print("📊 Step 5: 统计和通过率检查...")
print("-" * 50)

try:
    stats = evaluator.get_stats()
    
    print(f"  总评估数: {stats['total_evaluated']}")
    print(f"  推荐数: {stats['recommended']}")
    print(f"  推荐率: {stats['recommended'] / max(1, stats['total_evaluated']):.1%}")
    print(f"  否决数: {stats['rejected']}")
    print()
    
    print("  等级分布:")
    for level in ["S+", "S", "A", "B", "C", "D", "REJECTED"]:
        count = stats["by_level"].get(level, 0)
        if count > 0:
            bar = "█" * count
            print(f"    {level:8s}: {bar} ({count})")
    
    print()
    print("  阶段分布:")
    stage_desc = {"S0": "观察", "S1": "验证", "S2": "导入★", "S3": "放量", "S4": "加速", "S5": "成熟"}
    for stage in ["S0", "S1", "S2", "S3", "S4", "S5"]:
        count = stats["by_stage"].get(stage, 0)
        if count > 0:
            bar = "█" * count
            desc = stage_desc.get(stage, "")
            print(f"    {stage} {desc:6s}: {bar} ({count})")
    
    print()
    
    # 通过率检查
    consistency = evaluator.generate_consistency_report()
    print("  通过率控制检查:")
    print(f"    L2通过率: {consistency.stats.l2_pass_rate:.1%}")
    print(f"    目标范围: 5%-20%")
    if consistency.warnings:
        for warning in consistency.warnings:
            print(f"    ⚠️ {warning}")
    else:
        print("    ✅ 通过率正常")
    
    print()
    
except Exception as e:
    log_error('evaluation_errors', e, "统计和通过率检查")
    print(f"  ❌ 统计失败: {e}")

# ==================== Step 6: 生成报告 ====================
print("📝 Step 6: 生成推荐报告...")
print("-" * 50)

try:
    generator = ReportGenerator(evaluator)
    
    # 生成Markdown报告
    report_path = "/home/taotao/dev/QuantTest/TRQuant/docs/TENBAGGER_V2_E2E_REPORT.md"
    generator.save_report(report_path, format="markdown", filter_type="all")
    print(f"  ✅ Markdown报告: {report_path}")
    
    # 生成JSON报告
    json_path = "/home/taotao/dev/QuantTest/TRQuant/docs/TENBAGGER_V2_E2E_REPORT.json"
    generator.save_report(json_path, format="json", filter_type="all")
    print(f"  ✅ JSON报告: {json_path}")
    
    print()
    
except Exception as e:
    log_error('evaluation_errors', e, "生成报告")
    print(f"  ❌ 生成报告失败: {e}")

# ==================== 总结 ====================
print("=" * 70)
print("📊 端到端测试总结")
print("=" * 70)

print(f"""
数据源状态:
  - JQData: {"✅ 已连接" if jq_status else "❌ 未连接"}
  - AKShare: {"✅ 已连接" if ak_status else "❌ 未连接"}
""")

if jq_account_info:
    print(f"账号信息:")
    print(f"  - 每日流量限制: {jq_account_info.get('query_count_limit', 'N/A'):,} 条")
    print(f"  - 账号有效期: {jq_account_info.get('expire_time', 'N/A')}")
    print(f"  - 数据范围: {jq_account_info.get('date_range_start', 'N/A')[:10]} 至 {jq_account_info.get('date_range_end', 'N/A')[:10]}")
    print()

try:
    print(f"评估结果:")
    print(f"  - 候选股票: {len(candidate_stocks)} 只")
    print(f"  - 数据获取: 成功 {success_count}, 失败/低质量 {fail_count}")
    print(f"  - 总评估数: {stats['total_evaluated']}")
    print(f"  - 推荐数: {stats['recommended']}")
    print(f"  - 推荐率: {stats['recommended'] / max(1, stats['total_evaluated']):.1%}")
    print(f"  - 否决数: {stats['rejected']}")
    print()
    
    print("推荐列表 (A级及以上):")
    recommendations = evaluator.get_recommendations(min_level="A")
    if recommendations:
        for i, r in enumerate(recommendations, 1):
            print(f"  {i}. {r.symbol} {r.name} - {r.recommendation_level}级 ({r.final_score:.1f}分) [{r.stage}]")
    else:
        print("  无A级及以上推荐")
    print()
except:
    pass

# 错误统计
if any(error_stats.values()):
    print("错误统计:")
    for category, errors in error_stats.items():
        if errors:
            print(f"  - {category}: {len(errors)} 个错误")
            if len(errors) <= 3:
                for err in errors:
                    print(f"    • {err[:60]}")
    print()

print(f"报告文件:")
print(f"  - {report_path}")
print(f"  - {json_path}")
print()
print("测试完成!")
print("=" * 70)
