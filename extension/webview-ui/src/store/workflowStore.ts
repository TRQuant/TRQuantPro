/**
 * 工作流状态管理
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type StepStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface WorkflowStep {
  id: number;
  stepId: string;
  name: string;
  icon: string;
  status: StepStatus;
  result?: any;
  error?: string;
  startedAt?: string;
  completedAt?: string;
  duration?: number;
}

export interface WorkflowState {
  workflowId: string | null;
  steps: WorkflowStep[];
  context: Record<string, any>;
  isRunning: boolean;
  currentStep: number;
  error: string | null;
}

interface WorkflowActions {
  createWorkflow: () => Promise<void>;
  runStep: (step: number) => Promise<void>;
  updateStepStatus: (step: number, status: StepStatus, result?: any, error?: string) => void;
  getStepStatus: (step: number) => StepStatus;
  resetWorkflow: () => void;
  updateContext: (key: string, value: any) => void;
  getWorkflowStatus: () => Promise<void>;
}

const STEP_ID_MAP: Record<number, string> = {
  1: 'data_source',
  2: 'market_trend',
  3: 'mainline',
  4: 'candidate_pool',
  5: 'factor',
  6: 'strategy',
  7: 'backtest',
  8: 'optimization',
  9: 'report',
};

const WORKFLOW_STEPS: Omit<WorkflowStep, 'status' | 'result' | 'error' | 'startedAt' | 'completedAt' | 'duration'>[] = [
  { id: 1, stepId: 'data_source', name: '数据源检查', icon: '📡' },
  { id: 2, stepId: 'market_trend', name: '市场趋势分析', icon: '📈' },
  { id: 3, stepId: 'mainline', name: '投资主线识别', icon: '🔥' },
  { id: 4, stepId: 'candidate_pool', name: '候选池构建', icon: '📦' },
  { id: 5, stepId: 'factor', name: '因子构建', icon: '📊' },
  { id: 6, stepId: 'strategy', name: '策略生成', icon: '⚙️' },
  { id: 7, stepId: 'backtest', name: '回测验证', icon: '🧪' },
  { id: 8, stepId: 'optimization', name: '参数优化', icon: '🎛️' },
  { id: 9, stepId: 'report', name: '报告生成', icon: '📄' },
];

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

export const useWorkflowStore = create<WorkflowState & WorkflowActions>()(
  persist(
    (set, get) => ({
      workflowId: null,
      steps: WORKFLOW_STEPS.map(step => ({
        ...step,
        status: 'pending' as StepStatus,
      })),
      context: {},
      isRunning: false,
      currentStep: 0,
      error: null,
      createWorkflow: async () => {
        set({ isRunning: true, error: null });
        try {
          const result = await callMCP<{ workflow_id: string }>('workflow9.create', {});
          set({ workflowId: result.workflow_id, isRunning: false });
        } catch (error) {
          set({ isRunning: false, error: (error as Error).message });
        }
      },
      runStep: async (step: number) => {
        const { workflowId, createWorkflow, updateStepStatus } = get();
        let currentWorkflowId = workflowId;
        if (!currentWorkflowId) {
          await createWorkflow();
          currentWorkflowId = get().workflowId;
          if (!currentWorkflowId) {
            throw new Error('创建工作流失败');
          }
        }
        updateStepStatus(step, 'running');
        set({ isRunning: true, currentStep: step, error: null });
                try {
          const stepId = STEP_ID_MAP[step];
          if (!stepId) {
            throw new Error(`无效的步骤编号: ${step}`);
          }
          const result = await callMCP<any>('workflow9.run_step', {
            workflow_id: currentWorkflowId,
            step_id: stepId,
          });
          updateStepStatus(step, 'completed', result);
          set({
            isRunning: false,
            currentStep: step,
            context: { ...get().context, [step]: result },
          });
          if (step === 3 && result.mainlines) {
            set({ context: { ...get().context, mainlines: result.mainlines } });
          }
          if (step === 4 && result.stocks) {
            set({ context: { ...get().context, candidatePool: result.stocks } });
          }
        } catch (error) {
          updateStepStatus(step, 'failed', undefined, (error as Error).message);
          set({ isRunning: false, error: (error as Error).message });
        }
      },
      updateStepStatus: (step: number, status: StepStatus, result?: any, error?: string) => {
        set((state) => ({
          steps: state.steps.map((s) => {
            if (s.id === step) {
              const updated: WorkflowStep = { ...s, status, result, error };
              if (status === 'running' && !s.startedAt) {
                updated.startedAt = new Date().toISOString();
              }
              if (status === 'completed' || status === 'failed') {
                updated.completedAt = new Date().toISOString();
                if (s.startedAt) {
                  updated.duration = new Date(updated.completedAt).getTime() - new Date(s.startedAt).getTime();
                }
              }
              return updated;
            }
            return s;
          }),
        }));
      },
      getStepStatus: (step: number) => {
        const stepData = get().steps.find((s) => s.id === step);
        return stepData?.status || 'pending';
      },
      resetWorkflow: () => {
        set({
          workflowId: null,
          steps: WORKFLOW_STEPS.map(step => ({
            ...step,
            status: 'pending' as StepStatus,
          })),
          context: {},
          isRunning: false,
          currentStep: 0,
          error: null,
        });
      },
      updateContext: (key: string, value: any) => {
        set((state) => ({
          context: { ...state.context, [key]: value },
        }));
      },
      getWorkflowStatus: async () => {
        const { workflowId } = get();
        if (!workflowId) return;
        try {
          const result = await callMCP<any>('workflow9.status', { workflow_id: workflowId });
          if (result.steps) {
            set((state) => ({
              steps: state.steps.map((s) => {
                const serverStep = result.steps.find((ss: any) => ss.step_id === s.stepId);
                if (serverStep) {
                  return {
                    ...s,
                    status: serverStep.status || s.status,
                    result: serverStep.result || s.result,
                    error: serverStep.error || s.error,
                  };
                }
                return s;
              }),
            }));
          }
        } catch (error) {
          console.error('获取工作流状态失败:', error);
        }
      },
    }),
    {
      name: 'trquant-workflow-store',
      partialize: (state) => ({
        workflowId: state.workflowId,
        steps: state.steps,
        context: state.context,
        currentStep: state.currentStep,
      }),
    }
  )
);
