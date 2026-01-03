/**
 * 状态徽章组件
 * 
 * 统一的状态展示组件
 */

import React from 'react';
import { Tag } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined, LoadingOutlined, ClockCircleOutlined } from '@ant-design/icons';

export type StatusType = 'success' | 'error' | 'loading' | 'warning' | 'default';

interface StatusBadgeProps {
  status: StatusType;
  text?: string;
  icon?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  text,
  icon = true,
}) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'success':
        return {
          color: 'success',
          icon: <CheckCircleOutlined />,
          text: text || '成功',
        };
      case 'error':
        return {
          color: 'error',
          icon: <CloseCircleOutlined />,
          text: text || '失败',
        };
      case 'loading':
        return {
          color: 'processing',
          icon: <LoadingOutlined />,
          text: text || '处理中',
        };
      case 'warning':
        return {
          color: 'warning',
          icon: <ClockCircleOutlined />,
          text: text || '警告',
        };
      default:
        return {
          color: 'default',
          icon: <ClockCircleOutlined />,
          text: text || '待处理',
        };
    }
  };

  const config = getStatusConfig();

  return (
    <Tag color={config.color} icon={icon ? config.icon : undefined}>
      {config.text}
    </Tag>
  );
};

export default StatusBadge;

