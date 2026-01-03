/**
 * 十倍股详细评估模态框
 * 
 * 显示股票的详细评估信息
 */

import React from 'react';
import { Modal, Descriptions, Tag, Progress, Typography, Divider, Space, Card } from 'antd';
import { RocketOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

interface TenbaggerDetailModalProps {
  visible: boolean;
  stock: any | null;
  onClose: () => void;
}

const TenbaggerDetailModal: React.FC<TenbaggerDetailModalProps> = ({
  visible,
  stock,
  onClose,
}) => {
  if (!stock) return null;

  const report = stock.report || stock;
  const scorecard = report.scorecard || {};
  const stage = report.stage || 'S0';
  const level = report.level || 'C';

  // 阶段标签颜色
  const getStageColor = (stage: string) => {
    const stageMap: Record<string, string> = {
      'S0': 'blue',
      'S1': 'cyan',
      'S2': 'green',
      'S3': 'orange',
      'S4': 'red',
      'S5': 'purple',
    };
    return stageMap[stage] || 'default';
  };

  // 等级标签颜色
  const getLevelColor = (level: string) => {
    const levelMap: Record<string, string> = {
      'S+': 'gold',
      'S': 'orange',
      'A': 'green',
      'B': 'blue',
      'C': 'default',
      'D': 'red',
    };
    return levelMap[level] || 'default';
  };

  return (
    <Modal
      title={
        <Space>
          <RocketOutlined />
          <span>十倍股详细评估</span>
          {report.symbol && (
            <Tag color="blue">{report.symbol}</Tag>
          )}
          {report.name && (
            <Text strong>{report.name}</Text>
          )}
        </Space>
      }
      open={visible}
      onCancel={onClose}
      footer={null}
      width={800}
    >
      <div style={{ maxHeight: '70vh', overflowY: 'auto' }}>
        {/* 总体评估 */}
        <Card style={{ marginBottom: 16 }}>
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            <div>
              <Text strong>综合评分：</Text>
              <Progress
                percent={report.total_score || 0}
                status={report.total_score >= 80 ? 'success' : report.total_score >= 60 ? 'normal' : 'exception'}
                style={{ marginTop: 8 }}
              />
            </div>
            <Space>
              <div>
                <Text type="secondary">阶段：</Text>
                <Tag color={getStageColor(stage)} style={{ marginLeft: 8 }}>
                  {stage}
                </Tag>
              </div>
              <div>
                <Text type="secondary">等级：</Text>
                <Tag color={getLevelColor(level)} style={{ marginLeft: 8 }}>
                  {level}
                </Tag>
              </div>
            </Space>
            {report.summary && (
              <Paragraph>{report.summary}</Paragraph>
            )}
          </Space>
        </Card>

        {/* 7维评分卡 */}
        {Object.keys(scorecard).length > 0 && (
          <>
            <Title level={5}>7维评分卡</Title>
            <Descriptions bordered column={2} size="small" style={{ marginBottom: 16 }}>
              {Object.entries(scorecard).map(([key, value]: [string, any]) => (
                <Descriptions.Item key={key} label={key}>
                  <Progress
                    percent={value || 0}
                    size="small"
                    status={value >= 80 ? 'success' : value >= 60 ? 'normal' : 'exception'}
                  />
                </Descriptions.Item>
              ))}
            </Descriptions>
          </>
        )}

        {/* 财务数据 */}
        {report.financials && Object.keys(report.financials).length > 0 && (
          <>
            <Divider />
            <Title level={5}>财务数据</Title>
            <Descriptions bordered column={2} size="small" style={{ marginBottom: 16 }}>
              {Object.entries(report.financials).map(([key, value]: [string, any]) => (
                <Descriptions.Item key={key} label={key}>
                  {typeof value === 'number' ? value.toFixed(2) : String(value)}
                </Descriptions.Item>
              ))}
            </Descriptions>
          </>
        )}

        {/* 行业数据 */}
        {report.industry && Object.keys(report.industry).length > 0 && (
          <>
            <Divider />
            <Title level={5}>行业数据</Title>
            <Descriptions bordered column={2} size="small" style={{ marginBottom: 16 }}>
              {Object.entries(report.industry).map(([key, value]: [string, any]) => (
                <Descriptions.Item key={key} label={key}>
                  {typeof value === 'number' ? value.toFixed(2) : String(value)}
                </Descriptions.Item>
              ))}
            </Descriptions>
          </>
        )}

        {/* 技术指标 */}
        {report.technicals && Object.keys(report.technicals).length > 0 && (
          <>
            <Divider />
            <Title level={5}>技术指标</Title>
            <Descriptions bordered column={2} size="small" style={{ marginBottom: 16 }}>
              {Object.entries(report.technicals).map(([key, value]: [string, any]) => (
                <Descriptions.Item key={key} label={key}>
                  {typeof value === 'number' ? value.toFixed(2) : String(value)}
                </Descriptions.Item>
              ))}
            </Descriptions>
          </>
        )}

        {/* 评估建议 */}
        {report.recommendation && (
          <>
            <Divider />
            <Title level={5}>投资建议</Title>
            <Paragraph>{report.recommendation}</Paragraph>
          </>
        )}
      </div>
    </Modal>
  );
};

export default TenbaggerDetailModal;

