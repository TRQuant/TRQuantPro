/**
 * 十倍股状态管理
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface StockRanking {
  symbol: string;
  name: string;
  price: number;
  change_pct: number;
  tenbagger_score: number;
  level: 'S' | 'A' | 'B' | 'C';
  stage: string;
  dimensions?: {
    growth: number;
    profitability: number;
    valuation: number;
    momentum: number;
    quality: number;
    stage: string;
    event_score: number;
  };
}

export interface EvaluationResult {
  symbol: string;
  name: string;
  score: number;
  level: 'S' | 'A' | 'B' | 'C';
  stage: string;
  dimensions: {
    growth: number;
    profitability: number;
    valuation: number;
    momentum: number;
    quality: number;
    stage: string;
    event_score: number;
  };
  report?: any;
}

export interface PipelineStatus {
  raw_docs: number;
  events: number;
  stages: number;
  candidates: number;
}

export interface TenbaggerState {
  rankings: StockRanking[];
  pipelineStatus: PipelineStatus;
  evaluations: Record<string, EvaluationResult>;
  selectedStock: StockRanking | null;
  loading: boolean;
  error: string | null;
}

interface TenbaggerActions {
  getRankings: (limit?: number) => Promise<void>;
  evaluateStock: (symbol: string, name?: string) => Promise<void>;
  getReport: (symbol: string) => Promise<void>;
  getPipelineStatus: () => Promise<void>;
  setSelectedStock: (stock: StockRanking | null) => void;
  refresh: () => Promise<void>;
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

export const useTenbaggerStore = create<TenbaggerState & TenbaggerActions>()(
  persist(
    (set, get) => ({
      rankings: [],
      pipelineStatus: { raw_docs: 0, events: 0, stages: 0, candidates: 0 },
      evaluations: {},
      selectedStock: null,
      loading: false,
      error: null,
      getRankings: async (limit = 20) => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<{ rankings: StockRanking[] }>('tenbagger.rank', { top_n: limit });
          set({ rankings: result.rankings || [], loading: false });
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      evaluateStock: async (symbol: string, name?: string) => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<EvaluationResult>('tenbagger.evaluate', { symbol, name: name || '' });
          set((state) => ({
            evaluations: { ...state.evaluations, [symbol]: result },
            loading: false,
          }));
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      getReport: async (symbol: string) => {
        set({ loading: true, error: null });
        try {
          const result = await callMCP<any>('tenbagger.report', { symbol });
          set((state) => ({
            evaluations: {
              ...state.evaluations,
              [symbol]: { ...state.evaluations[symbol], report: result },
            },
            loading: false,
          }));
        } catch (error) {
          set({ loading: false, error: (error as Error).message });
        }
      },
      getPipelineStatus: async () => {
        try {
          const result = await callMCP<{ counts: { raw_docs: number; events: number; stages: number; candidates: number } }>('tenbagger.pipeline_status', {});
          if (result.counts) {
            set({
              pipelineStatus: {
                raw_docs: result.counts.raw_docs || 0,
                events: result.counts.events || 0,
                stages: result.counts.stages || 0,
                candidates: result.counts.candidates || 0,
              },
            });
          }
        } catch (error) {
          console.error('获取数据管道状态失败:', error);
        }
      },
      setSelectedStock: (stock) => set({ selectedStock: stock }),
      refresh: async () => {
        const { getRankings, getPipelineStatus } = get();
        await Promise.all([getRankings(), getPipelineStatus()]);
      },
    }),
    {
      name: 'trquant-tenbagger-store',
      partialize: (state) => ({
        rankings: state.rankings,
        pipelineStatus: state.pipelineStatus,
        evaluations: state.evaluations,
      }),
    }
  )
);
