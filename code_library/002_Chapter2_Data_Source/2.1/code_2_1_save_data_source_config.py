"""
文件名: code_2_1_save_data_source_config.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1_save_data_source_config.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:33:59
函数/类名: save_data_source_config

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from core.db import get_db_connection
import json

def save_data_source_config(name: str, source_type: str, config: dict):
        """
    save_data_source_config函数
    
    **设计原理**：
    - **核心功能**：实现save_data_source_config的核心逻辑
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
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO data_source_configs (name, source_type, config, status)
            VALUES (%s, %s, %s, 'active')
            ON CONFLICT (name) DO UPDATE
            SET source_type = EXCLUDED.source_type,
                config = EXCLUDED.config,
                updated_at = CURRENT_TIMESTAMP
     <CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.1/code_2_1_get_data_with_cache.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：