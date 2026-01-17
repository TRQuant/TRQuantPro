#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Extension Bridge
========================

与VS Code/Cursor Extension通信的Python桥接模块。
通过stdin/stdout传输JSON数据。
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# 导入工作流直接调用模块
try:
    from workflow_direct import run_workflow_step, get_workflow_context, clear_workflow_context
    WORKFLOW_DIRECT_AVAILABLE = True
except ImportError:
    WORKFLOW_DIRECT_AVAILABLE = False


# 添加TRQuant路径
# bridge.py 位于 TRQuant/extension/python/bridge.py
# 所以 parent.parent 是 extension/, parent.parent.parent 是 TRQuant/
_bridge_dir = Path(__file__).resolve().parent  # python/
_extension_dir = _bridge_dir.parent  # extension/
TRQUANT_ROOT = os.environ.get('TRQUANT_ROOT', str(_extension_dir.parent))  # TRQuant/

# 按顺序添加到sys.path
for _path in [TRQUANT_ROOT, os.path.join(TRQUANT_ROOT, 'mcp_servers')]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

try:
    from core.trend_analyzer import TrendAnalyzer
    from core.candidate_pool_builder import CandidatePoolBuilder
    from core.factors.factor_manager import FactorManager
    from core.strategy_generator import StrategyGenerator
    from core.workflow_orchestrator import get_workflow_orchestrator
    TRQUANT_AVAILABLE = True
except ImportError as e:
    TRQUANT_AVAILABLE = False
    IMPORT_ERROR = str(e)


def get_market_status(params: dict) -> dict:
    """获取市场状态"""
    if not TRQUANT_AVAILABLE:
        return mock_market_status()
    
    try:
        orchestrator = get_workflow_orchestrator()
        result = orchestrator.analyze_market_trend()
        
        if result.success:
            return {
                'ok': True,
                'data': {
                    'regime': result.details.get('position_suggestion', 'neutral'),
                    'index_trend': result.details.get('index_trend', {}),
                    'style_rotation': result.details.get('style_rotation', []),
                    'summary': result.summary
                }
            }
        else:
            return {'ok': False, 'error': result.summary}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def get_mainlines(params: dict) -> dict:
    """获取投资主线"""
    if not TRQUANT_AVAILABLE:
        return mock_mainlines()
    
    try:
        orchestrator = get_workflow_orchestrator()
        result = orchestrator.identify_mainlines()
        
        if result.success:
            mainlines = result.details.get('mainlines', [])
            return {
                'ok': True,
                'data': [
                    {
                        'name': m.get('name', ''),
                        'score': m.get('score', 0),
                        'industries': m.get('industries', []),
                        'logic': m.get('logic', '')
                    }
                    for m in mainlines[:params.get('top_n', 20)]
                ]
            }
        else:
            return {'ok': False, 'error': result.summary}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def recommend_factors(params: dict) -> dict:
    """推荐因子"""
    if not TRQUANT_AVAILABLE:
        return mock_factors()
    
    try:
        orchestrator = get_workflow_orchestrator()
        result = orchestrator.recommend_factors()
        
        if result.success:
            factors = result.details.get('factors', [])
            return {
                'ok': True,
                'data': [
                    {
                        'name': f.get('name', ''),
                        'category': f.get('category', '其他'),
                        'weight': f.get('weight', 0.5),
                        'reason': f.get('reason', '')
                    }
                    for f in factors
                ]
            }
        else:
            return {'ok': False, 'error': result.summary}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def generate_strategy(params: dict) -> dict:
    """生成策略代码"""
    platform = params.get('platform', 'ptrade')
    style = params.get('style', 'multi_factor')
    factors = params.get('factors', ['ROE_ttm', 'momentum_20d'])
    risk_params = params.get('risk_params', {
        'max_position': 0.1,
        'stop_loss': 0.08,
        'take_profit': 0.2
    })
    
    try:
        from tools.strategy_generator import get_strategy_generator
        generator = get_strategy_generator()
        
        result = generator.generate(
            platform=platform,
            style=style,
            factors=factors,
            risk_params=risk_params
        )
        
        return {'ok': True, 'data': result}
    except ImportError:
        return mock_strategy(params)
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def analyze_backtest(params: dict) -> dict:
    """分析回测结果"""
    return {
        'ok': True,
        'data': {
            'metrics': {
                'total_return': 15.5,
                'sharpe_ratio': 1.2,
                'max_drawdown': -8.3,
                'win_rate': 56.0
            },
            'diagnosis': ['策略在震荡市表现较好'],
            'suggestions': ['考虑增加止损机制']
        }
    }


def risk_assessment(params: dict) -> dict:
    """风险评估"""
    return {
        'ok': True,
        'data': {
            'overall_risk': 'medium',
            'metrics': {'var_95': -2.5, 'beta': 0.85},
            'warnings': []
        }
    }


def run_backtest(params: dict) -> dict:
    """运行回测"""
    try:
        from tools.backtest_engine import run_backtest as execute_backtest
        
        strategy_code = params.get('strategy_code', '')
        config = params.get('config', {})
        data_source = params.get('data_source', 'akshare')
        
        result = execute_backtest(strategy_code, config, data_source)
        
        if result.get('success'):
            return {'ok': True, 'data': result.get('result', {})}
        else:
            return {'ok': False, 'error': result.get('error', '回测执行失败')}
    except Exception as e:
        import traceback
        return {'ok': False, 'error': str(e), 'traceback': traceback.format_exc()}


def health_check(params: dict) -> dict:
    """健康检查"""
    return {
        'ok': True,
        'data': {
            'status': 'healthy',
            'trquant_available': TRQUANT_AVAILABLE,
            'timestamp': datetime.now().isoformat()
        }
    }


def _get_jqdata_client():
    """获取已认证的JQData客户端"""
    try:
        from jqdata.client import JQDataClient
        from config.config_manager import get_config_manager
        
        client = JQDataClient()
        cm = get_config_manager()
        jq_config = cm.get_jqdata_config()
        
        if jq_config and jq_config.get('username') and jq_config.get('password'):
            client.authenticate(jq_config['username'], jq_config['password'])
            if client.is_authenticated():
                return client
        return None
    except Exception as e:
        import logging
        logging.warning(f"JQData初始化失败: {e}")
        return None


