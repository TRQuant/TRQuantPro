import React, { useState } from 'react';
import { Card, Steps, Button, Table, Tag, Space, Alert, Row, Col, Descriptions, Typography, Collapse, Divider } from 'antd';
import { PlayCircleOutlined, CheckCircleOutlined, LoadingOutlined, CloseCircleOutlined, ThunderboltOutlined } from '@ant-design/icons';
import { useAppStore } from '@store/index';
import DataSourceStatusComponent, { DataSourceHealthStatus } from '../components/DataSourceStatus';
import { WorkflowStepChart } from '../components/ChartWrapper';
import { HelpTooltip, WorkflowStepHelp } from '../components/HelpTooltip';
import { useKeyboardShortcuts } from '../hooks/useKeyboardShortcuts';
import ExportButton from '../components/ExportButton';
import RefreshButton from '../components/RefreshButton';

const { Step } = Steps;
const { Panel } = Collapse;
const { Text, Paragraph } = Typography;

const workflowSteps = [
  { title: '数据源', description: '检查数据源连接', stepId: 'data_source' },
  { title: '市场趋势', description: '分析市场整体趋势', stepId: 'market_trend' },
  { title: '投资主线', description: '识别热门投资主线', stepId: 'mainline' },
  { title: '候选池', description: '构建股票候选池', stepId: 'candidate_pool' },
  { title: '因子构建', description: '计算多因子得分', stepId: 'factor' },
  { title: '策略生成', description: '生成交易策略', stepId: 'strategy' },
  { title: '回测', description: '历史数据回测', stepId: 'backtest' },
  { title: '优化', description: '参数优化调整', stepId: 'optimization' },
  { title: '报告', description: '生成分析报告', stepId: 'report' },
];

