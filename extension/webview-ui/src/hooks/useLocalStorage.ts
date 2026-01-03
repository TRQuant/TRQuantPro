/**
 * LocalStorage Hook
 * 
 * 简化localStorage的使用
 */

import { useState } from 'react';
import { getLocalStorage, setLocalStorage } from '../utils/storage';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = getLocalStorage<T>(key);
      return item !== undefined ? item : initialValue;
    } catch (error) {
      console.error(`[useLocalStorage] 读取失败: ${key}`, error);
      return initialValue;
    }
  });

  const setValue = (value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      setLocalStorage(key, valueToStore);
    } catch (error) {
      console.error(`[useLocalStorage] 保存失败: ${key}`, error);
    }
  };

  return [storedValue, setValue] as const;
}

