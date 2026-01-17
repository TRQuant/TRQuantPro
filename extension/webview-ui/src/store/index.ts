/**
 * 统一状态管理 (App Store)
 * 
 * 集成各个模块的状态，提供统一的访问入口。
 * 为了保持向后兼容，保留了部分逻辑，但底层通信已迁移到 WebviewMCPClient。
 */

import { create } from 'zustand';
import { getWebviewMCPClient } from '../services/webviewMCPClient';
import { Stock, Mainline } from '../types';

// 重新导出所有Store
export { useWorkflowStore } from './workflowStore';
export { useTenbaggerStore } from './tenbaggerStore';
export { useStrategyStore } from './strategyStore';

// 工作流状态
interface WorkflowState {
  workflowId: string | null;
  currentStep: number;
  stepResults: Record<number, any>;
  isLoading: boolean;
  error: string | null;
}

// 十倍股状态
interface TenbaggerState {
  rankings: Stock[];
  evaluating: boolean;
  selectedStock: Stock | null;
}

// 策略状态
interface StrategyState {
  templates: any[];
  currentStrategy: any | null;
  backtestResult: any | null;
}

// 应用状态
interface AppState {
  // UI状态
  activeTab: string;
  setActiveTab: (tab: string) => void;
  
  // 工作流
  workflow: WorkflowState;
  mainlines: Mainline[];
  candidatePool: Stock[];
  
  // 十倍股
  tenbagger: TenbaggerState;
  
  // 策略
  strategy: StrategyState;
  
  // 十倍股数据管道状态
  pipelineStatus: {
    raw_docs: number;
    events: number;
    stages: number;
    candidates: number;
  };
  setPipelineStatus: (status: AppState['pipelineStatus']) => void;
  
  // 统一的 MCP 调用
  callMCP: <T>(tool: string, args?: Record<string, any>) => Promise<T>;
  
  // 工作流操作
  createWorkflow: () => Promise<void>;
  runWorkflowStep: (step: number) => Promise<void>;
  updateWorkflowStepResult: (step: number, result: { success: boolean; result?: any; error?: string; details?: string }) => void;
  setWorkflowLoading: (loading: boolean, step?: number) => void;
  setMainlines: (mainlines: Mainline[]) => void;
  setCandidatePool: (stocks: Stock[]) => void;
  
  // 十倍股操作
  evaluateStock: (code: string) => Promise<void>;
  getRankings: () => Promise<void>;
  getPipelineStatus: () => Promise<void>;
  
  // 策略操作
  getStrategyTemplates: () => Promise<void>;
  scanTrend: () => Promise<void>;
}

