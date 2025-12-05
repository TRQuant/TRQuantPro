/**
 * 开发者功能区 TreeView Provider
 * ==============================
 * 
 * 提供开发者工具：
 * - 本地备份（复制文件到备份目录）
 * - Git Commit（提交到Git仓库）
 * - 刷新系统（重编译+安装+Reload Window）
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as cp from 'child_process';
import { logger } from '../utils/logger';

const MODULE = 'DeveloperProvider';

/**
 * 开发者功能项
 */
class DeveloperItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly command?: vscode.Command,
        public readonly icon?: string
    ) {
        super(label, collapsibleState);
        this.tooltip = label;
        this.contextValue = this.getContextValue();
        
        if (icon) {
            this.iconPath = new vscode.ThemeIcon(icon);
        }
    }
    
    private getContextValue(): string {
        if (this.label.includes('本地备份')) {
            return 'localBackup';
        } else if (this.label.includes('Git Commit')) {
            return 'gitCommit';
        } else if (this.label.includes('刷新')) {
            return 'refresh';
        }
        return '';
    }
}

/**
 * 开发者功能区数据提供者
 */
export class DeveloperProvider implements vscode.TreeDataProvider<DeveloperItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<DeveloperItem | undefined | null | void> = new vscode.EventEmitter<DeveloperItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<DeveloperItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private context: vscode.ExtensionContext) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: DeveloperItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: DeveloperItem): Thenable<DeveloperItem[]> {
        if (!element) {
            // 根节点：显示所有开发者功能
            return Promise.resolve([
                new DeveloperItem(
                    '💾 本地备份',
                    vscode.TreeItemCollapsibleState.None,
                    {
                        command: 'trquant.localBackup',
                        title: '本地备份',
                        arguments: []
                    },
                    'save'
                ),
                new DeveloperItem(
                    '📝 Git Commit',
                    vscode.TreeItemCollapsibleState.None,
                    {
                        command: 'trquant.gitCommit',
                        title: 'Git Commit',
                        arguments: []
                    },
                    'git-commit'
                ),
                new DeveloperItem(
                    '🔄 刷新系统',
                    vscode.TreeItemCollapsibleState.None,
                    {
                        command: 'trquant.refreshSystem',
                        title: '刷新系统',
                        arguments: []
                    },
                    'sync'
                )
            ]);
        }
        return Promise.resolve([]);
    }
}

/**
 * 注册开发者功能区
 */
export function registerDeveloperProvider(context: vscode.ExtensionContext): void {
    const provider = new DeveloperProvider(context);
    
    // 注册TreeView
    const treeView = vscode.window.createTreeView('trquant-developer', {
        treeDataProvider: provider,
        showCollapseAll: false
    });
    
    context.subscriptions.push(treeView);
    
    // 注册刷新命令
    const refreshCommand = vscode.commands.registerCommand('trquant.refreshDeveloper', () => {
        provider.refresh();
    });
    context.subscriptions.push(refreshCommand);
    
    logger.info('开发者功能区已注册', MODULE);
}

/**
 * 本地备份功能
 * 复制项目文件到备份目录（排除 node_modules, .git, .backups 等）
 */
export async function localBackup(context: vscode.ExtensionContext): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showWarningMessage('请先打开一个工作区');
        return;
    }

    const projectRoot = workspaceFolder.uri.fsPath;
    
    // 需要排除的目录和文件
    const excludePatterns = [
        'node_modules',
        '.git',
        '.backups',
        'venv',
        '__pycache__',
        '.pytest_cache',
        '.vscode',
        '.cursor',
        '*.pyc',
        '*.pyo',
        '*.log',
        'dist',
        'build',
        '*.vsix'
    ];
    
    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '💾 本地备份',
            cancellable: false
        }, async (progress) => {
            // 创建备份目录
            const backupDir = path.join(projectRoot, '.backups');
            if (!fs.existsSync(backupDir)) {
                fs.mkdirSync(backupDir, { recursive: true });
            }
            
            const backupTimestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const backupName = `backup-${backupTimestamp}`;
            const backupPath = path.join(backupDir, backupName);
            
            progress.report({ increment: 0, message: '正在创建备份目录...' });
            
            // 创建备份目录
            if (!fs.existsSync(backupPath)) {
                fs.mkdirSync(backupPath, { recursive: true });
            }
            
            // 创建备份说明文件
            const backupInfo = {
                timestamp: new Date().toISOString(),
                projectRoot: projectRoot,
                backupPath: backupPath
            };
            fs.writeFileSync(
                path.join(backupPath, 'backup-info.json'),
                JSON.stringify(backupInfo, null, 2),
                'utf-8'
            );
            
            progress.report({ increment: 10, message: '正在复制文件...' });
            
            // 复制文件
            await copyDirectory(projectRoot, backupPath, excludePatterns, progress);
            
            progress.report({ increment: 100, message: '备份完成！' });
            
            vscode.window.showInformationMessage(
                `✅ 本地备份完成！\n备份位置: ${backupPath}`,
                { modal: false }
            );
            
            logger.info('本地备份完成', MODULE, { backupPath });
        });
        
    } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error);
        logger.error(`本地备份失败: ${errorMsg}`, MODULE);
        vscode.window.showErrorMessage(`本地备份失败: ${errorMsg}`);
    }
}

