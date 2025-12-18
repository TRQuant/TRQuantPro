/**
 * TRQuant MCP Client V2 - 9步工作流完整集成
 * ==========================================
 * 
 * 提供完整的9步投资工作流MCP工具定义和调用接口
 * 
 * @version 2.0.0
 */

import { logger } from '../utils/logger';

const MODULE = 'MCPClientV2';

// ==================== 类型定义 ====================

/** MCP响应envelope */
export interface MCPResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    hint?: string;
  };
  metadata: {
    server_name: string;
    tool_name: string;
    version: string;
    trace_id?: string;
    timestamp: string;
    duration_ms?: number;
  };
}

/** 9步工作流步骤定义 */
export interface WorkflowStep {
  id: string;
  name: string;
  icon: string;
  color: string;
  mcp_tool: string;
  description: string;
}

/** 工作流状态 */
export interface WorkflowState {
  workflow_id: string;
  name: string;
  current_step: number;
  total_steps: number;
  steps: Array<{
    id: string;
    name: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    result?: unknown;
    started_at?: string;
    completed_at?: string;
  }>;
  context: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

// ==================== 响应类型 ====================

/** 数据源健康检查响应 */
export interface DataSourceHealthResponse {
  jqdata: { available: boolean; latency_ms?: number };
  akshare: { available: boolean; latency_ms?: number };
  mock: { available: boolean };
  active_source: string;
  recommendation: string;
}

/** 市场状态响应 */
export interface MarketStatusResponse {
  regime: 'risk_on' | 'risk_off' | 'neutral';
  index_trend: Record<string, { zscore: number; trend: string; change_pct: number }>;
  style_rotation: Array<{ style: string; score: number }>;
  breadth: { advance_decline: number; new_high_low: number };
  summary: string;
  updated_at: string;
}

/** 投资主线响应 */
export interface MainlineResponse {
  mainlines: Array<{
    name: string;
    score: number;
    industries: string[];
    logic: string;
    catalysts: string[];
    risks: string[];
  }>;
  market_context: string;
}

/** 候选池响应 */
export interface CandidatePoolResponse {
  pool_id: string;
  stocks: Array<{
    code: string;
    name: string;
    industry: string;
    score: number;
  }>;
  total_count: number;
  criteria: string[];
}

/** 因子推荐响应 */
export interface FactorRecommendResponse {
  factors: Array<{
    name: string;
    category: string;
    weight: number;
    ic_mean: number;
    reason: string;
  }>;
  market_regime: string;
  style_factors: string[];
}

/** 策略生成响应 */
export interface StrategyGenerateResponse {
  strategy_name: string;
  strategy_type: string;
  platform: string;
  code: string;
  params: Record<string, unknown>;
  description: string;
}

/** 回测结果响应 */
export interface BacktestResultResponse {
  success: boolean;
  metrics: {
    total_return: number;
    annual_return: number;
    sharpe_ratio: number;
    max_drawdown: number;
    calmar_ratio: number;
    win_rate: number;
    total_trades: number;
  };
  equity_curve?: number[];
  trades?: Array<{
    date: string;
    code: string;
    action: string;
    price: number;
    quantity: number;
  }>;
  duration_seconds: number;
  engine_used: string;
}

/** 优化结果响应 */
export interface OptimizeResultResponse {
  best_params: Record<string, unknown>;
  best_sharpe: number;
  best_return: number;
  all_results: Array<{
    params: Record<string, unknown>;
    sharpe: number;
    return_pct: number;
    drawdown: number;
  }>;
  total_trials: number;
  duration_seconds: number;
}

/** 报告生成响应 */
export interface ReportGenerateResponse {
  report_id: string;
  file_path: string;
  format: string;
  title: string;
  created_at: string;
}

// ==================== 9步工作流定义 ====================

export const WORKFLOW_9STEPS: WorkflowStep[] = [
  {
    id: 'data_source',
    name: '信息获取',
    icon: '📡',
    color: '#58a6ff',
    mcp_tool: 'data_source.check',
    description: '检查数据源连接状态，确保数据获取正常'
  },
  {
    id: 'market_trend',
    name: '市场趋势',
    icon: '📈',
    color: '#667eea',
    mcp_tool: 'market.status',
    description: '分析当前市场状态、趋势和风格轮动'
  },
  {
    id: 'mainline',
    name: '投资主线',
    icon: '🔥',
    color: '#F59E0B',
    mcp_tool: 'market.mainlines',
    description: '识别当前市场投资主线和热点板块'
  },
  {
    id: 'candidate_pool',
    name: '候选池构建',
    icon: '📦',
    color: '#a371f7',
    mcp_tool: 'data_source.candidate_pool',
    description: '根据投资主线构建候选股票池'
  },
  {
    id: 'factor',
    name: '因子构建',
    icon: '🧮',
    color: '#3fb950',
    mcp_tool: 'factor.recommend',
    description: '基于市场状态推荐量化因子组合'
  },
  {
    id: 'strategy',
    name: '策略生成',
    icon: '💻',
    color: '#d29922',
    mcp_tool: 'strategy_template.generate',
    description: '生成多平台量化策略代码'
  },
  {
    id: 'backtest',
    name: '回测验证',
    icon: '🔄',
    color: '#1E3A5F',
    mcp_tool: 'backtest.fast',
    description: '执行策略回测，验证策略有效性'
  },
  {
    id: 'optimization',
    name: '策略优化',
    icon: '⚙️',
    color: '#7C3AED',
    mcp_tool: 'optimizer.grid_search',
    description: '参数优化，寻找最优策略配置'
  },
  {
    id: 'report',
    name: '报告生成',
    icon: '📄',
    color: '#EC4899',
    mcp_tool: 'report.generate',
    description: '生成完整的投资研究报告'
  }
];

// ==================== MCP工具定义 ====================

export const MCP_TOOLS_V2 = {
  // Step 1: 数据源
  data_source: {
    check: {
      name: 'data_source.check',
      description: '检查所有数据源连接状态',
      params: {}
    },
    switch: {
      name: 'data_source.switch',
      description: '切换活跃数据源',
      params: {
        source: { type: 'string', enum: ['jqdata', 'akshare', 'mock'], required: true }
      }
    },
    candidate_pool: {
      name: 'data_source.candidate_pool',
      description: '构建候选股票池',
      params: {
        mainline: { type: 'string', description: '投资主线名称' },
        filters: { type: 'object', description: '筛选条件' },
        limit: { type: 'number', default: 100 }
      }
    }
  },
  
  // Step 2-3: 市场分析
  market: {
    status: {
      name: 'market.status',
      description: '获取市场当前状态和风格分析',
      params: {
        universe: { type: 'string', default: 'CN_EQ' }
      }
    },
    trend: {
      name: 'market.trend',
      description: '分析市场趋势',
      params: {
        period: { type: 'string', enum: ['short', 'medium', 'long'], default: 'short' }
      }
    },
    mainlines: {
      name: 'market.mainlines',
      description: '获取投资主线TOP N',
      params: {
        top_n: { type: 'number', default: 10 },
        time_horizon: { type: 'string', enum: ['short', 'medium', 'long'], default: 'short' }
      }
    },
    score_mainline: {
      name: 'market.score_mainline',
      description: '对投资主线进行五维评分',
      params: {
        mainline_name: { type: 'string', required: true }
      }
    }
  },
  
  // Step 5: 因子
  factor: {
    recommend: {
      name: 'factor.recommend',
      description: '基于市场状态推荐因子',
      params: {
        market_regime: { type: 'string', enum: ['risk_on', 'risk_off', 'neutral'] },
        top_n: { type: 'number', default: 10 }
      }
    },
    build: {
      name: 'factor.build',
      description: '构建自定义因子',
      params: {
        expression: { type: 'string', required: true },
        name: { type: 'string', required: true }
      }
    },
    backtest: {
      name: 'factor.backtest',
      description: '回测因子表现',
      params: {
        factor_name: { type: 'string', required: true },
        start_date: { type: 'string' },
        end_date: { type: 'string' }
      }
    }
  },
  
  // Step 6: 策略生成
  strategy: {
    template_list: {
      name: 'strategy_template.list',
      description: '列出所有策略模板',
      params: {
        category: { type: 'string', description: '过滤分类' }
      }
    },
    template_info: {
      name: 'strategy_template.info',
      description: '获取策略模板详情',
      params: {
        name: { type: 'string', required: true }
      }
    },
    generate: {
      name: 'strategy_template.generate',
      description: '生成策略代码',
      params: {
        strategy_type: { type: 'string', required: true, enum: ['momentum', 'mean_reversion', 'rotation'] },
        params: { type: 'object', description: '策略参数' },
        platform: { type: 'string', enum: ['joinquant', 'bullettrade', 'ptrade', 'qmt'], default: 'joinquant' }
      }
    },
    validate: {
      name: 'strategy.validate',
      description: '验证策略代码',
      params: {
        code: { type: 'string', required: true },
        platform: { type: 'string', default: 'joinquant' }
      }
    },
    convert: {
      name: 'strategy.convert',
      description: '转换策略到其他平台',
      params: {
        code: { type: 'string', required: true },
        from_platform: { type: 'string', default: 'joinquant' },
        to_platform: { type: 'string', required: true }
      }
    }
  },
  
  // Step 7: 回测
  backtest: {
    fast: {
      name: 'backtest.fast',
      description: '快速回测 (<5秒)',
      params: {
        securities: { type: 'array', required: true },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true },
        strategy: { type: 'string', default: 'momentum' },
        lookback: { type: 'number', default: 20 },
        top_n: { type: 'number', default: 10 }
      }
    },
    standard: {
      name: 'backtest.standard',
      description: '标准回测 (<30秒)',
      params: {
        securities: { type: 'array', required: true },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true },
        strategy: { type: 'string', default: 'momentum' },
        initial_capital: { type: 'number', default: 1000000 }
      }
    },
    bullettrade: {
      name: 'backtest.bullettrade',
      description: 'BulletTrade精确回测',
      params: {
        strategy_code: { type: 'string' },
        strategy_file: { type: 'string' },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true },
        initial_capital: { type: 'number', default: 1000000 }
      }
    },
    qmt: {
      name: 'backtest.qmt',
      description: 'QMT回测',
      params: {
        strategy_code: { type: 'string' },
        stock_pool: { type: 'array' },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true }
      }
    }
  },
  
  // Step 8: 优化
  optimizer: {
    grid_search: {
      name: 'optimizer.grid_search',
      description: '参数网格搜索',
      params: {
        strategy_type: { type: 'string', required: true },
        param_ranges: { type: 'object', required: true },
        securities: { type: 'array', required: true },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true }
      }
    },
    optuna: {
      name: 'optimizer.optuna',
      description: 'Optuna智能优化',
      params: {
        strategy_type: { type: 'string', required: true },
        param_space: { type: 'object', required: true },
        n_trials: { type: 'number', default: 100 }
      }
    },
    walk_forward: {
      name: 'optimizer.walk_forward',
      description: '滚动优化验证',
      params: {
        strategy_type: { type: 'string', required: true },
        window_size: { type: 'number', default: 252 }
      }
    }
  },
  
  // Step 9: 报告
  report: {
    generate: {
      name: 'report.generate',
      description: '生成回测报告',
      params: {
        result: { type: 'object', required: true },
        format: { type: 'string', enum: ['html', 'pdf', 'markdown'], default: 'html' },
        title: { type: 'string' },
        strategy_name: { type: 'string' }
      }
    },
    compare: {
      name: 'report.compare',
      description: '生成策略对比报告',
      params: {
        results: { type: 'array', required: true }
      }
    },
    diagnosis: {
      name: 'report.diagnosis',
      description: '生成策略诊断报告',
      params: {
        result: { type: 'object', required: true }
      }
    }
  },
  
  // 工作流管理
  workflow: {
    create: {
      name: 'workflow.create',
      description: '创建新工作流',
      params: {
        name: { type: 'string', default: '投资工作流' }
      }
    },
    status: {
      name: 'workflow.status',
      description: '获取工作流状态',
      params: {
        workflow_id: { type: 'string', required: true }
      }
    },
    run_step: {
      name: 'workflow.run_step',
      description: '执行指定步骤',
      params: {
        workflow_id: { type: 'string', required: true },
        step_index: { type: 'number', required: true },
        step_args: { type: 'object' }
      }
    },
    steps: {
      name: 'workflow.steps',
      description: '获取9步骤定义',
      params: {}
    }
  }
} as const;

