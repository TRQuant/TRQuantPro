#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
更新MCP配置文件，添加知识库相关服务器
"""

import json
import sys
from pathlib import Path

# 工作目录
OPE_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
MCP_CONFIG_PATH = Path.home() / ".cursor" / "mcp.json"

def load_config():
    """加载现有配置"""
    if MCP_CONFIG_PATH.exists():
        with open(MCP_CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"mcpServers": {}}

def update_config():
    """更新配置，添加知识库服务器"""
    config = load_config()
    servers = config.get("mcpServers", {})
    
    # 添加知识库服务器
    servers["kb-server"] = {
        "command": str(OPE_ROOT / "venv" / "bin" / "python"),
        "args": [
            str(OPE_ROOT / "mcp_servers" / "kb_server.py")
        ],
        "env": {
            "PYTHONIOENCODING": "utf-8",
            "TRQUANT_ROOT": str(OPE_ROOT)
        },
        "description": "📚 知识库服务器 - 策略知识库、API文档、最佳实践"
    }
    
    # 添加统一开发服务器（包含知识库工具）
    servers["unified-dev"] = {
        "command": str(OPE_ROOT / "venv" / "bin" / "python"),
        "args": [
            str(OPE_ROOT / "mcp_servers" / "unified_dev_server.py")
        ],
        "env": {
            "PYTHONIOENCODING": "utf-8",
            "TRQUANT_ROOT": str(OPE_ROOT)
        },
        "description": "🛠️ 统一开发工具服务器 - 任务管理、知识库、工作流 (57个工具)"
    }
    
    # 更新trquant-core和trquant-workflow路径（如果存在）
    if "trquant-core" in servers:
        servers["trquant-core"]["command"] = str(OPE_ROOT / "venv" / "bin" / "python")
        servers["trquant-core"]["args"] = [str(OPE_ROOT / "mcp_servers" / "trquant_core_server.py")]
        servers["trquant-core"]["env"]["TRQUANT_ROOT"] = str(OPE_ROOT)
    
    if "trquant-workflow" in servers:
        servers["trquant-workflow"]["command"] = str(OPE_ROOT / "venv" / "bin" / "python")
        servers["trquant-workflow"]["args"] = [str(OPE_ROOT / "mcp_servers" / "workflow_9steps_server.py")]
        servers["trquant-workflow"]["env"]["TRQUANT_ROOT"] = str(OPE_ROOT)
    
    config["mcpServers"] = servers
    
    return config

def main():
    print("=" * 70)
    print("🔧 更新MCP配置文件")
    print("=" * 70)
    
    # 备份现有配置
    if MCP_CONFIG_PATH.exists():
        backup_path = MCP_CONFIG_PATH.with_suffix('.json.backup')
        import shutil
        shutil.copy2(MCP_CONFIG_PATH, backup_path)
        print(f"✅ 已备份现有配置到: {backup_path}")
    
    # 更新配置
    config = update_config()
    
    # 保存配置
    MCP_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MCP_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 配置已更新: {MCP_CONFIG_PATH}")
    print(f"\n📋 已添加的服务器:")
    print(f"  - kb-server: 知识库服务器")
    print(f"  - unified-dev: 统一开发工具服务器")
    print(f"\n⚠️  请重启Cursor以使配置生效")

if __name__ == '__main__':
    main()
