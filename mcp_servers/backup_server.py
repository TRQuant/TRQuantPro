#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Backup Server
======================

使用官方Python MCP SDK实现的备份服务器
支持全部备份和essential files备份到data盘

运行方式:
    python mcp_servers/backup_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
"""

import sys
import json
import logging
import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('BackupServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    # 添加utils路径以导入envelope
    from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
    
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError:
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 创建服务器
server = Server("trquant-backup-server")

# 备份目标目录（data盘）
BACKUP_BASE_DIR = Path("/mnt/data/backups/TRQuant")
BACKUP_BASE_DIR.mkdir(parents=True, exist_ok=True)

# Essential files排除模式（可以下载构建的大型文件）
ESSENTIAL_EXCLUDE_PATTERNS = [
    # 依赖和构建产物
    "**/node_modules/**",
    "**/venv/**",
    "**/.venv/**",
    "**/env/**",
    "**/.env/**",
    "**/ENV/**",
    "**/__pycache__/**",
    "**/*.pyc",
    "**/*.pyo",
    "**/*.pyd",
    "**/*.so",
    "**/*.dylib",
    "**/*.dll",
    
    # 构建产物
    "**/dist/**",
    "**/build/**",
    "**/.next/**",
    "**/.nuxt/**",
    "**/.cache/**",
    "**/cache/**",
    "**/.parcel-cache/**",
    
    # 大文件
    "**/.taorui/**",
    "**/*.vsix",
    "**/*.sqlite3",
    "**/*.db",
    "**/*.sqlite",
    
    # 日志和临时文件
    "**/logs/**",
    "**/*.log",
    "**/*.tmp",
    "**/*.temp",
    "**/*.bak",
    "**/*.backup",
    
    # 数据文件（可以重新下载）
    "**/data/**",
    "**/*.csv",
    "**/*.xlsx",
    "**/*.xls",
    "**/*.pkl",
    "**/*.pickle",
    
    # Git相关
    "**/.git/**",
    "**/.gitignore",
    
    # IDE配置
    "**/.idea/**",
    "**/.vscode/**",
    "**/.cursor/**",
    
    # OS文件
    "**/.DS_Store",
    "**/Thumbs.db",
    "**/.directory",
    
    # 回测结果（可以重新生成）
    "**/backtest_results/**",
    "**/results/**",
    
    # 前端构建产物
    "**/extension/AShare-manual/node_modules/**",
    "**/extension/AShare-manual/.astro/**",
    "**/extension/AShare-manual/dist/**",
    "**/frontend/node_modules/**",
    "**/frontend/dist/**",
    "**/frontend/build/**",
    
    # Python包
    "**/site-packages/**",
    "**/pip/**",
    "**/setuptools/**",
]

# 需要备份的essential目录和文件模式
ESSENTIAL_INCLUDE_PATTERNS = [
    "**/*.py",
    "**/*.js",
    "**/*.ts",
    "**/*.tsx",
    "**/*.jsx",
    "**/*.json",
    "**/*.md",
    "**/*.txt",
    "**/*.yml",
    "**/*.yaml",
    "**/*.toml",
    "**/*.ini",
    "**/*.cfg",
    "**/*.conf",
    "**/*.sh",
    "**/*.ps1",
    "**/*.bat",
    "**/*.mjs",
    "**/*.astro",
    "**/*.css",
    "**/*.html",
    "**/*.xml",
    "**/*.sql",
    "**/*.mermaid",
    "**/*.mmd",
    "**/package.json",
    "**/package-lock.json",
    "**/requirements.txt",
    "**/pyproject.toml",
    "**/Pipfile",
    "**/Pipfile.lock",
    "**/poetry.lock",
    "**/tsconfig.json",
    "**/astro.config.mjs",
    "**/vite.config.*",
    "**/webpack.config.*",
    "**/.gitignore",
    "**/.gitattributes",
    "**/README*",
    "**/LICENSE*",
    "**/CHANGELOG*",
    "**/CONTRIBUTING*",
    "**/CODE_OF_CONDUCT*",
]


def should_exclude_essential(path: Path, root: Path) -> bool:
    """检查路径是否应该被essential备份排除"""
    rel_path = path.relative_to(root)
    path_str = str(rel_path).replace("\\", "/")
    
    # 检查排除模式
    for pattern in ESSENTIAL_EXCLUDE_PATTERNS:
        if path.match(pattern):
            return True
    
    # 对于essential备份，只包含特定类型的文件
    if path.is_file():
        # 检查是否匹配包含模式
        for pattern in ESSENTIAL_INCLUDE_PATTERNS:
            if path.match(pattern):
                return False
        # 如果不匹配任何包含模式，排除
        return True
    
    return False


def should_exclude_full(path: Path, root: Path) -> bool:
    """检查路径是否应该被全部备份排除（只排除明显不需要的）"""
    rel_path = path.relative_to(root)
    path_str = str(rel_path).replace("\\", "/")
    
    # 只排除明显不需要的
    exclude_patterns = [
        "**/.git/**",
        "**/__pycache__/**",
        "**/*.pyc",
        "**/*.pyo",
        "**/.DS_Store",
        "**/Thumbs.db",
    ]
    
    for pattern in exclude_patterns:
        if path.match(pattern):
            return True
    
    return False


def create_backup(source_dir: Path, backup_type: str = "full") -> Dict[str, Any]:
    """创建备份"""
    try:
        # 生成备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"TRQuant_{backup_type}_{timestamp}"
        backup_dir = BACKUP_BASE_DIR / backup_name
        backup_archive = BACKUP_BASE_DIR / f"{backup_name}.tar.gz"
        
        logger.info(f"开始创建{backup_type}备份: {backup_name}")
        logger.info(f"源目录: {source_dir}")
        logger.info(f"备份目录: {backup_dir}")
        logger.info(f"备份归档: {backup_archive}")
        
        # 创建备份目录
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # 统计信息
        files_copied = 0
        files_skipped = 0
        total_size = 0
        
        # 选择排除函数
        exclude_func = should_exclude_essential if backup_type == "essential" else should_exclude_full
        
        # 复制文件
        for root, dirs, files in source_dir.rglob("*"):
            root_path = Path(root)
            
            # 过滤目录
            dirs[:] = [d for d in dirs if not exclude_func(root_path / d, source_dir)]
            
            for file in files:
                file_path = root_path / file
                
                # 检查是否应该排除
                if exclude_func(file_path, source_dir):
                    files_skipped += 1
                    continue
                
                # 计算相对路径
                rel_path = file_path.relative_to(source_dir)
                dest_path = backup_dir / rel_path
                
                # 创建目标目录
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # 复制文件
                try:
                    shutil.copy2(file_path, dest_path)
                    files_copied += 1
                    total_size += file_path.stat().st_size
                except Exception as e:
                    logger.warning(f"复制文件失败: {file_path}, 错误: {e}")
                    files_skipped += 1
        
        # 创建tar.gz归档
        logger.info("创建tar.gz归档...")
        with tarfile.open(backup_archive, "w:gz") as tar:
            tar.add(backup_dir, arcname=backup_name)
        
        # 删除临时目录
        shutil.rmtree(backup_dir)
        
        # 计算归档大小
        archive_size = backup_archive.stat().st_size
        
        result = {
            "backup_name": backup_name,
            "backup_type": backup_type,
            "backup_path": str(backup_archive),
            "files_copied": files_copied,
            "files_skipped": files_skipped,
            "total_size_bytes": total_size,
            "archive_size_bytes": archive_size,
            "archive_size_mb": round(archive_size / (1024 * 1024), 2),
            "timestamp": timestamp,
            "source_dir": str(source_dir),
        }
        
        logger.info(f"备份完成: {backup_name}")
        logger.info(f"文件数: {files_copied} 复制, {files_skipped} 跳过")
        logger.info(f"归档大小: {result['archive_size_mb']} MB")
        
        return result
        
    except Exception as e:
        logger.error(f"创建备份失败: {e}", exc_info=True)
        raise


def list_backups() -> List[Dict[str, Any]]:
    """列出所有备份"""
    backups = []
    
    if not BACKUP_BASE_DIR.exists():
        return backups
    
    for backup_file in BACKUP_BASE_DIR.glob("TRQuant_*.tar.gz"):
        try:
            stat = backup_file.stat()
            backups.append({
                "name": backup_file.name,
                "path": str(backup_file),
                "size_bytes": stat.st_size,
                "size_mb": round(stat.st_size / (1024 * 1024), 2),
                "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
        except Exception as e:
            logger.warning(f"读取备份信息失败: {backup_file}, 错误: {e}")
    
    # 按创建时间排序（最新的在前）
    backups.sort(key=lambda x: x["created"], reverse=True)
    
    return backups


# 注册工具
@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="backup_full",
            description="创建完整备份到data盘，包含所有文件（排除.git等明显不需要的）",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_dir": {
                        "type": "string",
                        "description": "要备份的源目录路径（默认：项目根目录）",
                        "default": str(TRQUANT_ROOT)
                    }
                }
            }
        ),
        Tool(
            name="backup_essential",
            description="创建essential files备份到data盘，只备份源代码和配置文件，排除node_modules、venv、.taorui等可重新构建的文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_dir": {
                        "type": "string",
                        "description": "要备份的源目录路径（默认：项目根目录）",
                        "default": str(TRQUANT_ROOT)
                    }
                }
            }
        ),
        Tool(
            name="list_backups",
            description="列出data盘上的所有备份",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="delete_backup",
            description="删除指定的备份文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "backup_name": {
                        "type": "string",
                        "description": "要删除的备份文件名（完整名称或部分匹配）"
                    }
                },
                "required": ["backup_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        if name == "backup_full":
            source_dir = Path(arguments.get("source_dir", str(TRQUANT_ROOT)))
            if not source_dir.exists():
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": f"源目录不存在: {source_dir}"
                    }, ensure_ascii=False, indent=2)
                )]
            
            result = create_backup(source_dir, backup_type="full")
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "result": result
                }, ensure_ascii=False, indent=2)
            )]
        
        elif name == "backup_essential":
            source_dir = Path(arguments.get("source_dir", str(TRQUANT_ROOT)))
            if not source_dir.exists():
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": f"源目录不存在: {source_dir}"
                    }, ensure_ascii=False, indent=2)
                )]
            
            result = create_backup(source_dir, backup_type="essential")
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "result": result
                }, ensure_ascii=False, indent=2)
            )]
        
        elif name == "list_backups":
            backups = list_backups()
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "count": len(backups),
                    "backups": backups
                }, ensure_ascii=False, indent=2)
            )]
        
        elif name == "delete_backup":
            backup_name = arguments.get("backup_name")
            if not backup_name:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": "backup_name参数必需"
                    }, ensure_ascii=False, indent=2)
                )]
            
            # 查找匹配的备份文件
            backup_files = list(BACKUP_BASE_DIR.glob(f"*{backup_name}*"))
            
            if not backup_files:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "success": False,
                        "error": f"未找到匹配的备份: {backup_name}"
                    }, ensure_ascii=False, indent=2)
                )]
            
            deleted = []
            for backup_file in backup_files:
                try:
                    backup_file.unlink()
                    deleted.append(str(backup_file))
                except Exception as e:
                    logger.error(f"删除备份失败: {backup_file}, 错误: {e}")
            
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": True,
                    "deleted": deleted,
                    "count": len(deleted)
                }, ensure_ascii=False, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "success": False,
                    "error": f"未知工具: {name}"
                }, ensure_ascii=False, indent=2)
            )]
    
    except Exception as e:
        logger.error(f"工具调用失败: {name}, 错误: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e)
            }, ensure_ascii=False, indent=2)
        )]


# 主函数
async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

