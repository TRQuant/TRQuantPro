/**
 * 策略优化器类型定义
 * ===================
 * 
 * 定义策略分析、平台适配、报告生成所需的所有类型
 */

// ============================================================
// 平台类型
// ============================================================

export type Platform = 'joinquant' | 'ptrade' | 'qmt' | 'universal';
export type RealPlatform = 'joinquant' | 'ptrade' | 'qmt';

export interface PlatformInfo {
    name: string;
    displayName: string;
    description: string;
    apiVersion: string;
    features: string[];
}

export const PLATFORMS: Record<Platform, PlatformInfo> = {
    joinquant: {
        name: 'joinquant',
        displayName: '聚宽 JoinQuant',
        description: '量化研究和回测平台',
        apiVersion: '2.0',
        features: ['回测', '模拟交易', '研究环境']
    },
    ptrade: {
        name: 'ptrade',
        displayName: 'PTrade',
        description: '恒生实盘交易系统',
        apiVersion: '1.0',
        features: ['实盘交易', '程序化交易', '多账户']
    },
    qmt: {
        name: 'qmt',
        displayName: 'QMT迅投',
        description: '迅投量化交易平台',
        apiVersion: '2.0',
        features: ['实盘交易', '高频交易', '策略回测']
    },
    universal: {
        name: 'universal',
        displayName: '通用格式',
        description: 'TRQuant统一格式',
        apiVersion: '1.0',
        features: ['跨平台', '标准化', '可移植']
    }
};

// ============================================================
// 代码分析类型
// ============================================================

export interface CodeBlock {
    type: 'function' | 'class' | 'variable' | 'import' | 'comment' | 'logic';
    name: string;
    startLine: number;
    endLine: number;
    content: string;
    category?: 'selection' | 'timing' | 'risk' | 'execution' | 'util';
    dependencies?: string[];
}

export interface APIUsage {
    name: string;
    platform: Platform;
    line: number;
    params: Record<string, any>;
    context: string;
    canConvert: boolean;
    targetAPI?: string;
}

export interface FactorUsage {
    name: string;
    type: 'value' | 'growth' | 'quality' | 'momentum' | 'volatility' | 'technical' | 'custom';
    weight?: number;
    description?: string;
}

export interface IndicatorUsage {
    name: string;
    type: 'ma' | 'macd' | 'rsi' | 'kdj' | 'boll' | 'atr' | 'custom';
    params?: Record<string, any>;
}

export interface CompatibilityScore {
    score: number;          // 0-100
    level: 'full' | 'high' | 'medium' | 'low' | 'none';
    issues: CompatibilityIssue[];
    suggestions: string[];
}

export interface CompatibilityIssue {
    severity: 'error' | 'warning' | 'info';
    line: number;
    message: string;
    api: string;
    suggestion: string;
}

// ============================================================
// 策略分析结果
// ============================================================

export interface StrategyAnalysis {
    // 元信息
    meta: {
        name: string;
        author?: string;
        createTime?: string;
        description: string;
        backtestPeriod?: {
            start: string;
            end: string;
        };
        benchmark?: string;
    };

    // 核心组件
    components: {
        stockSelection: CodeBlock[];   // 选股逻辑
        timing: CodeBlock[];           // 择时逻辑
        riskControl: CodeBlock[];      // 风控逻辑
        execution: CodeBlock[];        // 执行逻辑
        utilities: CodeBlock[];        // 工具函数
    };

    // 依赖分析
    dependencies: {
        apis: APIUsage[];              // 使用的API
        factors: FactorUsage[];        // 使用的因子
        indicators: IndicatorUsage[];  // 使用的指标
        imports: string[];             // 导入的模块
    };

    // 平台兼容性
    compatibility: {
        sourcePlatform: Platform;
        joinquant: CompatibilityScore;
        ptrade: CompatibilityScore;
        qmt: CompatibilityScore;
    };

    // 统计信息
    stats: {
        totalLines: number;
        codeLines: number;
        commentLines: number;
        functionCount: number;
        classCount: number;
        complexity: 'low' | 'medium' | 'high';
    };
}

