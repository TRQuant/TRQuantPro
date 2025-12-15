import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import rehypeMathjax from 'rehype-mathjax';
import {
  transformerNotationDiff,
  transformerNotationHighlight,
  transformerNotationFocus,
  transformerMetaHighlight,
  transformerMetaWordHighlight,
  transformerNotationWordHighlight
} from '@shikijs/transformers';

import vercel from '@astrojs/vercel';

export default defineConfig({
  // 设置路径别名，任何位置可通过 ~/layouts 引用
  alias: {
    '~layouts': './src/layouts'
  },

  integrations: [mdx()],

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
    remarkPlugins: [],
    rehypePlugins: [rehypeMathjax],
    // 代码高亮配置 - 使用Shiki和VS Code主题
    syntaxHighlight: 'shiki',
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