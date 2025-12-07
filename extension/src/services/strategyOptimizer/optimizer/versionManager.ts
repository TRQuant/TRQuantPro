/**
 * 版本管理器
 * ==========
 * 
 * 管理策略版本，支持：
 * - 保存版本快照
 * - 查询版本列表
 * - 对比版本差异
 * - 回滚到指定版本
 */

// import * as vscode from 'vscode'; // 暂时未使用
import * as fs from 'fs';
import * as path from 'path';
import { logger } from '../../../utils/logger';
import { VersionManager, VersionInfo } from './interfaces';
import { BacktestResult } from './types';

const MODULE = 'VersionManager';

/** 完整版本信息 */
interface FullVersionInfo extends VersionInfo {
    code: string;
    tags: string[];
    metadata: Record<string, unknown>;
}

/**
 * 版本管理器实现
 */
export class VersionManagerImpl implements VersionManager {
    private storagePath: string;
    private versions: Map<string, FullVersionInfo[]> = new Map();
    
    constructor(storagePath: string) {
        this.storagePath = storagePath;
        this.ensureStorageExists();
        this.loadAllVersions();
    }
    
    /**
     * 确保存储目录存在
     */
    private ensureStorageExists(): void {
        const versionDir = path.join(this.storagePath, 'versions');
        if (!fs.existsSync(versionDir)) {
            fs.mkdirSync(versionDir, { recursive: true });
        }
    }
    
    /**
     * 加载所有版本
     */
    private loadAllVersions(): void {
        try {
            const versionDir = path.join(this.storagePath, 'versions');
            const files = fs.readdirSync(versionDir);
            
            for (const file of files) {
                if (file.endsWith('.json')) {
                    const strategyId = file.replace('.json', '');
                    const filePath = path.join(versionDir, file);
                    const content = fs.readFileSync(filePath, 'utf-8');
                    const versions = JSON.parse(content) as FullVersionInfo[];
                    this.versions.set(strategyId, versions);
                }
            }
            
            logger.info(`加载了 ${this.versions.size} 个策略的版本数据`, MODULE);
        } catch (error) {
            logger.warn(`加载版本数据失败: ${error}`, MODULE);
        }
    }
    
    /**
     * 保存版本到文件
     */
    private saveVersionsToFile(strategyId: string): void {
        try {
            const versionDir = path.join(this.storagePath, 'versions');
            const filePath = path.join(versionDir, `${strategyId}.json`);
            const versions = this.versions.get(strategyId) || [];
            fs.writeFileSync(filePath, JSON.stringify(versions, null, 2));
        } catch (error) {
            logger.error(`保存版本失败: ${error}`, MODULE);
            throw error;
        }
    }
    
    /**
     * 保存策略版本
     */
    async saveVersion(info: {
        strategyId: string;
        version: string;
        parameters: Record<string, string | number | boolean>;
        code: string;
        backtestResult?: BacktestResult;
        generatedBy: 'user' | 'algorithm' | 'ai';
        notes?: string;
    }): Promise<void> {
        const versionInfo: FullVersionInfo = {
            strategyId: info.strategyId,
            version: info.version,
            timestamp: new Date().toISOString(),
            parameters: info.parameters,
            backtestResult: info.backtestResult,
            notes: info.notes || '',
            code: info.code,
            tags: [],
            metadata: {
                generatedBy: info.generatedBy,
                savedAt: Date.now()
            }
        };
        
        if (!this.versions.has(info.strategyId)) {
            this.versions.set(info.strategyId, []);
        }
        
        const strategyVersions = this.versions.get(info.strategyId)!;
        
        // 检查是否存在相同版本号
        const existingIndex = strategyVersions.findIndex(v => v.version === info.version);
        if (existingIndex >= 0) {
            // 更新现有版本
            strategyVersions[existingIndex] = versionInfo;
        } else {
            // 添加新版本
            strategyVersions.unshift(versionInfo);
        }
        
        // 限制版本数量（保留最近50个）
        if (strategyVersions.length > 50) {
            strategyVersions.splice(50);
        }
        
        this.saveVersionsToFile(info.strategyId);
        logger.info(`版本已保存: ${info.strategyId} ${info.version}`, MODULE);
    }
    
