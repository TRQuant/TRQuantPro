/**
 * TRQuant MCP Client - 统一封装层
 * ================================
 * 
 * 提供统一的MCP工具调用接口
 * 
 * 功能：
 * 1. 统一的调用接口
 * 2. 参数验证
 * 3. 响应类型定义
 * 4. 错误处理
 * 
 * @author TRQuant Team
 * @version 1.0.0
 */

import { logger } from '../utils/logger';

const MODULE = 'MCPClient';

// ==================== 类型定义 ====================

/**
 * MCP响应元数据
 */
export interface MCPMetadata {
  server_name: string;
  tool_name: string;
  version: string;
  trace_id?: string;
  timestamp: string;
  duration_ms?: number;
}

/**
 * MCP错误信息
 */
export interface MCPError {
  code: string;
  message: string;
  hint?: string;
  details?: Record<string, unknown>;
}

/**
 * MCP响应envelope
 */
export interface MCPResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: MCPError;
  metadata: MCPMetadata;
}

/**
 * 市场状态响应
 */
export interface MarketStatusResponse {
  regime: 'risk_on' | 'risk_off' | 'neutral';
  index_trend: Record<string, { zscore: number; trend: string }>;
  style_rotation: Array<{ style: string; score: number }>;
  summary: string;
}

/**
 * 投资主线响应
 */
export interface MainlineResponse {
  name: string;
  score: number;
  industries: string[];
  logic: string;
}

/**
 * 因子推荐响应
 */
export interface FactorResponse {
  name: string;
  category: string;
  weight: number;
  reason: string;
}

/**
 * 策略生成响应
 */
export interface StrategyResponse {
  code: string;
  name: string;
  platform: 'ptrade' | 'qmt';
  style: string;
  factors: string[];
  risk_params: {
    max_position: number;
    stop_loss: number;
    take_profit: number;
  };
  description: string;
}

/**
 * 任务复杂度分析响应
 */
export interface TaskComplexityResponse {
  complexity: 'simple' | 'medium' | 'complex' | 'critical';
  complexity_score: number;
  recommended_mode: 'auto' | 'max';
  reason: string;
  factors: {
    file_count: number;
    dependencies_count: number;
    code_complexity: string;
    estimated_time?: string;
  };
}

/**
 * 上下文缓存响应
 */
export interface ContextCacheResponse {
  cached: boolean;
  file_path: string;
  context?: Record<string, unknown>;
  message: string;
}

// ==================== 工具定义 ====================

/**
 * MCP工具定义
 */
