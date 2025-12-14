"""
文件名: code_10_7_test_tool.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_test_tool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: test_tool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 启用详细日志
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('MCP')

# 测试工具调用
async def test_tool():
    server = MCPServer()
    result = await server.call_tool(
        "trquant_market_status",
        {"universe": "CN_EQ"}
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))