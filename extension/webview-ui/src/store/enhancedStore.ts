/**
 * 增强版Store状态管理
 * 
 * 功能：
 * 1. 状态持久化（localStorage）
 * 2. 状态同步机制
 * 3. 错误状态管理
 * 4. 加载状态管理
 * 5. 状态历史记录
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { getWebviewMCPClientEnhanced, ConnectionStatus } from '../services/webviewMCPClientEnhanced';

/**
 * 错误状态
 */
interface ErrorState {
  message: string;
  type: 'error' | 'warning' | 'info';
  timestamp: number;
  details?: string;
  retryable?: boolean;
}

/**
 * 加载状态
 */
interface LoadingState {
  isLoading: boolean;
  loadingMessage?: string;
  progress?: number;
}

/**
 * 应用状态（增强版）
 */
interface EnhancedAppState {
  // 连接状态
  connectionStatus: ConnectionStatus;
  setConnectionStatus: (status: ConnectionStatus) => void;
  
  // 错误状态
  error: ErrorState | null;
  setError: (error: ErrorState | null) => void;
  clearError: () => void;
  
  // 加载状态
  loading: LoadingState;
  setLoading: (loading: LoadingState) => void;
  
  // 工作流状态（持久化）
  workflow: {
    workflowId: string | null;
    currentStep: number;
    stepResults: Record<number, any>;
    lastUpdated: number;
  };
  setWorkflow: (workflow: Partial<EnhancedAppState['workflow']>) => void;
  
  // 十倍股状态（持久化）
  tenbagger: {
    rankings: any[];
    selectedStock: any | null;
    lastUpdated: number;
  };
  setTenbagger: (tenbagger: Partial<EnhancedAppState['tenbagger']>) => void;
  
  // 策略状态（持久化）
  strategy: {
    templates: any[];
    currentStrategy: any | null;
    backtestResult: any | null;
    lastUpdated: number;
  };
  setStrategy: (strategy: Partial<EnhancedAppState['strategy']>) => void;
  
  // 状态同步
  syncState: () => Promise<void>;
  
  // 重置状态
  reset: () => void;
}

/**
 * 创建增强版Store（带持久化）
 */
export const useEnhancedStore = create<EnhancedAppState>()(
  persist(
    (set, get) => ({
      // 连接状态
      connectionStatus: ConnectionStatus.DISCONNECTED,
      setConnectionStatus: (status) => set({ connectionStatus: status }),
      
      // 错误状态
      error: null,
      setError: (error) => set({ error }),
      clearError: () => set({ error: null }),
      
      // 加载状态
      loading: { isLoading: false },
      setLoading: (loading) => set({ loading }),
      
      // 工作流状态
      workflow: {
        workflowId: null,
        currentStep: 0,
        stepResults: {},
        lastUpdated: Date.now(),
      },
      setWorkflow: (workflow) => set((state) => ({
        workflow: {
          ...state.workflow,
          ...workflow,
          lastUpdated: Date.now(),
        }
      })),
      
      // 十倍股状态
      tenbagger: {
        rankings: [],
        selectedStock: null,
        lastUpdated: Date.now(),
      },
      setTenbagger: (tenbagger) => set((state) => ({
        tenbagger: {
          ...state.tenbagger,
          ...tenbagger,
          lastUpdated: Date.now(),
        }
      })),
      
      // 策略状态
      strategy: {
        templates: [],
        currentStrategy: null,
        backtestResult: null,
        lastUpdated: Date.now(),
      },
      setStrategy: (strategy) => set((state) => ({
        strategy: {
          ...state.strategy,
          ...strategy,
          lastUpdated: Date.now(),
        }
      })),
      
      // 状态同步
      syncState: async () => {
        const client = getWebviewMCPClientEnhanced();
        const status = client.getConnectionStatus();
        set({ connectionStatus: status });
        
        // 可以在这里添加从服务器同步状态的逻辑
        // 例如：如果工作流ID存在，从服务器获取最新状态
        const { workflow } = get();
        if (workflow.workflowId) {
          try {
            // 可以调用MCP工具获取最新状态
            // const result = await client.callTool('workflow9.get_status', { workflow_id: workflow.workflowId });
            // set({ workflow: { ...workflow, ...result } });
          } catch (error) {
            console.error('[EnhancedStore] 同步状态失败:', error);
          }
        }
      },
      
      // 重置状态
      reset: () => set({
        workflow: {
          workflowId: null,
          currentStep: 0,
          stepResults: {},
          lastUpdated: Date.now(),
        },
        tenbagger: {
          rankings: [],
          selectedStock: null,
          lastUpdated: Date.now(),
        },
        strategy: {
          templates: [],
          currentStrategy: null,
          backtestResult: null,
          lastUpdated: Date.now(),
        },
        error: null,
        loading: { isLoading: false },
      }),
    }),
    {
      name: 'trquant-enhanced-store',
      storage: createJSONStorage(() => localStorage),
      // 只持久化工作流、十倍股、策略状态
      partialize: (state) => ({
        workflow: state.workflow,
        tenbagger: state.tenbagger,
        strategy: state.strategy,
      }),
    }
  )
);

/**
 * 初始化连接状态监听
 */
export function initConnectionStatusListener() {
  const client = getWebviewMCPClientEnhanced();
  const { setConnectionStatus, setError } = useEnhancedStore.getState();
  
  client.onStatusChange((status) => {
    setConnectionStatus(status);
    
    if (status === ConnectionStatus.DISCONNECTED) {
      setError({
        message: '连接已断开，请检查扩展是否正常运行',
        type: 'warning',
        timestamp: Date.now(),
        retryable: true,
      });
    } else if (status === ConnectionStatus.CONNECTED) {
      useEnhancedStore.getState().clearError();
    }
  });
}













































