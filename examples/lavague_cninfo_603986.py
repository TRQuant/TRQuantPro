#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
使用LaVague从巨潮资讯网提取股票公告
====================================

任务: 访问巨潮资讯网，搜索股票代码603986，提取最近90天的所有公告

运行方式:
    cd /home/taotao/.cursor/worktrees/TRQuant/ope
    ./venv/bin/python examples/lavague_cninfo_603986.py
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler


def extract_announcements_603986():
    """提取603986最近90天的公告"""
    
    stock_code = "603986"
    days = 90
    
    print("=" * 80)
    print(f"使用LaVague提取股票 {stock_code} 的公告")
    print("=" * 80)
    print()
    print(f"股票代码: {stock_code}")
    print(f"时间范围: 最近 {days} 天")
    print(f"数据源: 巨潮资讯网 (http://www.cninfo.com.cn)")
    print()
    
    # 创建LaVague爬虫实例
    try:
        crawler = get_lavague_crawler(headless=True)
        
        if not crawler.engine:
            print("❌ LaVague未正确安装或初始化失败")
            print()
            print("请检查:")
            print("1. 是否已安装: ./venv/bin/python -m pip install lavague")
            print("2. 是否配置了OPENAI_API_KEY环境变量")
            print("3. 查看错误日志了解详情")
            return
        
        print("✅ LaVague引擎初始化成功")
        print()
        
        # 执行指令
        print("【步骤1】访问巨潮资讯网")
        print("-" * 80)
        
        instruction = f"""
        访问巨潮资讯网（http://www.cninfo.com.cn），
        搜索股票代码{stock_code}，
        进入公告页面，提取最近{days}天的所有公告。
        
        需要提取的信息包括：
        1. 公告标题
        2. 发布日期
        3. 公告类型（年报、季报、重大事项等）
        4. 公告链接（如果有）
        5. 公告摘要（如果有）
        
        请将所有公告整理为结构化数据，格式如下：
        {{
            "stock_code": "{stock_code}",
            "period_days": {days},
            "announcements": [
                {{
                    "title": "公告标题",
                    "publish_date": "YYYY-MM-DD",
                    "announcement_type": "公告类型",
                    "url": "公告链接",
                    "summary": "公告摘要"
                }},
                ...
            ],
            "total_count": 公告总数
        }}
        """
        
        print(f"执行指令: 搜索{stock_code}，提取最近{days}天的公告...")
        print()
        
        result = crawler.execute_instruction(instruction, max_actions=20)
        
        print()
        print("【步骤2】处理结果")
        print("-" * 80)
        
        if result.get("success"):
            print("✅ 指令执行成功")
            print()
            print(f"当前页面: {result.get('current_url', 'N/A')}")
            print(f"页面标题: {result.get('title', 'N/A')}")
            print(f"页面长度: {result.get('page_length', 0)} 字符")
            print(f"执行动作数: {result.get('actions_executed', 0)}")
            print()
            
            # 显示结果摘要
            result_text = result.get("result", "")
            if result_text:
                print("执行结果摘要:")
                print("-" * 80)
                # 显示前500字符
                preview = result_text[:500] if len(result_text) > 500 else result_text
                print(preview)
                if len(result_text) > 500:
                    print("...")
                print()
            
            # 保存结果
            output_file = TRQUANT_ROOT / "examples" / f"announcements_{stock_code}_{days}days.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            output_data = {
                "extraction_time": datetime.now().isoformat(),
                "stock_code": stock_code,
                "period_days": days,
                "source": "cninfo",
                "result": result,
                "raw_result": result_text
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 结果已保存到: {output_file}")
            print()
            
            # 尝试提取结构化数据
            print("【步骤3】提取结构化数据")
            print("-" * 80)
            
            extract_description = f"""
            从当前页面提取股票{stock_code}的公告数据，
            包括所有公告的标题、日期、类型、链接等信息。
            将数据整理为JSON格式。
            """
            
            extract_result = crawler.extract_data(extract_description)
            
            if extract_result.get("success"):
                print("✅ 数据提取成功")
                print(f"   提取的数据长度: {extract_result.get('page_source_length', 0)} 字符")
                
                # 保存提取的数据
                extract_output_file = TRQUANT_ROOT / "examples" / f"announcements_{stock_code}_extracted.json"
                extract_data = {
                    "extraction_time": datetime.now().isoformat(),
                    "stock_code": stock_code,
                    "period_days": days,
                    "extracted_data": extract_result.get("data", ""),
                    "page_source_length": extract_result.get("page_source_length", 0)
                }
                
                with open(extract_output_file, 'w', encoding='utf-8') as f:
                    json.dump(extract_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 提取的数据已保存到: {extract_output_file}")
            else:
                print(f"⚠️  数据提取失败: {extract_result.get('error')}")
                print("   但执行结果已保存，可以手动解析")
            
        else:
            print("❌ 指令执行失败")
            print(f"   错误: {result.get('error', '未知错误')}")
            print()
            print("可能的原因:")
            print("1. 网站访问失败（网络问题或网站限制）")
            print("2. 页面结构变化，LaVague无法识别")
            print("3. 需要登录或验证码")
            print("4. API调用失败（检查OPENAI_API_KEY）")
        
        # 关闭爬虫
        crawler.close()
        print()
        print("✅ LaVague引擎已关闭")
        
    except Exception as e:
        print(f"❌ 发生异常: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 80)
    print("任务完成")
    print("=" * 80)


if __name__ == "__main__":
    extract_announcements_603986()
