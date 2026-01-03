import React, { useEffect, useState } from 'react';
import { Card, Table, Button, Tag, Space, Row, Col, Statistic, Progress, Alert } from 'antd';
import { RocketOutlined } from '@ant-design/icons';
import { useAppStore } from '@store/index';
import { TenbaggerRankingChart } from '../components/ChartWrapper';
import TenbaggerDetailModal from '../components/TenbaggerDetailModal';
import ExportButton from '../components/ExportButton';
import RefreshButton from '../components/RefreshButton';
import SearchBar from '../components/SearchBar';
import { useDebounce } from '../hooks/useDebounce';

const TenbaggerPage: React.FC = () => {
  const { 
    tenbagger, 
    evaluateStock, 
    getRankings 
  } = useAppStore();
  
  const [searchCode, setSearchCode] = useState('');
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filteredRankings, setFilteredRankings] = useState<any[]>([]);
  
  // 防抖搜索
  const debouncedSearchCode = useDebounce(searchCode, 300);

  useEffect(() => {
    getRankings().catch(err => {
      setError(err instanceof Error ? err.message : '获取排名失败');
    });
  }, []);

  // 搜索过滤
  useEffect(() => {
    if (!debouncedSearchCode.trim()) {
      setFilteredRankings(tenbagger.rankings);
    } else {
      const filtered = tenbagger.rankings.filter((stock: any) => {
        const code = stock.code?.toLowerCase() || '';
        const name = stock.name?.toLowerCase() || '';
        const search = debouncedSearchCode.toLowerCase();
        return code.includes(search) || name.includes(search);
      });
      setFilteredRankings(filtered);
    }
  }, [debouncedSearchCode, tenbagger.rankings]);

  const handleEvaluate = async (code: string) => {
    setError(null);
    try {
      await evaluateStock(code);
      setDetailModalVisible(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : '评估失败');
    }
  };

  const columns = [
    { 
      title: '排名', 
      key: 'rank',
      width: 60,
      render: (_: any, __: any, index: number) => (
        <Tag color={index < 3 ? 'gold' : 'default'}>{index + 1}</Tag>
      )
    },
    { title: '代码', dataIndex: 'code', key: 'code', width: 80 },
    { title: '名称', dataIndex: 'name', key: 'name' },
    { 
      title: '当前价', 
      dataIndex: 'price', 
      key: 'price',
      render: (price: number) => `¥${price?.toFixed(2) || '-'}`
    },
    { 
      title: '涨跌幅', 
      dataIndex: 'change_pct', 
      key: 'change_pct',
      render: (pct: number) => (
        <span style={{ color: pct >= 0 ? '#52c41a' : '#ff4d4f' }}>
          {pct >= 0 ? '+' : ''}{pct?.toFixed(2) || '0.00'}%
        </span>
      )
    },
    { 
      title: '十倍潜力', 
      dataIndex: 'tenbagger_score', 
      key: 'tenbagger_score',
      render: (score: number) => (
        <Progress 
          percent={score || 0} 
          size="small" 
          status={score >= 80 ? 'success' : score >= 60 ? 'normal' : 'exception'}
        />
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: any) => (
        <Button 
          type="link" 
          size="small"
          onClick={() => handleEvaluate(record.code)}
        >
          详细评估
        </Button>
      )
    },
  ];

  return (
    <div style={{ padding: '16px 0' }}>
      {error && (
        <Alert
          message="错误"
          description={error}
          type="error"
          closable
          onClose={() => setError(null)}
          style={{ marginBottom: 16 }}
        />
      )}
      
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic 
              title="候选股票" 
              value={tenbagger.rankings.length} 
              prefix={<RocketOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic 
              title="高潜力(>80分)" 
              value={tenbagger.rankings.filter(s => (s as any).tenbagger_score >= 80).length}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic 
              title="中潜力(60-80分)" 
              value={tenbagger.rankings.filter(s => {
                const score = (s as any).tenbagger_score;
                return score >= 60 && score < 80;
              }).length}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic 
              title="待观察(<60分)" 
              value={tenbagger.rankings.filter(s => (s as any).tenbagger_score < 60).length}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 十倍股排名图表 */}
      {(filteredRankings.length > 0 || tenbagger.rankings.length > 0) && (
        <div style={{ marginBottom: 16 }}>
          <TenbaggerRankingChart 
            rankings={filteredRankings.length > 0 ? filteredRankings : tenbagger.rankings} 
            topN={20} 
          />
        </div>
      )}

      <Card 
        title="🎯 十倍股候选排行" 
        extra={
          <Space>
            <SearchBar
              placeholder="输入股票代码或名称"
              value={searchCode}
              onChange={setSearchCode}
              onSearch={(value) => value && handleEvaluate(value)}
              style={{ width: 300 }}
            />
            <Button 
              type="primary" 
              icon={<RocketOutlined />}
              loading={tenbagger.evaluating}
              onClick={() => searchCode && handleEvaluate(searchCode)}
            >
              评估
            </Button>
            <ExportButton 
              data={tenbagger.rankings} 
              filename="tenbagger_rankings"
              disabled={tenbagger.rankings.length === 0}
            />
            <RefreshButton
              onClick={() => {
                setError(null);
                getRankings().catch(err => {
                  setError(err instanceof Error ? err.message : '获取排名失败');
                });
              }}
              loading={tenbagger.evaluating}
            />
          </Space>
        }
      >
        <Table
          dataSource={filteredRankings.length > 0 ? filteredRankings : tenbagger.rankings}
          columns={columns}
          rowKey="code"
          pagination={{ pageSize: 10 }}
          loading={tenbagger.evaluating}
        />
      </Card>

      {/* 详细评估模态框 */}
      <TenbaggerDetailModal
        visible={detailModalVisible}
        stock={tenbagger.selectedStock}
        onClose={() => setDetailModalVisible(false)}
      />
    </div>
  );
};

export default TenbaggerPage;
