/**
 * TRQuant MCP Client V2 - 增强版统一封装层
 * ==========================================
 * 
 * 新增功能：
 * 1. 回测工具支持
 * 2. 策略管理工具
 * 3. 报告生成工具
 * 4. 进度回调
 * 5. WebSocket实时通信
 * 
 * @author TRQuant Team
 * @version 2.0.0
 */

import { logger } from '../utils/logger';

const MODULE = 'MCPClientV2';

// ==================== 类型定义 ====================

/**
 * 回测配置
 */
export interface BacktestConfig {
  strategy_path?: string;
  strategy_code?: string;
  start_date: string;
  end_date: string;
  initial_capital?: number;
  benchmark?: string;
  engine?: 'bullettrade' | 'qmt' | 'fast';
}

/**
 * 回测结果
 */
export interface BacktestResult {
  success: boolean;
  message?: string;
  total_return: number;
  annual_return: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  trade_count: number;
  report_path?: string;
  equity_curve?: number[];
  trades?: TradeRecord[];
}

/**
 * 交易记录
 */
export interface TradeRecord {
  date: string;
  symbol: string;
  direction: 'BUY' | 'SELL';
  price: number;
  volume: number;
  amount: number;
  commission: number;
  pnl: number;
}

/**
 * 策略信息
 */
export interface StrategyInfo {
  id: string;
  name: string;
  platform: 'bullettrade' | 'ptrade' | 'qmt';
  type: string;
  path: string;
  version: string;
  created_at: string;
  updated_at: string;
  performance?: {
    total_return: number;
    sharpe_ratio: number;
    last_backtest: string;
  };
}

/**
 * 报告信息
 */
export interface ReportInfo {
  id: string;
  name: string;
  strategy: string;
  engine: string;
  date: string;
  path: string;
  metrics: {
    total_return: number;
    sharpe_ratio: number;
    max_drawdown: number;
  };
}

/**
 * 进度回调
 */
export type ProgressCallback = (progress: number, message: string) => void;

/**
 * MCP调用选项
 */
export interface MCPCallOptions {
  timeout?: number;
  onProgress?: ProgressCallback;
  trace_id?: string;
}

/**
 * MCP响应
 */
export interface MCPResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
  trace_id: string;
  duration_ms: number;
}

// ==================== 工具定义 V2 ====================

