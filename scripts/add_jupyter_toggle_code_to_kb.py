#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 Jupyter Hide/Show Code 功能文档添加到知识库
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    KB_AVAILABLE = False
    print("⚠️  知识库模块未找到，将使用模拟模式")

def add_jupyter_toggle_code_to_kb():
    """将 Jupyter Hide/Show Code 文档添加到知识库"""
    
    # 读取文档内容
    doc_path = TRQUANT_ROOT / "docs" / "JUPYTER_HIDE_SHOW_CODE_FEATURE.md"
    if not doc_path.exists():
        print(f"❌ 文档不存在: {doc_path}")
        return False
    
    content = doc_path.read_text(encoding='utf-8')
    
    # 构建知识库条目
    title = "Jupyter Notebook Hide/Show Code 功能使用指南"
    
    # 添加重要的使用限制说明到内容开头
    enhanced_content = f"""# {title}

## ⚠️ 重要限制说明

### 仅支持浏览器版本的 Jupyter Notebook

- ✅ **浏览器 Jupyter Notebook**：功能完全正常
  - 通过 `http://localhost:8888` 访问
  - 使用 miniconda 环境的 Python kernel
  - JavaScript 代码可以正常执行
  
- ❌ **Cursor 内置 Notebook**：功能不可用
  - Cursor 的 notebook 界面不支持 `%%javascript` 魔法命令
  - JavaScript 代码无法在 Cursor 界面中执行
  - 需要使用浏览器版本的 Jupyter Notebook

---

{content}
"""
    
    tags = [
        "Jupyter Notebook",
        "JavaScript",
        "Notebook增强",
        "开发工具",
        "浏览器Jupyter",
        "miniconda",
        "Hide/Show Code",
        "代码隐藏",
        "Notebook展示"
    ]
    
    if not KB_AVAILABLE:
        print("📝 知识库模块不可用，将输出内容预览：")
        print("="*60)
        print(f"标题: {title}")
        print(f"标签: {', '.join(tags)}")
        print(f"内容长度: {len(enhanced_content)} 字符")
        print("\n内容预览（前500字符）:")
        print(enhanced_content[:500])
        print("\n⚠️  请手动添加到知识库或确保知识库模块可用")
        return False
    
    try:
        result = knowledge_add(
            title=title,
            content=enhanced_content,
            type="development_guide",
            tags=tags,
            source=str(doc_path.relative_to(TRQUANT_ROOT))
        )
        
        if result.get('success') or result.get('id') or result.get('knowledge_id'):
            kb_id = result.get('knowledge_id') or result.get('id') or 'unknown'
            print(f"✅ 成功添加到知识库 (ID: {kb_id})")
            print(f"   标题: {title}")
            print(f"   标签: {', '.join(tags)}")
            print(f"   来源: {doc_path.relative_to(TRQUANT_ROOT)}")
            return True
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"❌ 添加到知识库失败: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ 添加到知识库异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*60)
    print("📚 添加 Jupyter Hide/Show Code 文档到知识库")
    print("="*60)
    print()
    
    success = add_jupyter_toggle_code_to_kb()
    
    print()
    print("="*60)
    if success:
        print("✅ 添加完成")
    else:
        print("⚠️  添加失败或跳过")
    print("="*60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

