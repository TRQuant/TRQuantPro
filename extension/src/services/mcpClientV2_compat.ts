/**
 * MCP Client V2 兼容性类型定义
 * ============================
 * 供旧面板使用的类型定义和方法
 */

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
  engine?: string;
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
  trade_count?: number;
  report_path?: string;
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
export function formatPercent(value: number | undefined): string {
  if (value === undefined) return 'N/A';
  return (value * 100).toFixed(2) + '%';
}

/** 格式化时长 */
export function formatDuration(seconds: number | undefined): string {
  if (seconds === undefined) return 'N/A';
  if (seconds < 60) {
    return seconds.toFixed(1) + '秒';
  } else if (seconds < 3600) {
    return (seconds / 60).toFixed(1) + '分钟';
  } else {
    return (seconds / 3600).toFixed(1) + '小时';
  }
}

/** 构建回测参数 */
function buildBacktestParams(config: BacktestConfig): Record<string, unknown> {
  return {
    start_date: config.startDate || config.start_date,
    end_date: config.endDate || config.end_date,
    initial_capital: config.initialCapital || config.initial_capital,
    securities: config.securities,
    strategy: config.strategy,
    ...config.params
  };
}

/** 记录调用日志 */
function logCall(tool: string, args: unknown): void {
  console.log(`[MCP] ${tool}:`, args);
}

/** mcpClientV2 命名空间（兼容） */
export const mcpClientV2 = {
  buildBacktestParams,
  logCall
};