export const MCP_TOOLS = {
  // 业务工具
  trquant: {
    market_status: {
      name: 'trquant_market_status',
      description: '获取A股市场当前状态',
      params: {
        universe: { type: 'string', default: 'CN_EQ' }
      }
    },
    mainlines: {
      name: 'trquant_mainlines',
      description: '获取当前A股市场的投资主线',
      params: {
        top_n: { type: 'number', default: 10 },
        time_horizon: { type: 'string', enum: ['short', 'medium', 'long'], default: 'short' }
      }
    },
    recommend_factors: {
      name: 'trquant_recommend_factors',
      description: '基于市场状态推荐量化因子',
      params: {
        market_regime: { type: 'string', enum: ['risk_on', 'risk_off', 'neutral'], required: true },
        top_n: { type: 'number', default: 10 }
      }
    },
    generate_strategy: {
      name: 'trquant_generate_strategy',
      description: '生成PTrade或QMT量化策略代码',
      params: {
        factors: { type: 'array', required: true },
        style: { type: 'string', enum: ['multi_factor', 'momentum_growth', 'value', 'market_neutral'], default: 'multi_factor' },
        platform: { type: 'string', enum: ['ptrade', 'qmt'], default: 'ptrade' },
        max_position: { type: 'number', default: 0.1 },
        stop_loss: { type: 'number', default: 0.08 },
        take_profit: { type: 'number', default: 0.2 }
      }
    },
    analyze_backtest: {
      name: 'trquant_analyze_backtest',
      description: '分析回测结果，提供诊断和优化建议',
      params: {
        metrics: { type: 'object', required: true }
      }
    }
  },
  
  // 任务管理工具
  task: {
    analyze_complexity: {
      name: 'task.analyze_complexity',
      description: '分析任务复杂度，判断是否需要Max mode',
      params: {
        task_title: { type: 'string', required: true },
        task_description: { type: 'string' },
        estimated_time: { type: 'string' },
        dependencies: { type: 'array' },
        file_count: { type: 'number', default: 0 },
        code_complexity: { type: 'string', enum: ['low', 'medium', 'high'], default: 'medium' }
      }
    },
    get_context: {
      name: 'task.get_context',
      description: '获取文件上下文（带缓存）',
      params: {
        file_path: { type: 'string', required: true },
        max_age_hours: { type: 'number', default: 24 },
        force_refresh: { type: 'boolean', default: false }
      }
    },
    cache_context: {
      name: 'task.cache_context',
      description: '缓存文件上下文',
      params: {
        file_path: { type: 'string', required: true },
        context: { type: 'object', required: true }
      }
    },
    optimize_workflow: {
      name: 'task.optimize_workflow',
      description: '优化工作流',
      params: {
        task_title: { type: 'string', required: true },
        file_paths: { type: 'array', required: true }
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
  return `tr-${timestamp}-${random}`;
}

/**
 * 解析MCP响应
 */
export function parseMCPResponse<T>(responseText: string): MCPResponse<T> {
  try {
    const response = JSON.parse(responseText);
    
    // 检查是否是envelope格式
    if ('success' in response && 'metadata' in response) {
      return response as MCPResponse<T>;
    }
    
    // 兼容旧格式
    return {
      success: true,
      data: response as T,
      metadata: {
        server_name: 'unknown',
        tool_name: 'unknown',
        version: '1.0.0',
        timestamp: new Date().toISOString()
      }
    };
  } catch (error) {
    logger.error(`解析MCP响应失败: ${error}`, MODULE);
    return {
      success: false,
      error: {
        code: 'PARSE_ERROR',
        message: '解析响应失败',
        details: { raw: responseText.substring(0, 200) }
      },
      metadata: {
        server_name: 'unknown',
        tool_name: 'unknown',
        version: '1.0.0',
        timestamp: new Date().toISOString()
      }
    };
  }
}

/**
 * 验证响应是否成功
 */
export function isSuccessResponse<T>(response: MCPResponse<T>): response is MCPResponse<T> & { success: true; data: T } {
  return response.success === true && response.data !== undefined;
}

/**
 * 获取错误信息
 */
export function getErrorMessage(response: MCPResponse): string {
  if (response.success) {
    return '';
  }
  
  if (response.error) {
    let message = `[${response.error.code}] ${response.error.message}`;
    if (response.error.hint) {
      message += `\n提示: ${response.error.hint}`;
    }
    return message;
  }
  
  return '未知错误';
}

// ==================== MCP客户端类 ====================

/**
 * MCP客户端（用于文档和类型提示）
 * 
 * 注意：MCP工具由Cursor AI自动调用，扩展不直接调用
 * 这个类主要用于：
 * 1. 提供工具列表和参数说明
 * 2. 提供类型定义
 * 3. 提供响应解析工具
 */
export class MCPClient {
  /**
   * 获取所有可用工具列表
   */
  static getTools(): typeof MCP_TOOLS {
    return MCP_TOOLS;
  }
  
  /**
   * 获取工具描述（用于AI提示）
   */
  static getToolDescription(category: keyof typeof MCP_TOOLS, tool: string): string {
    const categoryTools = MCP_TOOLS[category] as Record<string, { description: string }>;
    const toolDef = categoryTools[tool];
    if (toolDef) {
      return toolDef.description;
    }
    return '';
  }
  
  /**
   * 构建工具调用参数
   */
  static buildParams<T extends Record<string, unknown>>(
    category: keyof typeof MCP_TOOLS,
    tool: string,
    params: Partial<T>
  ): T & { trace_id: string } {
    const trace_id = generateTraceId();
    return {
      ...params,
      trace_id
    } as T & { trace_id: string };
  }
  
  /**
   * 记录工具调用日志
   */
  static logToolCall(toolName: string, params: Record<string, unknown>): void {
    logger.info(`调用MCP工具: ${toolName}`, MODULE, {
      trace_id: params.trace_id,
      params: JSON.stringify(params).substring(0, 200)
    });
  }
  
  /**
   * 记录工具响应日志
   */
  static logToolResponse<T>(toolName: string, response: MCPResponse<T>): void {
    if (response.success) {
      logger.info(`MCP工具响应成功: ${toolName}`, MODULE, {
        trace_id: response.metadata.trace_id,
        duration_ms: response.metadata.duration_ms
      });
    } else {
      logger.error(`MCP工具响应失败: ${toolName}`, MODULE, {
        trace_id: response.metadata.trace_id,
        error_code: response.error?.code,
        error_message: response.error?.message
      });
    }
  }
}

// ==================== 导出 ====================

export default MCPClient;
