/**
 * 配置管理模块
 * 
 * 集中管理所有配置项，支持默认值和类型安全
 * 遵循开闭原则 - 对扩展开放，对修改关闭
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as os from 'os';
import * as fs from 'fs';
import { logger } from './logger';

/**
 * 配置接口定义
 */
export interface TRQuantConfig {
    // Python配置
    pythonPath: string;
    
    // 服务器配置
    serverHost: string;
    serverPort: number;
    timeout: number;
    
    // MCP配置
    mcpEnabled: boolean;
    mcpPort: number;
    
    // 功能配置
    autoRefresh: boolean;
    refreshInterval: number;
    
    // 策略配置
    defaultPlatform: 'ptrade' | 'qmt';
    defaultStyle: string;
    
    // 风控默认参数
    defaultRiskParams: {
        maxPosition: number;
        stopLoss: number;
        takeProfit: number;
    };
}

/**
 * 默认配置
 */
const DEFAULT_CONFIG: TRQuantConfig = {
    pythonPath: os.platform() === 'win32' ? 'python' : 'python3',
    serverHost: '127.0.0.1',
    serverPort: 5000,
    timeout: 60000,
    mcpEnabled: true,
    mcpPort: 5001,
    autoRefresh: false,
    refreshInterval: 300000, // 5分钟
    defaultPlatform: 'ptrade',
    defaultStyle: 'multi_factor',
    defaultRiskParams: {
        maxPosition: 0.1,
        stopLoss: 0.08,
        takeProfit: 0.2
    }
};

/**
 * 配置管理器
 */
export class ConfigManager {
    private static instance: ConfigManager;
    private config: TRQuantConfig;
    private disposables: vscode.Disposable[] = [];

    private constructor() {
        this.config = this.loadConfig();
        
        // 监听配置变化
        this.disposables.push(
            vscode.workspace.onDidChangeConfiguration(e => {
                if (e.affectsConfiguration('trquant')) {
                    this.config = this.loadConfig();
                }
            })
        );
    }

    /**
     * 获取单例
     */
    static getInstance(): ConfigManager {
        if (!ConfigManager.instance) {
            ConfigManager.instance = new ConfigManager();
        }
        return ConfigManager.instance;
    }

    /**
     * 加载配置
     */
    private loadConfig(): TRQuantConfig {
        const wsConfig = vscode.workspace.getConfiguration('trquant');
        
        return {
            pythonPath: wsConfig.get<string>('pythonPath') || DEFAULT_CONFIG.pythonPath,
            serverHost: wsConfig.get<string>('serverHost') || DEFAULT_CONFIG.serverHost,
            serverPort: wsConfig.get<number>('serverPort') || DEFAULT_CONFIG.serverPort,
            timeout: wsConfig.get<number>('timeout') || DEFAULT_CONFIG.timeout,
            mcpEnabled: wsConfig.get<boolean>('mcpEnabled') ?? DEFAULT_CONFIG.mcpEnabled,
            mcpPort: wsConfig.get<number>('mcpPort') || DEFAULT_CONFIG.mcpPort,
            autoRefresh: wsConfig.get<boolean>('autoRefresh') ?? DEFAULT_CONFIG.autoRefresh,
            refreshInterval: wsConfig.get<number>('refreshInterval') || DEFAULT_CONFIG.refreshInterval,
            defaultPlatform: wsConfig.get<'ptrade' | 'qmt'>('defaultPlatform') || DEFAULT_CONFIG.defaultPlatform,
            defaultStyle: wsConfig.get<string>('defaultStyle') || DEFAULT_CONFIG.defaultStyle,
            defaultRiskParams: {
                maxPosition: wsConfig.get<number>('defaultMaxPosition') || DEFAULT_CONFIG.defaultRiskParams.maxPosition,
                stopLoss: wsConfig.get<number>('defaultStopLoss') || DEFAULT_CONFIG.defaultRiskParams.stopLoss,
                takeProfit: wsConfig.get<number>('defaultTakeProfit') || DEFAULT_CONFIG.defaultRiskParams.takeProfit
            }
        };
    }

    /**
     * 获取完整配置
     */
    getConfig(): Readonly<TRQuantConfig> {
        return { ...this.config };
    }

    /**
     * 获取单个配置项
     */
    get<K extends keyof TRQuantConfig>(key: K): TRQuantConfig[K] {
        return this.config[key];
    }

