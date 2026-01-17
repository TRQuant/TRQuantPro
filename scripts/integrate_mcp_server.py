#!/usr/bin/env python3
"""
MCP服务器集成脚本

自动为MCP服务器集成新规范（参数验证、trace_id、错误处理）
"""

import sys
import re
from pathlib import Path

def integrate_mcp_server(server_path: str):
    """为MCP服务器集成新规范"""
    server_file = Path(server_path)
    
    if not server_file.exists():
        print(f"❌ 文件不存在: {server_path}")
        return False
    
    with open(server_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已集成
    if "mcp_integration_helper" in content:
        print(f"✅ {server_file.name} 已集成新规范")
        return True
    
    # 添加导入
    import_pattern = r"(from utils\.parameter_validator import|# 导入参数验证器)"
    new_import = """# 导入MCP集成辅助函数
try:
    from utils.mcp_integration_helper import process_mcp_tool_call
    from utils.trace_manager import TraceManager
    from utils.error_handler import ErrorCodes
except ImportError:
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from utils.mcp_integration_helper import process_mcp_tool_call
        from utils.trace_manager import TraceManager
        from utils.error_handler import ErrorCodes
    except ImportError:
        def process_mcp_tool_call(*args, **kwargs):
            raise NotImplementedError("mcp_integration_helper未安装")
"""
    
    if re.search(import_pattern, content):
        content = re.sub(import_pattern, new_import, content, count=1)
        print(f"✅ 已添加导入到 {server_file.name}")
    else:
        # 在文件开头添加导入
        lines = content.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if 'import' in line or 'from' in line:
                insert_pos = i + 1
        lines.insert(insert_pos, new_import)
        content = '\n'.join(lines)
        print(f"✅ 已在文件开头添加导入到 {server_file.name}")
    
    # 保存文件
    with open(server_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {server_file.name} 集成完成")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python integrate_mcp_server.py <server_path>")
        sys.exit(1)
    
    integrate_mcp_server(sys.argv[1])
