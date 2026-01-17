"""
文件名: code_11_1_use_strategy_generator.py
保存路径: code_library/011_Chapter11_User_Manual/11.1/code_11_1_use_strategy_generator.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/011_Chapter11_User_Manual/11.1_Quick_Start_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 使用策略生成器

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 在GUI中生成策略
1. 打开"策略开发"面板
2. 点击"策略生成器"
3. 选择策略风格：
   - 多因子（multi_factor）
   - 动量成长（momentum_growth）
   - 价值（value）
   - 市场中性（market_neutral）
4. 选择因子列表
5. 设置风险参数：
   - 最大仓位（max_position）
   - 止损线（stop_loss）
   - 止盈线（take_profit）
6. 选择目标平台（PTrade/QMT）
7. 点击"生成策略"
8. 查看生成的策略代码