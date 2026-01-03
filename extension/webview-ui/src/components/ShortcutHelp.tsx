/**
 * 快捷键帮助组件
 * 
 * 显示可用的键盘快捷键
 */

import React, { useState } from 'react';
import { Button, Modal, Table, Tag } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';

interface Shortcut {
  key: string;
  description: string;
  category: string;
}

const shortcuts: Shortcut[] = [
  { key: 'Ctrl+R', description: '刷新数据', category: '通用' },
  { key: 'Ctrl+F', description: '聚焦搜索框', category: '通用' },
  { key: 'Esc', description: '关闭对话框', category: '通用' },
];

const ShortcutHelp: React.FC = () => {
  const [visible, setVisible] = useState(false);

  const columns = [
    {
      title: '快捷键',
      dataIndex: 'key',
      key: 'key',
      render: (key: string) => (
        <Tag color="blue" style={{ fontFamily: 'monospace' }}>
          {key}
        </Tag>
      ),
    },
    {
      title: '说明',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      render: (category: string) => <Tag>{category}</Tag>,
    },
  ];

  return (
    <>
      <Button
        type="text"
        icon={<QuestionCircleOutlined />}
        onClick={() => setVisible(true)}
        title="查看快捷键帮助"
      >
        快捷键
      </Button>
      <Modal
        title="键盘快捷键"
        open={visible}
        onCancel={() => setVisible(false)}
        footer={null}
        width={600}
      >
        <Table
          dataSource={shortcuts}
          columns={columns}
          rowKey="key"
          pagination={false}
          size="small"
        />
      </Modal>
    </>
  );
};

export default ShortcutHelp;

