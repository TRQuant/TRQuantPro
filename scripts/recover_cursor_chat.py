#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cursor聊天记录恢复工具
====================

尝试从各种可能的存储位置恢复Cursor聊天记录
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))


def check_leveldb():
    """检查LevelDB数据库"""
    try:
        import plyvel
        db_path = Path.home() / '.config' / 'Cursor' / 'Local Storage' / 'leveldb'
        if not db_path.exists():
            return []
        
        db = plyvel.DB(str(db_path), create_if_missing=False)
        results = []
        
        # 搜索可能包含聊天记录的关键字
        keywords = ['chat', 'conversation', 'message', 'claude', 'cursor', 'assistant', 'user']
        
        for key, value in db:
            try:
                key_str = key.decode('utf-8', errors='ignore')
                value_str = value.decode('utf-8', errors='ignore')
                
                # 检查是否包含关键字
                if any(keyword in key_str.lower() or keyword in value_str.lower() for keyword in keywords):
                    results.append({
                        'key': key_str,
                        'value': value_str[:1000],  # 限制长度
                        'type': 'leveldb'
                    })
            except:
                continue
        
        db.close()
        return results
    except ImportError:
        print("⚠️  plyvel未安装，无法读取LevelDB")
        print("   安装方法: pip install plyvel")
        return []
    except Exception as e:
        print(f"❌ LevelDB读取失败: {e}")
        return []


def check_sqlite():
    """检查SQLite数据库"""
    results = []
    workspace_storage = Path.home() / '.config' / 'Cursor' / 'User' / 'workspaceStorage'
    
    if not workspace_storage.exists():
        return results
    
    try:
        import sqlite3
    except ImportError:
        return results
    
    for db_file in workspace_storage.rglob('*.db'):
        try:
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            
            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            for table in tables:
                table_name = table[0]
                try:
                    # 检查表结构
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    # 检查是否可能包含聊天记录
                    column_names = [col[1] for col in columns]
                    if any(keyword in str(column_names).lower() for keyword in ['chat', 'message', 'conversation', 'content', 'text']):
                        cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
                        rows = cursor.fetchall()
                        results.append({
                            'file': str(db_file),
                            'table': table_name,
                            'columns': column_names,
                            'rows': len(rows),
                            'sample': rows[:3] if rows else []
                        })
                except:
                    continue
            
            conn.close()
        except Exception as e:
            continue
    
    return results


def check_logs():
    """检查日志文件"""
    results = []
    log_dir = Path.home() / '.config' / 'Cursor' / 'logs'
    
    if not log_dir.exists():
        return results
    
    keywords = ['chat', 'conversation', 'message', 'claude', 'assistant', 'user']
    
    for log_file in log_dir.rglob('*.log'):
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if any(keyword in content.lower() for keyword in keywords):
                    # 提取相关行
                    lines = content.split('\n')
                    relevant_lines = [line for line in lines if any(keyword in line.lower() for keyword in keywords)]
                    if relevant_lines:
                        results.append({
                            'file': str(log_file),
                            'relevant_lines': relevant_lines[:20]  # 限制行数
                        })
        except:
            continue
    
    return results


def main():
    """主函数"""
    print("=" * 70)
    print("🔍 Cursor聊天记录恢复工具")
    print("=" * 70)
    print()
    
    all_results = {
        'timestamp': datetime.now().isoformat(),
        'leveldb_results': [],
        'sqlite_results': [],
        'log_results': []
    }
    
    # 检查LevelDB
    print("📋 检查LevelDB数据库...")
    leveldb_results = check_leveldb()
    all_results['leveldb_results'] = leveldb_results
    if leveldb_results:
        print(f"   ✅ 找到 {len(leveldb_results)} 条可能相关的记录")
    else:
        print("   ❌ 未找到相关记录")
    print()
    
    # 检查SQLite
    print("📋 检查SQLite数据库...")
    sqlite_results = check_sqlite()
    all_results['sqlite_results'] = sqlite_results
    if sqlite_results:
        print(f"   ✅ 找到 {len(sqlite_results)} 个可能相关的数据库")
        for result in sqlite_results[:5]:
            print(f"   - {Path(result['file']).name}: {result['table']}")
    else:
        print("   ❌ 未找到相关数据库")
    print()
    
    # 检查日志文件
    print("📋 检查日志文件...")
    log_results = check_logs()
    all_results['log_results'] = log_results
    if log_results:
        print(f"   ✅ 找到 {len(log_results)} 个可能相关的日志文件")
    else:
        print("   ❌ 未找到相关日志")
    print()
    
    # 保存结果
    output_file = Path.home() / '.cursor' / 'chat_recovery_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"💾 结果已保存到: {output_file}")
    print()
    
    # 总结
    total_found = len(leveldb_results) + len(sqlite_results) + len(log_results)
    if total_found > 0:
        print("=" * 70)
        print(f"✅ 找到 {total_found} 条可能相关的记录")
        print("=" * 70)
    else:
        print("=" * 70)
        print("❌ 未找到聊天记录")
        print("=" * 70)
        print()
        print("💡 建议:")
        print("   1. 检查Cursor是否登录了账户，聊天记录可能在云端")
        print("   2. 重要对话应该立即保存到项目文档")
        print("   3. 使用项目文档记录关键决策和进度")
        print("   4. 定期备份重要信息")


if __name__ == '__main__':
    main()