// ==================== 工具函数 ====================

/** 生成trace_id */
export function generateTraceId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `tr-${timestamp}-${random}`;
}

/** 解析MCP响应 */
export function parseMCPResponse<T>(responseText: string): MCPResponse<T> {
  try {
    const response = JSON.parse(responseText);
    if ('success' in response && 'metadata' in response) {
      return response as MCPResponse<T>;
    }
    return {
      success: true,
      data: response as T,
      metadata: {
        server_name: 'unknown',
        tool_name: 'unknown',
        version: '2.0.0',
        timestamp: new Date().toISOString()
      }
    };
  } catch (error) {
    return {
      success: false,
      error: {
        code: 'PARSE_ERROR',
        message: '解析响应失败'
      },
      metadata: {
        server_name: 'unknown',
        tool_name: 'unknown',
        version: '2.0.0',
        timestamp: new Date().toISOString()
      }
    };
  }
}

/** 获取步骤的MCP工具名 */
export function getStepMCPTool(stepId: string): string | undefined {
  const step = WORKFLOW_9STEPS.find(s => s.id === stepId);
  return step?.mcp_tool;
}

/** 获取步骤索引 */
export function getStepIndex(stepId: string): number {
  return WORKFLOW_9STEPS.findIndex(s => s.id === stepId);
}