/**
 * Git Commit 功能
 * 执行 git add 和 git commit
 */
export async function gitCommit(context: vscode.ExtensionContext): Promise<void> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        vscode.window.showWarningMessage('请先打开一个工作区');
        return;
    }

    const projectRoot = workspaceFolder.uri.fsPath;
    const gitDir = path.join(projectRoot, '.git');
    
    if (!fs.existsSync(gitDir)) {
        const result = await vscode.window.showWarningMessage(
            '当前目录不是Git仓库，是否初始化Git仓库？',
            '是',
            '否'
        );
        if (result !== '是') {
            return;
        }
        
        // 初始化Git仓库
        try {
            await executeCommand('git', ['init'], projectRoot);
            vscode.window.showInformationMessage('✅ Git仓库初始化成功');
        } catch (error) {
            vscode.window.showErrorMessage(`Git初始化失败: ${error}`);
            return;
        }
    }

    // 显示输入框让用户输入commit消息
    const timestamp = new Date().toISOString().slice(0, 19).replace('T', ' ');
    const commitMessage = await vscode.window.showInputBox({
        prompt: '请输入提交消息',
        placeHolder: '例如: feat: 添加新功能',
        value: `backup: ${timestamp}`
    });

    if (!commitMessage) {
        return;
    }

    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '📝 Git Commit',
            cancellable: false
        }, async (progress) => {
            progress.report({ increment: 0, message: '正在执行 git add...' });
            
            // 1. Git add
            await executeCommand('git', ['add', '-A'], projectRoot);
            logger.info('Git add 完成', MODULE);
            
            progress.report({ increment: 50, message: '正在执行 git commit...' });
            
            // 2. Git commit
            await executeCommand('git', ['commit', '-m', commitMessage], projectRoot);
            logger.info('Git commit 完成', MODULE);
            
            progress.report({ increment: 100, message: '提交完成！' });
            
            vscode.window.showInformationMessage(
                `✅ Git Commit 完成！\n提交消息: ${commitMessage}`,
                { modal: false }
            );
            
            logger.info('Git Commit 完成', MODULE, { commitMessage });
        });
        
    } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error);
        logger.error(`Git Commit 失败: ${errorMsg}`, MODULE);
        vscode.window.showErrorMessage(`Git Commit 失败: ${errorMsg}`);
    }
}

/**
 * 刷新系统功能
 * 执行：重编译 -> 安装扩展 -> Reload Window
 */
export async function refreshSystem(context: vscode.ExtensionContext): Promise<void> {
    // 获取扩展的安装路径或开发路径
    const extensionRoot = context.extensionPath;
    // 如果是开发模式，extensionPath 指向 extension/ 目录
    // 如果是安装模式，extensionPath 指向 ~/.cursor/extensions/xxx/
    // 我们需要找到包含 package.json 的目录
    let extensionDir = extensionRoot;
    
    // 检查是否是开发模式（extension/ 目录）
    const devPackageJson = path.join(extensionRoot, 'package.json');
    if (!fs.existsSync(devPackageJson)) {
        // 安装模式，尝试找到项目根目录
        // 通常项目根目录在 extensionPath 的上两级
        const possibleRoot = path.resolve(extensionRoot, '../../..');
        const rootPackageJson = path.join(possibleRoot, 'extension', 'package.json');
        if (fs.existsSync(rootPackageJson)) {
            extensionDir = path.join(possibleRoot, 'extension');
        } else {
            vscode.window.showErrorMessage('无法找到扩展开发目录。请在开发模式下使用此功能。');
            return;
        }
    }
    
    // 检查 package.json 是否存在
    const packageJson = path.join(extensionDir, 'package.json');
    if (!fs.existsSync(packageJson)) {
        vscode.window.showErrorMessage('未找到 package.json');
        return;
    }
    
    try {
        // 显示进度
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '🔄 刷新系统',
            cancellable: false
        }, async (progress) => {
            // 步骤1: 检查并安装依赖
            progress.report({ increment: 0, message: '正在检查依赖...' });
            logger.info('开始刷新系统', MODULE, { extensionDir });
            
            try {
                // 检查 node_modules 是否存在
                const nodeModules = path.join(extensionDir, 'node_modules');
                if (!fs.existsSync(nodeModules)) {
                    progress.report({ increment: 5, message: '正在安装依赖...' });
                    await executeShellCommand('npm install', extensionDir);
                    logger.info('依赖安装完成', MODULE);
                } else {
                    logger.info('依赖已存在，跳过安装', MODULE);
                }
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                logger.warn(`依赖检查/安装失败，继续尝试编译: ${errorMsg}`, MODULE);
            }
            
            // 步骤2: 编译 TypeScript
            progress.report({ increment: 20, message: '正在编译TypeScript...' });
            try {
                await executeShellCommand('npm run compile', extensionDir);
                progress.report({ increment: 40, message: '编译完成，正在打包扩展...' });
                logger.info('TypeScript编译完成', MODULE);
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                throw new Error(`编译失败: ${errorMsg}`);
            }
            
            // 步骤3: 打包扩展
            progress.report({ increment: 60, message: '正在打包扩展...' });
            try {
                await executeShellCommand('npx @vscode/vsce package --allow-missing-repository --no-dependencies', extensionDir);
                progress.report({ increment: 80, message: '打包完成，正在安装扩展...' });
                logger.info('扩展打包完成', MODULE);
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                throw new Error(`打包失败: ${errorMsg}`);
            }
            
            // 步骤4: 安装扩展
            progress.report({ increment: 90, message: '正在安装扩展...' });
            try {
                const vsixFiles = fs.readdirSync(extensionDir)
                    .filter(f => f.endsWith('.vsix'))
                    .sort()
                    .reverse();
                
                if (vsixFiles.length === 0) {
                    throw new Error('未找到.vsix文件');
                }
                
                const vsixPath = path.join(extensionDir, vsixFiles[0]);
                await executeShellCommand(`cursor --install-extension "${vsixPath}" --force`, extensionDir);
                progress.report({ increment: 100, message: '安装完成，即将重新加载窗口...' });
                logger.info('扩展安装完成', MODULE);
            } catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                throw new Error(`安装失败: ${errorMsg}`);
            }
        });
        
        // 步骤4: Reload Window
        vscode.window.showInformationMessage(
            '✅ 系统刷新完成！窗口即将重新加载...',
            { modal: false }
        );
        
        // 延迟一下再reload，让用户看到消息
        setTimeout(() => {
            vscode.commands.executeCommand('workbench.action.reloadWindow');
        }, 1000);
        
    } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error);
        logger.error(`刷新系统失败: ${errorMsg}`, MODULE);
        vscode.window.showErrorMessage(`刷新系统失败: ${errorMsg}`);
    }
}

