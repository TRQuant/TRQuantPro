"""
主线数据抓取面板 - 透明化设计

设计原则：
1. 预先显示所有表格结构，抓取后只填充数值
2. 异步抓取，不阻塞UI
3. 完整的方法论和数据解读说明
4. 生成Cursor分析Prompt并保存报告
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QGroupBox, QProgressBar,
    QMessageBox, QSizePolicy, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget, QTextEdit, QSplitter, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QDesktopServices
from PyQt6.QtCore import QUrl

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


# ============================================================
# 主线识别方法论
# ============================================================

METHODOLOGY_TEXT = """
【主线识别方法论】

主线是指在特定时期内，市场资金持续流入、热度持续上升的投资方向。
识别主线的核心在于：追踪资金流向 + 验证持续性 + 评估空间。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【六维评分模型】（总分100分）

1. 资金流向 (25分) - 主力资金是否持续流入
   • 行业/概念净流入金额
   • 大单/超大单占比
   • 连续流入天数

2. 热度排名 (20分) - 市场关注度是否上升
   • 涨停股数量
   • 板块涨幅排名
   • 成交量放大程度

3. 北向资金 (20分) - 外资是否认可
   • 北向资金净流入
   • 外资持仓变化
   • 持续性加分

4. 市场情绪 (15分) - 整体环境是否配合
   • 涨跌停比
   • 连板高度
   • 赚钱效应

5. 龙虎榜 (10分) - 主力机构是否参与
   • 机构净买入
   • 知名游资参与
   • 上榜股票数量

6. 政策催化 (10分) - 是否有政策支持
   • 政策利好
   • 产业趋势
   • 事件驱动

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【使用建议】

