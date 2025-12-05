/**
 * 策略报告生成器
 * ==============
 * 
 * 生成完整的策略分析报告，包括：
 * - 投资理念说明
 * - 代码架构分析
 * - 平台兼容性
 * - 优化建议
 * - 可视化图表
 */

import {
    StrategyAnalysis,
    StrategyReport,
    Platform,
    ConversionResult,
    Optimization,
    ModuleDescription,
    MermaidChart
} from '../types';

// ============================================================
// 报告生成器类
// ============================================================

export class ReportGenerator {
    
    /**
     * 生成完整策略报告
     */
    generate(
        analysis: StrategyAnalysis,
        conversionResult?: ConversionResult
    ): StrategyReport {
        return {
            title: `${analysis.meta.name} - 策略分析报告`,
            generatedAt: new Date().toLocaleString('zh-CN'),
            version: '1.0.0',
            
            investmentPhilosophy: this.generatePhilosophy(analysis),
            codeArchitecture: this.generateArchitecture(analysis),
            platformCompatibility: this.generateCompatibility(analysis, conversionResult),
            optimizations: this.generateOptimizations(analysis),
            codeQuality: this.generateQuality(analysis)
        };
    }
    
    /**
     * 生成Markdown格式报告
     */
    generateMarkdown(
        analysis: StrategyAnalysis,
        conversionResult?: ConversionResult
    ): string {
        const report = this.generate(analysis, conversionResult);
        
        return `# ${report.title}

> 生成时间: ${report.generatedAt}
> 版本: ${report.version}

---

## 📊 投资理念

### 核心逻辑
${report.investmentPhilosophy.coreLogic}

### 市场适应
${report.investmentPhilosophy.marketAdaptation}

### 风险管理
${report.investmentPhilosophy.riskManagement}

### 特色亮点
${report.investmentPhilosophy.uniqueFeatures.map(f => `- ${f}`).join('\n')}

---

## 🏗️ 代码架构

### 概述
${report.codeArchitecture.overview}

### 模块说明

${report.codeArchitecture.modules.map(m => `
#### ${m.name}
- **用途**: ${m.purpose}
- **复杂度**: ${m.complexity}
- **函数**: ${m.functions.join(', ')}
- **依赖**: ${m.dependencies.join(', ') || '无'}
`).join('\n')}

### 流程图

\`\`\`mermaid
${report.codeArchitecture.flowChart}
\`\`\`

### 数据流

\`\`\`mermaid
${report.codeArchitecture.dataFlow}
\`\`\`

---

## 🔄 平台兼容性

${report.platformCompatibility.summary}

| 平台 | 兼容度 | 等级 | 需修改 | 备注 |
|------|--------|------|--------|------|
${Object.entries(report.platformCompatibility.details).map(([platform, info]) => 
    `| ${platform} | ${info.score}% | ${info.level} | ${info.changes}处 | ${info.notes.join('; ')} |`
).join('\n')}

---

## 💡 优化建议

### 性能优化
${report.optimizations.performance.map(o => this.formatOptimization(o)).join('\n')}

### 风控优化
${report.optimizations.risk.map(o => this.formatOptimization(o)).join('\n')}

### 代码可读性
${report.optimizations.readability.map(o => this.formatOptimization(o)).join('\n')}

### 平台适配
${report.optimizations.platform.map(o => this.formatOptimization(o)).join('\n')}

---

## 📈 代码质量

**总分: ${report.codeQuality.score}/100**

| 指标 | 得分 |
|------|------|
| 可维护性 | ${report.codeQuality.metrics.maintainability}/100 |
| 可测试性 | ${report.codeQuality.metrics.testability}/100 |
| 文档完整性 | ${report.codeQuality.metrics.documentation}/100 |
| 复杂度控制 | ${report.codeQuality.metrics.complexity}/100 |

### 改进建议
${report.codeQuality.suggestions.map(s => `- ${s}`).join('\n')}

---

*报告由 TRQuant Strategy Optimizer 自动生成*
`;
    }
    
