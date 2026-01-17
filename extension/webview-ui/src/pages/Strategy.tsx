import React, { useEffect } from 'react';
import { Card, Table, Button, Tag, Space, Row, Col, Statistic, Descriptions } from 'antd';
import { 
  ThunderboltOutlined,
  ExperimentOutlined 
} from '@ant-design/icons';
import { useAppStore } from '@store/index';
import RefreshButton from '../components/RefreshButton';
import ExportButton from '../components/ExportButton';
import { MarketTrendChart } from '../components/ChartWrapper';

const StrategyPage: React.FC = () => {
  const { 
    strategy, 
    getStrategyTemplates, 
    scanTrend 
  } = useAppStore();

  const [trendData, setTrendData] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(false);

  useEffect(() => {
    getStrategyTemplates();
  }, []);

  const handleScanTrend = async () => {
    setLoading(true);
    try {
      const result = await scanTrend();
      setTrendData(result);
    } finally {
      setLoading(false);
    }
  };

  const templateColumns = [
    { title: '策略名称', dataIndex: 'name', key: 'name' },
    { title: '类型', dataIndex: 'type', key: 'type', render: (t: string) => <Tag>{t}</Tag> },
    { title: '描述', dataIndex: 'description', key: 'description' },
    { 
      title: '风险等级', 
      dataIndex: 'risk_level', 
      key: 'risk_level',
      render: (level: string) => (
        <Tag color={level === 'high' ? 'red' : level === 'medium' ? 'orange' : 'green'}>
          {level === 'high' ? '高' : level === 'medium' ? '中' : '低'}
        </Tag>
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, _record: any) => (
        <Space>
          <Button type="link" size="small">使用</Button>
          <Button type="link" size="small">回测</Button>
        </Space>
      )
    },
  ];

  return (
    <div style={{ padding: '16px 0' }}>
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={8}>
          <Card>
            <Statistic 
              title="策略模板" 
              value={strategy.templates.length} 
              prefix={<ExperimentOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic 
              title="市场趋势" 
              value={trendData?.trend || '未知'}
              valueStyle={{ 
                color: trendData?.trend === 'bull' ? '#52c41a' : 
                       trendData?.trend === 'bear' ? '#ff4d4f' : '#1890ff'
              }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic 
              title="推荐策略" 
              value={trendData?.recommended_strategy || '-'}
            />
          </Card>
        </Col>
      </Row>

      <Card 
        title="📈 市场趋势分析"
        style={{ marginBottom: 16 }}
        extra={
          <Space>
            {trendData && (
              <ExportButton 
                data={trendData} 
                filename="market_trend"
              />
            )}
            <RefreshButton
              onClick={handleScanTrend}
              loading={loading}
            />
            <Button 
              type="primary" 
              icon={<ThunderboltOutlined />}
              loading={loading}
              onClick={handleScanTrend}
            >
              扫描趋势
            </Button>
          </Space>
        }
      >
        {trendData ? (
          <>
            <Descriptions column={3} style={{ marginBottom: 16 }}>
              <Descriptions.Item label="市场趋势">
                <Tag color={trendData.trend === 'bull' ? 'green' : trendData.trend === 'bear' ? 'red' : 'blue'}>
                  {trendData.trend === 'bull' ? '牛市' : trendData.trend === 'bear' ? '熊市' : '震荡'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="置信度">{trendData.confidence || '-'}%</Descriptions.Item>
              <Descriptions.Item label="推荐策略">{trendData.recommended_strategy || '-'}</Descriptions.Item>
              <Descriptions.Item label="上涨板块">{trendData.up_sectors?.join(', ') || '-'}</Descriptions.Item>
              <Descriptions.Item label="下跌板块">{trendData.down_sectors?.join(', ') || '-'}</Descriptions.Item>
              <Descriptions.Item label="更新时间">{trendData.update_time || '-'}</Descriptions.Item>
            </Descriptions>
            {/* 如果有趋势数据，显示图表 */}
            {trendData.history && Array.isArray(trendData.history) && trendData.history.length > 0 && (
              <MarketTrendChart 
                trendData={trendData.history.map((item: any) => ({
                  date: item.date || item.time,
                  value: item.value || item.price,
                  volume: item.volume,
                }))}
                title="市场趋势图表"
              />
            )}
          </>
        ) : (
          <div style={{ textAlign: 'center', padding: 40, color: '#999' }}>
            点击"扫描趋势"获取市场分析
          </div>
        )}
      </Card>

      <Card 
        title="📋 策略模板库"
        extra={
          <Space>
            <ExportButton 
              data={strategy.templates} 
              filename="strategy_templates"
              disabled={strategy.templates.length === 0}
            />
            <RefreshButton
              onClick={getStrategyTemplates}
            />
          </Space>
        }
      >
        <Table
          dataSource={strategy.templates}
          columns={templateColumns}
          rowKey="name"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default StrategyPage;