    /**
     * 获取版本列表
     */
    async getVersions(strategyId: string): Promise<VersionInfo[]> {
        const versions = this.versions.get(strategyId) || [];
        return versions.map(v => ({
            strategyId: v.strategyId,
            version: v.version,
            timestamp: v.timestamp,
            parameters: v.parameters,
            backtestResult: v.backtestResult,
            notes: v.notes
        }));
    }
    
    /**
     * 获取指定版本
     */
    async getVersion(strategyId: string, version: string): Promise<VersionInfo | null> {
        const versions = this.versions.get(strategyId) || [];
        const versionInfo = versions.find(v => v.version === version);
        
        if (!versionInfo) {
            return null;
        }
        
        return {
            strategyId: versionInfo.strategyId,
            version: versionInfo.version,
            timestamp: versionInfo.timestamp,
            parameters: versionInfo.parameters,
            backtestResult: versionInfo.backtestResult,
            notes: versionInfo.notes
        };
    }
    
    /**
     * 获取版本代码
     */
    async getVersionCode(strategyId: string, version: string): Promise<string | null> {
        const versions = this.versions.get(strategyId) || [];
        const versionInfo = versions.find(v => v.version === version);
        return versionInfo?.code || null;
    }
    
    /**
     * 对比两个版本
     */
    async compareVersions(
        strategyId: string,
        version1: string,
        version2: string
    ): Promise<{
        parameterChanges: Array<{
            parameter: string;
            oldValue: string | number | boolean;
            newValue: string | number | boolean;
        }>;
        performanceComparison: {
            metric: string;
            version1Value: number;
            version2Value: number;
            change: number;
            changePercent: number;
        }[];
        codeChanges?: {
            additions: number;
            deletions: number;
            diff: string;
        };
    }> {
        const versions = this.versions.get(strategyId) || [];
        const v1 = versions.find(v => v.version === version1);
        const v2 = versions.find(v => v.version === version2);
        
        if (!v1 || !v2) {
            throw new Error('版本不存在');
        }
        
        // 参数变化
        const parameterChanges: Array<{
            parameter: string;
            oldValue: string | number | boolean;
            newValue: string | number | boolean;
        }> = [];
        
        const allParams = new Set([
            ...Object.keys(v1.parameters),
            ...Object.keys(v2.parameters)
        ]);
        
        for (const param of allParams) {
            const oldValue = v1.parameters[param];
            const newValue = v2.parameters[param];
            if (oldValue !== newValue) {
                parameterChanges.push({ parameter: param, oldValue, newValue });
            }
        }
        
        // 性能对比
        const performanceComparison: {
            metric: string;
            version1Value: number;
            version2Value: number;
            change: number;
            changePercent: number;
        }[] = [];
        
        const metrics = ['totalReturn', 'annualizedReturn', 'sharpeRatio', 'maxDrawdown', 'winRate'];
        
        for (const metric of metrics) {
            const metricKey = metric as keyof import('./types').BacktestMetrics;
            const v1Value = typeof v1.backtestResult?.metrics[metricKey] === 'number' 
                ? v1.backtestResult.metrics[metricKey] 
                : 0;
            const v2Value = typeof v2.backtestResult?.metrics[metricKey] === 'number'
                ? v2.backtestResult.metrics[metricKey]
                : 0;
            const change = v2Value - v1Value;
            const changePercent = v1Value !== 0 ? (change / Math.abs(v1Value)) * 100 : 0;
            
            performanceComparison.push({
                metric,
                version1Value: v1Value,
                version2Value: v2Value,
                change,
                changePercent
            });
        }
        
        // 代码变化（简单统计）
        const code1Lines = v1.code.split('\n');
        const code2Lines = v2.code.split('\n');
        
        let additions = 0;
        let deletions = 0;
        
        // 简单diff算法
        const code1Set = new Set(code1Lines);
        const code2Set = new Set(code2Lines);
        
        for (const line of code2Lines) {
            if (!code1Set.has(line)) additions++;
        }
        for (const line of code1Lines) {
            if (!code2Set.has(line)) deletions++;
        }
        
        return {
            parameterChanges,
            performanceComparison,
            codeChanges: {
                additions,
                deletions,
                diff: `+${additions} / -${deletions} 行`
            }
        };
    }
    
