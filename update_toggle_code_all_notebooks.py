#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新所有 notebook 的 Hide/Show Code 功能（使用标准格式代码）
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

def update_notebook_toggle_code(notebook_path):
    """更新 notebook 的第一个 cell 为新的 toggle code 代码"""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # 检查第一个 cell 是否是 toggle code
        should_update = False
        if nb['cells']:
            first_cell = nb['cells'][0]
            first_cell_source = ''.join(first_cell.get('source', []))
            
            # 如果第一个 cell 是 code 类型且包含 toggleCodeBtn，需要更新
            if first_cell.get('cell_type') == 'code' and 'toggleCodeBtn' in first_cell_source:
                should_update = True
            # 如果第一个 cell 不是 toggle code，需要添加
            elif 'toggleCodeBtn' not in first_cell_source:
                should_update = True
        
        if not should_update and nb['cells']:
            return False, "已是最新版本"
        
        # 创建新的 toggle code cell
        new_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {
                "tags": []
            },
            "outputs": [],
            "source": TOGGLE_CODE_JS.split('\n')
        }
        
        # 如果第一个 cell 已经是 toggle code，替换它；否则插入到第一个位置
        if nb['cells'] and nb['cells'][0].get('cell_type') == 'code':
            first_source = ''.join(nb['cells'][0].get('source', []))
            if 'toggleCodeBtn' in first_source:
                # 替换第一个 cell
                nb['cells'][0] = new_cell
            else:
                # 插入到第一个位置
                nb['cells'].insert(0, new_cell)
        else:
            # 插入到第一个位置
            nb['cells'].insert(0, new_cell)
        
        # 保存 notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        return True, "已更新"
    
    except Exception as e:
        return False, f"错误: {str(e)}"

def main():
    project_root = Path(__file__).parent
    notebooks_dir = project_root / "notebooks"
    
    if not notebooks_dir.exists():
        print(f"❌ notebooks 目录不存在: {notebooks_dir}")
        return 1
    
    # 查找所有 .ipynb 文件（排除 checkpoints）
    notebook_files = [
        f for f in notebooks_dir.rglob("*.ipynb")
        if '.ipynb_checkpoints' not in str(f)
    ]
    
    if not notebook_files:
        print(f"❌ 未找到任何 .ipynb 文件")
        return 1
    
    print(f"📋 找到 {len(notebook_files)} 个 notebook 文件")
    print("🔄 使用标准格式代码更新...")
    print("="*60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for nb_path in sorted(notebook_files):
        relative_path = nb_path.relative_to(project_root)
        success, message = update_notebook_toggle_code(nb_path)
        
        if success:
            if message == "已是最新版本":
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
    print(f"   ✅ 成功更新: {success_count}")
    print(f"   ⏭️  已是最新: {skip_count}")
    print(f"   ❌ 错误: {error_count}")
    print(f"   📦 总计: {len(notebook_files)}")
    
    if success_count > 0:
        print("\n✅ 所有 notebook 已更新为标准格式代码！")
    
    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())