/**
 * 执行命令的辅助函数
 */
function executeCommand(command: string, args: string[], cwd: string): Promise<string> {
    return new Promise((resolve, reject) => {
        // 不使用 shell: true，这样可以正确处理包含空格的参数
        const proc = cp.spawn(command, args, {
            cwd: cwd,
            shell: false,
            stdio: ['ignore', 'pipe', 'pipe']
        });
        
        let stdout = '';
        let stderr = '';
        
        proc.stdout?.on('data', (data) => {
            stdout += data.toString();
        });
        
        proc.stderr?.on('data', (data) => {
            stderr += data.toString();
        });
        
        proc.on('close', (code) => {
            if (code === 0) {
                resolve(stdout);
            } else {
                reject(new Error(`命令执行失败 (退出码: ${code}): ${stderr || stdout}`));
            }
        });
        
        proc.on('error', (error) => {
            reject(new Error(`命令执行错误: ${error.message}`));
        });
    });
}

/**
 * 执行 shell 命令的辅助函数（用于需要 shell 特性的命令）
 */
function executeShellCommand(command: string, cwd: string): Promise<string> {
    return new Promise((resolve, reject) => {
        cp.exec(command, { cwd }, (error, stdout, stderr) => {
            if (error) {
                reject(new Error(`命令执行失败: ${stderr || error.message}`));
            } else {
                resolve(stdout);
            }
        });
    });
}

/**
 * 复制目录（排除指定模式）
 */
async function copyDirectory(
    src: string,
    dest: string,
    excludePatterns: string[],
    progress: vscode.Progress<{ message?: string; increment?: number }>
): Promise<void> {
    const shouldExclude = (name: string): boolean => {
        return excludePatterns.some(pattern => {
            if (pattern.includes('*')) {
                // 简单的通配符匹配
                const regex = new RegExp('^' + pattern.replace(/\*/g, '.*') + '$');
                return regex.test(name);
            }
            return name === pattern || name.includes(pattern);
        });
    };
    
    const copyRecursive = async (srcDir: string, destDir: string): Promise<void> => {
        const entries = fs.readdirSync(srcDir, { withFileTypes: true });
        
        for (const entry of entries) {
            const srcPath = path.join(srcDir, entry.name);
            const destPath = path.join(destDir, entry.name);
            
            // 跳过排除项
            if (shouldExclude(entry.name)) {
                continue;
            }
            
            // 跳过备份目录本身
            if (srcPath === dest || srcPath.startsWith(dest + path.sep)) {
                continue;
            }
            
            if (entry.isDirectory()) {
                fs.mkdirSync(destPath, { recursive: true });
                await copyRecursive(srcPath, destPath);
            } else if (entry.isFile()) {
                fs.copyFileSync(srcPath, destPath);
            }
        }
    };
    
    await copyRecursive(src, dest);
}

