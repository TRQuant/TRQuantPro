"""
数据收集工具使用示例
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tools.data_collector import WebCrawler, PDFDownloader, AcademicScraper, SourceRecommender


def example_web_crawler():
    """示例：爬取网页"""
    print("=== 网页爬虫示例 ===")
    
    crawler = WebCrawler(
        output_dir=Path("data/collected/web"),
        delay_range=(1, 2),
        respect_robots=True
    )
    
    files = crawler.collect(
        url="https://www.joinquant.com/help",
        max_depth=2,
        allowed_domains=["www.joinquant.com"]
    )
    
    print(f"下载了 {len(files)} 个文件")
    for f in files[:5]:  # 只显示前5个
        print(f"  - {f}")


def example_pdf_downloader():
    """示例：下载PDF"""
    print("\n=== PDF下载器示例 ===")
    
    downloader = PDFDownloader(output_dir=Path("data/collected/pdfs"))
    
    # 示例PDF URL（需要替换为实际URL）
    pdf_url = "https://arxiv.org/pdf/2301.00001.pdf"
    files = downloader.collect(pdf_url, filename="example_paper.pdf")
    
    print(f"下载了 {len(files)} 个PDF文件")
    for f in files:
        print(f"  - {f}")


def example_academic_scraper():
    """示例：从arXiv下载论文"""
    print("\n=== 学术论文下载示例 ===")
    
    scraper = AcademicScraper(output_dir=Path("data/collected/papers"))
    
    files = scraper.collect(
        database="arxiv",
        query="quantitative+trading+OR+algorithmic+trading",
        max_results=10
    )
    
    print(f"下载了 {len(files)} 个文件")
    for f in files[:5]:  # 只显示前5个
        print(f"  - {f}")
    
    # 列出支持的数据库
    print("\n支持的数据库:")
    databases = scraper.list_databases()
    for name, info in databases.items():
        print(f"  - {name}: {info['description']}")


def example_source_recommender():
    """示例：信息源推荐"""
    print("\n=== 信息源推荐示例 ===")
    
    recommender = SourceRecommender()
    
    sources = recommender.recommend(
        keywords=["量化投资", "策略开发", "回测"],
        source_type="documentation",
        min_quality=7.0,
        language="zh"
    )
    
    print(f"推荐了 {len(sources)} 个信息源:")
    for src in sources:
        print(f"  - {src.name} ({src.type})")
        print(f"    URL: {src.url}")
        print(f"    质量分数: {src.quality_score}")
        print(f"    访问方式: {src.access_method}")
        print()


if __name__ == "__main__":
    print("数据收集工具使用示例\n")
    
    # 运行示例
    try:
        example_source_recommender()
        # example_web_crawler()  # 需要网络连接
        # example_pdf_downloader()  # 需要网络连接
        # example_academic_scraper()  # 需要网络连接
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()