const WorkflowPage: React.FC = () => {
  const { 
    workflow, 
    mainlines, 
    candidatePool,
    runWorkflowStep,
    createWorkflow
  } = useAppStore();
  
  const [expandedStep, setExpandedStep] = useState<number | null>(null);

  // 键盘快捷键支持
  useKeyboardShortcuts([
    {
      key: 'r',
      ctrl: true,
      handler: () => {
        // 刷新工作流
        if (workflow.workflowId) {
          // 可以添加刷新逻辑
        }
      },
    },
  ]);

  const mainlineColumns = [
    { title: '主线名称', dataIndex: 'name', key: 'name' },
    { 
      title: '评分', 
      dataIndex: 'score', 
      key: 'score',
      render: (score: number) => <Tag color="blue">{score.toFixed(1)}</Tag>
    },
    { 
      title: '趋势', 
      dataIndex: 'trend', 
      key: 'trend',
      render: (trend: string) => (
        <Tag color={trend === 'up' ? 'green' : trend === 'down' ? 'red' : 'default'}>
          {trend === 'up' ? '上涨' : trend === 'down' ? '下跌' : '震荡'}
        </Tag>
      )
    },
    { 
      title: '涨跌幅', 
      dataIndex: 'change_pct', 
      key: 'change_pct',
      render: (pct: number) => (
        <span style={{ color: pct >= 0 ? '#52c41a' : '#ff4d4f' }}>
          {pct >= 0 ? '+' : ''}{pct.toFixed(2)}%
        </span>
      )
    },
    { 
      title: '资金流(亿)', 
      dataIndex: 'fund_flow', 
      key: 'fund_flow',
      render: (flow: number) => flow.toFixed(2)
    },
  ];

  const stockColumns = [
    { title: '代码', dataIndex: 'code', key: 'code' },
    { title: '名称', dataIndex: 'name', key: 'name' },
    { 
      title: '价格', 
      dataIndex: 'price', 
      key: 'price',
      render: (price: number) => `¥${price.toFixed(2)}`
    },
    { 
      title: '涨跌幅', 
      dataIndex: 'change_pct', 
      key: 'change_pct',
      render: (pct: number) => (
        <span style={{ color: pct >= 0 ? '#52c41a' : '#ff4d4f' }}>
          {pct >= 0 ? '+' : ''}{pct.toFixed(2)}%
        </span>
      )
    },
  ];

  return (
    <div style={{ padding: '16px 0' }}>
      {workflow.error && (
        <Alert 
          message="错误" 
          description={workflow.error} 
          type="error" 
          closable 
          style={{ marginBottom: 16 }}
        />
      )}
      
      <Card 
        title={
          <Space>
            <span>📊 9步投资工作流</span>
            <HelpTooltip 
              content="9步投资工作流是TRQuant的核心功能，从数据源检查到最终报告生成，完整覆盖量化投资全流程"
              title="工作流说明"
            />
          </Space>
        }
        extra={
          <Space>
            <ExportButton 
              data={workflow.stepResults} 
              filename="workflow_results"
              disabled={Object.keys(workflow.stepResults).length === 0}
            />
            <RefreshButton
              onClick={async () => {
                if (workflow.workflowId) {
                  // 刷新工作流状态
                  await createWorkflow();
                }
              }}
              loading={workflow.isLoading}
            />
            <Button
              type="primary"
              icon={<ThunderboltOutlined />}
              onClick={async () => {
                // 一键执行所有步骤
                if (!workflow.workflowId) {
                  await createWorkflow();
                }
                // 依次执行所有步骤
                for (let i = 1; i <= 9; i++) {
                  await runWorkflowStep(i);
                }
              }}
              loading={workflow.isLoading}
            >
              一键执行
            </Button>
          </Space>
        }
        style={{ marginBottom: 16 }}
      >
        <Steps current={workflow.currentStep} size="small">
          {workflowSteps.map((step, index) => {
            const stepResult = workflow.stepResults[index + 1];
            const stepResultData = stepResult?.step_result || stepResult?.data || stepResult;
            const isSuccess = stepResultData?.success !== false;
            const isFailed = stepResultData?.success === false || stepResultData?.error;
            
            return (
              <Step 
                key={index} 
                title={
                  <Space>
                    <span>{step.title}</span>
                    <HelpTooltip 
                      content={WorkflowStepHelp[step.stepId] || step.description}
                      title={step.title}
                    />
                  </Space>
                }
                description={step.description}
                status={
                  workflow.isLoading && workflow.currentStep === index + 1 
                    ? 'process'
                    : isFailed
                    ? 'error'
                    : isSuccess && stepResult
                    ? 'finish'
                    : 'wait'
                }
                icon={
                  workflow.isLoading && workflow.currentStep === index + 1 
                    ? <LoadingOutlined /> 
                    : isFailed
                    ? <CloseCircleOutlined style={{ color: '#ff4d4f' }} />
                    : stepResult && isSuccess
                    ? <CheckCircleOutlined style={{ color: '#52c41a' }} />
                    : undefined
                }
              />
            );
          })}
        </Steps>
        
        <div style={{ marginTop: 24, textAlign: 'center' }}>
          <Space wrap>
            {workflowSteps.map((step, index) => {
              const stepResult = workflow.stepResults[index + 1];
              const stepResultData = stepResult?.step_result || stepResult?.data || stepResult;
              const isSuccess = stepResultData?.success !== false;
              const isFailed = stepResultData?.success === false || stepResultData?.error;
              
              return (
                <Button
                  key={index}
                  type={workflow.currentStep === index + 1 ? 'primary' : 'default'}
                  danger={isFailed}
                  icon={
                    workflow.isLoading && workflow.currentStep === index + 1 
                      ? <LoadingOutlined /> 
                      : isFailed
                      ? <CloseCircleOutlined />
                      : stepResult && isSuccess
                      ? <CheckCircleOutlined />
                      : <PlayCircleOutlined />
                  }
                  loading={workflow.isLoading && workflow.currentStep === index + 1}
                  onClick={() => runWorkflowStep(index + 1)}
                  disabled={workflow.isLoading}
                >
                  步骤 {index + 1}: {step.title}
                </Button>
              );
            })}
          </Space>
        </div>
        
        {/* 工作流执行状态图表 */}
        {Object.keys(workflow.stepResults).length > 0 && (
          <div style={{ marginTop: 24 }}>
            <WorkflowStepChart stepResults={workflow.stepResults} type="bar" />
          </div>
        )}
        
        {/* 步骤结果详情展示 */}
        <Divider />
        <Collapse 
          activeKey={expandedStep !== null ? [expandedStep.toString()] : []}
          onChange={(keys: string | string[]) => setExpandedStep(Array.isArray(keys) && keys.length > 0 ? parseInt(keys[0] as string) : null)}
          style={{ marginTop: 16 }}
        >
          {workflowSteps.map((step, index) => {
            const stepNum = index + 1;
            const stepResult = workflow.stepResults[stepNum];
            if (!stepResult) return null;
            
            const stepResultData = stepResult?.step_result || stepResult?.data || stepResult;
            const isSuccess = stepResultData?.success !== false;
            
            // 数据源检查特殊处理
            if (stepNum === 1 && stepResultData?.health_status) {
              return (
                <Panel 
                  header={
                    <Space>
                      <span>步骤 {stepNum}: {step.title}</span>
                      {isSuccess ? (
                        <Tag color="success" icon={<CheckCircleOutlined />}>成功</Tag>
                      ) : (
                        <Tag color="error" icon={<CloseCircleOutlined />}>失败</Tag>
                      )}
                      {stepResultData.summary && (
                        <Text type="secondary" style={{ fontSize: 12 }}>
                          {stepResultData.summary}
                        </Text>
                      )}
                    </Space>
                  } 
                  key={stepNum}
                >
                  <DataSourceStatusComponent
                    healthStatus={stepResultData.health_status as DataSourceHealthStatus}
                    summary={stepResultData.summary}
                    method={stepResultData.method}
                    availableCount={stepResultData.available_count}
                    totalCount={stepResultData.total_count}
                  />
                  {stepResultData.error && (
                    <Alert
                      message="错误信息"
                      description={stepResultData.error}
                      type="error"
                      style={{ marginTop: 16 }}
                    />
                  )}
                </Panel>
              );
            }
            
            // 其他步骤的通用展示
            return (
              <Panel 
                header={
                  <Space>
                    <span>步骤 {stepNum}: {step.title}</span>
                    {isSuccess ? (
                      <Tag color="success" icon={<CheckCircleOutlined />}>成功</Tag>
                    ) : (
                      <Tag color="error" icon={<CloseCircleOutlined />}>失败</Tag>
                    )}
                  </Space>
                } 
                key={stepNum}
              >
                <Descriptions bordered size="small" column={1}>
                  <Descriptions.Item label="状态">
                    {isSuccess ? (
                      <Tag color="success">成功</Tag>
                    ) : (
                      <Tag color="error">失败</Tag>
                    )}
                  </Descriptions.Item>
                  {stepResultData.summary && (
                    <Descriptions.Item label="摘要">
                      {stepResultData.summary}
                    </Descriptions.Item>
                  )}
                  {stepResultData.method && (
                    <Descriptions.Item label="执行方法">
                      {stepResultData.method}
                    </Descriptions.Item>
                  )}
                  {stepResultData.error && (
                    <Descriptions.Item label="错误信息">
                      <Text type="danger">{stepResultData.error}</Text>
                    </Descriptions.Item>
                  )}
                  {stepResultData.details && (
                    <Descriptions.Item label="详细信息">
                      <Paragraph style={{ margin: 0 }}>
                        <pre style={{ whiteSpace: 'pre-wrap', fontSize: 12 }}>
                          {typeof stepResultData.details === 'string' 
                            ? stepResultData.details 
                            : JSON.stringify(stepResultData.details, null, 2)}
                        </pre>
                      </Paragraph>
                    </Descriptions.Item>
                  )}
                </Descriptions>
                
                {stepResultData && Object.keys(stepResultData).length > 0 && (
                  <div style={{ marginTop: 16 }}>
                    <Text strong>完整结果数据：</Text>
                    <pre style={{ 
                      background: '#f5f5f5', 
                      padding: 12, 
                      borderRadius: 4, 
                      marginTop: 8,
                      fontSize: 12,
                      maxHeight: 300,
                      overflow: 'auto'
                    }}>
                      {JSON.stringify(stepResultData, null, 2)}
                    </pre>
                  </div>
                )}
              </Panel>
            );
          })}
        </Collapse>
      </Card>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="🔥 投资主线" size="small">
            {mainlines.length > 0 ? (
              <Table
                dataSource={mainlines}
                columns={mainlineColumns}
                rowKey="name"
                pagination={false}
                size="small"
              />
            ) : (
              <div style={{ textAlign: 'center', padding: 20, color: '#999' }}>
                请先运行步骤3获取投资主线
              </div>
            )}
          </Card>
        </Col>
        <Col span={12}>
          <Card title="📋 候选池" size="small">
            {candidatePool.length > 0 ? (
              <Table
                dataSource={candidatePool}
                columns={stockColumns}
                rowKey="code"
                pagination={{ pageSize: 5 }}
                size="small"
              />
            ) : (
              <div style={{ textAlign: 'center', padding: 20, color: '#999' }}>
                请先运行步骤4构建候选池
              </div>
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default WorkflowPage;
