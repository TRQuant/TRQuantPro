/**
 * ECharts图表包装组件
 * 
 * 提供统一的图表配置和样式
 */

import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card } from 'antd';

interface ChartWrapperProps {
  title?: string;
  option: any;
  height?: number | string;
  width?: number | string;
  loading?: boolean;
  style?: React.CSSProperties;
  onChartReady?: (chart: any) => void;
}

const ChartWrapper: React.FC<ChartWrapperProps> = ({
  title,
  option,
  height = 400,
  width = '100%',
  loading = false,
  style,
  onChartReady,
}) => {
  // 默认主题配置
  const defaultOption = useMemo(() => ({
    backgroundColor: 'transparent',
    textStyle: {
      color: 'var(--vscode-foreground)',
      fontSize: 12,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'var(--vscode-editor-background)',
      borderColor: 'var(--vscode-panel-border)',
      textStyle: {
        color: 'var(--vscode-foreground)',
      },
    },
    legend: {
      textStyle: {
        color: 'var(--vscode-foreground)',
      },
    },
    ...option,
  }), [option]);

  const chartContent = loading ? (
    <div style={{ height, width, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      加载中...
    </div>
  ) : (
    <ReactECharts
      option={defaultOption}
      style={{ height, width, ...style }}
      onChartReady={onChartReady}
      opts={{ renderer: 'canvas' }}
    />
  );

  if (title) {
    return (
      <Card title={title} style={{ marginBottom: 16 }}>
        {chartContent}
      </Card>
    );
  }

  return chartContent;
};

/**
 * 工作流步骤结果图表
 */
export const WorkflowStepChart: React.FC<{
  stepResults: Record<number, any>;
  type?: 'line' | 'bar' | 'pie';
}> = ({ stepResults, type = 'line' }) => {
  const option = useMemo(() => {
    const steps = Object.keys(stepResults).map(Number).sort();
    const successData = steps.map(step => {
      const result = stepResults[step];
      const success = result?.step_result?.success !== false && !result?.error;
      return success ? 1 : 0;
    });
    const failData = steps.map(step => {
      const result = stepResults[step];
      const success = result?.step_result?.success !== false && !result?.error;
      return success ? 0 : 1;
    });

    if (type === 'bar') {
      return {
        xAxis: {
          type: 'category',
          data: steps.map(s => `步骤${s}`),
        },
        yAxis: {
          type: 'value',
          max: 1,
        },
        series: [
          {
            name: '成功',
            type: 'bar',
            data: successData,
            itemStyle: { color: '#52c41a' },
          },
          {
            name: '失败',
            type: 'bar',
            data: failData,
            itemStyle: { color: '#ff4d4f' },
          },
        ],
      };
    }

    return {
      xAxis: {
        type: 'category',
        data: steps.map(s => `步骤${s}`),
      },
      yAxis: {
        type: 'value',
        max: 1,
      },
      series: [
        {
          name: '执行状态',
          type: 'line',
            data: steps.map((_step, idx) => ({
            value: successData[idx],
            itemStyle: {
              color: successData[idx] === 1 ? '#52c41a' : '#ff4d4f',
            },
          })),
          markPoint: {
            data: [
              { type: 'max', name: '最大值' },
            ],
          },
        },
      ],
    };
  }, [stepResults, type]);

  return (
    <ChartWrapper
      title="工作流执行状态"
      option={option}
      height={300}
    />
  );
};

/**
 * 十倍股排名图表
 */
export const TenbaggerRankingChart: React.FC<{
  rankings: any[];
  topN?: number;
}> = ({ rankings, topN = 10 }) => {
  const option = useMemo(() => {
    const topRankings = rankings.slice(0, topN);
    
    return {
      xAxis: {
        type: 'value',
        name: '十倍潜力得分',
      },
      yAxis: {
        type: 'category',
        data: topRankings.map(r => r.name || r.code).reverse(),
        inverse: true,
      },
      series: [
        {
          name: '十倍潜力',
          type: 'bar',
          data: topRankings.map(r => ({
            value: r.tenbagger_score || 0,
            itemStyle: {
              color: (r.tenbagger_score || 0) >= 80 ? '#52c41a' : 
                     (r.tenbagger_score || 0) >= 60 ? '#1890ff' : '#faad14',
            },
          })).reverse(),
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
          },
        },
      ],
    };
  }, [rankings, topN]);

  return (
    <ChartWrapper
      title={`十倍股排名 Top ${topN}`}
      option={option}
      height={400}
    />
  );
};

/**
 * 市场趋势图表
 */
export const MarketTrendChart: React.FC<{
  trendData: {
    date: string;
    value: number;
    volume?: number;
  }[];
  title?: string;
}> = ({ trendData, title = '市场趋势' }) => {
  const option = useMemo(() => {
    return {
      tooltip: {
        trigger: 'axis',
      },
      legend: {
        data: ['价格', '成交量'],
      },
      xAxis: {
        type: 'category',
        data: trendData.map(d => d.date),
      },
      yAxis: [
        {
          type: 'value',
          name: '价格',
          position: 'left',
        },
        {
          type: 'value',
          name: '成交量',
          position: 'right',
        },
      ],
      series: [
        {
          name: '价格',
          type: 'line',
          data: trendData.map(d => d.value),
          smooth: true,
          itemStyle: { color: '#1890ff' },
        },
        ...(trendData[0]?.volume ? [{
          name: '成交量',
          type: 'bar',
          yAxisIndex: 1,
          data: trendData.map(d => d.volume || 0),
          itemStyle: { color: '#52c41a' },
        }] : []),
      ],
    };
  }, [trendData]);

  return (
    <ChartWrapper
      title={title}
      option={option}
      height={400}
    />
  );
};

export default ChartWrapper;

