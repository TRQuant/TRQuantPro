"""
文件名: code_10_4_create_sidebar.py
保存路径: code_library/010_Chapter10_Development_Guide/10.4/code_10_4_create_sidebar.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.4_Desktop_System_Development_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: create_sidebar

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def create_sidebar(self):
        """
    create_sidebar函数
    
    **设计原理**：
    - **核心功能**：实现create_sidebar的核心逻辑
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
    sidebar = QFrame()
    sidebar.setFixedWidth(240)
    sidebar.setStyleSheet(f"""
        QFrame {{
            background-color: {Colors.BG_TERTIARY};
            border-right: 1px solid {Colors.BORDER_PRIMARY};
        }}
    """)
    
    layout = QVBoxLayout(sidebar)
    layout.setSpacing(8)
    layout.setContentsMargins(12, 20, 12, 20)
    
    # Logo和标题
    title_label = QLabel("📊 韬睿量化")
    title_label.setStyleSheet(f"""
        QLabel {{
            color: {Colors.PRIMARY};
            font-size: 20px;
            font-weight: 700;
            padding: 12px;
        }}
    """)
    layout.addWidget(title_label)
    
    layout.addSpacing(20)
    
    # 导航按钮
    nav_items = [
        ("🏠", "首页", 0),
        ("📡", "数据源", 1),
        ("📊", "市场分析", 2),
        ("🎯", "主线识别", 3),
        ("📈", "候选池", 4),
        ("🔢", "因子库", 5),
        ("🛠️", "策略开发", 6),
        ("🔄", "回测验证", 7),
        ("💼", "实盘交易", 8),
    ]
    
    self.nav_buttons = []
    for icon, text, index in nav_items:
        btn = SidebarButton(icon, text)
        btn.clicked.connect(lambda checked, idx=index: self.switch_panel(idx))
        layout.addWidget(btn)
        self.nav_buttons.append(btn)
    
    # 默认选中首页
    if self.nav_buttons:
        self.nav_buttons[0].setChecked(True)
    
    layout.addStretch()
    
    return sidebar