export const useAppStore = create<AppState>((set, get) => ({
  // UI状态
  activeTab: 'workflow',
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  // 工作流初始状态
  workflow: {
    workflowId: null,
    currentStep: 0,
    stepResults: {},
    isLoading: false,
    error: null,
  },
  mainlines: [],
  candidatePool: [],
  
  // 十倍股初始状态
  tenbagger: {
    rankings: [],
    evaluating: false,
    selectedStock: null,
  },
  
  // 十倍股数据管道状态
  pipelineStatus: {
    raw_docs: 0,
    events: 0,
    stages: 0,
    candidates: 0,
  },
  setPipelineStatus: (status) => set({ pipelineStatus: status }),
  
  // 策略初始状态
  strategy: {
    templates: [],
    currentStrategy: null,
    backtestResult: null,
  },
  
  // 统一的 MCP 调用 (使用 WebviewMCPClient)
  callMCP: async <T>(tool: string, args: Record<string, any> = {}): Promise<T> => {
    const client = getWebviewMCPClient();
    return client.callTool<T>(tool, args);
  },
  
  // 工作流操作
  createWorkflow: async () => {
    const { callMCP } = get();
    set(state => ({ 
      workflow: { ...state.workflow, isLoading: true, error: null } 
    }));
    
    try {
      const result = await callMCP<{ workflow_id: string }>('workflow9.create', {});
      set(state => ({
        workflow: {
          ...state.workflow,
          workflowId: result.workflow_id,
          isLoading: false,
        }
      }));
    } catch (error) {
      set(state => ({
        workflow: {
          ...state.workflow,
          isLoading: false,
          error: (error as Error).message,
        }
      }));
    }
  },
  
  runWorkflowStep: async (step: number) => {
    const { callMCP, workflow } = get();
    const stepIdMap: Record<number, string> = {
      1: 'data_source',
      2: 'market_trend',
      3: 'mainline',
      4: 'candidate_pool',
      5: 'factor',
      6: 'strategy',
      7: 'backtest',
      8: 'optimize',
      9: 'report',
    };
    
    set(state => ({
      workflow: { ...state.workflow, isLoading: true, error: null }
    }));
    
    try {
      // 确保有工作流
      let workflowId = workflow.workflowId;
      if (!workflowId) {
        const createResult = await callMCP<{ workflow_id: string }>('workflow9.create', {});
        workflowId = createResult.workflow_id;
        set(state => ({
          workflow: { ...state.workflow, workflowId }
        }));
      }
      
      const result = await callMCP<any>('workflow9.run_step', {
        workflow_id: workflowId,
        step_id: stepIdMap[step],
      });
      
      // 处理返回结果：可能是 { success, step_id, step_result } 或直接是结果数据
      const stepResult = result?.step_result || result?.data || result;
      
      set(state => ({
        workflow: {
          ...state.workflow,
          currentStep: step,
          stepResults: { 
            ...state.workflow.stepResults, 
            [step]: {
              ...result,
              step_result: stepResult,
            }
          },
          isLoading: false,
        }
      }));
      
      // 如果是主线步骤，更新主线数据
      if (step === 3 && result.mainlines) {
        set({ mainlines: result.mainlines });
      }
      
      // 如果是候选池步骤，更新候选池数据
      if (step === 4 && result.stocks) {
        set({ candidatePool: result.stocks });
      }
    } catch (error) {
      set(state => ({
        workflow: {
          ...state.workflow,
          isLoading: false,
          error: (error as Error).message,
        }
      }));
    }
  },
  
  updateWorkflowStepResult: (step, resultData) => {
    set(state => {
      // 处理结果数据：可能是 { step_result } 或直接是结果
      const stepResult = resultData.result?.step_result || resultData.result?.data || resultData.result;
      
      return {
        workflow: {
          ...state.workflow,
          currentStep: step,
          stepResults: {
            ...state.workflow.stepResults,
            [step]: {
              success: resultData.success,
              step_result: stepResult,
              error: resultData.error,
              details: resultData.details,
            }
          },
          isLoading: false,
          error: resultData.success ? null : (resultData.error || '步骤执行失败'),
        }
      };
    });
  },
  
  setWorkflowLoading: (loading, step) => {
    set(state => ({
      workflow: {
        ...state.workflow,
        isLoading: loading,
        currentStep: step || state.workflow.currentStep,
      }
    }));
  },
  
  setMainlines: (mainlines) => set({ mainlines }),
  setCandidatePool: (stocks) => set({ candidatePool: stocks }),
  
  // 十倍股操作
  evaluateStock: async (code: string) => {
    const { callMCP } = get();
    set(state => ({
      tenbagger: { ...state.tenbagger, evaluating: true }
    }));
    
    try {
      // 使用正确的参数名：symbol 而不是 security_id
      const result = await callMCP<any>('tenbagger.evaluate', { symbol: code });
      set(state => ({
        tenbagger: {
          ...state.tenbagger,
          evaluating: false,
          selectedStock: result?.report || result,
        }
      }));
    } catch (error) {
      console.error('评估股票失败:', error);
      set(state => ({
        tenbagger: { 
          ...state.tenbagger, 
          evaluating: false 
        }
      }));
      // 显示错误提示
      throw error;
    }
  },
  
  getRankings: async () => {
    const { callMCP } = get();
    set(state => ({
      tenbagger: { ...state.tenbagger, evaluating: true }
    }));
    
    try {
      const result = await callMCP<{ rankings: Stock[] }>('tenbagger.rank', { top_n: 20 });
      set(state => ({
        tenbagger: { 
          ...state.tenbagger, 
          rankings: result.rankings || result || [],
          evaluating: false
        }
      }));
    } catch (error) {
      console.error('获取排名失败:', error);
      set(state => ({
        tenbagger: { ...state.tenbagger, evaluating: false }
      }));
      throw error;
    }
  },

  getPipelineStatus: async () => {
    const { callMCP } = get();
    try {
      const result = await callMCP<{ counts: { raw_docs: number; events: number; stages: number; candidates: number } }>('tenbagger_v2.pipeline_status', {});
      if (result && result.counts) {
        set({ pipelineStatus: result.counts });
      }
    } catch (error) {
      console.error('获取数据管道状态失败:', error);
    }
  },
  
  // 策略操作
  getStrategyTemplates: async () => {
    const { callMCP } = get();
    try {
      const result = await callMCP<{ templates: any[] }>('strategy.list_templates', {});
      set(state => ({
        strategy: { ...state.strategy, templates: result.templates || [] }
      }));
    } catch (error) {
      console.error('获取策略模板失败:', error);
    }
  },
  
  scanTrend: async () => {
    const { callMCP } = get();
    try {
      const result = await callMCP<any>('market.trend', {});
      return result;
    } catch (error) {
      console.error('趋势扫描失败:', error);
    }
  },
}));