    /**
     * 更新配置项
     */
    async set<K extends keyof TRQuantConfig>(
        key: K, 
        value: TRQuantConfig[K],
        target: vscode.ConfigurationTarget = vscode.ConfigurationTarget.Global
    ): Promise<void> {
        const wsConfig = vscode.workspace.getConfiguration('trquant');
        await wsConfig.update(key, value, target);
    }

    /**
     * 获取Python解释器完整路径
     * 
     * 优先级：
     * 0. 硬编码标准路径: /home/taotao/dev/QuantTest/TRQuant/venv/bin/python
     * 1. 工作区路径/venv/bin/python (项目根目录)
     * 2. TRQUANT_ROOT/venv/bin/python (环境变量)
     * 3. extensionPath/venv/bin/python (开发模式)
     * 4. 配置的路径
     */
        getPythonPath(extensionPath: string): string {
        const configPath = this.config.pythonPath;
        const isWindows = os.platform() === 'win32';
        
        // 辅助函数：获取venv中的python路径
        const getVenvPython = (venvPath: string) => isWindows
            ? path.join(venvPath, 'Scripts', 'python.exe')
            : path.join(venvPath, 'bin', 'python');
        
        // 0. 硬编码标准路径（最高优先级）- 强制使用
        const standardPython = '/home/taotao/dev/QuantTest/TRQuant/venv/bin/python';
        if (!isWindows) {
            try {
                if (fs.existsSync(standardPython)) {
                    logger.debug(`使用硬编码标准Python路径: ${standardPython}`, 'ConfigManager');
                    return standardPython;
                } else {
                    logger.warn(`硬编码路径不存在，但继续尝试: ${standardPython}`, 'ConfigManager');
                    // 即使不存在也返回，让spawn自己处理错误
                    return standardPython;
                }
            } catch (error) {
                logger.warn(`检查硬编码路径时出错: ${error}`, 'ConfigManager');
                // 即使出错也返回标准路径
                return standardPython;
            }
        }
        
        // 如果是绝对路径且文件存在，直接返回
        if (path.isAbsolute(configPath) && fs.existsSync(configPath)) {
            return configPath;
        }
        
        // 1. 首先检查工作区路径下的 venv（项目根目录）
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (workspaceFolders && workspaceFolders.length > 0) {
            const workspacePath = workspaceFolders[0].uri.fsPath;
            const workspaceVenvPython = getVenvPython(path.join(workspacePath, 'venv'));
            if (fs.existsSync(workspaceVenvPython)) {
                logger.debug(`使用工作区Python路径: ${workspaceVenvPython}`, 'ConfigManager');
                return workspaceVenvPython;
            }
        }
        
        // 2. 通过TRQUANT_ROOT环境变量找到项目根目录
        const trquantRoot = process.env.TRQUANT_ROOT;
        if (trquantRoot) {
            const envVenvPython = getVenvPython(path.join(trquantRoot, 'venv'));
            if (fs.existsSync(envVenvPython)) {
                logger.debug(`使用TRQUANT_ROOT Python路径: ${envVenvPython}`, 'ConfigManager');
                return envVenvPython;
            }
        }
        
        // 3. 检查extensionPath下的venv（开发模式，扩展在项目目录中）
        const extVenvPython = getVenvPython(path.join(extensionPath, 'venv'));
        if (fs.existsSync(extVenvPython)) {
            logger.debug(`使用扩展路径Python: ${extVenvPython}`, 'ConfigManager');
            return extVenvPython;
        }
        
        // 4. 尝试从extensionPath推断项目根目录
        if (extensionPath.endsWith('extension') || extensionPath.endsWith('extension/') || extensionPath.endsWith('extension\\')) {
            const projectRoot = path.dirname(extensionPath);
            const inferredVenvPython = getVenvPython(path.join(projectRoot, 'venv'));
            if (fs.existsSync(inferredVenvPython)) {
                logger.debug(`使用推断的Python路径: ${inferredVenvPython}`, 'ConfigManager');
                return inferredVenvPython;
            }
        }
        
        // 5. 回退到配置的路径或系统python
        logger.warn(`未找到venv Python，回退到: ${configPath}`, 'ConfigManager');
        return configPath;
    }
        

    /**
     * 释放资源
     */
    dispose(): void {
        this.disposables.forEach(d => d.dispose());
    }
}

// 导出便捷方法
export const config = ConfigManager.getInstance();

