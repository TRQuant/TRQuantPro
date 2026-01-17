/**
 * 通知中心组件
 * 
 * 统一的通知管理
 */

import React, { useState } from 'react';
import { Badge, Popover, List, Button, Space, Typography } from 'antd';
import { BellOutlined, CheckCircleOutlined, CloseCircleOutlined, InfoCircleOutlined, WarningOutlined } from '@ant-design/icons';

const { Text } = Typography;

export type NotificationType = 'success' | 'error' | 'info' | 'warning';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message: string;
  timestamp: number;
  read: boolean;
}

interface NotificationCenterProps {
  notifications: Notification[];
  onMarkAsRead?: (id: string) => void;
  onMarkAllAsRead?: () => void;
  onClear?: () => void;
}

const NotificationCenter: React.FC<NotificationCenterProps> = ({
  notifications,
  onMarkAsRead,
  onMarkAllAsRead,
  onClear,
}) => {
  const [visible, setVisible] = useState(false);
  const unreadCount = notifications.filter(n => !n.read).length;

  const getIcon = (type: NotificationType) => {
    switch (type) {
      case 'success':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'error':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
      case 'warning':
        return <WarningOutlined style={{ color: '#faad14' }} />;
      default:
        return <InfoCircleOutlined style={{ color: '#1890ff' }} />;
    }
  };

  const content = (
    <div style={{ width: 360, maxHeight: 400, overflowY: 'auto' }}>
      <div style={{ padding: '8px 0', borderBottom: '1px solid #f0f0f0', marginBottom: 8 }}>
        <Space style={{ width: '100%', justifyContent: 'space-between' }}>
          <Text strong>通知中心</Text>
          <Space>
            {unreadCount > 0 && (
              <Button type="link" size="small" onClick={onMarkAllAsRead}>
                全部已读
              </Button>
            )}
            <Button type="link" size="small" onClick={onClear}>
              清空
            </Button>
          </Space>
        </Space>
      </div>
      {notifications.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
          暂无通知
        </div>
      ) : (
        <List
          dataSource={notifications}
          renderItem={(item: Notification) => (
            <List.Item
              style={{
                padding: '8px 0',
                backgroundColor: item.read ? 'transparent' : '#f0f7ff',
                cursor: 'pointer',
              }}
              onClick={() => {
                if (!item.read && onMarkAsRead) {
                  onMarkAsRead(item.id);
                }
              }}
            >
              <List.Item.Meta
                avatar={getIcon(item.type)}
                title={
                  <Space>
                    <Text strong={!item.read}>{item.title}</Text>
                    {!item.read && <Badge status="processing" />}
                  </Space>
                }
                description={
                  <div>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {item.message}
                    </Text>
                    <div style={{ marginTop: 4 }}>
                      <Text type="secondary" style={{ fontSize: 11 }}>
                        {new Date(item.timestamp).toLocaleString('zh-CN')}
                      </Text>
                    </div>
                  </div>
                }
              />
            </List.Item>
          )}
        />
      )}
    </div>
  );

  return (
    <Popover
      content={content}
      title={null}
      trigger="click"
      open={visible}
      onOpenChange={setVisible}
      placement="bottomRight"
    >
      <Badge count={unreadCount} size="small">
        <Button
          type="text"
          icon={<BellOutlined />}
          style={{ fontSize: 18 }}
        />
      </Badge>
    </Popover>
  );
};

export default NotificationCenter;