// ==================== 导出 ====================

export default {
  WORKFLOW_9STEPS,
  MCP_TOOLS_V2,
  generateTraceId,
  parseMCPResponse,
  getStepMCPTool,
  getStepIndex
};

// ==================== 兼容性类型 (旧面板使用) ====================

/** 回测配置（兼容旧面板） */
export interface BacktestConfig {
  startDate?: string;
  endDate?: string;
  start_date?: string;
  end_date?: string;
  initialCapital?: number;
  initial_capital?: number;
  securities?: string[];
  strategy?: string;
  strategy_path?: string;
  params?: Record<string, unknown>;
  [key: string]: unknown;
}

/** 回测结果（兼容旧面板） */
export interface BacktestResult {
  success?: boolean;
  total_return?: number;
  annual_return?: number;
  sharpe_ratio?: number;
  max_drawdown?: number;
  win_rate?: number;
  total_trades?: number;
  metrics?: {
    total_return?: number;
    annual_return?: number;
    sharpe_ratio?: number;
    max_drawdown?: number;
    win_rate?: number;
    total_trades?: number;
  };
  trades?: any[];
  equity_curve?: number[];
  duration_seconds?: number;
  [key: string]: unknown;
}

/** 报告信息（兼容旧面板） */
export interface ReportInfo {
  report_id?: string;
  id?: string;
  title?: string;
  name?: string;
  format?: string;
  file_path?: string;
  path?: string;
  created_at?: string;
  strategy?: string;
  engine?: string;
  date?: string;
  metrics?: Record<string, unknown>;
  [key: string]: unknown;
}

/** 格式化百分比 */
export function formatPercent(value: number): string {
  return (value * 100).toFixed(2) + '%';
}

/** 格式化时长 */
export function formatDuration(seconds: number): string {
  if (seconds < 60) {
    return seconds.toFixed(1) + '秒';
  } else if (seconds < 3600) {
    return (seconds / 60).toFixed(1) + '分钟';
  } else {
    return (seconds / 3600).toFixed(1) + '小时';
  }
}

/** mcpClientV2 命名空间（兼容） */
export const mcpClientV2 = {
  generateTraceId,
  parseMCPResponse,
  getStepMCPTool,
  getStepIndex,
  WORKFLOW_9STEPS,
  MCP_TOOLS_V2
};
