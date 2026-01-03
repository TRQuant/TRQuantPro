/**
 * 错误边界组件
 * 
 * 用于捕获React组件树中的错误，提供友好的错误提示
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Alert, Button, Card, Typography, Space } from 'antd';
import { ReloadOutlined, BugOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[ErrorBoundary] 捕获到错误:', error, errorInfo);
    
    this.setState({
      error,
      errorInfo,
    });

    // 调用错误处理回调
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // 可以在这里发送错误报告到服务器
    // this.reportError(error, errorInfo);
  }

  handleReload = () => {
    window.location.reload();
  };

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render() {
    if (this.state.hasError) {
      // 如果提供了自定义fallback，使用它
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // 默认错误UI
      return (
        <div style={{ padding: '24px', maxWidth: '800px', margin: '0 auto' }}>
          <Card>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Alert
                message="应用出现错误"
                description="很抱歉，应用遇到了一个错误。请尝试重新加载或联系技术支持。"
                type="error"
                icon={<BugOutlined />}
                showIcon
              />

              <div>
                <Title level={4}>错误信息</Title>
                <Text code style={{ display: 'block', marginBottom: '16px' }}>
                  {this.state.error?.message || '未知错误'}
                </Text>

                {this.state.errorInfo && (
                  <details style={{ marginTop: '16px' }}>
                    <summary style={{ cursor: 'pointer', marginBottom: '8px' }}>
                      <Text strong>查看详细堆栈信息</Text>
                    </summary>
                    <pre
                      style={{
                        background: '#f5f5f5',
                        padding: '12px',
                        borderRadius: '4px',
                        overflow: 'auto',
                        maxHeight: '300px',
                        fontSize: '12px',
                      }}
                    >
                      {this.state.errorInfo.componentStack}
                    </pre>
                  </details>
                )}
              </div>

              <Space>
                <Button
                  type="primary"
                  icon={<ReloadOutlined />}
                  onClick={this.handleReload}
                >
                  重新加载页面
                </Button>
                <Button onClick={this.handleReset}>
                  尝试恢复
                </Button>
              </Space>

              <Paragraph type="secondary" style={{ fontSize: '12px', marginTop: '16px' }}>
                如果问题持续存在，请检查浏览器控制台获取更多信息，或联系技术支持。
              </Paragraph>
            </Space>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}

/**
 * 函数式错误边界（使用React 18+的useErrorBoundary Hook）
 */
export function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  fallback?: ReactNode
) {
  return function WithErrorBoundaryComponent(props: P) {
    return (
      <ErrorBoundary fallback={fallback}>
        <Component {...props} />
      </ErrorBoundary>
    );
  };
}

export default ErrorBoundary;













































