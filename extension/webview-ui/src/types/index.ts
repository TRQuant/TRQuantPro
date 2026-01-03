// 主线类型
export interface Mainline {
  name: string;
  score: number;
  trend: 'up' | 'down' | 'neutral';
  change_pct: number;
  fund_flow: number;
  sectors?: string[];
}

// 股票类型
export interface Stock {
  code: string;
  name: string;
  price: number;
  change_pct: number;
  volume?: number;
  market_cap?: number;
  tenbagger_score?: number;
}

// 工作流步骤结果
export interface StepResult {
  success: boolean;
  step_name: string;
  summary: string;
  details?: Record<string, any>;
  error?: string;
}

// 策略模板
export interface StrategyTemplate {
  name: string;
  type: string;
  description: string;
  risk_level: 'low' | 'medium' | 'high';
  params?: Record<string, any>;
}

// 趋势数据
export interface TrendData {
  trend: 'bull' | 'bear' | 'neutral';
  confidence: number;
  recommended_strategy: string;
  up_sectors: string[];
  down_sectors: string[];
  update_time: string;
}

// MCP调用结果
export interface MCPResult<T = any> {
  success: boolean;
  data?: T;
  error?: string;
}

// VS Code 消息类型
export interface VSCodeMessage {
  type: 'mcpCall' | 'mcpResult' | 'error' | 'info';
  id?: string;
  tool?: string;
  args?: Record<string, any>;
  result?: any;
  error?: string;
}
