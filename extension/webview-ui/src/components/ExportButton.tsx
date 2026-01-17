/**
 * 导出按钮组件
 * 
 * 支持导出数据为JSON、CSV等格式
 */

import React from 'react';
import { Button, Dropdown, MenuProps } from 'antd';
import { DownloadOutlined, FileTextOutlined, TableOutlined } from '@ant-design/icons';

interface ExportButtonProps {
  data: any;
  filename?: string;
  disabled?: boolean;
}

const ExportButton: React.FC<ExportButtonProps> = ({
  data,
  filename = 'export',
  disabled = false,
}) => {
  /**
   * 导出为JSON
   */
  const exportJSON = () => {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  /**
   * 导出为CSV
   */
  const exportCSV = () => {
    if (!Array.isArray(data) || data.length === 0) {
      console.warn('数据不是数组或为空，无法导出CSV');
      return;
    }

    // 获取表头
    const headers = Object.keys(data[0]);
    const csvRows = [
      headers.join(','),
      ...data.map(row => 
        headers.map(header => {
          const value = row[header];
          // 处理包含逗号的值
          if (typeof value === 'string' && value.includes(',')) {
            return `"${value}"`;
          }
          return value ?? '';
        }).join(',')
      ),
    ];

    const csvStr = csvRows.join('\n');
    const blob = new Blob(['\ufeff' + csvStr], { type: 'text/csv;charset=utf-8;' }); // 添加BOM支持中文
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const menuItems: MenuProps['items'] = [
    {
      key: 'json',
      label: '导出为JSON',
      icon: <FileTextOutlined />,
      onClick: exportJSON,
    },
    {
      key: 'csv',
      label: '导出为CSV',
      icon: <TableOutlined />,
      onClick: exportCSV,
      disabled: !Array.isArray(data) || data.length === 0,
    },
  ];

  return (
    <Dropdown menu={{ items: menuItems }} trigger={['click']}>
      <Button 
        icon={<DownloadOutlined />} 
        disabled={disabled}
      >
        导出数据
      </Button>
    </Dropdown>
  );
};

export default ExportButton;













































