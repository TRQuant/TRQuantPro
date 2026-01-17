/**
 * 工作流步骤卡片组件
 * 
 * 提供更丰富的步骤展示和交互
 */

import React from 'react';
import { Card, Tag, Space, Button, Tooltip, Progress, Typography } from 'antd';
import { 
  CheckCircleOutlined, 
  CloseCircleOutlined, 
  LoadingOutlined, 
  PlayCircleOutlined,
  InfoCircleOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';

const { Text } = Typography;

interface WorkflowStepCardProps {
  step: {
    title: string;
    description: string;
    stepId: string;
  };
  stepNumber: number;
  status: 'wait' | 'process' | 'finish' | 'error';
  result?: any;
  isLoading?: boolean;
  onRun?: () => void;
  onViewDetails?: () => void;
}

const WorkflowStepCard: React.FC<WorkflowStepCardProps> = ({
  step,
  stepNumber,
  status,
  result,
  isLoading = false,
  onRun,
  onViewDetails,
}) => {
  const getStatusIcon = () => {
    if (isLoading) {
      return <LoadingOutlined style={{ color: '#1890ff' }} />;
    }
    switch (status) {
      case 'finish':
        return <CheckCircleOutlined style={{ color: '#52c41a' }} />;
      case 'error':
        return <CloseCircleOutlined style={{ color: '#ff4d4f' }} />;
      case 'process':
        return <LoadingOutlined style={{ color: '#1890ff' }} />;
      default:
        return <ClockCircleOutlined style={{ color: '#d9d9d9' }} />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'finish':
        return 'success';
      case 'error':
        return 'error';
      case 'process':
        return 'processing';
      default:
        return 'default';
    }
  };

  const getStatusText = () => {
    if (isLoading) return '执行中...';
    switch (status) {
      case 'finish':
        return '已完成';
      case 'error':
        return '执行失败';
      case 'process':
        return '处理中';
      default:
        return '待执行';
    }
  };

  const stepResult = result?.step_result || result?.data || result;
  const hasResult = !!result;

  return (
    <Card
      size="small"
      style={{
        marginBottom: 12,
        borderLeft: status === 'finish' ? '3px solid #52c41a' :
                    status === 'error' ? '3px solid #ff4d4f' :
                    status === 'process' ? '3px solid #1890ff' : '3px solid #d9d9d9',
      }}
      title={
        <Space>
          <span style={{ fontWeight: 'bold' }}>步骤 {stepNumber}: {step.title}</span>
          {getStatusIcon()}
          <Tag color={getStatusColor()}>{getStatusText()}</Tag>
          {stepResult?.summary && (
            <Tooltip title={stepResult.summary}>
              <InfoCircleOutlined style={{ color: '#1890ff' }} />
            </Tooltip>
          )}
        </Space>
      }
      extra={
        <Space>
          {hasResult && (
            <Button 
              type="link" 
              size="small"
              onClick={onViewDetails}
            >
              查看详情
            </Button>
          )}
          <Button
            type={status === 'finish' ? 'default' : 'primary'}
            size="small"
            icon={isLoading ? <LoadingOutlined /> : <PlayCircleOutlined />}
            loading={isLoading}
            onClick={onRun}
            disabled={isLoading}
          >
            {status === 'finish' ? '重新执行' : '执行'}
          </Button>
        </Space>
      }
    >
      <Space direction="vertical" size="small" style={{ width: '100%' }}>
        <Text type="secondary">{step.description}</Text>
        
        {/* 执行进度 */}
        {isLoading && (
          <Progress 
            percent={stepResult?.progress || 0} 
            status="active" 
            size="small"
          />
        )}

        {/* 执行结果摘要 */}
        {hasResult && !isLoading && (
          <div>
            {stepResult?.summary && (
              <Text>{stepResult.summary}</Text>
            )}
            {stepResult?.method && (
              <div style={{ marginTop: 8 }}>
                <Text type="secondary" style={{ fontSize: 12 }}>
                  执行方法: {stepResult.method}
                </Text>
              </div>
            )}
            {stepResult?.error && (
              <div style={{ marginTop: 8 }}>
                <Text type="danger" style={{ fontSize: 12 }}>
                  {stepResult.error}
                </Text>
              </div>
            )}
          </div>
        )}

        {/* 数据统计 */}
        {stepResult && typeof stepResult === 'object' && (
          <div style={{ marginTop: 8 }}>
            {stepResult.available_count !== undefined && (
              <Tag color="blue">
                可用: {stepResult.available_count}/{stepResult.total_count || 'N'}
              </Tag>
            )}
            {stepResult.count && (
              <Tag color="green">数量: {stepResult.count}</Tag>
            )}
            {stepResult.duration && (
              <Tag color="default">耗时: {stepResult.duration}ms</Tag>
            )}
          </div>
        )}
      </Space>
    </Card>
  );
};

export default WorkflowStepCard;

