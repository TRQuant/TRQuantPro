/**
 * 策略状态管理
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface StrategyTemplate {
  id: string;
  name: string;
  type: string;
  description: string;
  risk_level: 'low' | 'medium' | 'high';
  category: string;
  parameters?: Record<string, any>;
}

export interface GeneratedStrategy {
  id: string;
  name: string;
  code: string;
  platform: 'ptrade' | 'qmt' | 'other';
  parameters: Record<string, any>;
  createdAt: string;
}

export interface BacktestResult {
  id: string;
  strategyId: string;
  strategyName: string;
  startDate: string;
  endDate: string;
  totalReturn: number;
  sharpeRatio: number;
  maxDrawdown: number;
  winRate: number;
  metrics: Record<string, any>;
  createdAt: string;
}

export interface StrategyState {
  templates: StrategyTemplate[];
  generated: GeneratedStrategy[];
  backtestResults: BacktestResult[];
  currentStrategy: GeneratedStrategy | null;
  currentBacktest: BacktestResult | null;
  loading: boolean;
  error: string | null;
}

interface StrategyActions {
  getTemplates: () => Promise<void>;
  generateStrategy: (templateId: string, params: Record<string, any>, platform: string) => Promise<void>;
  runBacktest: (strategyId: string, config: Record<string, any>) => Promise<void>;
  getBacktestResults: () => Promise<void>;
  setCurrentStrategy: (strategy: GeneratedStrategy | null) => void;
  setCurrentBacktest: (backtest: BacktestResult | null) => void;
  scanTrend: () => Promise<any>;
}

import { getVSCodeAPI } from '../utils/vscodeApi';

// 使用单例 VS Code API
const vscode = getVSCodeAPI();

async function callMCP<T>(tool: string, args: Record<string, any>): Promise<T> {
  return new Promise((resolve, reject) => {
    if (!vscode) {
      reject(new Error('VS Code API not available'));
      return;
    }
    const messageId = `mcp_${Date.now()}_${Math.random()}`;
    const handler = (event: MessageEvent) => {
      const message = event.data;
      if (message.type === 'mcpResult' && message.id === messageId) {
        window.removeEventListener('message', handler);
        if (message.error) {
          reject(new Error(message.error));
        } else {
          resolve(message.result as T);
        }
      }
    };
    window.addEventListener('message', handler);
    vscode.postMessage({
      type: 'mcpCall',
      id: messageId,
      tool,
      args,
    });
    setTimeout(() => {
      window.removeEventListener('message', handler);
      reject(new Error('MCP call timeout'));
    }, 30000);
  });
}

export const useStrategyStore = create<StrategyState & StrategyActions>()(
  persist(
    (set) => ({
      templates: [],
      generated: [],
      backtestResults: [],
      currentStrategy: null,
      currentBacktest: null,
      loading: false,
      error: null,
      getTemplates: async () => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<{ templates: StrategyTemplate[] }>('strategy.list_templates', {});
          set({ templates: result.templates || [], loading: false });
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      generateStrategy: async (templateId: string, params: Record<string, any>, platform: string) => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<{ strategy_id: string; name: string; code: string; platform: string }>('strategy.generate', {
            template_id: templateId,
            parameters: params,
            platform,
          });
          const strategy: GeneratedStrategy = {
            id: result.strategy_id,
            name: result.name,
            code: result.code,
            platform: platform as 'ptrade' | 'qmt' | 'other',
            parameters: params,
            createdAt: new Date().toISOString(),
          };
          set((state) => ({
            generated: [...state.generated, strategy],
            currentStrategy: strategy,
            loading: false,
          }));
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      runBacktest: async (strategyId: string, config: Record<string, any>) => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<BacktestResult>('backtest.run', { strategy_id: strategyId, config });
          set((state) => ({
            backtestResults: [...state.backtestResults, result],
            currentBacktest: result,
            loading: false,
          }));
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      getBacktestResults: async () => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<{ results: BacktestResult[] }>('backtest.list', {});
          set({ backtestResults: result.results || [], loading: false });
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      setCurrentStrategy: (strategy) => set({ currentStrategy: strategy }),
      setCurrentBacktest: (backtest) => set({ currentBacktest: backtest }),
      scanTrend: async () => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<any>('market.trend', {});
          set({ loading: false });
          return result;
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
          throw error;
        }
      },
    }),
    {
      name: 'trquant-strategy-store',
      partialize: (state) => ({
        templates: state.templates,
        generated: state.generated,
        backtestResults: state.backtestResults,
        currentStrategy: state.currentStrategy,
        currentBacktest: state.currentBacktest,
      }),
    }
  )
);