def call_workflow9_tool(tool_name: str, arguments: dict) -> dict:
    """调用9步工作流工具（直接调用，类似十倍股）"""
    import traceback
    import asyncio
    import json
    from datetime import datetime
    
    # #region agent log
    try:
        with open('/home/taotao/dev/QuantTest/TRQuant/.cursor/debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'sessionId': 'debug-session',
                'runId': 'run1',
                'hypothesisId': 'D',
                'location': 'bridge.py:243',
                'message': 'call_workflow9_tool entry',
                'data': {'tool_name': tool_name, 'arguments': arguments},
                'timestamp': int(datetime.now().timestamp() * 1000)
            }, ensure_ascii=False) + '\n')
    except: pass
    # #endregion
    
    try:
        # 添加 mcp_servers 到路径
        mcp_servers_path = os.path.join(TRQUANT_ROOT, 'mcp_servers')
        if mcp_servers_path not in sys.path:
            sys.path.insert(0, mcp_servers_path)
        
        # 确保项目根目录在路径中
        if TRQUANT_ROOT not in sys.path:
            sys.path.insert(0, TRQUANT_ROOT)
        
        # 导入工作流服务器
        from workflow_9steps_server import _handle_tool
        
        # #region agent log
        try:
            with open('/home/taotao/dev/QuantTest/TRQuant/.cursor/debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'D',
                    'location': 'bridge.py:264',
                    'message': 'before asyncio.run',
                    'data': {'tool_name': tool_name, 'has_arguments': bool(arguments)},
                    'timestamp': int(datetime.now().timestamp() * 1000)
                }, ensure_ascii=False) + '\n')
        except: pass
        # #endregion
        
        # ✅ 使用asyncio.run()（Python 3.7+推荐方式）
        # 自动创建和管理事件循环，避免冲突和DeprecationWarning
        # 参考：FastMCP和标准MCP服务器都使用这种方式
        result = asyncio.run(_handle_tool(tool_name, arguments))
        
        # #region agent log
        try:
            with open('/home/taotao/dev/QuantTest/TRQuant/.cursor/debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'C',
                    'location': 'bridge.py:270',
                    'message': 'after asyncio.run',
                    'data': {'result_type': type(result).__name__, 'is_dict': isinstance(result, dict), 'has_success': isinstance(result, dict) and 'success' in result, 'result_keys': list(result.keys()) if isinstance(result, dict) else []},
                    'timestamp': int(datetime.now().timestamp() * 1000)
                }, ensure_ascii=False) + '\n')
        except: pass
        # #endregion
        
        # 确保返回格式一致
        if isinstance(result, dict):
            if 'success' not in result:
                result['success'] = True
            return_value = {'ok': result.get('success', True), 'data': result, 'error': result.get('error')}
        else:
            return_value = {'ok': True, 'data': result}
        
        # #region agent log
        try:
            with open('/home/taotao/dev/QuantTest/TRQuant/.cursor/debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'C',
                    'location': 'bridge.py:280',
                    'message': 'call_workflow9_tool exit success',
                    'data': {'ok': return_value.get('ok'), 'has_data': 'data' in return_value, 'has_error': bool(return_value.get('error'))},
                    'timestamp': int(datetime.now().timestamp() * 1000)
                }, ensure_ascii=False) + '\n')
        except: pass
        # #endregion
        
        return return_value
            
    except Exception as e:
        import traceback
        error_msg = f'Workflow9工具调用失败: {str(e)}'
        logger.error(f'{error_msg}\n{traceback.format_exc()}')
        
        # #region agent log
        try:
            with open('/home/taotao/dev/QuantTest/TRQuant/.cursor/debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'run1',
                    'hypothesisId': 'D',
                    'location': 'bridge.py:285',
                    'message': 'call_workflow9_tool exception',
                    'data': {'error': str(e), 'error_type': type(e).__name__},
                    'timestamp': int(datetime.now().timestamp() * 1000)
                }, ensure_ascii=False) + '\n')
        except: pass
        # #endregion
        
        return {
            'ok': False, 
            'error': error_msg,
            'traceback': traceback.format_exc(),
            'hint': '请检查：1) workflow_9steps_server 模块是否可用 2) 依赖是否安装完整'
        }


def call_tenbagger_tool(tool_name: str, arguments: dict) -> dict:
    """调用完整的十倍股V2评估系统"""
    import traceback
    
    try:
        # 添加 mcp_servers 到路径
        mcp_servers_path = os.path.join(TRQUANT_ROOT, 'mcp_servers')
        if mcp_servers_path not in sys.path:
            sys.path.insert(0, mcp_servers_path)
        
        # ============ JQData金融数据功能 ============
        if tool_name == 'tenbagger.jqdata_scan':
            # 从JQData扫描并评估
            return _jqdata_scan_and_evaluate(arguments)
        
        elif tool_name == 'tenbagger.jqdata_stock':
            # 获取单只股票的JQData数据
            return _get_jqdata_stock(arguments)
        
        elif tool_name == 'tenbagger.jqdata_filter':
            # JQData条件筛选
            return _jqdata_filter(arguments)
        
        
        # ============ 数据库相关功能 ============
        elif tool_name == 'tenbagger.db_rankings':
            # 从数据库获取排名
            return _get_db_rankings(arguments)
        
        elif tool_name == 'tenbagger.db_stages':
            # 获取阶段记录
            return _get_db_stages(arguments)
        
        elif tool_name == 'tenbagger.db_scorecards':
            # 获取评分卡
            return _get_db_scorecards(arguments)
        
        elif tool_name == 'tenbagger.db_stats':
            # 获取数据库统计
            return _get_db_stats()
        
        elif tool_name == 'tenbagger.scan':
            # 扫描候选池
            return _scan_candidates(arguments)
        
        elif tool_name == 'tenbagger.refresh':
            # 刷新数据（重新评估）
            return _refresh_tenbagger_data(arguments)
        
        # ============ 评估功能 ============
        elif tool_name == 'tenbagger.evaluate':
            return _evaluate_stock(arguments)
        
        elif tool_name == 'tenbagger.report':
            return _get_report(arguments)
            
        elif tool_name == 'tenbagger.rank':
            return _get_rankings(arguments)
            
        elif tool_name == 'tenbagger.filter':
            return _filter_stocks(arguments)
            
        elif tool_name == 'tenbagger.stats':
            return _get_stats()
            
        elif tool_name == 'tenbagger.batch':
            return _batch_evaluate(arguments)
        
        return {'ok': False, 'error': f'未知的tenbagger工具: {tool_name}'}
        
    except Exception as e:
        return {'ok': False, 'error': f'Tenbagger工具调用失败: {str(e)}', 'traceback': traceback.format_exc()}


