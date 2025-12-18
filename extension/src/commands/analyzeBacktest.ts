// Stub file
import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
export async function analyzeBacktest(client: TRQuantClient, context: vscode.ExtensionContext): Promise<void> {
    vscode.window.showInformationMessage('回测分析功能开发中');
}
