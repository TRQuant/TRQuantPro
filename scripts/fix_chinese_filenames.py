#!/usr/bin/env python3
"""
修复代码库中的中文文件名，重命名为英文并更新Markdown引用
"""
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CODE_LIBRARY = PROJECT_ROOT / "code_library"
MARKDOWN_DIR = PROJECT_ROOT / "extension/AShare-manual/src/pages/ashare-book6"

# 中文到英文的映射
CHINESE_TO_ENGLISH = {
    # 12.3
    "保存配置": "save_config",
    "加载配置": "load_config",
    "配置方法": "configuration_method",
    
    # 4.4
    "在Python代码中使用": "use_in_python",
    "完整工作流示例": "complete_workflow_example",
    "工具定义": "tool_definition",
    "市场分析": "market_analysis",
    "查询主线识别相关代码": "query_mainline_code",
    "查询主线识别相关文档": "query_mainline_docs",
    "爬取主线分析相关网页": "crawl_mainline_web",
    "知识库查询": "knowledge_base_query",
    "返回结果": "return_result",
    
    # 11.1
    "使用策略生成器": "use_strategy_generator",
    "执行市场分析": "execute_market_analysis",
    "执行策略回测": "execute_strategy_backtest",
    "配置AKShare": "config_akshare",
    "配置JQData": "config_jqdata",
    
    # 11.3
    "执行内容": "execute_content",
}

def find_chinese_filenames():
    """查找所有包含中文的文件名"""
    chinese_files = []
    for root, dirs, files in os.walk(CODE_LIBRARY):
        for file in files:
            if file.endswith('.py') and any('\u4e00' <= char <= '\u9fff' for char in file):
                chinese_files.append(Path(root) / file)
    return chinese_files

def extract_chinese_name(filename):
    """从文件名中提取中文部分"""
    # 匹配 code_X_X_中文部分.py
    match = re.search(r'code_\d+_\d+_(.+)\.py', filename.name)
    if match:
        return match.group(1)
    return None

def translate_to_english(chinese_name):
    """将中文名称翻译为英文"""
    return CHINESE_TO_ENGLISH.get(chinese_name, chinese_name.lower().replace(' ', '_'))

def generate_new_filename(old_path, english_name):
    """生成新的英文文件名"""
    return old_path.parent / f"code_{old_path.stem.split('_')[1]}_{old_path.stem.split('_')[2]}_{english_name}.py"

def update_markdown_references(old_path, new_path):
    """更新Markdown文件中的引用"""
    old_relative = old_path.relative_to(PROJECT_ROOT)
    new_relative = new_path.relative_to(PROJECT_ROOT)
    
    # 查找所有Markdown文件
    for md_file in MARKDOWN_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            if str(old_relative) in content:
                # 替换filePath引用
                content = content.replace(
                    f'filePath="{old_relative}"',
                    f'filePath="{new_relative}"'
                )
                content = content.replace(
                    f'filePath="{old_relative.as_posix()}"',
                    f'filePath="{new_relative.as_posix()}"'
                )
                md_file.write_text(content, encoding='utf-8')
                print(f"  ✅ 更新引用: {md_file.relative_to(PROJECT_ROOT)}")
        except Exception as e:
            print(f"  ⚠️  更新失败 {md_file}: {e}")

def main():
    """主函数"""
    chinese_files = find_chinese_filenames()
    
    if not chinese_files:
        print("✅ 没有找到中文文件名")
        return
    
    print(f"找到 {len(chinese_files)} 个中文文件名，开始修复...\n")
    
    renamed_count = 0
    for old_path in chinese_files:
        chinese_name = extract_chinese_name(old_path)
        if not chinese_name:
            print(f"⚠️  无法提取中文名称: {old_path}")
            continue
        
        english_name = translate_to_english(chinese_name)
        new_path = generate_new_filename(old_path, english_name)
        
        # 检查新文件名是否已存在
        if new_path.exists():
            print(f"⚠️  目标文件已存在: {new_path.name}")
            # 检查内容是否相同
            if old_path.read_bytes() == new_path.read_bytes():
                print(f"  → 内容相同，删除旧文件: {old_path.name}")
                old_path.unlink()
                update_markdown_references(old_path, new_path)
                renamed_count += 1
            else:
                print(f"  → 内容不同，保留旧文件")
            continue
        
        try:
            # 重命名文件
            old_path.rename(new_path)
            print(f"✅ {old_path.name}")
            print(f"   → {new_path.name}")
            
            # 更新Markdown引用
            update_markdown_references(old_path, new_path)
            
            renamed_count += 1
        except Exception as e:
            print(f"❌ 重命名失败 {old_path}: {e}")
    
    print(f"\n✅ 完成！共修复 {renamed_count}/{len(chinese_files)} 个文件")

if __name__ == "__main__":
    main()

