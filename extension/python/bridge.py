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
TRQUANT_ROOT = os.environ.get('TRQUANT_ROOT', str(Path(__file__).parent.parent.parent))
sys.path.insert(0, TRQUANT_ROOT)

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


def call_mcp_tool(params: dict) -> dict:
    """调用MCP工具"""
    try:
        from core.mcp.client import MCPClient
        
        tool_name = params.get('tool_name')
        arguments = params.get('arguments', {})
        trace_id = params.get('trace_id', f'trace_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        if not tool_name:
            return {'ok': False, 'error': '缺少tool_name参数'}
        
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
    'clear_workflow_context': clear_workflow_context_action
}


def main():
    """主函数"""
    try:
        request_str = sys.stdin.read()
        request = json.loads(request_str)
        
        action = request.get('action')
        params = request.get('params', {})
        
        if action not in ACTIONS:
            response = {'ok': False, 'error': f'未知动作: {action}'}
        else:
            response = ACTIONS[action](params)
        
        print(json.dumps(response, ensure_ascii=False))
        
    except json.JSONDecodeError as e:
        print(json.dumps({'ok': False, 'error': f'JSON解析错误: {e}'}))
    except Exception as e:
        print(json.dumps({'ok': False, 'error': str(e)}))


if __name__ == '__main__':
    main()
