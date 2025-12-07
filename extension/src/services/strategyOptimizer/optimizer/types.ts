/**
 * 策略优化模块类型定义
 * =====================
 * 
 * 根据《策略优化模块设计方案》定义的类型
 */

// ============================================================
// 优化算法类型
// ============================================================

export type OptimizationAlgorithm = 
    | 'grid_search'      // 网格搜索
    | 'random_search'    // 随机搜索
    | 'bayesian'         // 贝叶斯优化
    | 'genetic'          // 遗传算法
    | 'reinforcement'    // 强化学习
    | 'simulated_annealing'  // 模拟退火
    | 'pso';            // 粒子群优化

export interface OptimizationConfig {
    algorithm: OptimizationAlgorithm;
    maxIterations?: number;
    maxTime?: number;  // 最大运行时间（秒）
    parallel?: boolean;  // 是否并行执行
    randomSeed?: number;
    // 算法特定参数
    algorithmParams?: Record<string, unknown>;
}

// ============================================================
// 策略参数定义
// ============================================================

export interface ParameterRange {
    name: string;
    type: 'int' | 'float' | 'bool' | 'categorical';
    min?: number;
    max?: number;
    step?: number;
    values?: (string | number | boolean)[];  // 分类变量的可选值
    default?: string | number | boolean;
    description?: string;
}

export interface StrategyConfig {
    code?: string;  // 策略代码
    configFile?: string;  // 配置文件路径
    parameters: Record<string, string | number | boolean>;  // 当前参数值
    parameterRanges: ParameterRange[];  // 可优化参数范围
    fixedParameters?: Record<string, string | number | boolean>;  // 固定参数（不可优化）
    constraints?: OptimizationConstraint[];  // 约束条件
}

// ============================================================
// 优化约束
// ============================================================

export interface OptimizationConstraint {
    type: 'max_drawdown' | 'max_position' | 'max_turnover' | 'factor_exposure' | 'industry_concentration' | 'custom';
    condition: string;  // 约束条件表达式
    value: number;  // 约束值
    description?: string;
}

// ============================================================
// 优化目标
// ============================================================

export interface OptimizationObjective {
    metric: 'sharpe_ratio' | 'annual_return' | 'max_drawdown' | 'calmar_ratio' | 'win_rate' | 'profit_factor' | 'custom';
    direction: 'maximize' | 'minimize';
    weight?: number;  // 多目标优化时的权重
    target?: number;  // 目标值（可选）
}

export interface OptimizationTarget {
    objectives: OptimizationObjective[];
    constraints?: OptimizationConstraint[];
}

// ============================================================
// 回测结果
// ============================================================

export interface BacktestMetrics {
    // 收益指标
    totalReturn: number;           // 总收益率
    annualReturn: number;           // 年化收益率
    monthlyReturn?: number[];       // 月度收益序列
    
    // 风险指标
    volatility: number;             // 波动率
    maxDrawdown: number;            // 最大回撤
    sharpeRatio: number;            // 夏普比率
    calmarRatio: number;            // 卡玛比率
    
    // 交易指标
    winRate: number;                // 胜率
    profitFactor: number;           // 盈亏比
    totalTrades: number;            // 总交易次数
    avgHoldDays: number;            // 平均持仓天数
    
    // 因子暴露
    factorExposure?: Record<string, number>;
    
    // 其他
    benchmarkReturn?: number;       // 基准收益
    alpha?: number;                 // Alpha
    beta?: number;                  // Beta
}

export interface BacktestResult {
    strategyId: string;
    strategyVersion: string;
    parameters: Record<string, string | number | boolean>;
    metrics: BacktestMetrics;
    equityCurve?: number[];         // 权益曲线
    trades?: TradeRecord[];         // 交易记录
    positions?: PositionRecord[];    // 持仓记录
    timestamp: string;
    backtestConfig?: {
        startDate: string;
        endDate: string;
        initialCapital: number;
        commission: number;
    };
}

