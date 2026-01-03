/**
 * 搜索栏组件
 * 
 * 统一的搜索输入框
 */

import React from 'react';
import { Input, Button } from 'antd';
import { SearchOutlined, ClearOutlined } from '@ant-design/icons';

interface SearchBarProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (value: string) => void;
  onClear?: () => void;
  allowClear?: boolean;
  style?: React.CSSProperties;
}

const SearchBar: React.FC<SearchBarProps> = ({
  placeholder = '请输入搜索关键词',
  value,
  onChange,
  onSearch,
  onClear,
  allowClear = true,
  style,
}) => {
  const handleSearch = (searchValue: string) => {
    if (onSearch) {
      onSearch(searchValue);
    }
  };

  const handleClear = () => {
    if (onChange) {
      onChange('');
    }
    if (onClear) {
      onClear();
    }
  };

  return (
    <Input
      placeholder={placeholder}
      value={value}
      onChange={(e: React.ChangeEvent<HTMLInputElement>) => onChange?.(e.target.value)}
      onPressEnter={(e: React.KeyboardEvent<HTMLInputElement>) => handleSearch((e.target as HTMLInputElement).value)}
      allowClear={allowClear}
      prefix={<SearchOutlined />}
      suffix={
        value && allowClear ? (
          <Button
            type="text"
            size="small"
            icon={<ClearOutlined />}
            onClick={handleClear}
            style={{ border: 'none', padding: 0 }}
          />
        ) : null
      }
      style={style}
    />
  );
};

export default SearchBar;

