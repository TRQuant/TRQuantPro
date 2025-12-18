"""
文件名: code_7_2___init__.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.2/code_7_2___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.2_Strategy_Generation_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from pathlib import Path
import json
from datetime import datetime

class StrategyFileManager:
    """策略文件管理器"""
    
    def __init__(self, strategies_dir: str = "strategies/generated"):
        self.strategies_dir = Path(strategies_dir)
        self.strategies_dir.mkdir(parents=True, exist_ok=True)
        
        self.metadata_dir = self.strategies_dir / ".metadata"
        self.metadata_dir.mkdir(exist_ok=True)
    
    def save_strategy(
        self,
        strategy_draft: StrategyDraft,
        code: str,
        platform: str = "ptrade"
    ) -> Dict[str, str]:
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        # 生成文件名
        safe_name = self._sanitize_filename(strategy_draft.name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.py"
        
        # 保存代码文件
        file_path = self.strategies_dir / platform / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 保存元数据
        metadata = {
            'strategy_draft': strategy_draft.to_dict(),
            'file_path': str(file_path),
            'platform': platform,
            'created_at': datetime.now().isoformat(),
            'version': strategy_draft.version
        }
        
        metadata_path = self.metadata_dir / f"{safe_name}_{timestamp}.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return {
            'file_path': str(file_path),
            'metadata_path': str(metadata_path),
            'strategy_name': strategy_draft.name,
            'version': strategy_draft.version
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        import re
        # 移除非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # 限制长度
        if len(filename) > 100:
            filename = filename[:100]
        return filename