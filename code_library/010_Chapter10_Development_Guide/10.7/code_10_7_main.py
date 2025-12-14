"""
文件名: code_10_7_main.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_main.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: main

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

async def main():
        """
    main函数
    
    **设计原理**：
    - **核心功能**：实现main的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    logger.info("TRQuant MCP Server 启动...")
    server = MCPServer()
    
    # 使用stdio通信
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)
    
    writer_transport, writer_protocol = await asyncio.get_event_loop().connect_write_pipe(
        asyncio.streams.FlowControlMixin, sys.stdout
    )
    writer = asyncio.StreamWriter(writer_transport, writer_protocol, reader, asyncio.get_event_loop())
    
    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            
            request = json.loads(line.decode('utf-8'))
            response = await handle_request(request, server)
            
            if response:
                response_str = json.dumps(response, ensure_ascii=False) + '\n'
                writer.write(response_str.encode('utf-8'))
                await writer.drain()
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
        except Exception as e:
            logger.error(f"处理请求错误: {e}")

if __name__ == "__main__":
    asyncio.run(main())