def _jqdata_scan_and_evaluate(args: dict) -> dict:
    """从JQData扫描并评估十倍股候选"""
    try:
        jq_client = _get_jqdata_client()
        if not jq_client:
            return {'ok': False, 'error': 'JQData未配置，请检查config/jqdata_config.yaml'}
        
        from jqdatasdk import query, valuation, indicator
        from utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher
        from utils.tenbagger_v2 import get_evaluator_v2
        
        # 筛选参数
        min_market_cap = args.get('min_market_cap', 20)  # 最小市值（亿）
        max_market_cap = args.get('max_market_cap', 300)  # 最大市值（亿）
        min_roe = args.get('min_roe', 8)  # 最低ROE
        min_revenue_growth = args.get('min_revenue_growth', 15)  # 最低营收增速
        limit = args.get('limit', 30)  # 最多返回数量
        
        end_date = jq_client.get_available_end_date()
        
        # JQData筛选
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.roe,
            indicator.inc_revenue_year_on_year,
            indicator.inc_net_profit_year_on_year,
            indicator.gross_profit_margin
        ).filter(
            valuation.market_cap >= min_market_cap,
            valuation.market_cap <= max_market_cap,
            indicator.roe >= min_roe,
            indicator.inc_revenue_year_on_year >= min_revenue_growth
        ).order_by(
            indicator.inc_net_profit_year_on_year.desc()
        ).limit(limit * 2)  # 多取一些以备过滤
        
        df = jq_client.get_fundamentals(q, date=end_date)
        
        if df is None or df.empty:
            return {'ok': True, 'data': {'count': 0, 'stocks': [], 'source': 'jqdata'}}
        
        # 过滤ST股票
        all_secs = jq_client.get_all_securities(['stock'])
        
        fetcher = TenbaggerDataFetcher(jq_client)
        evaluator = get_evaluator_v2()
        
        results = []
        for _, row in df.iterrows():
            code = row['code']
            
            # 过滤ST
            if code in all_secs.index:
                name = all_secs.loc[code, 'display_name']
                if 'ST' in name or '*ST' in name:
                    continue
            else:
                name = code
            
            # 获取完整数据并评估
            try:
                data = fetcher.fetch_complete_data(code)
                
                # 简化评估 - 计算综合分数
                roe = row['roe'] if row['roe'] else 0
                revenue_g = row['inc_revenue_year_on_year'] if row['inc_revenue_year_on_year'] else 0
                profit_g = row['inc_net_profit_year_on_year'] if row['inc_net_profit_year_on_year'] else 0
                gross_m = row['gross_profit_margin'] if row['gross_profit_margin'] else 0
                
                # 简单的评分公式
                score = min(100, max(0, 
                    roe * 1.5 +  # ROE权重
                    min(revenue_g, 50) * 0.5 +  # 营收增速
                    min(profit_g, 50) * 0.8 +  # 利润增速
                    gross_m * 0.3  # 毛利率
                ))
                
                # 确定等级
                if score >= 80: level = 'S+'
                elif score >= 70: level = 'S'
                elif score >= 60: level = 'A'
                elif score >= 50: level = 'B'
                elif score >= 40: level = 'C'
                else: level = 'D'
                
                results.append({
                    'symbol': code,
                    'name': name,
                    'market_cap': round(row['market_cap'], 2),
                    'roe': round(roe, 2),
                    'revenue_growth': round(revenue_g, 2),
                    'profit_growth': round(profit_g, 2),
                    'gross_margin': round(gross_m, 2),
                    'score': round(score, 1),
                    'level': level,
                    'stage': 'S1' if score >= 60 else 'S0'
                })
            except Exception as e:
                logger.warning(f"评估 {code} 失败: {e}")
                continue
            
            if len(results) >= limit:
                break
        
        # 按评分排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return {'ok': True, 'data': {
            'count': len(results),
            'stocks': results,
            'date': end_date,
            'filters': {
                'market_cap': f'{min_market_cap}-{max_market_cap}亿',
                'min_roe': f'{min_roe}%',
                'min_revenue_growth': f'{min_revenue_growth}%'
            },
            'source': 'jqdata'
        }}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'JQData扫描失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_jqdata_stock(args: dict) -> dict:
    """获取单只股票的JQData详细数据"""
    try:
        jq_client = _get_jqdata_client()
        if not jq_client:
            return {'ok': False, 'error': 'JQData未配置'}
        
        symbol = args.get('symbol', '')
        if not symbol:
            return {'ok': False, 'error': '请提供股票代码'}
        
        mcp_path = os.path.join(TRQUANT_ROOT, 'mcp_servers')
        if mcp_path not in sys.path:
            sys.path.insert(0, mcp_path)
        
        from utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher
        
        fetcher = TenbaggerDataFetcher(jq_client)
        data = fetcher.fetch_complete_data(symbol)
        
        # 评估
        from utils.tenbagger_v2 import get_evaluator_v2
        evaluator = get_evaluator_v2()
        name = data.get('stock_name', symbol)
        report = evaluator.evaluate(symbol, name, data)
        
        return {'ok': True, 'data': {
            'symbol': symbol,
            'name': name,
            'financials': {
                'roe': data.get('roe'),
                'roa': data.get('roa'),
                'gross_margin': data.get('gross_margin'),
                'revenue_growth': data.get('revenue_growth'),
                'profit_growth': data.get('profit_growth'),
            },
            'valuation': {
                'pe_ratio': data.get('pe_ratio'),
                'pb_ratio': data.get('pb_ratio'),
                'ps_ratio': data.get('ps_ratio'),
                'market_cap': data.get('market_cap'),
            },
            'technicals': {
                'price_change_pct': data.get('price_change_pct'),
                'volume_ratio': data.get('volume_ratio'),
                'ma_trend': data.get('ma_trend'),
                'relative_strength': data.get('relative_strength'),
                'breakout_signal': data.get('breakout_signal'),
            },
            'evaluation': {
                'score': round(report.final_score if hasattr(report, 'final_score') else report.total_score, 1),
                'level': report.level.value if hasattr(report, 'level') else report.eval_level.value,
                'stage': report.stage if hasattr(report, 'stage') else 'S0',
            },
            'data_quality': data.get('data_quality', 0),
            'source': 'jqdata'
        }}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'获取股票数据失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_akshare_realtime(args: dict) -> dict:
    """获取实时行情（AKShare）"""
    try:
        import akshare as ak
        
        symbols = args.get('symbols', [])
        if not symbols:
            return {'ok': False, 'error': '请提供股票代码列表'}
        
        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        
        if df is None or df.empty:
            return {'ok': False, 'error': 'AKShare数据获取失败'}
        
        # 过滤指定股票
        codes = [s.split('.')[0] for s in symbols]  # 去掉后缀
        df = df[df['代码'].isin(codes)]
        
        results = []
        for _, row in df.iterrows():
            code = row['代码']
            # 添加后缀
            if code.startswith('6'):
                full_code = f"{code}.XSHG"
            else:
                full_code = f"{code}.XSHE"
            
            results.append({
                'symbol': full_code,
                'name': row.get('名称', ''),
                'price': float(row.get('最新价', 0) or 0),
                'change': float(row.get('涨跌幅', 0) or 0),
                'change_amount': float(row.get('涨跌额', 0) or 0),
                'volume': float(row.get('成交量', 0) or 0),
                'amount': float(row.get('成交额', 0) or 0),
                'open': float(row.get('今开', 0) or 0),
                'high': float(row.get('最高', 0) or 0),
                'low': float(row.get('最低', 0) or 0),
                'prev_close': float(row.get('昨收', 0) or 0),
                'turnover': float(row.get('换手率', 0) or 0),
                'pe': float(row.get('市盈率-动态', 0) or 0),
                'pb': float(row.get('市净率', 0) or 0),
                'market_cap': float(row.get('总市值', 0) or 0) / 1e8,  # 转为亿
            })
        
        return {'ok': True, 'data': {
            'count': len(results),
            'stocks': results,
            'source': 'akshare',
            'timestamp': datetime.now().isoformat()
        }}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'AKShare实时行情失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_akshare_spot(args: dict) -> dict:
    """获取A股全市场实时数据（AKShare）"""
    try:
        import akshare as ak
        
        limit = args.get('limit', 100)
        sort_by = args.get('sort_by', 'amount')  # amount/change/turnover
        ascending = args.get('ascending', False)
        
        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        
        if df is None or df.empty:
            return {'ok': False, 'error': 'AKShare数据获取失败'}
        
        # 排序字段映射
        sort_map = {
            'amount': '成交额',
            'change': '涨跌幅',
            'turnover': '换手率',
            'volume': '成交量',
            'price': '最新价'
        }
        sort_col = sort_map.get(sort_by, '成交额')
        
        # 过滤掉无效数据
        df = df[df['最新价'].notna() & (df['最新价'] > 0)]
        
        # 排序
        if sort_col in df.columns:
            df = df.sort_values(sort_col, ascending=ascending)
        
        df = df.head(limit)
        
        results = []
        for _, row in df.iterrows():
            code = row['代码']
            if code.startswith('6'):
                full_code = f"{code}.XSHG"
            else:
                full_code = f"{code}.XSHE"
            
            results.append({
                'symbol': full_code,
                'name': row.get('名称', ''),
                'price': float(row.get('最新价', 0) or 0),
                'change': float(row.get('涨跌幅', 0) or 0),
                'volume': float(row.get('成交量', 0) or 0) / 10000,  # 转为万手
                'amount': float(row.get('成交额', 0) or 0) / 1e8,  # 转为亿
                'turnover': float(row.get('换手率', 0) or 0),
                'pe': float(row.get('市盈率-动态', 0) or 0),
                'market_cap': float(row.get('总市值', 0) or 0) / 1e8,  # 转为亿
            })
        
        return {'ok': True, 'data': {
            'count': len(results),
            'stocks': results,
            'sort_by': sort_by,
            'source': 'akshare',
            'timestamp': datetime.now().isoformat()
        }}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'AKShare市场数据失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_akshare_hot(args: dict) -> dict:
    """获取热门股票/板块（AKShare）"""
    try:
        import akshare as ak
        
        category = args.get('category', 'stock')  # stock/industry/concept
        limit = args.get('limit', 20)
        
        if category == 'industry':
            # 行业板块涨幅排名
            df = ak.stock_board_industry_name_em()
            if df is not None and not df.empty:
                results = []
                for _, row in df.head(limit).iterrows():
                    results.append({
                        'name': row.get('板块名称', ''),
                        'change': float(row.get('涨跌幅', 0) or 0),
                        'leader': row.get('领涨股票', ''),
                        'leader_change': float(row.get('领涨股票-涨跌幅', 0) or 0),
                    })
                return {'ok': True, 'data': {'count': len(results), 'items': results, 'category': 'industry', 'source': 'akshare'}}
        
        elif category == 'concept':
            # 概念板块涨幅排名
            df = ak.stock_board_concept_name_em()
            if df is not None and not df.empty:
                results = []
                for _, row in df.head(limit).iterrows():
                    results.append({
                        'name': row.get('板块名称', ''),
                        'change': float(row.get('涨跌幅', 0) or 0),
                        'leader': row.get('领涨股票', ''),
                        'leader_change': float(row.get('领涨股票-涨跌幅', 0) or 0),
                    })
                return {'ok': True, 'data': {'count': len(results), 'items': results, 'category': 'concept', 'source': 'akshare'}}
        
        else:
            # 涨幅榜
            df = ak.stock_zh_a_spot_em()
            if df is not None and not df.empty:
                df = df[df['最新价'].notna() & (df['最新价'] > 0)]
                df = df.sort_values('涨跌幅', ascending=False).head(limit)
                results = []
                for _, row in df.iterrows():
                    code = row['代码']
                    if code.startswith('6'):
                        full_code = f"{code}.XSHG"
                    else:
                        full_code = f"{code}.XSHE"
                    results.append({
                        'symbol': full_code,
                        'name': row.get('名称', ''),
                        'price': float(row.get('最新价', 0) or 0),
                        'change': float(row.get('涨跌幅', 0) or 0),
                        'amount': float(row.get('成交额', 0) or 0) / 1e8,
                    })
                return {'ok': True, 'data': {'count': len(results), 'items': results, 'category': 'stock', 'source': 'akshare'}}
        
        return {'ok': False, 'error': '无数据'}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'AKShare热门数据失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_akshare_price(args: dict) -> dict:
    """获取历史价格（AKShare）"""
    try:
        import akshare as ak
        
        symbol = args.get('symbol', '')
        if not symbol:
            return {'ok': False, 'error': '请提供股票代码'}
        
        days = args.get('days', 60)
        
        # 去掉后缀
        code = symbol.split('.')[0]
        
        # 计算日期
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
        
        df = ak.stock_zh_a_hist(
            symbol=code,
            period='daily',
            start_date=start_date,
            end_date=end_date,
            adjust='qfq'
        )
        
        if df is None or df.empty:
            return {'ok': False, 'error': '未获取到价格数据'}
        
        prices = []
        for _, row in df.iterrows():
            prices.append({
                'date': str(row.get('日期', '')),
                'open': float(row.get('开盘', 0)),
                'high': float(row.get('最高', 0)),
                'low': float(row.get('最低', 0)),
                'close': float(row.get('收盘', 0)),
                'volume': float(row.get('成交量', 0)),
                'amount': float(row.get('成交额', 0)),
                'change': float(row.get('涨跌幅', 0) or 0),
            })
        
        # 计算一些技术指标
        if len(prices) > 0:
            latest = prices[-1]
            first = prices[0]
            period_change = (latest['close'] / first['close'] - 1) * 100 if first['close'] > 0 else 0
        else:
            period_change = 0
        
        return {'ok': True, 'data': {
            'symbol': symbol,
            'count': len(prices),
            'prices': prices,
            'period_change': round(period_change, 2),
            'source': 'akshare',
            'timestamp': datetime.now().isoformat()
        }}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'AKShare价格数据失败: {str(e)}', 'traceback': traceback.format_exc()}


