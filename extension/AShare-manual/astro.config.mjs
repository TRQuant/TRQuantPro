import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import rehypeMermaid from 'rehype-mermaid';
import rehypeMathjax from 'rehype-mathjax';
import {
  transformerNotationDiff,
  transformerNotationHighlight,
  transformerNotationFocus,
  transformerMetaHighlight,
  transformerMetaWordHighlight,
  transformerNotationWordHighlight
} from '@shikijs/transformers';
import remarkCodeFromFile from './src/plugins/remark-code-from-file-v2.mjs';
import watchCodeLibrary from './src/integrations/watch-code-library-v3.mjs';
import viteCodeLibraryWatcher from './src/plugins/vite-code-library-watcher-working.mjs';

import vercel from '@astrojs/vercel';

export default defineConfig({
  // 设置路径别名，任何位置可通过 ~/layouts 引用
  alias: {
    '~layouts': './src/layouts'
  },

  integrations: [mdx(), watchCodeLibrary()], // 已修复错误处理

  vite: {
    // 添加Vite插件监控代码库
    plugins: [viteCodeLibraryWatcher()],
    // 忽略 Mermaid 生成的临时文件
    server: {
      watch: {
        ignored: ['**/*.mmd'],
        // 监控代码库目录，实现代码文件修改后自动更新
        // 注意：code_library在项目根目录，需要向上查找
      },
      // 允许访问项目外的文件（code_library在TRQuant根目录）
      fs: {
        strict: false,
      }
    },
    // 配置额外的文件监控
    // 注意：Vite默认只监控项目内的文件，外部文件需要特殊处理
  },

  // 内容配置
  content: {
    // 忽略realtime目录的自动集合生成
    collections: {
      realtime: {
        type: 'data'
      }
    }
  },

  markdown: {
    // 允许HTML在Markdown中渲染
    allowHTML: true,
    // 配置remark和rehype插件
    remarkPlugins: [remarkCodeFromFile],
    // 配置 rehype-mermaid，使用 img-svg 策略生成静态 SVG 图片
    // 优化配置：使用专业配色方案，支持暗色模式
    rehypePlugins: [
      rehypeMathjax,
      [rehypeMermaid, { 
        strategy: 'img-svg', 
        dark: true, 
        colorScheme: 'base',  // 使用 base 主题以便自定义
        themeVariables: {
          primaryColor: '#3b82f6',
          primaryTextColor: '#ffffff',
          primaryBorderColor: '#2563eb',
          lineColor: '#64748b',
          secondaryColor: '#1e293b',
          tertiaryColor: '#334155',
          background: 'transparent',
          mainBkg: 'transparent',
          secondBkg: 'transparent',
          tertiaryBkg: 'transparent'
        }
      }]
    ],
    // 代码高亮配置 - 使用Shiki和VS Code主题
    // 重要：排除 mermaid 语言，避免与 rehype-mermaid 冲突
    syntaxHighlight: {
      type: 'shiki',
      excludeLangs: ['mermaid']
    },
    shikiConfig: {
      // 使用VS Code官方主题
      themes: {
        light: 'light-plus',
        dark: 'dark-plus'
      },
      // 启用代码换行
      wrap: true,
      // 保持代码缩进格式
      preserveIndent: true,
      // 支持的语言（保持默认设置）
      langs: [],
      // 添加转换器支持
      transformers: [
        transformerNotationDiff(),
        transformerNotationHighlight(),
        transformerNotationFocus(),
        transformerMetaHighlight(),
        transformerMetaWordHighlight(),
        transformerNotationWordHighlight()
      ]
    }
  },

  adapter: vercel()
});