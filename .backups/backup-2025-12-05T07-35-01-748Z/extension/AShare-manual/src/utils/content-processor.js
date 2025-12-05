// 页面内容处理器 - 自动识别和标记金融关键词
import { detectFinancialKeywords, getKeywordDefinition, FINANCIAL_KEYWORDS_DB } from './glossary-auto-detector.js';

// 已处理页面缓存
const PROCESSED_CONTENT_CACHE = new Map();

// 关键词优先级配置
const KEYWORD_PRIORITY = {
  '高倍股': 10,
  'Ten-bagger': 9,
  'Five-bagger': 8,
  '护城河': 7,
  '市盈率': 6,
  'PE': 6,
  'ROE': 5,
  '估值': 5,
  '技术分析': 4,
  '基本面分析': 4,
  '风险管理': 3,
  '投资策略': 2,
  '资产配置': 1
};

// 内容处理配置
const PROCESSING_CONFIG = {
  maxKeywordsPerPage: 50,        // 每页最多处理的关键词数量
  minKeywordLength: 2,           // 最小关键词长度
  excludePatterns: [             // 排除的模式
    /\d+/,                       // 纯数字
    /^[a-zA-Z]$/,               // 单个字母
    /^\s+$/                      // 空白字符
  ],
  prioritizeFirstOccurrence: true // 优先处理首次出现
};

// 智能内容处理器
export class ContentProcessor {
  constructor(options = {}) {
    this.config = { ...PROCESSING_CONFIG, ...options };
    this.pageKeywords = new Map();
    this.processedCount = 0;
  }

  // 主要处理函数
  async processContent(content, pageUrl, options = {}) {
    const cacheKey = `${pageUrl}_${this.getContentHash(content)}`;
    
    // 检查缓存
    if (PROCESSED_CONTENT_CACHE.has(cacheKey) && !options.forceRefresh) {
      return PROCESSED_CONTENT_CACHE.get(cacheKey);
    }

    try {
      console.log(`🔍 Processing content for page: ${pageUrl}`);
      
      // 1. 检测金融关键词
      const detection = detectFinancialKeywords(content, pageUrl);
      console.log(`📊 Detected ${detection.keywords.length} keywords:`, detection.keywords);

      // 2. 过滤和排序关键词
      const filteredKeywords = this.filterAndSortKeywords(detection.keywords);
      console.log(`✅ Filtered to ${filteredKeywords.length} keywords:`, filteredKeywords);

      // 3. 处理关键词标记
      const processedContent = await this.markupKeywords(content, filteredKeywords, pageUrl);

      // 4. 缓存结果
      const result = {
        content: processedContent,
        keywords: filteredKeywords,
        keywordCount: filteredKeywords.length,
        pageUrl: pageUrl,
        processedAt: new Date().toISOString()
      };

      PROCESSED_CONTENT_CACHE.set(cacheKey, result);
      this.processedCount++;

      console.log(`✅ Content processing completed for ${pageUrl}`);
      return result;

    } catch (error) {
      console.error(`❌ Error processing content for ${pageUrl}:`, error);
      return {
        content: content,
        keywords: [],
        keywordCount: 0,
        pageUrl: pageUrl,
        error: error.message
      };
    }
  }

  // 过滤和排序关键词
  filterAndSortKeywords(keywords) {
    return keywords
      .filter(keyword => this.isValidKeyword(keyword))
      .sort((a, b) => {
        const priorityA = KEYWORD_PRIORITY[a] || 0;
        const priorityB = KEYWORD_PRIORITY[b] || 0;
        return priorityB - priorityA;
      })
      .slice(0, this.config.maxKeywordsPerPage);
  }

  // 验证关键词有效性
  isValidKeyword(keyword) {
    if (!keyword || keyword.length < this.config.minKeywordLength) {
      return false;
    }

    return !this.config.excludePatterns.some(pattern => pattern.test(keyword));
  }

  // 为关键词添加标记
  async markupKeywords(content, keywords, pageUrl) {
    let processedContent = content;
    const processedKeywords = new Set();

    for (const keyword of keywords) {
      try {
        // 获取关键词定义
        const definition = await getKeywordDefinition(keyword);
        
        // 存储到全局数据库
        FINANCIAL_KEYWORDS_DB.set(keyword, {
          ...definition,
          pageUrl: pageUrl,
          firstAppearance: new Date().toISOString(),
          priority: KEYWORD_PRIORITY[keyword] || 0
        });

        // 创建标记
        const markup = this.createKeywordMarkup(keyword, definition);
        
        // 替换内容（只替换第一次出现）
        const regex = new RegExp(`\\b${this.escapeRegex(keyword)}\\b`, 'i');
        if (regex.test(processedContent) && !processedKeywords.has(keyword.toLowerCase())) {
          processedContent = processedContent.replace(regex, markup);
          processedKeywords.add(keyword.toLowerCase());
          
          console.log(`🏷️  Marked keyword: ${keyword}`);
        }

      } catch (error) {
        console.warn(`⚠️  Failed to process keyword "${keyword}":`, error);
      }
    }

    return processedContent;
  }

