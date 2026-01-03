"""
基础功能测试
不依赖网络连接
"""
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
# Also add extension directory for imports
extension_dir = project_root / "extension"
if extension_dir.exists():
    sys.path.insert(0, str(extension_dir))

def test_imports():
    """测试导入"""
    print("测试导入...")
    try:
        from tools.data_collector import WebCrawler, PDFDownloader, AcademicScraper, SourceRecommender
        print("✅ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_source_recommender():
    """测试信息源推荐器（不需要网络）"""
    print("\n测试信息源推荐器...")
    try:
        from tools.data_collector import SourceRecommender
        
        recommender = SourceRecommender()
        
        # 测试推荐
        sources = recommender.recommend(
            keywords=["量化投资", "策略开发"],
            min_quality=7.0
        )
        
        print(f"✅ 推荐了 {len(sources)} 个信息源")
        for src in sources[:3]:  # 显示前3个
            print(f"   - {src.name} ({src.type})")
        
        # 测试列出所有信息源
        all_sources = recommender.list_all_sources()
        print(f"✅ 共有 {len(all_sources)} 个信息源")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_academic_scraper_list():
    """测试学术爬虫列表功能（不需要网络）"""
    print("\n测试学术爬虫列表功能...")
    try:
        from tools.data_collector import AcademicScraper
        
        scraper = AcademicScraper(output_dir=Path("/tmp"))
        databases = scraper.list_databases()
        
        print(f"✅ 支持的数据库:")
        for name, info in databases.items():
            print(f"   - {name}: {info['description']} ({'免费' if info['free'] else '付费'})")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("=" * 50)
    print("数据收集工具基础功能测试")
    print("=" * 50)
    
    results = []
    
    # 测试导入
    results.append(("导入测试", test_imports()))
    
    # 测试信息源推荐器
    results.append(("信息源推荐器", test_source_recommender()))
    
    # 测试学术爬虫列表
    results.append(("学术爬虫列表", test_academic_scraper_list()))
    
    # 总结
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print("=" * 50)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 所有基础测试通过！")
    else:
        print("\n⚠️ 部分测试失败，请检查依赖安装")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