def _jqdata_filter(args: dict) -> dict:
    """JQData条件筛选"""
    try:
        jq_client = _get_jqdata_client()
        if not jq_client:
            return {'ok': False, 'error': 'JQData未配置'}
        
        from jqdatasdk import query, valuation, indicator
        
        # 筛选条件
        index_code = args.get('index', '')  # hs300, zz500, zz1000
        min_market_cap = args.get('min_market_cap', 0)
        max_market_cap = args.get('max_market_cap', 10000)
        min_roe = args.get('min_roe', 0)
        min_revenue_growth = args.get('min_revenue_growth', -100)
        min_profit_growth = args.get('min_profit_growth', -100)
        limit = args.get('limit', 50)
        
        end_date = jq_client.get_available_end_date()
        
        # 构建查询
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.roe,
            indicator.inc_revenue_year_on_year,
            indicator.inc_net_profit_year_on_year
        ).filter(
            valuation.market_cap >= min_market_cap,
            valuation.market_cap <= max_market_cap
        )
        
        if min_roe > 0:
            q = q.filter(indicator.roe >= min_roe)
        if min_revenue_growth > -100:
            q = q.filter(indicator.inc_revenue_year_on_year >= min_revenue_growth)
        if min_profit_growth > -100:
            q = q.filter(indicator.inc_net_profit_year_on_year >= min_profit_growth)
        
        q = q.order_by(indicator.roe.desc()).limit(limit)
        
        df = jq_client.get_fundamentals(q, date=end_date)
        
        if df is None or df.empty:
            return {'ok': True, 'data': {'count': 0, 'stocks': [], 'source': 'jqdata'}}
        
        # 获取股票名称
        all_secs = jq_client.get_all_securities(['stock'])
        
        stocks = []
        for _, row in df.iterrows():
            code = row['code']
            name = all_secs.loc[code, 'display_name'] if code in all_secs.index else code
            
            # 过滤ST
            if 'ST' in name:
                continue
                
            stocks.append({
                'symbol': code,
                'name': name,
                'market_cap': round(row['market_cap'], 2),
                'roe': round(row['roe'], 2) if row['roe'] else 0,
                'revenue_growth': round(row['inc_revenue_year_on_year'], 2) if row['inc_revenue_year_on_year'] else 0,
                'profit_growth': round(row['inc_net_profit_year_on_year'], 2) if row['inc_net_profit_year_on_year'] else 0,
            })
        
        return {'ok': True, 'data': {
            'count': len(stocks),
            'stocks': stocks,
            'date': end_date,
            'source': 'jqdata'
        }}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'筛选失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_db_rankings(args: dict) -> dict:
    """从MongoDB获取排名数据"""
    try:
        from pymongo import MongoClient, DESCENDING
        
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=3000)
        db = client.get_database("trquant")
        
        min_score = args.get('min_score', 50)
        limit = args.get('limit', 50)
        
        # 从scorecards集合获取
        scorecards = list(db.scorecards.find(
            {"total_score": {"$gte": min_score}},
            {"_id": 0}
        ).sort("total_score", DESCENDING).limit(limit))
        
        return {'ok': True, 'data': {
            'count': len(scorecards),
            'rankings': scorecards,
            'source': 'mongodb'
        }}
    except Exception as e:
        # 如果数据库不可用，返回模拟数据
        return _get_mock_rankings(args)