export const MCP_TOOLS_V2 = {
  // 回测工具
  backtest: {
    bullettrade: {
      name: 'backtest.bullettrade',
      description: '使用BulletTrade引擎运行回测',
      params: {
        strategy_path: { type: 'string', description: '策略文件路径' },
        strategy_code: { type: 'string', description: '策略代码（与path二选一）' },
        start_date: { type: 'string', required: true, description: '开始日期 YYYY-MM-DD' },
        end_date: { type: 'string', required: true, description: '结束日期 YYYY-MM-DD' },
        initial_capital: { type: 'number', default: 1000000, description: '初始资金' },
        benchmark: { type: 'string', default: '000300.XSHG', description: '基准指数' }
      }
    },
    qmt: {
      name: 'backtest.qmt',
      description: '使用QMT引擎运行回测',
      params: {
        strategy_path: { type: 'string', description: '策略文件路径' },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true },
        initial_capital: { type: 'number', default: 1000000 }
      }
    },
    quick: {
      name: 'backtest.quick',
      description: '快速向量化回测',
      params: {
        signals: { type: 'object', required: true, description: '信号矩阵' },
        prices: { type: 'object', required: true, description: '价格数据' },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true }
      }
    },
    compare: {
      name: 'backtest.compare',
      description: '对比多个策略回测结果',
      params: {
        strategy_ids: { type: 'array', required: true, description: '策略ID列表' },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true }
      }
    },
    status: {
      name: 'backtest.status',
      description: '获取回测任务状态',
      params: {
        task_id: { type: 'string', required: true }
      }
    }
  },

  // 策略管理工具
  strategy: {
    list: {
      name: 'strategy.list',
      description: '列出所有策略',
      params: {
        platform: { type: 'string', description: '平台筛选' },
        type: { type: 'string', description: '类型筛选' }
      }
    },
    get: {
      name: 'strategy.get',
      description: '获取策略详情',
      params: {
        strategy_id: { type: 'string', required: true }
      }
    },
    generate: {
      name: 'strategy.generate',
      description: '生成策略代码',
      params: {
        template: { type: 'string', required: true, description: '模板名称' },
        factors: { type: 'array', required: true },
        platform: { type: 'string', default: 'bullettrade' },
        params: { type: 'object', description: '策略参数' }
      }
    },
    convert: {
      name: 'strategy.convert',
      description: '转换策略到其他平台',
      params: {
        strategy_path: { type: 'string', required: true },
        target_platform: { type: 'string', required: true, enum: ['ptrade', 'qmt', 'bullettrade'] }
      }
    }
  },

  // 报告工具
  report: {
    generate: {
      name: 'report.generate',
      description: '生成回测报告',
      params: {
        backtest_result: { type: 'object', required: true },
        format: { type: 'string', default: 'html', enum: ['html', 'pdf', 'json'] },
        template: { type: 'string', default: 'default' }
      }
    },
    list: {
      name: 'report.list',
      description: '列出所有报告',
      params: {
        strategy: { type: 'string' },
        limit: { type: 'number', default: 20 }
      }
    },
    get: {
      name: 'report.get',
      description: '获取报告详情',
      params: {
        report_id: { type: 'string', required: true }
      }
    },
    export: {
      name: 'report.export',
      description: '导出报告',
      params: {
        report_id: { type: 'string', required: true },
        format: { type: 'string', required: true, enum: ['pdf', 'xlsx', 'csv'] }
      }
    }
  },

  // 优化工具
  optimizer: {
    optuna: {
      name: 'optimizer.optuna',
      description: '使用Optuna进行策略参数优化',
      params: {
        strategy_path: { type: 'string', required: true },
        params_space: { type: 'object', required: true, description: '参数搜索空间' },
        n_trials: { type: 'number', default: 50 },
        direction: { type: 'string', default: 'maximize', enum: ['maximize', 'minimize'] },
        target_metric: { type: 'string', default: 'sharpe_ratio' }
      }
    },
    grid: {
      name: 'optimizer.grid_search',
      description: '网格搜索优化',
      params: {
        strategy_path: { type: 'string', required: true },
        param_grid: { type: 'object', required: true }
      }
    }
  },

  // 因子分析工具
  factor: {
    analyze: {
      name: 'factor.ic_analysis',
      description: 'IC/IR因子分析',
      params: {
        factor_data: { type: 'object', required: true },
        returns_data: { type: 'object', required: true },
        periods: { type: 'array', default: [1, 5, 10, 20] }
      }
    },
    evaluate: {
      name: 'factor.evaluate',
      description: '综合因子评估',
      params: {
        factor_name: { type: 'string', required: true },
        start_date: { type: 'string', required: true },
        end_date: { type: 'string', required: true }
      }
    },
    recommend: {
      name: 'factor.recommend',
      description: '因子推荐',
      params: {
        market_regime: { type: 'string', required: true, enum: ['risk_on', 'risk_off', 'neutral'] },
        top_n: { type: 'number', default: 10 }
      }
    }
  },

  // 市场分析工具
  market: {
    status: {
      name: 'trquant.market_status',
      description: '获取市场状态',
      params: {
        universe: { type: 'string', default: 'CN_EQ' }
      }
    },
    mainlines: {
      name: 'trquant.mainlines',
      description: '获取投资主线',
      params: {
        top_n: { type: 'number', default: 10 },
        time_horizon: { type: 'string', default: 'short' }
      }
    }
  }
} as const;

// ==================== 工具函数 ====================

/**
 * 生成trace_id
 */
export function generateTraceId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `tr2-${timestamp}-${random}`;
}

/**
 * 格式化持续时间
 */
