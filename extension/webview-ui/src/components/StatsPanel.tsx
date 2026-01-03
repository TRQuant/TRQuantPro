/**
 * 统计面板组件
 * 
 * 显示数据统计信息
 */

import React from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

export interface StatItem {
  title: string;
  value: number | string;
  prefix?: React.ReactNode;
  suffix?: string;
  valueStyle?: React.CSSProperties;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

interface StatsPanelProps {
  title?: string;
  stats: StatItem[];
  columns?: number;
}

const StatsPanel: React.FC<StatsPanelProps> = ({
  title,
  stats,
  columns = 4,
}) => {
  const span = 24 / columns;

  return (
    <Card title={title} style={{ marginBottom: 16 }}>
      <Row gutter={16}>
        {stats.map((stat, index) => (
          <Col span={span} key={index}>
            <Statistic
              title={stat.title}
              value={stat.value}
              prefix={stat.prefix}
              suffix={stat.suffix}
              valueStyle={stat.valueStyle}
            />
            {stat.trend && (
              <div style={{ marginTop: 8 }}>
                <span
                  style={{
                    color: stat.trend.isPositive ? '#52c41a' : '#ff4d4f',
                    fontSize: 12,
                  }}
                >
                  {stat.trend.isPositive ? (
                    <ArrowUpOutlined />
                  ) : (
                    <ArrowDownOutlined />
                  )}{' '}
                  {Math.abs(stat.trend.value).toFixed(2)}%
                </span>
              </div>
            )}
          </Col>
        ))}
      </Row>
    </Card>
  );
};

export default StatsPanel;

