/**
 * 刷新按钮组件
 * 
 * 带加载状态的刷新按钮
 */

import React from 'react';
import { Button } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';

interface RefreshButtonProps {
  onClick: () => void | Promise<void>;
  loading?: boolean;
  disabled?: boolean;
  size?: 'small' | 'middle' | 'large';
}

const RefreshButton: React.FC<RefreshButtonProps> = ({
  onClick,
  loading = false,
  disabled = false,
  size = 'middle',
}) => {
  return (
    <Button
      icon={<ReloadOutlined />}
      loading={loading}
      disabled={disabled}
      onClick={onClick}
      size={size}
    >
      刷新
    </Button>
  );
};

export default RefreshButton;













