def _get_db_stages(args: dict) -> dict:
    """从MongoDB获取阶段数据"""
    try:
        from pymongo import MongoClient, DESCENDING
        
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=3000)
        db = client.get_database("trquant")
        
        stage_filter = args.get('stage')
        limit = args.get('limit', 100)
        
        query = {}
        if stage_filter:
            query['current_stage'] = stage_filter
        
        stages = list(db.stages.find(query, {"_id": 0}).sort("confidence", DESCENDING).limit(limit))
        
        # 统计各阶段数量
        stage_counts = {}
        for s in ['S0', 'S1', 'S2', 'S3']:
            stage_counts[s] = db.stages.count_documents({'current_stage': s})
        
        return {'ok': True, 'data': {
            'stages': stages,
            'counts': stage_counts,
            'source': 'mongodb'
        }}
    except Exception as e:
        return _get_mock_stages(args)


def _get_db_scorecards(args: dict) -> dict:
    """从MongoDB获取评分卡"""
    try:
        from pymongo import MongoClient, DESCENDING
        
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=3000)
        db = client.get_database("trquant")
        
        symbol = args.get('symbol')
        if symbol:
            card = db.scorecards.find_one({'security_id': symbol}, {'_id': 0})
            return {'ok': True, 'data': {'scorecard': card} if card else {'scorecard': None}}
        
        min_grade = args.get('min_grade', 'C')
        grade_order = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'F': 5}
        
        cards = list(db.scorecards.find({}, {'_id': 0}).sort('total_score', DESCENDING).limit(50))
        filtered = [c for c in cards if grade_order.get(c.get('grade', 'F'), 5) <= grade_order.get(min_grade, 3)]
        
        return {'ok': True, 'data': {
            'count': len(filtered),
            'scorecards': filtered,
            'source': 'mongodb'
        }}
    except Exception as e:
        return _get_mock_scorecards(args)


def _get_db_stats() -> dict:
    """从MongoDB获取统计数据"""
    try:
        from pymongo import MongoClient
        
        client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=3000)
        db = client.get_database("trquant")
        
        # 评分卡统计
        total_scorecards = db.scorecards.count_documents({})
        grade_stats = {}
        for g in ['A', 'B', 'C', 'D', 'F']:
            grade_stats[g] = db.scorecards.count_documents({'grade': g})
        
        # 阶段统计
        stage_stats = {}
        for s in ['S0', 'S1', 'S2', 'S3']:
            stage_stats[s] = db.stages.count_documents({'current_stage': s})
        
        # 平均分
        pipeline = [{"$group": {"_id": None, "avg_score": {"$avg": "$total_score"}}}]
        avg_result = list(db.scorecards.aggregate(pipeline))
        avg_score = avg_result[0]['avg_score'] if avg_result else 0
        
        return {'ok': True, 'data': {
            'total_evaluated': total_scorecards,
            'by_grade': grade_stats,
            'by_stage': stage_stats,
            'avg_score': round(avg_score, 1),
            'source': 'mongodb'
        }}
    except Exception as e:
        return _get_mock_stats()


