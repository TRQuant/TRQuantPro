/**
 * 加载指示器组件
 * 
 * 提供统一的加载状态展示
 */

import React from 'react';
import { Progress, Space, Typography, Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

const { Text } = Typography;

interface LoadingIndicatorProps {
  loading: boolean;
  message?: string;
  progress?: number;
  size?: 'small' | 'default' | 'large';
  fullScreen?: boolean;
  tip?: string;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({
  loading,
  message,
  progress,
  size = 'default',
  fullScreen = false,
  tip,
}) => {
  if (!loading) {
    return null;
  }

  const antIcon = <LoadingOutlined style={{ fontSize: size === 'large' ? 48 : 24 }} spin />;

  const content = (
    <Space direction="vertical" size="middle" align="center">
      <Spin indicator={antIcon} size={size} tip={tip || message || '加载中...'} />
      {message && (
        <Text type="secondary">{message}</Text>
      )}
      {progress !== undefined && (
        <Progress
          percent={progress}
          status="active"
          style={{ width: 200 }}
          showInfo
        />
      )}
    </Space>
  );

  if (fullScreen) {
    return (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'rgba(255, 255, 255, 0.8)',
          zIndex: 9999,
        }}
      >
        {content}
      </div>
    );
  }

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px',
        minHeight: '200px',
      }}
    >
      {content}
    </div>
  );
};

/**
 * 内联加载指示器（用于按钮、表格等）
 */
export const InlineLoading: React.FC<{ loading: boolean; children: React.ReactNode }> = ({
  loading,
  children,
}) => {
  if (loading) {
    return <Spin size="small" />;
  }
  return <>{children}</>;
};

/**
 * 骨架屏加载（用于内容区域）
 */
export const SkeletonLoading: React.FC<{ loading: boolean; children: React.ReactNode }> = ({
  loading,
  children,
}) => {
  if (loading) {
    return (
      <div style={{ padding: '16px' }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div style={{ height: '20px', background: '#f0f0f0', borderRadius: '4px' }} />
          <div style={{ height: '20px', background: '#f0f0f0', borderRadius: '4px', width: '80%' }} />
          <div style={{ height: '20px', background: '#f0f0f0', borderRadius: '4px', width: '60%' }} />
        </Space>
      </div>
    );
  }
  return <>{children}</>;
};

export default LoadingIndicator;

