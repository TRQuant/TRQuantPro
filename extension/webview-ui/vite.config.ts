import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import { resolve } from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: './',  // 使用相对路径，关键修复！
  build: {
    outDir: 'dist',
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name].[ext]',
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
      }
    },
    chunkSizeWarningLimit: 1000, // 提高警告阈值到1MB
    sourcemap: false, // 生产环境不生成sourcemap
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@pages': resolve(__dirname, 'src/pages'),
      '@hooks': resolve(__dirname, 'src/hooks'),
      '@store': resolve(__dirname, 'src/store'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@types': resolve(__dirname, 'src/types')
    }
  }
});