• 得分 ≥ 80分：强主线，可重点配置
• 得分 70-79分：较强主线，可适当参与
• 得分 60-69分：一般主线，观察为主
• 得分 < 60分：弱主线，暂不参与
"""

# ============================================================
# 数据项定义 - 包含解读说明
# ============================================================

DATA_ITEMS = {
    "sector_flow": {
        "name": "行业板块资金流向",
        "source": "同花顺 via AKShare",
        "api": "ak.stock_fund_flow_industry()",
        "columns": ["行业", "涨跌幅", "净流入(亿)", "流入", "流出", "领涨股"],
        "interpretation": "净流入为正表示资金流入该行业，连续多日流入说明主力看好",
        "usage": "识别资金集中的行业，作为主线候选",
    },
    "concept_flow": {
        "name": "概念板块资金流向",
        "source": "同花顺 via AKShare",
        "api": "ak.stock_fund_flow_concept()",
        "columns": ["概念", "涨跌幅", "净流入(亿)", "流入", "流出", "领涨股"],
        "interpretation": "概念板块反映市场炒作方向，净流入大的概念往往是当前主线",
        "usage": "发现市场炒作主线和题材热点",
    },
    "northbound": {
        "name": "北向资金流向",
        "source": "东方财富 via AKShare",
        "api": "ak.stock_hsgt_fund_flow_summary_em()",
        "columns": ["类型", "今日净买入", "今日买入", "今日卖出"],
        "interpretation": "北向资金代表外资态度，持续流入说明外资看好A股",
        "usage": "判断外资态度，外资持续流入的方向是中长期主线",
    },
    "limit_up": {
        "name": "涨停板统计",
        "source": "东方财富 via AKShare",
        "api": "ak.stock_zt_pool_em()",
        "columns": ["代码", "名称", "涨停时间", "连板数", "所属概念"],
        "interpretation": "涨停数量反映市场情绪，连板股所属概念往往是当前主线",
        "usage": "发现短线强势主线，追踪连板龙头",
    },
    "dragon_tiger": {
        "name": "龙虎榜数据",
        "source": "东方财富 via AKShare",
        "api": "ak.stock_lhb_detail_em()",
        "columns": ["代码", "名称", "上榜原因", "买入额", "卖出额"],
        "interpretation": "龙虎榜显示主力资金动向，机构买入的股票值得关注",
        "usage": "追踪机构和游资动向，发现主力介入的个股",
    },
}


class SingleDataFetcher(QThread):
    """单个数据源抓取线程 - 不阻塞UI"""
    finished = pyqtSignal(str, dict)
    
    def __init__(self, data_type: str):
        super().__init__()
        self.data_type = data_type
    
    def run(self):
        try:
            from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
            fetcher = RealDataFetcher()
            
            result = None
            if self.data_type == "sector_flow":
                result = fetcher.fetch_sector_flow()
            elif self.data_type == "concept_flow":
                result = fetcher.fetch_concept_board()
            elif self.data_type == "northbound":
                result = fetcher.fetch_northbound_flow()
            elif self.data_type == "limit_up":
                result = fetcher.fetch_market_sentiment()
            elif self.data_type == "dragon_tiger":
                result = fetcher.fetch_dragon_tiger()
            
            if result and result.success:
                self.finished.emit(self.data_type, {
                    "success": True,
                    "data": result.data,
                    "source": result.source,
                    "time": datetime.now().strftime("%H:%M:%S"),
                })
            else:
                self.finished.emit(self.data_type, {
                    "success": False,
                    "error": result.error if result else "获取失败",
                })
        except Exception as e:
            self.finished.emit(self.data_type, {
                "success": False,
                "error": str(e)[:50],
            })


class DataTableWidget(QFrame):
    """数据表格组件 - 预显示结构"""
    
    def __init__(self, data_type: str, parent=None):
        super().__init__(parent)
        self.data_type = data_type
        self.info = DATA_ITEMS.get(data_type, {})
        self.fetcher = None
        self._setup_ui()
    
    def _setup_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        
        # 标题行
        header = QHBoxLayout()
        
        title = QLabel(f"📊 {self.info.get('name', self.data_type)}")
        title.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; border: none;")
        header.addWidget(title)
        
        # 来源
        source = QLabel(f"[{self.info.get('source', '')}]")
        source.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 10px; border: none;")
        header.addWidget(source)
        
        header.addStretch()
        
        # 状态
        self.status_label = QLabel("⏳ 等待抓取")
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 10px; border: none;")
        header.addWidget(self.status_label)
        
        # 抓取按钮
        self.fetch_btn = QPushButton("抓取")
        self.fetch_btn.setFixedSize(50, 24)
        self.fetch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
            }}
            QPushButton:hover {{ background-color: {Colors.PRIMARY}dd; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.fetch_btn.clicked.connect(self._start_fetch)
        header.addWidget(self.fetch_btn)
        
        layout.addLayout(header)
        
        # 数据解读
        interp = QLabel(f"💡 解读: {self.info.get('interpretation', '')}")
        interp.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 10px; border: none;")
        interp.setWordWrap(True)
        layout.addWidget(interp)
        
        # 数据表格 - 预显示列头
        self.table = QTableWidget()
        columns = self.info.get("columns", [])
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.setRowCount(5)  # 预留5行
        
        # 填充占位符
        for row in range(5):
            for col in range(len(columns)):
                item = QTableWidgetItem("--")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor(Colors.TEXT_MUTED))
                self.table.setItem(row, col, item)
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                font-size: 10px;
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{
                padding: 2px 4px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                padding: 4px;
                font-weight: bold;
                font-size: 10px;
            }}
        """)
        self.table.verticalHeader().setVisible(False)
        self.table.setMaximumHeight(140)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
    
    def _start_fetch(self):
        """开始抓取"""
        if self.fetcher and self.fetcher.isRunning():
            return
        
        self.fetch_btn.setEnabled(False)
        self.status_label.setText("🔄 抓取中...")
        self.status_label.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 10px; border: none;")
        
        self.fetcher = SingleDataFetcher(self.data_type)
        self.fetcher.finished.connect(self._on_fetch_finished)
        self.fetcher.start()
    
    def _on_fetch_finished(self, data_type: str, result: Dict):
        """抓取完成"""
        self.fetch_btn.setEnabled(True)
        
        if result.get("success"):
            self.status_label.setText(f"✅ {result.get('time', '')}")
            self.status_label.setStyleSheet(f"color: {Colors.SUCCESS}; font-size: 10px; border: none;")
            self._fill_data(result.get("data", []))
        else:
            self.status_label.setText(f"❌ {result.get('error', '失败')[:20]}")
            self.status_label.setStyleSheet(f"color: {Colors.ERROR}; font-size: 10px; border: none;")
    
    def _fill_data(self, data: Any):
        """填充数据到表格"""
        if not data:
            return
        
        if isinstance(data, dict):
            data = [data]
        
        if not isinstance(data, list):
            return
        
        columns = self.info.get("columns", [])
        rows = min(len(data), 10)
        self.table.setRowCount(rows)
        
        # 字段映射
        field_map = {
            "行业": ["sector_name", "行业", "行业名称"],
            "概念": ["board_name", "概念", "概念名称"],
            "涨跌幅": ["change_pct", "涨跌幅", "行业-涨跌幅"],
            "净流入(亿)": ["main_net_inflow", "net_inflow", "净流入", "净额"],
            "流入": ["inflow", "流入资金"],
            "流出": ["outflow", "流出资金"],
            "领涨股": ["leader_stock", "领涨股"],
            "类型": ["板块", "type"],
            "今日净买入": ["成交净买额", "net_buy", "today_net"],
            "今日买入": ["买入金额", "buy"],
            "今日卖出": ["卖出金额", "sell"],
            "代码": ["code", "股票代码", "代码"],
            "名称": ["name", "股票名称", "名称"],
            "涨停时间": ["first_time", "涨停时间"],
            "连板数": ["连板数", "continuous"],
            "所属概念": ["concept", "所属概念"],
            "上榜原因": ["reason", "上榜原因"],
            "买入额": ["buy_amount", "买入金额"],
            "卖出额": ["sell_amount", "卖出金额"],
        }
        
        for row, item in enumerate(data[:rows]):
            if not isinstance(item, dict):
                continue
            
            for col, col_name in enumerate(columns):
                value = "--"
                
                # 尝试多个可能的字段名
                for field in field_map.get(col_name, [col_name]):
                    if field in item:
                        value = item[field]
                        break
                
                # 格式化数值
                if isinstance(value, float):
                    if "涨跌" in col_name or "幅" in col_name:
                        value = f"{value:+.2f}%"
                    elif "亿" in col_name or "净" in col_name:
                        value = f"{value:.2f}"
                    else:
                        value = f"{value:.2f}"
                else:
                    value = str(value)[:12]
                
                cell = QTableWidgetItem(value)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # 涨跌着色
                if "+" in value or (isinstance(value, str) and value.replace(".", "").replace("-", "").isdigit()):
                    try:
                        num = float(value.replace("%", "").replace("+", ""))
                        if num > 0:
                            cell.setForeground(QColor(Colors.SUCCESS))
                        elif num < 0:
                            cell.setForeground(QColor(Colors.ERROR))
                    except:
                        pass
                
                self.table.setItem(row, col, cell)
    
    def get_data(self) -> List[Dict]:
        """获取当前表格数据"""
        data = []
        columns = self.info.get("columns", [])
        
        for row in range(self.table.rowCount()):
            row_data = {}
            for col, col_name in enumerate(columns):
                item = self.table.item(row, col)
                if item:
                    row_data[col_name] = item.text()
            if row_data and row_data.get(columns[0], "--") != "--":
                data.append(row_data)
        
        return data


