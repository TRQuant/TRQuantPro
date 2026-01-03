/**
 * Vite配置 - 性能优化版本
 */

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@store': path.resolve(__dirname, './src/store'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@services': path.resolve(__dirname, './src/services'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@types': path.resolve(__dirname, './src/types'),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // 将React和React-DOM单独打包
          'react-vendor': ['react', 'react-dom'],
          // 将Ant Design单独打包
          'antd-vendor': ['antd', '@ant-design/icons'],
          // 将ECharts单独打包
          'echarts-vendor': ['echarts', 'echarts-for-react'],
          // 将Zustand单独打包
          'zustand-vendor': ['zustand'],
        },
      },
    },
    chunkSizeWarningLimit: 1000, // 提高警告阈值到1MB
    sourcemap: false, // 生产环境不生成sourcemap
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // 移除console
        drop_debugger: true, // 移除debugger
      },
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'antd', '@ant-design/icons', 'zustand'],
  },
});













































