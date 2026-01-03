/**
 * 数据表格组件
 * 
 * 增强的数据表格，支持排序、筛选、导出等
 */

import { Table } from 'antd';
import ExportButton from './ExportButton';

interface DataTableProps<T = any> {
  showExport?: boolean;
  exportFilename?: string;
  dataSource?: T[];
  [key: string]: any; // 支持所有Table的其他属性
}

function DataTable<T extends Record<string, any> = any>({
  showExport = true,
  exportFilename = 'table_data',
  dataSource = [],
  ...tableProps
}: DataTableProps<T>) {
  return (
    <div>
      {showExport && dataSource && dataSource.length > 0 && (
        <div style={{ marginBottom: 16, textAlign: 'right' }}>
          <ExportButton data={dataSource} filename={exportFilename} />
        </div>
      )}
      <Table<T> dataSource={dataSource} {...(tableProps as any)} />
    </div>
  );
}

export default DataTable;

