/**
 * 数据源状态展示组件
 * 用于显示数据源检查的详细结果
 */
import React from 'react';
import { Card, Table, Tag, Space, Typography, Statistic, Row, Col } from 'antd';
import { CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';

const { Text } = Typography;

export interface DataSourceStatus {
  available: boolean;
  latency_ms?: number;
  last_check?: string;
  error_count?: number;
  success_rate?: number;
  error?: string;
  message?: string;
}

export interface DataSourceHealthStatus {
  [key: string]: DataSourceStatus;
}

export interface DataSourceStatusProps {
  healthStatus?: DataSourceHealthStatus;
  summary?: string;
  method?: string;
  availableCount?: number;
  totalCount?: number;
}

const DataSourceStatusComponent: React.FC<DataSourceStatusProps> = ({
  healthStatus = {},
  summary,
  method,
  availableCount,
  totalCount,
}) => {
  const dataSourceNames: Record<string, string> = {
    jqdata: '聚宽数据',
    akshare: 'AKShare',
    tushare: 'Tushare',
  };

  const columns = [
    {
      title: '数据源',
      dataIndex: 'name',
      key: 'name',
      render: (text: string) => <Text strong>{text}</Text>,
    },
    {
      title: '状态',
      dataIndex: 'available',
      key: 'available',
      render: (available: boolean) => (
        <Tag
          icon={available ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
          color={available ? 'success' : 'error'}
        >
          {available ? '可用' : '不可用'}
        </Tag>
      ),
    },
    {
      title: '延迟',
      dataIndex: 'latency_ms',
      key: 'latency_ms',
      render: (latency: number | undefined) => {
        if (latency === undefined || latency === null) return <Text type="secondary">-</Text>;
        const color = latency < 100 ? 'success' : latency < 500 ? 'warning' : 'error';
        return <Tag color={color}>{latency.toFixed(2)} ms</Tag>;
      },
    },
    {
      title: '成功率',
      dataIndex: 'success_rate',
      key: 'success_rate',
      render: (rate: number | undefined) => {
        if (rate === undefined || rate === null) return <Text type="secondary">-</Text>;
        const color = rate >= 95 ? 'success' : rate >= 80 ? 'warning' : 'error';
        return <Tag color={color}>{rate.toFixed(1)}%</Tag>;
      },
    },
    {
      title: '错误次数',
      dataIndex: 'error_count',
      key: 'error_count',
      render: (count: number | undefined) => {
        if (count === undefined || count === null) return <Text type="secondary">-</Text>;
        return <Text type={count === 0 ? 'success' : 'danger'}>{count}</Text>;
      },
    },
    {
      title: '最后检查',
      dataIndex: 'last_check',
      key: 'last_check',
      render: (time: string | undefined) => {
        if (!time) return <Text type="secondary">-</Text>;
        try {
          const date = new Date(time);
          return <Text type="secondary">{date.toLocaleString('zh-CN')}</Text>;
        } catch {
          return <Text type="secondary">{time}</Text>;
        }
      },
    },
    {
      title: '备注',
      dataIndex: 'message',
      key: 'message',
      render: (message: string | undefined, record: DataSourceStatus) => {
        if (message) return <Text type="success">{message}</Text>;
        if (record.error) return <Text type="danger">{record.error}</Text>;
        return <Text type="secondary">-</Text>;
      },
    },
  ];

  const dataSource = Object.entries(healthStatus).map(([key, status]) => ({
    key,
    name: dataSourceNames[key] || key,
    ...status,
  }));

  const available = availableCount ?? Object.values(healthStatus).filter(s => s.available).length;
  const total = totalCount ?? Object.keys(healthStatus).length;

  return (
    <Card
      title={
        <Space>
          <span>📡 数据源状态</span>
          {summary && <Text type="secondary" style={{ fontSize: 12 }}>({summary})</Text>}
        </Space>
      }
      size="small"
    >
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={8}>
          <Statistic
            title="可用数据源"
            value={available}
            suffix={`/ ${total}`}
            valueStyle={{ color: available > 0 ? '#3f8600' : '#cf1322' }}
            prefix={<CheckCircleOutlined />}
          />
        </Col>
        <Col span={8}>
          <Statistic
            title="检查方法"
            value={method || '未知'}
            valueStyle={{ fontSize: 14 }}
          />
        </Col>
        <Col span={8}>
          <Statistic
            title="可用率"
            value={total > 0 ? ((available / total) * 100).toFixed(1) : 0}
            suffix="%"
            valueStyle={{ color: (available / total) >= 0.5 ? '#3f8600' : '#cf1322' }}
          />
        </Col>
      </Row>

      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        size="small"
        rowKey="key"
      />
    </Card>
  );
};

export default DataSourceStatusComponent;
