def _scan_candidates(args: dict) -> dict:
    """从JQData扫描候选股票池"""
    try:
        # 初始化JQData客户端
        jq_client = _get_jqdata_client()
        if not jq_client:
            return {'ok': False, 'error': 'JQData未配置或认证失败'}
        
        from core.candidate_pool_builder import CandidatePoolBuilder
        
        # 筛选参数
        min_market_cap = args.get('min_market_cap', 10)  # 亿
        max_market_cap = args.get('max_market_cap', 100)
        index_code = args.get('index', 'zz500')  # 默认中证500
        min_roe = args.get('min_roe', 5)  # 最低ROE
        
        builder = CandidatePoolBuilder(jq_client=jq_client)
        
        # 获取指数成分股
        import jqdatasdk as jq
        end_date = jq_client.get_available_end_date()
        
        index_map = {
            'hs300': '000300.XSHG',
            'zz500': '000905.XSHG',
            'zz1000': '000852.XSHG'
        }
        index_symbol = index_map.get(index_code, '000905.XSHG')
        stocks = jq.get_index_stocks(index_symbol, date=end_date)
        
        # 筛选（按市值和ROE）
        from jqdatasdk import query, valuation, indicator
        
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.roe,
            indicator.inc_net_profit_year_on_year
        ).filter(
            valuation.code.in_(stocks),
            valuation.market_cap >= min_market_cap,
            valuation.market_cap <= max_market_cap,
            indicator.roe >= min_roe
        ).order_by(
            indicator.roe.desc()
        ).limit(50)
        
        df = jq_client.get_fundamentals(q, date=end_date)
        
        if df is not None and not df.empty:
            # 获取股票名称
            all_secs = jq_client.get_all_securities(['stock'])
            
            candidates = []
            for _, row in df.iterrows():
                code = row['code']
                name = all_secs.loc[code, 'display_name'] if code in all_secs.index else code
                candidates.append({
                    'symbol': code,
                    'name': name,
                    'market_cap': round(row['market_cap'], 2),
                    'roe': round(row['roe'], 2) if row['roe'] else 0,
                    'profit_growth': round(row['inc_net_profit_year_on_year'], 2) if row['inc_net_profit_year_on_year'] else 0
                })
            
            return {'ok': True, 'data': {
                'count': len(candidates),
                'candidates': candidates,
                'index': index_code,
                'date': end_date,
                'source': 'jqdata'
            }}
        
        return {'ok': True, 'data': {'count': 0, 'candidates': [], 'source': 'jqdata'}}
        
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'扫描候选池失败: {str(e)}', 'traceback': traceback.format_exc()}


def _refresh_tenbagger_data(args: dict) -> dict:
    """刷新十倍股数据"""
    try:
        from crawlers.pipeline import DataPipeline
        
        pipeline = DataPipeline()
        result = pipeline.run_full_pipeline(page_size=args.get('page_size', 10))
        
        return {'ok': True, 'data': result.to_dict()}
    except Exception as e:
        return {'ok': False, 'error': f'刷新数据失败: {str(e)}'}


def _evaluate_stock(args: dict) -> dict:
    """评估单只股票（从JQData获取数据）"""
    try:
        symbol = args.get('symbol', '')
        name = args.get('name', symbol)
        data = args.get('data', {})
        
        # 如果没有提供数据，从JQData获取
        if not data or len(data) < 5:
            jq_client = _get_jqdata_client()
            if jq_client:
                from utils.tenbagger_v2.data_fetcher import TenbaggerDataFetcher
                fetcher = TenbaggerDataFetcher(jq_client)
                data = fetcher.fetch_complete_data(symbol)
                
                # 获取股票名称
                if not name or name == symbol:
                    name = data.get('stock_name', symbol)
        
        # 使用V2评估器
        try:
            from utils.tenbagger_v2 import get_evaluator_v2
            evaluator = get_evaluator_v2()
            report = evaluator.evaluate(symbol, name, data)
            return {'ok': True, 'data': {
                'report': report.to_dict(),
                'data_source': 'jqdata' if data.get('data_quality', 0) > 0.5 else 'default'
            }}
        except Exception as e:
            # 回退到V1评估器
            from utils.tenbagger_evaluator import get_evaluator
            evaluator = get_evaluator()
            report = evaluator.evaluate(symbol, name, data)
            return {'ok': True, 'data': {'report': report.to_dict(), 'data_source': 'v1_fallback'}}
            
    except Exception as e:
        import traceback
        return {'ok': False, 'error': f'评估失败: {str(e)}', 'traceback': traceback.format_exc()}


def _get_report(args: dict) -> dict:
    """获取评估报告"""
    try:
        from utils.tenbagger_v2 import get_evaluator_v2
        evaluator = get_evaluator_v2()
        report = evaluator.get_report(args.get('symbol', ''))
        if report:
            return {'ok': True, 'data': {'report': report.to_dict()}}
        return {'ok': False, 'error': '未找到报告'}
    except:
        return {'ok': False, 'error': '获取报告失败'}


def _get_rankings(args: dict) -> dict:
    """获取排名"""
    try:
        from utils.tenbagger_v2 import get_evaluator_v2
        evaluator = get_evaluator_v2()
        rankings = evaluator.get_recommendations(min_level=args.get('min_level', 'B'))
        return {'ok': True, 'data': {
            'count': len(rankings),
            'rankings': [r.to_dict() for r in rankings[:args.get('top_n', 20)]]
        }}
    except Exception as e:
        return _get_mock_rankings(args)


def _filter_stocks(args: dict) -> dict:
    """筛选股票"""
    min_level = args.get('min_level', 'A')
    return _get_rankings({'min_level': min_level, 'top_n': 50})


def _get_stats() -> dict:
    """获取评估统计"""
    return _get_db_stats()


def _batch_evaluate(args: dict) -> dict:
    """批量评估"""
    stocks = args.get('stocks', [])
    results = []
    
    for stock in stocks[:20]:  # 限制最多20只
        result = _evaluate_stock({
            'symbol': stock.get('symbol', ''),
            'name': stock.get('name', ''),
            'data': stock.get('data', {})
        })
        if result.get('ok'):
            report = result['data'].get('report', {})
            results.append({
                'symbol': stock.get('symbol'),
                'score': report.get('total_score', 0),
                'level': report.get('eval_level', 'D')
            })
    
    return {'ok': True, 'data': {'evaluated': len(results), 'results': results}}