    /**
     * 删除版本
     */
    async deleteVersion(strategyId: string, version: string): Promise<void> {
        const versions = this.versions.get(strategyId);
        if (!versions) return;
        
        const index = versions.findIndex(v => v.version === version);
        if (index >= 0) {
            versions.splice(index, 1);
            this.saveVersionsToFile(strategyId);
            logger.info(`版本已删除: ${strategyId} ${version}`, MODULE);
        }
    }
    
    /**
     * 为版本添加标签
     */
    async addTag(strategyId: string, version: string, tag: string): Promise<void> {
        const versions = this.versions.get(strategyId);
        if (!versions) return;
        
        const versionInfo = versions.find(v => v.version === version);
        if (versionInfo && !versionInfo.tags.includes(tag)) {
            versionInfo.tags.push(tag);
            this.saveVersionsToFile(strategyId);
        }
    }
    
    /**
     * 按标签查找版本
     */
    async findByTag(strategyId: string, tag: string): Promise<VersionInfo[]> {
        const versions = this.versions.get(strategyId) || [];
        return versions
            .filter(v => v.tags.includes(tag))
            .map(v => ({
                strategyId: v.strategyId,
                version: v.version,
                timestamp: v.timestamp,
                parameters: v.parameters,
                backtestResult: v.backtestResult,
                notes: v.notes
            }));
    }
    
    /**
     * 获取最佳版本（按指定指标）
     */
    async getBestVersion(
        strategyId: string,
        metric: 'sharpeRatio' | 'totalReturn' | 'maxDrawdown'
    ): Promise<VersionInfo | null> {
        const versions = this.versions.get(strategyId) || [];
        
        if (versions.length === 0) return null;
        
        let best = versions[0];
        const metricKey = metric as keyof import('./types').BacktestMetrics;
        let bestValue = typeof best.backtestResult?.metrics[metricKey] === 'number'
            ? best.backtestResult.metrics[metricKey]
            : 0;
        
        for (const v of versions) {
            const value = typeof v.backtestResult?.metrics[metricKey] === 'number'
                ? v.backtestResult.metrics[metricKey]
                : 0;
            
            // 对于回撤，越小越好
            const isBetter = metric === 'maxDrawdown'
                ? value < bestValue
                : value > bestValue;
            
            if (isBetter) {
                best = v;
                bestValue = value;
            }
        }
        
        return {
            strategyId: best.strategyId,
            version: best.version,
            timestamp: best.timestamp,
            parameters: best.parameters,
            backtestResult: best.backtestResult,
            notes: best.notes
        };
    }
    
    /**
     * 导出版本历史
     */
    async exportVersionHistory(strategyId: string): Promise<string> {
        const versions = this.versions.get(strategyId) || [];
        
        let markdown = `# 策略版本历史: ${strategyId}\n\n`;
        markdown += `生成时间: ${new Date().toLocaleString('zh-CN')}\n\n`;
        markdown += `共 ${versions.length} 个版本\n\n`;
        markdown += `---\n\n`;
        
        for (const v of versions) {
            markdown += `## ${v.version}\n\n`;
            markdown += `- **时间**: ${new Date(v.timestamp).toLocaleString('zh-CN')}\n`;
            markdown += `- **备注**: ${v.notes || '无'}\n`;
            markdown += `- **生成方式**: ${v.metadata.generatedBy}\n`;
            
            if (v.backtestResult?.metrics) {
                const m = v.backtestResult.metrics;
                markdown += `\n### 回测指标\n\n`;
                markdown += `| 指标 | 值 |\n`;
                markdown += `|------|----|\n`;
                markdown += `| 总收益 | ${(m.totalReturn * 100).toFixed(2)}% |\n`;
                markdown += `| 夏普比率 | ${m.sharpeRatio.toFixed(2)} |\n`;
                markdown += `| 最大回撤 | ${(m.maxDrawdown * 100).toFixed(2)}% |\n`;
            }
            
            markdown += `\n### 参数\n\n`;
            markdown += '```json\n';
            markdown += JSON.stringify(v.parameters, null, 2);
            markdown += '\n```\n\n';
            
            markdown += `---\n\n`;
        }
        
        return markdown;
    }
}

/**
 * 创建版本管理器
 */
export function createVersionManager(storagePath: string): VersionManager {
    return new VersionManagerImpl(storagePath);
}




