    /**
     * 生成HTML格式报告
     */
    generateHTML(
        analysis: StrategyAnalysis,
        conversionResult?: ConversionResult
    ): string {
        const report = this.generate(analysis, conversionResult);
        
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${report.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        :root {
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #e2e8f0;
            --text-muted: #94a3b8;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        .meta {
            color: var(--text-muted);
            margin-bottom: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
            color: var(--primary);
            margin: 2rem 0 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        h3 {
            font-size: 1.2rem;
            margin: 1.5rem 0 0.5rem;
        }
        
        .card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }
        
        th, td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        th {
            background: rgba(99,102,241,0.2);
            font-weight: 600;
        }
        
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .badge-success { background: rgba(16,185,129,0.2); color: var(--success); }
        .badge-warning { background: rgba(245,158,11,0.2); color: var(--warning); }
        .badge-danger { background: rgba(239,68,68,0.2); color: var(--danger); }
        .badge-info { background: rgba(99,102,241,0.2); color: var(--primary); }
        
        .score {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .progress {
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 0.5rem;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            border-radius: 4px;
        }
        
        ul {
            list-style-position: inside;
            margin: 0.5rem 0;
        }
        
        li {
            margin: 0.25rem 0;
        }
        
        .mermaid {
            background: rgba(255,255,255,0.05);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .optimization {
            border-left: 3px solid var(--primary);
            padding-left: 1rem;
            margin: 1rem 0;
        }
        
        .optimization.high { border-color: var(--danger); }
        .optimization.medium { border-color: var(--warning); }
        .optimization.low { border-color: var(--success); }
        
        code {
            background: rgba(99,102,241,0.2);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-family: 'Fira Code', monospace;
            font-size: 0.9em;
        }
        
        pre {
            background: rgba(0,0,0,0.3);
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }
        
        pre code {
            background: none;
            padding: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>${report.title}</h1>
        <p class="meta">📅 ${report.generatedAt} | 🔖 版本 ${report.version}</p>
        
        <!-- 投资理念 -->
        <h2>📊 投资理念</h2>
        <div class="grid">
            <div class="card">
                <h3>🎯 核心逻辑</h3>
                <p>${report.investmentPhilosophy.coreLogic}</p>
            </div>
            <div class="card">
                <h3>📈 市场适应</h3>
                <p>${report.investmentPhilosophy.marketAdaptation}</p>
            </div>
            <div class="card">
                <h3>🛡️ 风险管理</h3>
                <p>${report.investmentPhilosophy.riskManagement}</p>
            </div>
        </div>
        <div class="card">
            <h3>✨ 特色亮点</h3>
            <ul>
                ${report.investmentPhilosophy.uniqueFeatures.map(f => `<li>${f}</li>`).join('')}
            </ul>
        </div>
        
        <!-- 代码架构 -->
        <h2>🏗️ 代码架构</h2>
        <div class="card">
            <p>${report.codeArchitecture.overview}</p>
        </div>
        
        <div class="grid">
            ${report.codeArchitecture.modules.map(m => `
            <div class="card">
                <h3>${m.name}</h3>
                <p>${m.purpose}</p>
                <p><span class="badge badge-info">${m.complexity}复杂度</span></p>
                <p><strong>函数:</strong> ${m.functions.join(', ')}</p>
            </div>
            `).join('')}
        </div>
        
        <div class="card">
            <h3>流程图</h3>
            <div class="mermaid">
${report.codeArchitecture.flowChart}
            </div>
        </div>
        
        <!-- 平台兼容性 -->
        <h2>🔄 平台兼容性</h2>
        <div class="card">
            <p>${report.platformCompatibility.summary}</p>
            <table>
                <tr>
                    <th>平台</th>
                    <th>兼容度</th>
                    <th>等级</th>
                    <th>需修改</th>
                    <th>备注</th>
                </tr>
                ${Object.entries(report.platformCompatibility.details).map(([platform, info]) => `
                <tr>
                    <td><strong>${platform}</strong></td>
                    <td>
                        <div>${info.score}%</div>
                        <div class="progress"><div class="progress-bar" style="width: ${info.score}%"></div></div>
                    </td>
                    <td><span class="badge ${info.score >= 80 ? 'badge-success' : info.score >= 50 ? 'badge-warning' : 'badge-danger'}">${info.level}</span></td>
                    <td>${info.changes}处</td>
                    <td>${info.notes.join('; ')}</td>
                </tr>
                `).join('')}
            </table>
        </div>
        
        <!-- 优化建议 -->
        <h2>💡 优化建议</h2>
        ${this.renderOptimizationsHTML(report.optimizations)}
        
        <!-- 代码质量 -->
        <h2>📈 代码质量</h2>
        <div class="card">
            <div style="text-align: center; margin-bottom: 1rem;">
                <div class="score">${report.codeQuality.score}</div>
                <div class="meta">总分 / 100</div>
            </div>
            <div class="grid">
                ${Object.entries(report.codeQuality.metrics).map(([key, value]) => `
                <div>
                    <div style="display: flex; justify-content: space-between;">
                        <span>${this.translateMetric(key)}</span>
                        <span>${value}/100</span>
                    </div>
                    <div class="progress"><div class="progress-bar" style="width: ${value}%"></div></div>
                </div>
                `).join('')}
            </div>
            <h3 style="margin-top: 1.5rem;">改进建议</h3>
            <ul>
                ${report.codeQuality.suggestions.map(s => `<li>${s}</li>`).join('')}
            </ul>
        </div>
        
        <p class="meta" style="text-align: center; margin-top: 3rem;">
            报告由 TRQuant Strategy Optimizer 自动生成
        </p>
    </div>
    
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'dark',
            themeVariables: {
                primaryColor: '#6366f1',
                primaryTextColor: '#e2e8f0',
                primaryBorderColor: '#4f46e5',
                lineColor: '#94a3b8',
                secondaryColor: '#1e293b',
                tertiaryColor: '#0f172a'
            }
        });
    </script>
</body>
</html>`;
    }
    
    // ============================================================
    // 私有方法
    // ============================================================
    
    /**
     * 生成投资理念
     */
    private generatePhilosophy(analysis: StrategyAnalysis): StrategyReport['investmentPhilosophy'] {
        const factors = analysis.dependencies.factors;
        const hasRisk = analysis.components.riskControl.length > 0;
        const hasTiming = analysis.components.timing.length > 0;
        
        // 根据因子类型确定核心逻辑
        let coreLogic = '基于';
        const factorTypes = [...new Set(factors.map(f => f.type))];
        if (factorTypes.length > 0) {
            const typeNames: Record<string, string> = {
                'value': '价值',
                'growth': '成长',
                'quality': '质量',
                'momentum': '动量',
                'volatility': '波动'
            };
            coreLogic += factorTypes.map(t => typeNames[t] || t).join('+') + '多因子模型';
        } else {
            coreLogic += '量化选股模型';
        }
        coreLogic += '，筛选具有投资价值的标的';
        
        // 市场适应
        let marketAdaptation = '';
        if (hasTiming) {
            marketAdaptation = '具备市场择时能力，根据市场趋势动态调整仓位';
        } else {
            marketAdaptation = '采用固定策略，适合长期持有';
        }
        
        // 风险管理
        let riskManagement = '';
        if (hasRisk) {
            const riskFuncs = analysis.components.riskControl.map(b => b.name);
            if (riskFuncs.some(f => f.includes('stop'))) {
                riskManagement = '设有止损止盈机制，控制单票风险';
            } else {
                riskManagement = '包含风险控制模块，管理组合风险';
            }
        } else {
            riskManagement = '建议添加风控模块以控制下行风险';
        }
        
        // 特色
        const uniqueFeatures: string[] = [];
        if (analysis.stats.complexity === 'low') {
            uniqueFeatures.push('代码简洁，易于理解和维护');
        }
        if (factors.length >= 3) {
            uniqueFeatures.push(`多维度因子评估（${factors.length}个因子）`);
        }
        if (hasTiming) {
            uniqueFeatures.push('动态市场适应能力');
        }
        if (hasRisk) {
            uniqueFeatures.push('完善的风险控制体系');
        }
        if (analysis.dependencies.indicators.length > 0) {
            uniqueFeatures.push(`技术指标辅助（${analysis.dependencies.indicators.map(i => i.name).join('、')}）`);
        }
        
        return {
            coreLogic,
            marketAdaptation,
            riskManagement,
            uniqueFeatures
        };
    }
    
    /**
     * 生成代码架构
     */
    private generateArchitecture(analysis: StrategyAnalysis): StrategyReport['codeArchitecture'] {
        const modules: ModuleDescription[] = [];
        
        // 选股模块
        if (analysis.components.stockSelection.length > 0) {
            modules.push({
                name: '选股模块',
                purpose: '根据因子筛选投资标的',
                functions: analysis.components.stockSelection.map(b => b.name),
                dependencies: ['数据获取', '因子计算'],
                complexity: analysis.components.stockSelection.length > 3 ? 'high' : 'medium'
            });
        }
        
        // 择时模块
        if (analysis.components.timing.length > 0) {
            modules.push({
                name: '择时模块',
                purpose: '判断市场趋势，生成交易信号',
                functions: analysis.components.timing.map(b => b.name),
                dependencies: ['市场数据', '技术指标'],
                complexity: 'medium'
            });
        }
        
        // 风控模块
        if (analysis.components.riskControl.length > 0) {
            modules.push({
                name: '风控模块',
                purpose: '控制风险，保护资金安全',
                functions: analysis.components.riskControl.map(b => b.name),
                dependencies: ['持仓数据', '价格数据'],
                complexity: 'medium'
            });
        }
        
        // 执行模块
        if (analysis.components.execution.length > 0) {
            modules.push({
                name: '执行模块',
                purpose: '执行交易指令，管理持仓',
                functions: analysis.components.execution.map(b => b.name),
                dependencies: ['选股结果', '风控检查'],
                complexity: 'medium'
            });
        }
        
        // 生成流程图
        const flowChart = this.generateFlowChart(analysis);
        const dataFlow = this.generateDataFlow(analysis);
        
        return {
            overview: `策略包含 ${modules.length} 个核心模块，${analysis.stats.functionCount} 个函数，代码复杂度为${analysis.stats.complexity === 'low' ? '低' : analysis.stats.complexity === 'medium' ? '中' : '高'}。`,
            modules,
            flowChart,
            dataFlow
        };
    }
    
    /**
     * 生成流程图
     */
    private generateFlowChart(analysis: StrategyAnalysis): string {
        return `graph TD
    A[策略启动] --> B[初始化配置]
    B --> C{每日执行}
    C --> D[数据获取]
    D --> E[选股筛选]
    E --> F[因子打分]
    F --> G{风控检查}
    G -->|通过| H[执行交易]
    G -->|不通过| I[调整持仓]
    H --> J[记录日志]
    I --> J
    J --> C
    
    style A fill:#6366f1,stroke:#4f46e5,color:#fff
    style H fill:#10b981,stroke:#059669,color:#fff
    style G fill:#f59e0b,stroke:#d97706,color:#fff`;
    }
    
    /**
     * 生成数据流图
     */
    private generateDataFlow(analysis: StrategyAnalysis): string {
        return `graph LR
    subgraph 数据层
        A1[行情数据]
        A2[财务数据]
        A3[持仓数据]
    end
    
    subgraph 计算层
        B1[因子计算]
        B2[指标计算]
        B3[风险评估]
    end
    
    subgraph 决策层
        C1[选股决策]
        C2[仓位决策]
        C3[交易执行]
    end
    
    A1 --> B1
    A2 --> B1
    A1 --> B2
    A3 --> B3
    B1 --> C1
    B2 --> C2
    B3 --> C2
    C1 --> C3
    C2 --> C3
    
    style A1 fill:#3b82f6,stroke:#2563eb,color:#fff
    style A2 fill:#3b82f6,stroke:#2563eb,color:#fff
    style A3 fill:#3b82f6,stroke:#2563eb,color:#fff
    style C3 fill:#10b981,stroke:#059669,color:#fff`;
    }
    
    /**
     * 生成兼容性报告
     */
    private generateCompatibility(
        analysis: StrategyAnalysis,
        conversionResult?: ConversionResult
    ): StrategyReport['platformCompatibility'] {
        const details: any = {};
        
        for (const platform of ['joinquant', 'ptrade', 'qmt'] as const) {
            const compat = analysis.compatibility[platform];
            details[platform] = {
                score: compat.score,
                level: this.translateLevel(compat.level),
                changes: compat.issues.filter((i: any) => i.severity === 'error').length,
                notes: compat.suggestions.slice(0, 2)
            };
        }
        
        const sourcePlatform = analysis.compatibility.sourcePlatform;
        const summary = `当前代码基于 ${sourcePlatform.toUpperCase()} 平台开发。` +
            `可直接在 ${sourcePlatform} 运行，转换到其他平台需要进行API适配。`;
        
        return { summary, details };
    }
    
    /**
     * 生成优化建议
     */
    private generateOptimizations(analysis: StrategyAnalysis): StrategyReport['optimizations'] {
        const optimizations: StrategyReport['optimizations'] = {
            performance: [],
            risk: [],
            readability: [],
            platform: []
        };
        
        // 性能优化
        if (analysis.stats.totalLines > 500) {
            optimizations.performance.push({
                category: '性能',
                priority: 'medium',
                title: '代码量较大',
                description: '策略代码超过500行，建议拆分模块',
                impact: '提高代码可维护性和执行效率'
            });
        }
        
        // 风控优化
        if (analysis.components.riskControl.length === 0) {
            optimizations.risk.push({
                category: '风控',
                priority: 'high',
                title: '缺少风控模块',
                description: '建议添加止损、止盈、仓位管理等风控机制',
                impact: '控制下行风险，保护资金安全',
                implementation: '添加 check_risk() 函数，设置止损线-8%，止盈线20%'
            });
        }
        
        // 可读性优化
        if (analysis.stats.commentLines < analysis.stats.codeLines * 0.2) {
            optimizations.readability.push({
                category: '文档',
                priority: 'low',
                title: '注释不足',
                description: '代码注释比例低于20%，建议增加注释',
                impact: '提高代码可读性和可维护性'
            });
        }
        
        // 平台优化
        for (const platform of ['ptrade', 'qmt'] as const) {
            const compat = analysis.compatibility[platform];
            if (compat.score < 100) {
                optimizations.platform.push({
                    category: '平台适配',
                    priority: compat.score < 50 ? 'high' : 'medium',
                    title: `${platform.toUpperCase()} 适配`,
                    description: `需要修改 ${compat.issues.filter((i: any) => i.severity === 'error').length} 处API调用`,
                    impact: `支持在 ${platform.toUpperCase()} 平台运行`,
                    implementation: compat.suggestions.join('\n')
                });
            }
        }
        
        return optimizations;
    }
    
    /**
     * 生成代码质量评估
     */
    private generateQuality(analysis: StrategyAnalysis): StrategyReport['codeQuality'] {
        const metrics = {
            maintainability: 0,
            testability: 0,
            documentation: 0,
            complexity: 0
        };
        
        // 可维护性
        metrics.maintainability = Math.min(100, Math.max(0,
            100 - (analysis.stats.totalLines / 10) + 
            (analysis.stats.functionCount * 5) -
            (analysis.stats.complexity === 'high' ? 20 : analysis.stats.complexity === 'medium' ? 10 : 0)
        ));
        
        // 可测试性
        metrics.testability = Math.min(100,
            analysis.stats.functionCount * 10 +
            (analysis.components.utilities.length * 5)
        );
        
        // 文档完整性
        const docRatio = analysis.stats.commentLines / analysis.stats.totalLines;
        metrics.documentation = Math.min(100, docRatio * 200);
        
        // 复杂度控制
        metrics.complexity = analysis.stats.complexity === 'low' ? 90 :
            analysis.stats.complexity === 'medium' ? 70 : 50;
        
        const score = Math.round(
            (metrics.maintainability + metrics.testability + 
             metrics.documentation + metrics.complexity) / 4
        );
        
        const suggestions: string[] = [];
        if (metrics.maintainability < 70) {
            suggestions.push('建议拆分大函数，保持单个函数不超过50行');
        }
        if (metrics.testability < 70) {
            suggestions.push('建议增加工具函数，提高代码复用性');
        }
        if (metrics.documentation < 70) {
            suggestions.push('建议为每个函数添加docstring说明');
        }
        if (metrics.complexity < 70) {
            suggestions.push('建议简化复杂逻辑，使用设计模式重构');
        }
        
        return {
            score,
            metrics: {
                maintainability: Math.round(metrics.maintainability),
                testability: Math.round(metrics.testability),
                documentation: Math.round(metrics.documentation),
                complexity: Math.round(metrics.complexity)
            },
            suggestions
        };
    }
    
    /**
     * 格式化优化建议
     */
    private formatOptimization(opt: Optimization): string {
        return `
#### ${opt.priority === 'high' ? '🔴' : opt.priority === 'medium' ? '🟡' : '🟢'} ${opt.title}

- **优先级**: ${opt.priority === 'high' ? '高' : opt.priority === 'medium' ? '中' : '低'}
- **描述**: ${opt.description}
- **影响**: ${opt.impact}
${opt.implementation ? `- **实现**: ${opt.implementation}` : ''}
`;
    }
    
    /**
     * 渲染优化建议HTML
     */
    private renderOptimizationsHTML(optimizations: StrategyReport['optimizations']): string {
        const categories = [
            { key: 'performance', title: '🚀 性能优化', items: optimizations.performance },
            { key: 'risk', title: '🛡️ 风控优化', items: optimizations.risk },
            { key: 'readability', title: '📖 代码可读性', items: optimizations.readability },
            { key: 'platform', title: '🔄 平台适配', items: optimizations.platform }
        ];
        
        return categories.map(cat => `
            <div class="card">
                <h3>${cat.title}</h3>
                ${cat.items.length === 0 ? '<p class="meta">暂无优化建议</p>' : 
                  cat.items.map(opt => `
                    <div class="optimization ${opt.priority}">
                        <h4>${opt.title}</h4>
                        <p>${opt.description}</p>
                        <p class="meta">影响: ${opt.impact}</p>
                        ${opt.implementation ? `<p><strong>建议:</strong> ${opt.implementation}</p>` : ''}
                    </div>
                  `).join('')
                }
            </div>
        `).join('');
    }
    
    /**
     * 翻译兼容性等级
     */
    private translateLevel(level: string): string {
        const map: Record<string, string> = {
            'full': '完全兼容',
            'high': '高度兼容',
            'medium': '部分兼容',
            'low': '低兼容',
            'none': '不兼容'
        };
        return map[level] || level;
    }
    
    /**
     * 翻译质量指标
     */
    private translateMetric(key: string): string {
        const map: Record<string, string> = {
            'maintainability': '可维护性',
            'testability': '可测试性',
            'documentation': '文档完整性',
            'complexity': '复杂度控制'
        };
        return map[key] || key;
    }
}

// 导出单例
export const reportGenerator = new ReportGenerator();