  // 创建关键词标记HTML
  createKeywordMarkup(keyword, definition) {
    const definitionData = JSON.stringify(definition)
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
    
    return `<span class="glossary-term auto-detected" 
                  data-term="${keyword}" 
                  data-definition="${definitionData}" 
                  data-priority="${KEYWORD_PRIORITY[keyword] || 0}"
                  title="${definition.description}">
              ${keyword}
            </span>`;
  }

  // 转义正则表达式特殊字符
  escapeRegex(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  // 生成内容哈希
  getContentHash(content) {
    let hash = 0;
    for (let i = 0; i < content.length; i++) {
      const char = content.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return hash.toString();
  }

  // 获取处理统计
  getProcessingStats() {
    return {
      processedPages: this.processedCount,
      cachedResults: PROCESSED_CONTENT_CACHE.size,
      totalKeywords: FINANCIAL_KEYWORDS_DB.size,
      keywordsByCategory: this.getKeywordsByCategory()
    };
  }

  // 按类别获取关键词
  getKeywordsByCategory() {
    const categories = {};
    FINANCIAL_KEYWORDS_DB.forEach((data, keyword) => {
      const category = data.category || '未分类';
      if (!categories[category]) {
        categories[category] = [];
      }
      categories[category].push(keyword);
    });
    return categories;
  }

  // 清除缓存
  clearCache() {
    PROCESSED_CONTENT_CACHE.clear();
    console.log('📝 Content processing cache cleared');
  }
}

// 全局内容处理器实例
export const globalContentProcessor = new ContentProcessor();

// 便捷处理函数
export async function processPageContent(content, pageUrl, options = {}) {
  return await globalContentProcessor.processContent(content, pageUrl, options);
}

// 批量处理多个页面
export async function batchProcessPages(pages, options = {}) {
  const results = [];
  const { concurrency = 3 } = options;
  
  console.log(`🚀 Starting batch processing of ${pages.length} pages`);
  
  for (let i = 0; i < pages.length; i += concurrency) {
    const batch = pages.slice(i, i + concurrency);
    const batchPromises = batch.map(async ({ content, url }) => {
      try {
        const result = await globalContentProcessor.processContent(content, url, options);
        return { success: true, url, result };
      } catch (error) {
        return { success: false, url, error: error.message };
      }
    });
    
    const batchResults = await Promise.all(batchPromises);
    results.push(...batchResults);
    
    console.log(`📊 Processed batch ${Math.floor(i / concurrency) + 1}/${Math.ceil(pages.length / concurrency)}`);
  }
  
  console.log(`✅ Batch processing completed: ${results.filter(r => r.success).length}/${pages.length} successful`);
  return results;
}

// 获取页面关键词摘要
export function getPageKeywordSummary(pageUrl) {
  const pageKeywords = [];
  FINANCIAL_KEYWORDS_DB.forEach((data, keyword) => {
    if (data.pageUrl === pageUrl) {
      pageKeywords.push({ keyword, ...data });
    }
  });

  return {
    pageUrl,
    keywordCount: pageKeywords.length,
    keywords: pageKeywords.sort((a, b) => (b.priority || 0) - (a.priority || 0)),
    categories: pageKeywords.reduce((acc, { category }) => {
      acc[category] = (acc[category] || 0) + 1;
      return acc;
    }, {})
  };
}

// 搜索关键词
export function searchKeywordsInContent(query, options = {}) {
  const { category, minPriority = 0, pageUrl } = options;
  const results = [];
  
  FINANCIAL_KEYWORDS_DB.forEach((data, keyword) => {
    const matchesQuery = keyword.toLowerCase().includes(query.toLowerCase()) ||
                        data.description.toLowerCase().includes(query.toLowerCase());
    const matchesCategory = !category || data.category === category;
    const matchesPriority = (data.priority || 0) >= minPriority;
    const matchesPage = !pageUrl || data.pageUrl === pageUrl;
    
    if (matchesQuery && matchesCategory && matchesPriority && matchesPage) {
      results.push({ keyword, ...data });
    }
  });
  
  return results.sort((a, b) => (b.priority || 0) - (a.priority || 0));
}

// 导出处理结果
export function exportProcessingResults() {
  return {
    processedPages: Array.from(PROCESSED_CONTENT_CACHE.keys()),
    keywords: Object.fromEntries(FINANCIAL_KEYWORDS_DB),
    stats: globalContentProcessor.getProcessingStats(),
    exportDate: new Date().toISOString()
  };
} 
 