export interface TradeRecord {
    date: string;
    symbol: string;
    action: 'buy' | 'sell';
    price: number;
    quantity: number;
    commission: number;
    pnl?: number;
}

export interface PositionRecord {
    date: string;
    symbol: string;
    quantity: number;
    price: number;
    value: number;
}

// ============================================================
// 优化迭代结果
// ============================================================

export interface OptimizationIteration {
    iteration: number;
    candidateId: string;
    parameters: Record<string, string | number | boolean>;
    backtestResult: BacktestResult;
    score: number;  // 综合评分
    timestamp: string;
}

export interface OptimizationProgress {
    currentIteration: number;
    totalIterations?: number;
    bestScore: number;
    bestParameters: Record<string, string | number | boolean>;
    iterations: OptimizationIteration[];
    status: 'running' | 'completed' | 'stopped' | 'error';
    startTime: string;
    elapsedTime?: number;  // 已用时间（秒）
}

// ============================================================
// 优化结果
// ============================================================

export interface OptimizationResult {
    optimizationId: string;
    strategyId: string;
    algorithm: OptimizationAlgorithm;
    config: OptimizationConfig;
    target: OptimizationTarget;
    
    // 最佳策略
    bestStrategy: {
        version: string;
        parameters: Record<string, string | number | boolean>;
        backtestResult: BacktestResult;
        score: number;
    };
    
    // 对比结果
    comparison: {
        original: BacktestResult;
        optimized: BacktestResult;
        improvement: {
            metric: string;
            before: number;
            after: number;
            change: number;  // 变化百分比
        }[];
    };
    
    // 优化过程
    progress: OptimizationProgress;
    
    // 策略改动说明
    changes: StrategyChange[];
    
    // 优化日志
    log: OptimizationLogEntry[];
    
    timestamp: string;
}

export interface StrategyChange {
    type: 'parameter' | 'logic' | 'factor' | 'risk_control';
    description: string;
    before: string | number | boolean | null | Record<string, unknown>;
    after: string | number | boolean | null | Record<string, unknown>;
    reason: string;
    impact: string;
}

export interface OptimizationLogEntry {
    timestamp: string;
    level: 'info' | 'warning' | 'error';
    message: string;
    data?: unknown;
}

// ============================================================
// 上下文信息
// ============================================================

export interface MarketContext {
    regime: 'bull' | 'bear' | 'neutral' | 'unknown';
    mainlines?: string[];  // 投资主线
    riskPreference?: 'aggressive' | 'moderate' | 'conservative';
    marketFactors?: Record<string, number>;  // 市场因子
    timestamp: string;
}

export interface OptimizationContext {
    marketContext: MarketContext;
    strategyTemplate?: string;  // 策略模板ID
    availableFactors?: string[];  // 可用因子列表
    dataVersion?: string;  // 数据版本
}

// ============================================================
// 版本管理
// ============================================================

export interface StrategyVersion {
    versionId: string;
    strategyId: string;
    version: string;  // 如 "v20251201_r3"
    parameters: Record<string, string | number | boolean>;
    code?: string;
    backtestResult?: BacktestResult;
    generatedBy: 'algorithm' | 'ai' | 'manual';
    tags?: string[];
    notes?: string;
    timestamp: string;
    parentVersion?: string;  // 父版本ID
}

export interface VersionComparison {
    version1: StrategyVersion;
    version2: StrategyVersion;
    differences: {
        parameters: Record<string, { before: string | number | boolean; after: string | number | boolean }>;
        codeDiff?: string;
        performanceDiff: {
            metric: string;
            before: number;
            after: number;
            change: number;
        }[];
    };
}

// ============================================================
// AI辅助改写
// ============================================================

export interface AIOptimizationRequest {
    strategyCode: string;
    backtestResult: BacktestResult;
    optimizationGoal: string;  // 优化目标描述
    constraints?: string[];  // 约束条件描述
    context?: OptimizationContext;
}

export interface AIOptimizationResponse {
    modifiedCode: string;
    changes: StrategyChange[];
    explanation: string;
    confidence?: number;
}