# ============ 模拟数据（数据库不可用时使用）============

def _get_mock_rankings(args: dict) -> dict:
    """模拟排名数据"""
    mock_data = [
        {'security_id': '000688.XSHE', 'name': '国城矿业', 'total_score': 72.5, 'grade': 'A', 'current_stage': 'S1'},
        {'security_id': '000426.XSHE', 'name': '兴业银锡', 'total_score': 68.3, 'grade': 'B', 'current_stage': 'S1'},
        {'security_id': '300750.XSHE', 'name': '宁德时代', 'total_score': 65.8, 'grade': 'B', 'current_stage': 'S2'},
        {'security_id': '000603.XSHE', 'name': '盛达资源', 'total_score': 63.2, 'grade': 'B', 'current_stage': 'S1'},
        {'security_id': '000833.XSHE', 'name': '粤桂股份', 'total_score': 58.7, 'grade': 'C', 'current_stage': 'S0'},
        {'security_id': '000737.XSHE', 'name': '北方铜业', 'total_score': 55.4, 'grade': 'C', 'current_stage': 'S1'},
    ]
    return {'ok': True, 'data': {'count': len(mock_data), 'rankings': mock_data, 'source': 'mock'}}


def _get_mock_stages(args: dict) -> dict:
    """模拟阶段数据"""
    return {'ok': True, 'data': {
        'stages': [],
        'counts': {'S0': 45, 'S1': 23, 'S2': 8, 'S3': 3},
        'source': 'mock'
    }}


def _get_mock_scorecards(args: dict) -> dict:
    """模拟评分卡数据"""
    return {'ok': True, 'data': {'count': 0, 'scorecards': [], 'source': 'mock'}}


def _get_mock_stats() -> dict:
    """模拟统计数据"""
    return {'ok': True, 'data': {
        'total_evaluated': 79,
        'by_grade': {'A': 8, 'B': 21, 'C': 35, 'D': 12, 'F': 3},
        'by_stage': {'S0': 45, 'S1': 23, 'S2': 8, 'S3': 3},
        'avg_score': 54.3,
        'source': 'mock'
    }}


