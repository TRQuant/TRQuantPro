#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant MCP Server
==================

Model Context Protocol Server for TRQuant
让Cursor AI能够调用TRQuant功能
"""

import sys
import json
import os
from pathlib import Path
from typing import Any, Dict, List

# 导入bridge中的函数
from bridge import (
    get_market_status,
    get_mainlines,
    recommend_factors,
    generate_strategy,
    analyze_backtest,
    risk_assessment
)


class MCPServer:
    """MCP Server实现"""
    
    def __init__(self):
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, Dict]:
        """注册MCP工具"""
        return {
            'trquant_get_market_status': {
                'name': 'trquant_get_market_status',
                'description': '获取A股市场状态，包括市场Regime、指数趋势、风格轮动',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'universe': {
                            'type': 'string',
                            'description': '股票池，默认CN_EQ（A股）',
                            'default': 'CN_EQ'
                        },
                        'as_of': {
                            'type': 'string',
                            'description': '日期，格式YYYY-MM-DD',
                            'default': ''
                        }
                    }
                },
                'handler': get_market_status
            },
            'trquant_get_mainlines': {
                'name': 'trquant_get_mainlines',
                'description': '获取当前A股投资主线，包括热门概念、行业轮动',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'top_n': {
                            'type': 'integer',
                            'description': '返回主线数量',
                            'default': 20
                        },
                        'time_horizon': {
                            'type': 'string',
                            'description': '时间周期：short/medium/long',
                            'default': 'short'
                        }
                    }
                },
                'handler': get_mainlines
            },
            'trquant_recommend_factors': {
                'name': 'trquant_recommend_factors',
                'description': '基于市场状态推荐适合的量化因子',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'market_regime': {
                            'type': 'string',
                            'description': '市场状态：risk_on/risk_off/neutral'
                        },
                        'mainlines': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'description': '关注的投资主线'
                        }
                    }
                },
                'handler': recommend_factors
            },
            'trquant_generate_strategy': {
                'name': 'trquant_generate_strategy',
                'description': '生成PTrade量化策略代码',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'factors': {
                            'type': 'array',
                            'items': {'type': 'string'},
                            'description': '使用的因子列表'
                        },
                        'style': {
                            'type': 'string',
                            'description': '策略风格：multi_factor/momentum_growth/value/market_neutral',
                            'default': 'multi_factor'
                        },
                        'risk_params': {
                            'type': 'object',
                            'description': '风控参数',
                            'properties': {
                                'max_position': {'type': 'number', 'default': 0.1},
                                'stop_loss': {'type': 'number', 'default': 0.08},
                                'take_profit': {'type': 'number', 'default': 0.2}
                            }
                        }
                    },
                    'required': ['factors']
                },
                'handler': generate_strategy
            },
            'trquant_analyze_backtest': {
                'name': 'trquant_analyze_backtest',
                'description': '分析回测结果，提供诊断和优化建议',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'backtest_file': {
                            'type': 'string',
                            'description': '回测结果文件路径'
                        },
                        'backtest_data': {
                            'type': 'object',
                            'description': '回测数据JSON'
                        }
                    }
                },
                'handler': analyze_backtest
            },
            'trquant_risk_assessment': {
                'name': 'trquant_risk_assessment',
                'description': '评估投资组合风险',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'portfolio': {
                            'type': 'object',
                            'description': '持仓组合'
                        }
                    },
                    'required': ['portfolio']
                },
                'handler': risk_assessment
            }
        }
    
    def handle_request(self, request: Dict) -> Dict:
        """处理MCP请求"""
        method = request.get('method', '')
        params = request.get('params', {})
        request_id = request.get('id')
        
        if method == 'initialize':
            return self._handle_initialize(request_id)
        elif method == 'tools/list':
            return self._handle_tools_list(request_id)
        elif method == 'tools/call':
            return self._handle_tools_call(request_id, params)
        else:
            return self._error_response(request_id, -32601, f'Method not found: {method}')
    
    def _handle_initialize(self, request_id) -> Dict:
        """处理初始化请求"""
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {
                'protocolVersion': '2024-11-05',
                'capabilities': {
                    'tools': {}
                },
                'serverInfo': {
                    'name': 'trquant-mcp-server',
                    'version': '0.1.0'
                }
            }
        }
    
    def _handle_tools_list(self, request_id) -> Dict:
        """返回工具列表"""
        tools = [
            {
                'name': t['name'],
                'description': t['description'],
                'inputSchema': t['inputSchema']
            }
            for t in self.tools.values()
        ]
        
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': {'tools': tools}
        }
    
    def _handle_tools_call(self, request_id, params: Dict) -> Dict:
        """调用工具"""
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        if tool_name not in self.tools:
            return self._error_response(request_id, -32602, f'Unknown tool: {tool_name}')
        
        try:
            handler = self.tools[tool_name]['handler']
            result = handler(arguments)
            
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'result': {
                    'content': [
                        {
                            'type': 'text',
                            'text': json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            }
        except Exception as e:
            return self._error_response(request_id, -32000, str(e))
    
    def _error_response(self, request_id, code: int, message: str) -> Dict:
        """错误响应"""
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': code,
                'message': message
            }
        }
    
    def run(self):
        """运行MCP Server（stdio模式）"""
        server = self
        
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                response = server.handle_request(request)
                
                sys.stdout.write(json.dumps(response) + '\n')
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    'jsonrpc': '2.0',
                    'id': None,
                    'error': {
                        'code': -32700,
                        'message': str(e)
                    }
                }
                sys.stdout.write(json.dumps(error_response) + '\n')
                sys.stdout.flush()


def main():
    """主函数"""
    server = MCPServer()
    server.run()


if __name__ == '__main__':
    main()

