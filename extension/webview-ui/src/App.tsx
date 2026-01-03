import React, { useEffect, useRef } from 'react';
import { Tabs, Layout, Typography, Alert, Badge } from 'antd';
import { 
  DashboardOutlined, 
  RocketOutlined, 
  LineChartOutlined,
  SettingOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  LoadingOutlined
} from '@ant-design/icons';
import ShortcutHelp from './components/ShortcutHelp';
import NotificationCenter from './components/NotificationCenter';
import { useNotifications } from './hooks/useNotifications';
// 使用懒加载优化性能
import { lazy, Suspense } from 'react';
import LoadingIndicatorComponent from './components/LoadingIndicator';

const WorkflowPage = lazy(() => import('@pages/Workflow'));
const TenbaggerPage = lazy(() => import('@pages/Tenbagger'));
const StrategyPage = lazy(() => import('@pages/Strategy'));
import { useAppStore } from '@store/index';
import { getVSCodeAPI } from './utils/vscodeApi';
import ErrorBoundary from './components/ErrorBoundary';
import { initConnectionStatusListener, useEnhancedStore } from './store/enhancedStore';
import { ConnectionStatus } from './services/webviewMCPClientEnhanced';

const { Header, Content } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const { activeTab, setActiveTab, updateWorkflowStepResult, setWorkflowLoading } = useAppStore();
  const { connectionStatus, error, loading, clearError } = useEnhancedStore();
  const { notifications, addNotification, markAsRead, markAllAsRead, clear: clearNotifications } = useNotifications();
  
  // 初始化连接状态监听
  useEffect(() => {
    initConnectionStatusListener();
  }, []);

  // 监听错误并添加通知
  useEffect(() => {
    if (error) {
      addNotification('error', '错误', error.message);
    }
  }, [error, addNotification]);

  // 监听连接状态变化并添加通知
  useEffect(() => {
    if (connectionStatus === ConnectionStatus.CONNECTED) {
      addNotification('success', '连接成功', '已连接到MCP服务器');
    } else if (connectionStatus === ConnectionStatus.DISCONNECTED) {
      addNotification('warning', '连接断开', '请检查扩展是否正常运行');
    }
  }, [connectionStatus, addNotification]);
  
  // 使用ref来保持监听器引用，确保正确清理
  const messageHandlerRef = useRef<((event: MessageEvent) => void) | null>(null);
  
  // 监听来自统一仪表板的消息（只注册一次）
  useEffect(() => {
    const vscode = getVSCodeAPI();
    if (!vscode) {
      console.warn('[App] VS Code API not available');
      return;
    }
    
    // 如果已经有监听器，先清理
    if (messageHandlerRef.current) {
      window.removeEventListener('message', messageHandlerRef.current);
      messageHandlerRef.current = null;
    }
    
    const handleMessage = (event: MessageEvent) => {
      const message = event.data;
      
      // 只处理来自VS Code的消息
      if (!message || typeof message !== 'object' || !message.command) return;
      
      // 处理工作流步骤结果
      if (message.command === 'workflow.stepResult') {
        const { step, result, success, error, details } = message;
        updateWorkflowStepResult(step, {
          success,
          result,
          error,
          details,
        });
      }
      
      // 处理工作流加载状态
      if (message.command === 'workflow.loading') {
        setWorkflowLoading(message.loading, message.step);
      }
    };
    
    // 保存引用以便清理
    messageHandlerRef.current = handleMessage;
    
    // 注册监听器
    window.addEventListener('message', handleMessage);
    console.log('[App] 消息监听器已注册');
    
    // 清理函数
    return () => {
      if (messageHandlerRef.current) {
        window.removeEventListener('message', messageHandlerRef.current);
        messageHandlerRef.current = null;
        console.log('[App] 消息监听器已清理');
      }
    };
    // 空依赖数组，只在组件挂载时注册一次
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const tabItems = [
    {
      key: 'workflow',
      label: (
        <span>
          <DashboardOutlined />
          9步工作流
        </span>
      ),
      children: (
        <Suspense fallback={<LoadingIndicatorComponent loading={true} message="加载工作流页面..." />}>
          <WorkflowPage />
        </Suspense>
      ),
    },
    {
      key: 'tenbagger',
      label: (
        <span>
          <RocketOutlined />
          十倍股识别
        </span>
      ),
      children: (
        <Suspense fallback={<LoadingIndicatorComponent loading={true} message="加载十倍股页面..." />}>
          <TenbaggerPage />
        </Suspense>
      ),
    },
    {
      key: 'strategy',
      label: (
        <span>
          <LineChartOutlined />
          趋势策略
        </span>
      ),
      children: (
        <Suspense fallback={<LoadingIndicatorComponent loading={true} message="加载策略页面..." />}>
          <StrategyPage />
        </Suspense>
      ),
    },
  ];

  // 连接状态图标
  const getConnectionIcon = () => {
    switch (connectionStatus) {
      case ConnectionStatus.CONNECTED:
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case ConnectionStatus.CONNECTING:
        return <LoadingOutlined style={{ color: '#1890ff' }} />;
      case ConnectionStatus.DISCONNECTED:
      case ConnectionStatus.ERROR:
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
      default:
        return null;
    }
  };

  const getConnectionText = () => {
    switch (connectionStatus) {
      case ConnectionStatus.CONNECTED:
        return '已连接';
      case ConnectionStatus.CONNECTING:
        return '连接中';
      case ConnectionStatus.DISCONNECTED:
        return '未连接';
      case ConnectionStatus.ERROR:
        return '连接错误';
      default:
        return '未知';
    }
  };

  return (
    <ErrorBoundary>
      <Layout style={{ minHeight: '100vh', background: 'var(--vscode-editor-background)' }}>
        <Header style={{ 
          background: 'var(--vscode-sideBar-background)', 
          padding: '0 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <Title level={4} style={{ margin: 0, color: 'var(--vscode-foreground)' }}>
            🐉 TRQuant 统一仪表盘
          </Title>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <Badge 
              status={connectionStatus === ConnectionStatus.CONNECTED ? 'success' : 'error'}
              text={
                <span style={{ color: 'var(--vscode-foreground)', fontSize: '12px' }}>
                  {getConnectionIcon()} {getConnectionText()}
                </span>
              }
            />
            <ShortcutHelp />
            <NotificationCenter
              notifications={notifications}
              onMarkAsRead={markAsRead}
              onMarkAllAsRead={markAllAsRead}
              onClear={clearNotifications}
            />
            <SettingOutlined style={{ fontSize: 18, color: 'var(--vscode-foreground)', cursor: 'pointer' }} />
          </div>
        </Header>
        <Content style={{ padding: '16px' }}>
          {/* 错误提示 */}
          {error && (
            <Alert
              message={error.message}
              description={error.details}
              type={error.type}
              closable
              onClose={clearError}
              style={{ marginBottom: '16px' }}
              action={
                error.retryable && (
                  <span 
                    style={{ cursor: 'pointer', color: '#1890ff' }}
                    onClick={() => {
                      clearError();
                      window.location.reload();
                    }}
                  >
                    重试
                  </span>
                )
              }
            />
          )}
          
          {/* 加载指示器 */}
          {loading.isLoading && (
            <LoadingIndicatorComponent
              loading={loading.isLoading}
              message={loading.loadingMessage}
              progress={loading.progress}
            />
          )}
          
          {/* 主要内容 */}
          {!loading.isLoading && (
            <Tabs
              activeKey={activeTab}
              onChange={setActiveTab}
              items={tabItems}
              type="card"
              size="large"
            />
          )}
        </Content>
      </Layout>
    </ErrorBoundary>
  );
};

export default App;
