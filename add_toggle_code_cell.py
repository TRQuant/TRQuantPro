#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在所有 notebook 的第一个 cell 添加 Hide/Show Code 功能
"""

import json
import sys
from pathlib import Path

TOGGLE_CODE_JS = """%%javascript
(() => {
  // 只隐藏编辑器，不隐藏 cell 的 toolbar / prompt
  const selectors = ['.jp-InputArea-editor', '.cm-editor', '.CodeMirror'];

  // 找到当前 Notebook 使用的编辑器 DOM（优先匹配第一个存在的 selector）
  function getEditors() {
    for (const s of selectors) {
      const nodes = document.querySelectorAll(s);
      if (nodes.length) return { sel: s, nodes };
    }
    return { sel: null, nodes: [] };
  }

  // 切换显示/隐藏
  function toggle() {
    const { sel, nodes } = getEditors();
    if (!nodes.length) return alert('没找到编辑器区域：' + selectors.join(' / '));

    const hide = nodes[0].style.display !== 'none';
    nodes.forEach(n => n.style.display = hide ? 'none' : '');

    // 仅用于调试：输出当前使用的 selector
    console.log("toggle selector:", sel);
  }

  // 创建右上角按钮（避免重复创建）
  let btn = document.getElementById('toggleCodeBtn');
  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'toggleCodeBtn';
    btn.textContent = 'Hide/Show Code';
    btn.style.cssText =
      'position:fixed;top:12px;right:12px;z-index:99999;padding:6px 12px;border-radius:6px;';
    btn.addEventListener('click', toggle);
    document.body.appendChild(btn);
  }

  // 默认隐藏编辑器（只隐藏代码，不影响按钮/工具栏/输出）
  const { nodes } = getEditors();
  nodes.forEach(n => n.style.display = 'none');
})();"""

def add_toggle_code_to_notebook(notebook_path):
    """在 notebook 的第一个 cell 添加 toggle code 代码"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # 检查第一个 cell 是否已经有这个代码
        if nb['cells']:
            first_cell_source = ''.join(nb['cells'][0].get('source', []))
            if 'toggleCodeBtn' in first_cell_source or 'Hide/Show Code' in first_cell_source:
                return False, "已存在"
        
        # 创建新的 code cell 作为第一个 cell
        new_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {
                "tags": []
            },
            "outputs": [],
            "source": TOGGLE_CODE_JS.split('\n')
        }
        
        # 插入到第一个位置
        nb['cells'].insert(0, new_cell)
        
        # 保存 notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        return True, "已添加"
    
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    project_root = Path(__file__).parent
    notebooks_dir = project_root / "notebooks"
    
    if not notebooks_dir.exists():
        print(f"❌ notebooks 目录不存在: {notebooks_dir}")
        return 1
    
    # 查找所有 .ipynb 文件
    notebook_files = list(notebooks_dir.rglob("*.ipynb"))
    
    if not notebook_files:
        print(f"❌ 未找到任何 .ipynb 文件")
        return 1
    
    print(f"📋 找到 {len(notebook_files)} 个 notebook 文件")
    print("="*60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for nb_path in sorted(notebook_files):
        relative_path = nb_path.relative_to(project_root)
        success, message = add_toggle_code_to_notebook(nb_path)
        
        if success:
            if message == "已存在":
                print(f"⏭️  {relative_path} - {message}")
                skip_count += 1
            else:
                print(f"✅ {relative_path} - {message}")
                success_count += 1
        else:
            print(f"❌ {relative_path} - {message}")
            error_count += 1
    
    print("="*60)
    print(f"\n📊 统计:")
    print(f"   ✅ 成功添加: {success_count}")
    print(f"   ⏭️  已存在: {skip_count}")
    print(f"   ❌ 错误: {error_count}")
    print(f"   📦 总计: {len(notebook_files)}")
    
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

