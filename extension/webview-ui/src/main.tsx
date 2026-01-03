import React from 'react';
import ReactDOM from 'react-dom/client';
import { ConfigProvider, theme } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import App from './App';
import './styles/index.css';

// 获取VS Code主题
const getVSCodeTheme = () => {
  const body = document.body;
  const isDark = body.classList.contains('vscode-dark') || 
                 body.getAttribute('data-vscode-theme-kind') === 'vscode-dark';
  return isDark ? theme.darkAlgorithm : theme.defaultAlgorithm;
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider
      locale={zhCN}
      theme={{
        algorithm: getVSCodeTheme(),
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <App />
    </ConfigProvider>
  </React.StrictMode>
);
