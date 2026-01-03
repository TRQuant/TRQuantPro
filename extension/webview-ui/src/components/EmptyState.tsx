/**
 * 空状态组件
 * 
 * 统一的无数据展示
 */

import React from 'react';
import { Empty, Button } from 'antd';
import { InboxOutlined } from '@ant-design/icons';

interface EmptyStateProps {
  description?: string;
  action?: {
    text: string;
    onClick: () => void;
  };
  image?: React.ReactNode;
}

const EmptyState: React.FC<EmptyStateProps> = ({
  description = '暂无数据',
  action,
  image,
}) => {
  return (
    <Empty
      image={image || <InboxOutlined style={{ fontSize: 64, color: '#d9d9d9' }} />}
      description={description}
    >
      {action && (
        <Button type="primary" onClick={action.onClick}>
          {action.text}
        </Button>
      )}
    </Empty>
  );
};

export default EmptyState;













