// ============================================================
// 平台适配类型
// ============================================================

export interface APIMapping {
    source: {
        platform: Platform;
        api: string;
        signature: string;
    };
    target: {
        platform: Platform;
        api: string;
        signature: string;
    };
    paramMapping: Record<string, string | ((value: any, context: any) => any)>;
    returnMapping?: (result: any) => any;
    notes?: string[];
    examples?: {
        before: string;
        after: string;
    };
}

export interface ConversionResult {
    success: boolean;
    targetPlatform: Platform;
    originalCode: string;
    convertedCode: string;
    changes: CodeChange[];
    warnings: string[];
    errors: string[];
    stats: {
        totalChanges: number;
        apiChanges: number;
        structureChanges: number;
        addedLines: number;
        removedLines: number;
    };
}

export interface CodeChange {
    type: 'api_replace' | 'param_change' | 'structure_change' | 'add' | 'remove' | 'comment';
    line: number;
    original: string;
    converted: string;
    reason: string;
}

// ============================================================
// 报告类型
// ============================================================

export interface StrategyReport {
    // 基本信息
    title: string;
    generatedAt: string;
    version: string;

    // 投资理念
    investmentPhilosophy: {
        coreLogic: string;
        marketAdaptation: string;
        riskManagement: string;
        uniqueFeatures: string[];
    };

    // 代码架构
    codeArchitecture: {
        overview: string;
        modules: ModuleDescription[];
        flowChart: string;  // Mermaid格式
        dataFlow: string;   // Mermaid格式
    };

    // 平台兼容性
    platformCompatibility: {
        summary: string;
        details: Record<Platform, {
            score: number;
            level: string;
            changes: number;
            notes: string[];
        }>;
    };

    // 优化建议
    optimizations: {
        performance: Optimization[];
        risk: Optimization[];
        readability: Optimization[];
        platform: Optimization[];
    };

    // 代码质量
    codeQuality: {
        score: number;
        metrics: {
            maintainability: number;
            testability: number;
            documentation: number;
            complexity: number;
        };
        suggestions: string[];
    };
}

export interface ModuleDescription {
    name: string;
    purpose: string;
    functions: string[];
    dependencies: string[];
    complexity: 'low' | 'medium' | 'high';
}

export interface Optimization {
    category: string;
    priority: 'high' | 'medium' | 'low';
    title: string;
    description: string;
    impact: string;
    implementation?: string;
    codeExample?: {
        before: string;
        after: string;
    };
}

// ============================================================
// 学习引擎类型
// ============================================================

export interface LearningData {
    patterns: StrategyPattern[];
    apiMappings: APIMapping[];
    bestPractices: BestPractice[];
    userFeedback: UserFeedback[];
}

export interface StrategyPattern {
    id: string;
    name: string;
    category: 'selection' | 'timing' | 'risk' | 'execution';
    description: string;
    codeTemplate: string;
    effectiveness: number;  // 0-100
    usageCount: number;
}

export interface BestPractice {
    id: string;
    title: string;
    category: string;
    description: string;
    example: string;
    references: string[];
}

export interface UserFeedback {
    timestamp: string;
    strategyId: string;
    type: 'correction' | 'improvement' | 'bug' | 'feature';
    content: string;
    resolved: boolean;
}

// ============================================================
// 可视化类型
// ============================================================

export interface VisualizationData {
    flowChart: MermaidChart;
    architectureDiagram: MermaidChart;
    dependencyGraph: MermaidChart;
    compatibilityMatrix: CompatibilityMatrix;
}

export interface MermaidChart {
    type: 'flowchart' | 'sequence' | 'class' | 'state' | 'er' | 'pie';
    direction?: 'TD' | 'LR' | 'BT' | 'RL';
    content: string;
}

export interface CompatibilityMatrix {
    platforms: Platform[];
    features: string[];
    matrix: Record<string, Record<Platform, boolean | 'partial'>>;
}

