#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试OpenManus Browser工具
访问东方财富网站
"""
import sys
import asyncio
from pathlib import Path

# 添加OpenManus路径
OPENMANUS_DIR = Path(__file__).parent.parent / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))

async def test_browser_access():
    """测试浏览器工具访问网站"""
    print("=" * 80)
    print("OpenManus Browser工具测试")
    print("=" * 80)
    
    try:
        from app.tool.browser_use_tool import BrowserUseTool
        
        print("\n1. 创建Browser工具...")
        browser = BrowserUseTool()
        print("   ✅ Browser工具创建成功")
        
        print("\n2. 访问东方财富网站...")
        print("   URL: https://www.eastmoney.com")
        
        # 访问网站
        result = await browser.execute(
            action="go_to_url",
            url="https://www.eastmoney.com"
        )
        
        print("\n3. 访问结果:")
        if hasattr(result, 'output'):
            print(f"   输出: {result.output[:200]}...")
        elif isinstance(result, dict):
            print(f"   结果: {result}")
        else:
            print(f"   结果类型: {type(result)}")
            print(f"   结果: {str(result)[:200]}...")
        
        print("\n4. 提取页面标题...")
        # 提取页面内容
        extract_result = await browser.execute(
            action="extract_content",
            goal="获取页面标题和主要新闻标题"
        )
        
        print("\n5. 提取结果:")
        if hasattr(extract_result, 'output') and extract_result.output:
            print(f"   输出: {extract_result.output[:500]}...")
        elif hasattr(extract_result, 'error'):
            print(f"   错误: {extract_result.error}")
            print("   ⚠️  注意: extract_content功能需要LLM API（可选）")
        elif isinstance(extract_result, dict):
            print(f"   结果: {extract_result}")
        else:
            print(f"   结果类型: {type(extract_result)}")
            if extract_result:
                print(f"   结果: {str(extract_result)[:500]}...")
            else:
                print("   ⚠️  结果为空（可能需要LLM API）")
        
        print("\n6. 清理资源...")
        await browser.cleanup()
        print("   ✅ 清理完成")
        
        print("\n" + "=" * 80)
        print("测试完成")
        print("=" * 80)
        print("\n✅ Browser工具测试成功")
        print("\n在Cursor Chat中使用:")
        print('  "使用browser工具访问 https://www.eastmoney.com"')
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n⚠️  注意: 这个测试会启动浏览器，可能需要一些时间...")
    print("按Ctrl+C可以中断测试\n")
    
    try:
        asyncio.run(test_browser_access())
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
    except Exception as e:
        print(f"\n\n测试异常: {e}")
