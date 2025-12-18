"""
文件名: code_5_4_complete_workflow_example.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.4/code_5_4_complete_workflow_example.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: 完整工作流示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 查询相关知识库
knowledge = client.call_tool(
    "kb.query",
    {
        "query": "候选池构建 股票池管理 筛选规则 股票评分",
        "collection": "both",
        "top_k": 5
    }
)

# 2. 如果知识库结果不足，收集外部资料
if len(knowledge) < 3:
    external_data = client.call_tool(
        "data_collector.crawl_web",
        {
            "url": "https://example.com/candidate-pool-construction",
            "extract_text": True
        }
    )

# 3. 基于知识库结果构建候选池
from core.candidate_pool_builder import CandidatePoolBuilder

builder = CandidatePoolBuilder()

# 从主线构建候选池
mainline_name = "AI算力基础设施"
pool = builder.build_from_mainline(
    mainline_name=mainline_name,
    mainline_type="concept"
)

# 4. 对候选股票进行评分
from core.stock_scorer import StockScorer

scorer = StockScorer()
for stock in pool.stocks:
    score_result = scorer.score_stock(
        stock_code=stock.code,
        # ... 其他参数
    )
    stock.composite_score = score_result['composite_score']