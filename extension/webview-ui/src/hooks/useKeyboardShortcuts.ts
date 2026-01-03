/**
 * 键盘快捷键Hook
 * 
 * 提供全局快捷键支持
 */

import { useEffect } from 'react';

interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  handler: () => void;
  description?: string;
}

export function useKeyboardShortcuts(shortcuts: KeyboardShortcut[]) {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      shortcuts.forEach(({ key, ctrl, shift, alt, handler }) => {
        const keyMatch = event.key.toLowerCase() === key.toLowerCase();
        const ctrlMatch = ctrl ? event.ctrlKey || event.metaKey : !event.ctrlKey && !event.metaKey;
        const shiftMatch = shift ? event.shiftKey : !event.shiftKey;
        const altMatch = alt ? event.altKey : !event.altKey;

        if (keyMatch && ctrlMatch && shiftMatch && altMatch) {
          event.preventDefault();
          handler();
        }
      });
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [shortcuts]);
}

/**
 * 常用快捷键定义
 */
export const CommonShortcuts = {
  REFRESH: {
    key: 'r',
    ctrl: true,
    handler: () => {
      // 刷新当前页面数据
      window.location.reload();
    },
    description: '刷新数据 (Ctrl+R)',
  },
  SEARCH: {
    key: 'f',
    ctrl: true,
    handler: () => {
      // 聚焦搜索框
      const searchInput = document.querySelector('input[placeholder*="搜索"], input[placeholder*="输入"]') as HTMLInputElement;
      if (searchInput) {
        searchInput.focus();
      }
    },
    description: '搜索 (Ctrl+F)',
  },
};













































