/**
 * 帮助提示组件
 * 
 * 提供上下文相关的帮助信息
 */

import React from 'react';
import { Tooltip, Button } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

interface HelpTooltipProps {
  content: string | React.ReactNode;
  title?: string;
  placement?: 'top' | 'bottom' | 'left' | 'right';
}

export const HelpTooltip: React.FC<HelpTooltipProps> = ({
  content,
  title,
  placement = 'top',
}) => {
  return (
    <Tooltip
      title={
        <div>
          {title && <div style={{ fontWeight: 'bold', marginBottom: 4 }}>{title}</div>}
          <div>{content}</div>
        </div>
      }
      placement={placement}
    >
      <Button
        type="text"
        size="small"
        icon={<QuestionCircleOutlined />}
        style={{ padding: 0, height: 'auto' }}
      />
    </Tooltip>
  );
};

/**
 * 工作流步骤帮助信息
 */
export const WorkflowStepHelp: Record<string, string> = {
  data_source: '检查数据源连接状态，包括JQData、AKShare、Tushare等数据源的可用性和延迟',
  market_trend: '分析市场整体趋势，包括大盘指数走势、市场情绪、资金流向等',
  mainline: '识别当前热门投资主线，如AI、新能源、医药等主题投资机会',
  candidate_pool: '基于主线和市场趋势，构建股票候选池，筛选潜在投资标的',
  factor: '计算多因子得分，包括财务因子、成长因子、估值因子、技术因子等',
  strategy: '根据因子得分和市场情况，生成交易策略，包括买入卖出信号',
  backtest: '使用历史数据回测策略，评估策略的收益率、夏普比率、最大回撤等指标',
  optimization: '优化策略参数，寻找最优参数组合，提高策略表现',
  report: '生成完整的分析报告，包括策略表现、风险评估、投资建议等',
};

export default HelpTooltip;













































