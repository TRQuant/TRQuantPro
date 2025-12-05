// 金融术语API调用测试脚本
import { getTermDefinition, getWikipediaTerm, getMultipleTerms, getCacheStats } from './finance-glossary.js';

// 测试术语列表
const TEST_TERMS = [
  'Bitcoin',
  'Ethereum', 
  'NASDAQ',
  'S&P 500',
  'Federal Reserve',
  'Quantitative Easing',
  'Blockchain',
  'Artificial Intelligence',
  'Machine Learning',
  'Cloud Computing'
];

// 测试单个术语
async function testSingleTerm(term) {
  console.log(`\n🔍 测试术语: ${term}`);
  console.log('='.repeat(50));
  
  try {
    const result = await getTermDefinition(term, {
      preferLocal: false,
      includeWikipedia: true,
      includeInvestopedia: true
    });
    
    if (result) {
      console.log('✅ 获取成功:');
      console.log(`   术语: ${result.term}`);
      console.log(`   全名: ${result.fullName}`);
      console.log(`   分类: ${result.category}`);
      console.log(`   来源: ${result.source || 'local'}`);
      console.log(`   描述: ${result.description.substring(0, 100)}...`);
      if (result.example) {
        console.log(`   示例: ${result.example.substring(0, 80)}...`);
      }
    } else {
      console.log('❌ 未找到定义');
    }
  } catch (error) {
    console.log(`❌ 获取失败: ${error.message}`);
  }
}

// 测试批量获取
async function testBatchTerms() {
  console.log('\n🚀 批量测试术语');
  console.log('='.repeat(50));
  
  try {
    const results = await getMultipleTerms(TEST_TERMS.slice(0, 5), {
      preferLocal: false,
      includeWikipedia: true
    });
    
    console.log(`✅ 批量获取完成，成功获取 ${Object.keys(results).length} 个术语:`);
    
    Object.entries(results).forEach(([term, data]) => {
      console.log(`   • ${term}: ${data.source || 'local'} - ${data.description.substring(0, 60)}...`);
    });
  } catch (error) {
    console.log(`❌ 批量获取失败: ${error.message}`);
  }
}

// 测试缓存功能
function testCache() {
  console.log('\n💾 缓存统计');
  console.log('='.repeat(50));
  
  const stats = getCacheStats();
  console.log(`   总缓存项: ${stats.total}`);
  console.log(`   有效缓存: ${stats.valid}`);
  console.log(`   过期缓存: ${stats.expired}`);
  console.log(`   来源分布:`, stats.sources);
}

// 测试Wikipedia API
async function testWikipediaAPI() {
  console.log('\n🌐 Wikipedia API 测试');
  console.log('='.repeat(50));
  
  const testTerms = ['Bitcoin', 'NASDAQ', 'Federal Reserve'];
  
  for (const term of testTerms) {
    try {
      console.log(`\n🔍 查询: ${term}`);
      const result = await getWikipediaTerm(term);
      
      if (result) {
        console.log(`   ✅ 成功: ${result.fullName}`);
        console.log(`   📝 描述: ${result.description.substring(0, 80)}...`);
        console.log(`   🔗 URL: ${result.url || 'N/A'}`);
      } else {
        console.log(`   ❌ 未找到`);
      }
    } catch (error) {
      console.log(`   ❌ 错误: ${error.message}`);
    }
  }
}

// 性能测试
async function performanceTest() {
  console.log('\n⚡ 性能测试');
  console.log('='.repeat(50));
  
  const startTime = Date.now();
  
  // 测试本地术语
  const localStart = Date.now();
  for (let i = 0; i < 100; i++) {
    getTermDefinition('PE', { preferLocal: true });
  }
  const localTime = Date.now() - localStart;
  
  // 测试API术语（带缓存）
  const apiStart = Date.now();
  await getTermDefinition('Bitcoin', { preferLocal: false });
  const apiTime = Date.now() - apiStart;
  
  const totalTime = Date.now() - startTime;
  
  console.log(`   本地查询 (100次): ${localTime}ms`);
  console.log(`   API查询 (1次): ${apiTime}ms`);
  console.log(`   总耗时: ${totalTime}ms`);
}

// 主测试函数
async function runAllTests() {
  console.log('🎯 金融术语API功能测试开始');
  console.log('='.repeat(60));
  
  // 1. 测试单个术语
  await testSingleTerm('Bitcoin');
  await testSingleTerm('NASDAQ');
  await testSingleTerm('PE'); // 本地术语
  
  // 2. 测试批量获取
  await testBatchTerms();
  
  // 3. 测试Wikipedia API
  await testWikipediaAPI();
  
  // 4. 测试缓存功能
  testCache();
  
  // 5. 性能测试
  await performanceTest();
  
  console.log('\n🎉 所有测试完成');
  console.log('='.repeat(60));
}

// 如果直接运行此脚本
if (typeof window === 'undefined') {
  // Node.js 环境
  runAllTests().catch(console.error);
} else {
  // 浏览器环境
  window.runGlossaryTests = runAllTests;
}

export { runAllTests, testSingleTerm, testBatchTerms, testWikipediaAPI, performanceTest }; 
 