export function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${(ms / 60000).toFixed(1)}min`;
}

/**
 * 格式化百分比
 */
export function formatPercent(value: number, decimals = 2): string {
  return `${(value * 100).toFixed(decimals)}%`;
}

/**
 * 格式化数字
 */
export function formatNumber(value: number, decimals = 2): string {
  if (Math.abs(value) >= 1e8) {
    return `${(value / 1e8).toFixed(decimals)}亿`;
  }
  if (Math.abs(value) >= 1e4) {
    return `${(value / 1e4).toFixed(decimals)}万`;
  }
  return value.toFixed(decimals);
}

// ==================== MCP客户端V2类 ====================

/**
 * MCP客户端V2
 * 
 * 提供增强的MCP工具调用功能
 */
export class MCPClientV2 {
  private static _instance: MCPClientV2;
  private _pendingTasks: Map<string, { resolve: Function; reject: Function; timeout: NodeJS.Timeout }> = new Map();
  
  private constructor() {}
  
  /**
   * 获取单例实例
   */
  static getInstance(): MCPClientV2 {
    if (!MCPClientV2._instance) {
      MCPClientV2._instance = new MCPClientV2();
    }
    return MCPClientV2._instance;
  }
  
  /**
   * 获取所有工具定义
   */
  getTools(): typeof MCP_TOOLS_V2 {
    return MCP_TOOLS_V2;
  }
  
  /**
   * 获取工具描述
   */
  getToolDescription(category: keyof typeof MCP_TOOLS_V2, tool: string): string {
    const categoryTools = MCP_TOOLS_V2[category] as Record<string, { description: string }>;
    const toolDef = categoryTools[tool];
    return toolDef?.description ?? '';
  }
  
  /**
   * 构建回测参数
   */
  buildBacktestParams(config: BacktestConfig): Record<string, unknown> {
    return {
      strategy_path: config.strategy_path,
      strategy_code: config.strategy_code,
      start_date: config.start_date,
      end_date: config.end_date,
      initial_capital: config.initial_capital ?? 1000000,
      benchmark: config.benchmark ?? '000300.XSHG',
      trace_id: generateTraceId()
    };
  }
  
  /**
   * 构建策略生成参数
   */
  buildStrategyParams(
    template: string,
    factors: string[],
    platform: string = 'bullettrade',
    params: Record<string, unknown> = {}
  ): Record<string, unknown> {
    return {
      template,
      factors,
      platform,
      params,
      trace_id: generateTraceId()
    };
  }
  
  /**
   * 构建优化参数
   */
  buildOptimizerParams(
    strategyPath: string,
    paramsSpace: Record<string, unknown>,
    options: {
      n_trials?: number;
      direction?: 'maximize' | 'minimize';
      target_metric?: string;
    } = {}
  ): Record<string, unknown> {
    return {
      strategy_path: strategyPath,
      params_space: paramsSpace,
      n_trials: options.n_trials ?? 50,
      direction: options.direction ?? 'maximize',
      target_metric: options.target_metric ?? 'sharpe_ratio',
      trace_id: generateTraceId()
    };
  }
  
  /**
   * 解析回测结果
   */
  parseBacktestResult(response: unknown): BacktestResult {
    const data = response as Record<string, unknown>;
    return {
      success: Boolean(data.success),
      message: String(data.message ?? ''),
      total_return: Number(data.total_return ?? 0),
      annual_return: Number(data.annual_return ?? 0),
      sharpe_ratio: Number(data.sharpe_ratio ?? 0),
      max_drawdown: Number(data.max_drawdown ?? 0),
      win_rate: Number(data.win_rate ?? 0),
      trade_count: Number(data.trade_count ?? data.total_trades ?? 0),
      report_path: String(data.report_path ?? ''),
      equity_curve: data.equity_curve as number[] | undefined,
      trades: data.trades as TradeRecord[] | undefined
    };
  }
  
  /**
   * 格式化回测结果为显示文本
   */
  formatBacktestResult(result: BacktestResult): string {
    const lines = [
      '📊 回测结果',
      '━'.repeat(40),
      `总收益: ${formatPercent(result.total_return)}`,
      `年化收益: ${formatPercent(result.annual_return)}`,
      `夏普比率: ${result.sharpe_ratio.toFixed(2)}`,
      `最大回撤: ${formatPercent(result.max_drawdown)}`,
      `胜率: ${formatPercent(result.win_rate)}`,
      `交易次数: ${result.trade_count}`,
      '━'.repeat(40)
    ];
    
    if (result.report_path) {
      lines.push(`报告路径: ${result.report_path}`);
    }
    
    return lines.join('\n');
  }
  
  /**
   * 记录工具调用日志
   */
  logCall(toolName: string, params: Record<string, unknown>): void {
    logger.info(`[MCP] 调用工具: ${toolName}`, MODULE, {
      trace_id: params.trace_id,
      params: JSON.stringify(params).substring(0, 300)
    });
  }
  
  /**
   * 记录工具响应日志
   */
  logResponse<T>(toolName: string, response: MCPResponse<T>): void {
    if (response.success) {
      logger.info(`[MCP] 响应成功: ${toolName}`, MODULE, {
        trace_id: response.trace_id,
        duration: formatDuration(response.duration_ms)
      });
    } else {
      logger.error(`[MCP] 响应失败: ${toolName}`, MODULE, {
        trace_id: response.trace_id,
        error: response.error?.message
      });
    }
  }
}

// ==================== 导出 ====================

export const mcpClientV2 = MCPClientV2.getInstance();
export default MCPClientV2;
