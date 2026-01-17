// Stub file
import * as vscode from 'vscode';
import { TRQuantClient } from '../services/trquantClient';
export async function runBacktest(client: TRQuantClient, context: vscode.ExtensionContext): Promise<void> {
    vscode.window.showInformationMessage('运行回测功能开发中');
}
