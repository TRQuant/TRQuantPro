#!/usr/bin/env python3
"""将已爬取的JQData文档存入知识库"""
import sys, json
from pathlib import Path
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

def format_kb_content(doc):
    """格式化文档为知识库内容"""
    content = f"""JQData API文档: {doc['title']}

来源URL: {doc['url']}

"""
    
    doc_content = doc.get('content', '')
    
    if len(doc_content) > 5000:
        content += f"主要内容:\n{doc_content[:5000]}...\n\n(内容已截断，完整内容请查看文档文件)"
    else:
        content += f"主要内容:\n{doc_content}\n"
    
    return content

def main():
    output_dir = Path('/home/taotao/dev/QuantTest/TRQuant/docs/jqdata_crawled')
    
    # 读取所有批次结果
    all_docs = []
    batch_files = sorted(output_dir.glob('batch_*.json'))
    
    print(f"找到 {len(batch_files)} 个批次文件")
    
    for batch_file in batch_files:
        with open(batch_file, 'r', encoding='utf-8') as f:
            batch_docs = json.load(f)
            all_docs.extend(batch_docs)
    
    success_docs = [d for d in all_docs if d.get('status') == 'success']
    print(f"总共 {len(all_docs)} 个文档")
    print(f"成功: {len(success_docs)} 个")
    print()
    
    # 格式化知识库内容
    print("格式化知识库内容...")
    kb_items = []
    
    for doc in success_docs:
        kb_content = format_kb_content(doc)
        kb_item = {
            'title': f"JQData API: {doc['title']}",
            'content': kb_content,
            'url': doc['url'],
            'index': doc.get('index', 0),
            'original_title': doc['title']
        }
        kb_items.append(kb_item)
    
    # 保存知识库格式文件
    kb_file = output_dir / 'kb_all_items.json'
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb_items, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(kb_items)} 个文档已格式化")
    print(f"   知识库格式文件: {kb_file}")
    print()
    print("=" * 70)
    print("准备存入知识库...")
    print("=" * 70)
    print()
    print("提示: 由于文档数量较多，建议分批存入知识库")
    print("可以使用以下命令逐个存入:")
    print()
    for i, item in enumerate(kb_items[:10], 1):
        print(f"{i}. {item['title'][:60]}")

if __name__ == "__main__":
    main()