def call_mcp_tool(params: dict) -> dict:
    """调用MCP工具"""
    try:
        tool_name = params.get('tool_name')
        arguments = params.get('arguments', {})
        trace_id = params.get('trace_id', f'trace_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        if not tool_name:
            return {'ok': False, 'error': '缺少tool_name参数'}
        
        # 直接处理tenbagger工具（绕过MCP服务器）
        if tool_name.startswith('tenbagger.'):
            return call_tenbagger_tool(tool_name, arguments)
        
        # 直接处理workflow9工具（类似十倍股，绕过MCP服务器）
        if tool_name.startswith('workflow9.'):
            return call_workflow9_tool(tool_name, arguments)
        
        # 其他工具通过MCPClient调用
        from core.mcp.client import MCPClient
        
        # 获取当前Python解释器路径（bridge.py使用的Python，应该是正确的venv）
        python_path = sys.executable
        
        # 尝试从环境变量获取项目根目录
        project_root = os.environ.get('TRQUANT_ROOT')
        if not project_root:
            # 从bridge.py的位置推断项目根目录
            bridge_dir = Path(__file__).parent
            # bridge.py在extension/python/，项目根目录是extension/的父目录
            project_root = str(bridge_dir.parent.parent)
        
        # 确保使用绝对路径
        project_root_path = Path(project_root).resolve()
        
        client = MCPClient(project_root=project_root_path, python_path=python_path)
        result = client.call(tool_name, arguments)
        
        if result.success:
            return {
                'ok': True,
                'data': result.data,
                'trace_id': trace_id,
                'duration': result.duration
            }
        else:
            return {
                'ok': False,
                'error': result.error or 'MCP工具调用失败',
                'trace_id': trace_id
            }
            
    except ImportError as e:
        return {
            'ok': False,
            'error': f'MCP客户端不可用: {str(e)}',
            'hint': '请确保core.mcp.client模块可用'
        }
    except Exception as e:
        import traceback
        return {
            'ok': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }


# Mock数据
def mock_market_status():
    return {
        'ok': True,
        'data': {
            'regime': 'risk_on',
            'index_trend': {
                'SH000300': {'zscore': 0.8, 'trend': 'up'},
                'SZ399006': {'zscore': 1.2, 'trend': 'up'}
            },
            'style_rotation': [
                {'style': 'growth', 'score': 0.7},
                {'style': 'value', 'score': -0.2}
            ],
            'summary': '当前市场风险偏好回升，成长风格占优。'
        }
    }


def mock_mainlines():
    return {
        'ok': True,
        'data': [
            {'name': 'AI人工智能', 'score': 0.92, 'industries': ['半导体', '软件'], 'logic': 'AI产业链持续景气'},
            {'name': '新能源汽车', 'score': 0.85, 'industries': ['汽车', '电池'], 'logic': '渗透率持续提升'},
            {'name': '医药创新', 'score': 0.78, 'industries': ['创新药', '医疗器械'], 'logic': '政策支持'}
        ]
    }


def mock_factors():
    return {
        'ok': True,
        'data': [
            {'name': 'ROE_ttm', 'category': '盈利能力', 'weight': 0.8, 'reason': '高ROE反映优质经营'},
            {'name': 'revenue_growth', 'category': '成长性', 'weight': 0.75, 'reason': '成长股市场占优'},
            {'name': 'momentum_20d', 'category': '动量', 'weight': 0.7, 'reason': '趋势延续性强'}
        ]
    }


def mock_strategy(params: dict):
    style = params.get('style', 'multi_factor')
    factors = params.get('factors', ['ROE_ttm', 'momentum_20d'])
    
    code = f'''# -*- coding: utf-8 -*-
"""TRQuant生成策略 - {style}"""

def initialize(context):
    context.max_position = 0.1
    context.universe = get_index_stocks('000300.XSHG')
    run_daily(rebalance, time='9:35')

def rebalance(context):
    factor_data = get_factor_data(context.universe, {factors})
    scores = calculate_composite_score(factor_data)
    selected = scores.nlargest(10).index.tolist()
    adjust_positions(context, selected)
'''
    
    return {
        'ok': True,
        'data': {
            'code': code,
            'name': f'{style}_strategy',
            'factors': factors
        }
    }


# ==================== 工作流Action函数 ====================

def run_workflow_step_action(params: dict) -> dict:
    """运行工作流步骤"""
    if not WORKFLOW_DIRECT_AVAILABLE:
        return {'ok': False, 'error': 'workflow_direct模块不可用'}
    
    try:
        # 直接调用workflow_direct的函数（它已经是同步的）
        result = run_workflow_step(params)
        return result
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def get_workflow_context_action(params: dict) -> dict:
    """获取工作流上下文"""
    if not WORKFLOW_DIRECT_AVAILABLE:
        return {'ok': False, 'error': 'workflow_direct模块不可用'}
    
    try:
        return get_workflow_context(params)
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def clear_workflow_context_action(params: dict) -> dict:
    """清除工作流上下文"""
    if not WORKFLOW_DIRECT_AVAILABLE:
        return {'ok': False, 'error': 'workflow_direct模块不可用'}
    
    try:
        return clear_workflow_context(params)
    except Exception as e:
        return {'ok': False, 'error': str(e)}


# 动作分发

def get_backtest_results(params: dict) -> dict:
    """从MongoDB获取回测结果列表"""
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        db = client["trquant"]
        
        results = []
        
        for doc in db["backtest_results"].find().sort("created_at", -1).limit(50):
            results.append({
                "id": str(doc.get("_id", "")),
                "name": doc.get("name", doc.get("strategy_name", "未命名")),
                "strategy": doc.get("strategy", doc.get("strategy_type", "未知")),
                "startDate": doc.get("start_date", ""),
                "endDate": doc.get("end_date", ""),
                "totalReturn": doc.get("total_return", doc.get("metrics", {}).get("total_return", 0)),
                "sharpeRatio": doc.get("sharpe_ratio", doc.get("metrics", {}).get("sharpe_ratio", 0)),
                "maxDrawdown": doc.get("max_drawdown", doc.get("metrics", {}).get("max_drawdown", 0)),
                "winRate": doc.get("win_rate", doc.get("metrics", {}).get("win_rate", 0)),
                "createdAt": str(doc.get("created_at", "")),
                "source": "mongodb"
            })
        
        for doc in db["real_backtest_results"].find().sort("timestamp", -1).limit(20):
            results.append({
                "id": str(doc.get("_id", "")),
                "name": doc.get("name", "实盘回测"),
                "strategy": doc.get("strategy", "实盘策略"),
                "startDate": doc.get("start_date", ""),
                "endDate": doc.get("end_date", ""),
                "totalReturn": doc.get("total_return", 0),
                "sharpeRatio": doc.get("sharpe_ratio", 0),
                "maxDrawdown": doc.get("max_drawdown", 0),
                "winRate": doc.get("win_rate", 0),
                "createdAt": str(doc.get("timestamp", "")),
                "source": "real_backtest"
            })
        
        client.close()
        return {'ok': True, 'data': {'results': results, 'count': len(results)}}
        
    except Exception as e:
        return {'ok': False, 'error': f'获取回测结果失败: {str(e)}'}


def delete_backtest_result(params: dict) -> dict:
    """删除回测结果"""
    try:
        from pymongo import MongoClient
        from bson import ObjectId
        
        result_id = params.get("id")
        if not result_id:
            return {'ok': False, 'error': '缺少结果ID'}
        
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        db = client["trquant"]
        
        deleted = db["backtest_results"].delete_one({"_id": ObjectId(result_id)})
        if deleted.deleted_count == 0:
            deleted = db["real_backtest_results"].delete_one({"_id": ObjectId(result_id)})
        
        client.close()
        
        if deleted.deleted_count > 0:
            return {'ok': True, 'data': {'message': '删除成功'}}
        else:
            return {'ok': False, 'error': '未找到该记录'}
            
    except Exception as e:
        return {'ok': False, 'error': f'删除失败: {str(e)}'}


ACTIONS = {
    'get_market_status': get_market_status,
    'get_mainlines': get_mainlines,
    'recommend_factors': recommend_factors,
    'generate_strategy': generate_strategy,
    'analyze_backtest': analyze_backtest,
    'risk_assessment': risk_assessment,
    'run_backtest': run_backtest,
    'health_check': health_check,
    'call_mcp_tool': call_mcp_tool,
    'run_workflow_step': run_workflow_step_action,
    'get_workflow_context': get_workflow_context_action,
    'clear_workflow_context': clear_workflow_context_action,
    'get_backtest_results': get_backtest_results,
    'delete_backtest_result': delete_backtest_result,
    # AKShare实时数据
    'akshare.realtime': lambda p: _get_akshare_realtime(p),
    'akshare.spot': lambda p: _get_akshare_spot(p),
    'akshare.hot': lambda p: _get_akshare_hot(p),
    'akshare.price': lambda p: _get_akshare_price(p),
}


def main():
    """主函数"""
    import traceback
    import logging
    
    # 配置日志（仅输出到stderr，不影响stdout的JSON输出）
    logging.basicConfig(
        level=logging.INFO,
        format='[Bridge] %(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stderr
    )
    logger = logging.getLogger(__name__)
    
    try:
        request_str = sys.stdin.read()
        if not request_str:
            print(json.dumps({'ok': False, 'error': '未收到请求数据'}))
            return
        
        logger.info(f'收到请求: {len(request_str)} 字节')
        
        request = json.loads(request_str)
        action = request.get('action')
        params = request.get('params', {})
        
        logger.info(f'执行动作: {action}')
        
        if action not in ACTIONS:
            error_msg = f'未知动作: {action}'
            logger.error(error_msg)
            print(json.dumps({'ok': False, 'error': error_msg}))
            return
        
        # 执行动作
        start_time = datetime.now()
        try:
            response = ACTIONS[action](params)
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f'动作执行成功: {action} (耗时: {elapsed:.2f}s)')
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            error_msg = f'执行动作失败: {action} - {str(e)}'
            logger.error(f'{error_msg} (耗时: {elapsed:.2f}s)')
            logger.error(traceback.format_exc())
            print(json.dumps({
                'ok': False,
                'error': error_msg,
                'traceback': traceback.format_exc() if '--debug' in sys.argv else None
            }))
            return
        
        # 输出响应
        print(json.dumps(response, ensure_ascii=False))
        
    except json.JSONDecodeError as e:
        error_msg = f'JSON解析错误: {e}'
        logger.error(error_msg)
        print(json.dumps({'ok': False, 'error': error_msg}))
    except Exception as e:
        error_msg = f'未处理的错误: {str(e)}'
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        print(json.dumps({
            'ok': False,
            'error': error_msg,
            'traceback': traceback.format_exc() if '--debug' in sys.argv else None
        }))


if __name__ == '__main__':
    main()
