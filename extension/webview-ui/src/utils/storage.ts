/**
 * 本地存储工具
 * 
 * 封装localStorage和sessionStorage
 */

class StorageWrapper {
  private storage: globalThis.Storage;

  constructor(type: 'local' | 'session' = 'local') {
    this.storage = type === 'local' ? window.localStorage : window.sessionStorage;
  }

  /**
   * 设置值
   */
  set<T>(key: string, value: T): void {
    try {
      const serialized = JSON.stringify(value);
      this.storage.setItem(key, serialized);
    } catch (error) {
      console.error(`[Storage] 设置值失败: ${key}`, error);
    }
  }

  /**
   * 获取值
   */
  get<T>(key: string, defaultValue?: T): T | undefined {
    try {
      const item = this.storage.getItem(key);
      if (item === null) {
        return defaultValue;
      }
      return JSON.parse(item) as T;
    } catch (error) {
      console.error(`[Storage] 获取值失败: ${key}`, error);
      return defaultValue;
    }
  }

  /**
   * 删除值
   */
  remove(key: string): void {
    try {
      this.storage.removeItem(key);
    } catch (error) {
      console.error(`[Storage] 删除值失败: ${key}`, error);
    }
  }

  /**
   * 清空所有
   */
  clear(): void {
    try {
      this.storage.clear();
    } catch (error) {
      console.error('[Storage] 清空失败', error);
    }
  }

  /**
   * 获取所有键
   */
  keys(): string[] {
    const keys: string[] = [];
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key) {
        keys.push(key);
      }
    }
    return keys;
  }

  /**
   * 检查是否存在
   */
  has(key: string): boolean {
    return this.storage.getItem(key) !== null;
  }
}

// 导出单例
export const localStorageWrapper = new StorageWrapper('local');
export const sessionStorageWrapper = new StorageWrapper('session');

// 便捷函数
export function setLocalStorage<T>(key: string, value: T): void {
  localStorageWrapper.set(key, value);
}

export function getLocalStorage<T>(key: string, defaultValue?: T): T | undefined {
  return localStorageWrapper.get(key, defaultValue);
}

export function removeLocalStorage(key: string): void {
  localStorageWrapper.remove(key);
}

export function setSessionStorage<T>(key: string, value: T): void {
  sessionStorageWrapper.set(key, value);
}

export function getSessionStorage<T>(key: string, defaultValue?: T): T | undefined {
  return sessionStorageWrapper.get(key, defaultValue);
}

export function removeSessionStorage(key: string): void {
  sessionStorageWrapper.remove(key);
}