class DataStatusPanel(QWidget):
    """主线数据抓取面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tables = {}
        self.all_data = {}
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ========== 顶部工具栏 ==========
        toolbar = QFrame()
        toolbar.setStyleSheet(f"background-color: {Colors.BG_SECONDARY}; border-bottom: 1px solid {Colors.BORDER_PRIMARY};")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 10, 16, 10)
        
        title = QLabel("📡 主线数据抓取")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        toolbar_layout.addWidget(title)
        
        toolbar_layout.addStretch()
        
        # 一键抓取
        self.fetch_all_btn = QPushButton("🚀 一键抓取全部")
        self.fetch_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {Colors.PRIMARY}dd; }}
        """)
        self.fetch_all_btn.clicked.connect(self._fetch_all)
        toolbar_layout.addWidget(self.fetch_all_btn)
        
        # 生成报告
        self.report_btn = QPushButton("📝 生成Cursor分析报告")
        self.report_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #27ae60; }}
        """)
        self.report_btn.clicked.connect(self._generate_report)
        toolbar_layout.addWidget(self.report_btn)
        
        layout.addWidget(toolbar)
        
        # ========== 滚动区域 ==========
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: {Colors.BG_PRIMARY}; }}")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(16)
        
        # ========== 方法论说明 ==========
        method_card = QFrame()
        method_card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.PRIMARY}40;
                border-radius: 8px;
            }}
        """)
        method_layout = QVBoxLayout(method_card)
        method_layout.setContentsMargins(16, 12, 16, 12)
        
        method_title = QLabel("📐 主线识别方法论")
        method_title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        method_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; border: none;")
        method_layout.addWidget(method_title)
        
        method_text = QTextEdit()
        method_text.setPlainText(METHODOLOGY_TEXT)
        method_text.setReadOnly(True)
        method_text.setMaximumHeight(200)
        method_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                font-size: 11px;
                font-family: 'Microsoft YaHei', monospace;
            }}
        """)
        method_layout.addWidget(method_text)
        
        content_layout.addWidget(method_card)
        
        # ========== 数据抓取区域 ==========
        data_title = QLabel("📊 数据抓取（点击各表格的「抓取」按钮或「一键抓取全部」）")
        data_title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        data_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(data_title)
        
        # 数据表格
        for data_type in DATA_ITEMS.keys():
            table_widget = DataTableWidget(data_type)
            self.tables[data_type] = table_widget
            content_layout.addWidget(table_widget)
        
        # ========== 数据使用说明 ==========
        usage_card = QFrame()
        usage_card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        usage_layout = QVBoxLayout(usage_card)
        usage_layout.setContentsMargins(16, 12, 16, 12)
        
        usage_title = QLabel("📖 数据使用说明")
        usage_title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        usage_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; border: none;")
        usage_layout.addWidget(usage_title)
        
        usage_text = QLabel(
            "【如何使用这些数据识别主线】\n\n"
            "1️⃣ 行业板块资金流向：找出净流入最大的行业，这是资金主攻方向\n"
            "2️⃣ 概念板块资金流向：找出净流入最大的概念，这是市场炒作主线\n"
            "3️⃣ 北向资金流向：外资净买入为正说明外资看好，是中长期主线信号\n"
            "4️⃣ 涨停板统计：连板股所属概念往往是当前最强主线\n"
            "5️⃣ 龙虎榜数据：机构买入的股票值得关注，可能是主线龙头\n\n"
            "【综合判断】\n"
            "• 多个数据源指向同一方向 → 强主线\n"
            "• 资金持续流入 + 涨停股增加 → 主线启动\n"
            "• 北向资金 + 机构买入 → 中长期主线\n"
            "• 概念热度高 + 龙头连板 → 短线主线"
        )
        usage_text.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px; border: none;")
        usage_text.setWordWrap(True)
        usage_layout.addWidget(usage_text)
        
        content_layout.addWidget(usage_card)
        
        # ========== 报告输出区域 ==========
        self.report_card = QFrame()
        self.report_card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.SUCCESS}40;
                border-radius: 8px;
            }}
        """)
        self.report_card.setVisible(False)
        report_layout = QVBoxLayout(self.report_card)
        report_layout.setContentsMargins(16, 12, 16, 12)
        
        report_title = QLabel("📝 分析报告已生成")
        report_title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        report_title.setStyleSheet(f"color: {Colors.SUCCESS}; border: none;")
        report_layout.addWidget(report_title)
        
        self.report_path_label = QLabel("")
        self.report_path_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px; border: none;")
        self.report_path_label.setWordWrap(True)
        report_layout.addWidget(self.report_path_label)
        
        report_btns = QHBoxLayout()
        
        self.open_folder_btn = QPushButton("📂 打开文件夹")
        self.open_folder_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ background-color: {Colors.BG_HOVER}; }}
        """)
        self.open_folder_btn.clicked.connect(self._open_report_folder)
        report_btns.addWidget(self.open_folder_btn)
        
        self.copy_prompt_btn = QPushButton("📋 复制Prompt到剪贴板")
        self.copy_prompt_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
            }}
            QPushButton:hover {{ background-color: {Colors.PRIMARY}dd; }}
        """)
        self.copy_prompt_btn.clicked.connect(self._copy_prompt)
        report_btns.addWidget(self.copy_prompt_btn)
        
        report_btns.addStretch()
        report_layout.addLayout(report_btns)
        
        content_layout.addWidget(self.report_card)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _fetch_all(self):
        """一键抓取所有数据"""
        for table in self.tables.values():
            table._start_fetch()
    
    def _generate_report(self):
        """生成Cursor分析报告"""
        # 收集所有数据
        all_data = {}
        for data_type, table in self.tables.items():
            all_data[data_type] = {
                "name": DATA_ITEMS[data_type]["name"],
                "data": table.get_data(),
            }
        
        # 生成报告
        report_dir = Path.home() / ".local/share/trquant/analysis_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"mainline_analysis_{timestamp}.md"
        prompt_file = report_dir / f"cursor_prompt_{timestamp}.md"
        
        # 生成Markdown报告
        report_content = self._generate_markdown_report(all_data)
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        # 生成Cursor Prompt
        prompt_content = self._generate_cursor_prompt(all_data)
        with open(prompt_file, "w", encoding="utf-8") as f:
            f.write(prompt_content)
        
        self.last_prompt = prompt_content
        self.last_report_dir = str(report_dir)
        
        # 显示结果
        self.report_card.setVisible(True)
        self.report_path_label.setText(
            f"📄 报告文件: {report_file}\n"
            f"📄 Prompt文件: {prompt_file}\n\n"
            f"💡 提示: 复制Prompt到Cursor Chat中，让AI帮你分析主线"
        )
        
        logger.info(f"分析报告已生成: {report_file}")
    
    def _generate_markdown_report(self, data: Dict) -> str:
        """生成Markdown格式报告"""
        now = datetime.now()
        
        report = f"""# 主线识别分析报告

**生成时间**: {now.strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 数据概览

"""
        for data_type, info in data.items():
            name = info["name"]
            items = info["data"]
            
            report += f"### {name}\n\n"
            
            if items:
                # 表头
                headers = list(items[0].keys())
                report += "| " + " | ".join(headers) + " |\n"
                report += "| " + " | ".join(["---"] * len(headers)) + " |\n"
                
                # 数据行
                for item in items[:10]:
                    row = [str(item.get(h, "")) for h in headers]
                    report += "| " + " | ".join(row) + " |\n"
                
                report += "\n"
            else:
                report += "*暂无数据*\n\n"
        
        report += """
---

## 📐 分析方法

本报告基于以下数据源进行主线识别：

1. **行业板块资金流向** - 识别资金集中的行业
2. **概念板块资金流向** - 发现市场炒作主线
3. **北向资金流向** - 判断外资态度
4. **涨停板统计** - 追踪短线强势主线
5. **龙虎榜数据** - 追踪机构和游资动向

---

*报告由韬睿量化平台自动生成*
"""
        return report
    
    def _generate_cursor_prompt(self, data: Dict) -> str:
        """生成Cursor分析Prompt"""
        now = datetime.now()
        
        prompt = f"""# A股主线识别分析请求

**分析时间**: {now.strftime("%Y-%m-%d %H:%M:%S")}

## 📊 今日市场数据

请基于以下数据，帮我识别当前A股市场的投资主线：

"""
        # 添加各数据源的数据
        for data_type, info in data.items():
            name = info["name"]
            items = info["data"]
            
            prompt += f"### {name}\n\n"
            
            if items:
                for i, item in enumerate(items[:5], 1):
                    prompt += f"{i}. "
                    parts = []
                    for k, v in item.items():
                        parts.append(f"{k}: {v}")
                    prompt += ", ".join(parts) + "\n"
                prompt += "\n"
            else:
                prompt += "*暂无数据*\n\n"
        
        prompt += """
---

## 🎯 分析要求

请根据上述数据，完成以下分析：

### 1. 主线识别
- 识别出当前市场的 **3-5条主要投资主线**
- 每条主线说明：名称、核心逻辑、资金流向支撑

### 2. 主线评分
对每条主线进行评分（满分100分），评分维度：
- 资金流向得分 (25分)
- 热度排名得分 (20分)
- 北向资金得分 (20分)
- 市场情绪得分 (15分)
- 龙虎榜得分 (10分)
- 政策催化得分 (10分)

### 3. 操作建议
- 每条主线的推荐操作（买入/观望/回避）
- 龙头股推荐（每条主线1-3只）
- 买入时机建议

### 4. 风险提示
- 当前市场主要风险
- 各主线的潜在风险

---

请以专业量化分析师的角度，给出详细的分析报告。
"""
        return prompt
    
    def _open_report_folder(self):
        """打开报告文件夹"""
        if hasattr(self, "last_report_dir"):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.last_report_dir))
    
    def _copy_prompt(self):
        """复制Prompt到剪贴板"""
        if hasattr(self, "last_prompt"):
            clipboard = QApplication.clipboard()
            clipboard.setText(self.last_prompt)
            QMessageBox.information(self, "已复制", "Cursor分析Prompt已复制到剪贴板！\n\n请粘贴到Cursor Chat中进行分析。")
    
    def get_status_summary(self) -> Dict:
        """获取状态摘要（兼容旧接口）"""
        return {
            "status": "正常",
            "ok_count": len(self.tables),
            "total_count": len(self.tables),
        }
