/**
 * MCP Server 注册器
 * 将TRQuant MCP Server注册到Cursor
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export class MCPRegistrar {
    /**
     * 注册MCP Server到Cursor
     */
    static async registerServer(context: vscode.ExtensionContext): Promise<void> {
        const extensionPath = context.extensionPath;
        const mcpServerPath = path.join(extensionPath, 'python', 'mcp_server.py');

        // 检查MCP Server文件是否存在
        if (!fs.existsSync(mcpServerPath)) {
            throw new Error(`MCP Server文件不存在: ${mcpServerPath}`);
        }

        // 获取Python路径
        const config = vscode.workspace.getConfiguration('trquant');
        const pythonPath = config.get<string>('pythonPath') || 'python';

        // 尝试使用Cursor MCP API（如果可用）
        try {
            // @ts-ignore - Cursor特有API
            if (vscode.cursor?.mcp?.registerServer) {
                // @ts-ignore
                await vscode.cursor.mcp.registerServer({
                    name: 'trquant',
                    command: pythonPath,
                    args: [mcpServerPath],
                    env: {
                        PYTHONIOENCODING: 'utf-8',
                        TRQUANT_ROOT: path.dirname(extensionPath)
                    }
                });
                console.log('TRQuant MCP Server registered via Cursor API');
                return;
            }
        } catch (e) {
            console.log('Cursor MCP API not available, using fallback');
        }

        // Fallback: 写入.cursor/mcp.json配置文件
        await this.writeConfigFile(context, pythonPath, mcpServerPath);
    }

    /**
     * 写入MCP配置文件
     */
    private static async writeConfigFile(
        context: vscode.ExtensionContext,
        pythonPath: string,
        mcpServerPath: string
    ): Promise<void> {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders || workspaceFolders.length === 0) {
            throw new Error('没有打开的工作区');
        }

        const workspaceRoot = workspaceFolders[0].uri.fsPath;
        const cursorDir = path.join(workspaceRoot, '.cursor');
        const mcpConfigPath = path.join(cursorDir, 'mcp.json');

        // 确保.cursor目录存在
        if (!fs.existsSync(cursorDir)) {
            fs.mkdirSync(cursorDir, { recursive: true });
        }

        // 读取现有配置或创建新配置
        let mcpConfig: any = { mcpServers: {} };
        if (fs.existsSync(mcpConfigPath)) {
            try {
                mcpConfig = JSON.parse(fs.readFileSync(mcpConfigPath, 'utf-8'));
            } catch (e) {
                // 忽略解析错误，使用默认配置
            }
        }

        // 添加TRQuant MCP Server配置
        mcpConfig.mcpServers = mcpConfig.mcpServers || {};
        mcpConfig.mcpServers['trquant'] = {
            command: pythonPath,
            args: [mcpServerPath],
            env: {
                PYTHONIOENCODING: 'utf-8',
                TRQUANT_ROOT: path.dirname(context.extensionPath)
            }
        };

        // 写入配置文件
        fs.writeFileSync(mcpConfigPath, JSON.stringify(mcpConfig, null, 2));
        console.log(`MCP config written to ${mcpConfigPath}`);
    }

    /**
     * 注销MCP Server
     */
    static async unregisterServer(context: vscode.ExtensionContext): Promise<void> {
        try {
            // @ts-ignore
            if (vscode.cursor?.mcp?.unregisterServer) {
                // @ts-ignore
                await vscode.cursor.mcp.unregisterServer('trquant');
            }
        } catch (e) {
            // 忽略
        }
    }
}

