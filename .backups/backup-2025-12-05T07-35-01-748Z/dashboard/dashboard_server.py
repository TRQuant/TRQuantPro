# -*- coding: utf-8 -*-
"""
量化策略全流程工作台 - Web仪表盘服务
基于Flask的轻量级Web服务，提供实时数据展示
"""
import sys
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
from flask import Flask, render_template, jsonify, send_from_directory, request, abort
from flask_cors import CORS
import html

try:
    from ptrade_bridge.service import PTradeBridgeService, PTradeBridgeConfig
except ImportError:
    PTradeBridgeService = None
    PTradeBridgeConfig = None

try:
    import markdown  # type: ignore
except ImportError:
    markdown = None

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# 注册A股策略管理API
try:
    from dashboard.astock_api import astock_bp
    app.register_blueprint(astock_bp)
except ImportError:
    pass

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
STRATEGY_DIRS = [
    PROJECT_ROOT / "strategies" / "examples",      # 本地示例策略
    PROJECT_ROOT / "strategies" / "ptrade",         # PTrade策略
    PROJECT_ROOT / "strategies" / "qmt",           # QMT策略
    PROJECT_ROOT / "strategies" / "quantconnect",  # QuantConnect+IBKR策略
]
CONFIG_DIR = PROJECT_ROOT / "config"

# 多平台数据目录
PTRADE_DATA_DIR = PROJECT_ROOT / "data" / "ptrade"
PTRADE_BACKTEST_DIR = PTRADE_DATA_DIR / "backtest_results"
PTRADE_TRADES_DIR = PTRADE_DATA_DIR / "trade_records"

QMT_DATA_DIR = PROJECT_ROOT / "data" / "qmt"
QMT_BACKTEST_DIR = QMT_DATA_DIR / "backtest_results"
QMT_TRADES_DIR = QMT_DATA_DIR / "trade_records"

QC_DATA_DIR = PROJECT_ROOT / "data" / "quantconnect"
QC_BACKTEST_DIR = QC_DATA_DIR / "backtest_results"
QC_TRADES_DIR = QC_DATA_DIR / "trade_records"

DOCS_DIR = PROJECT_ROOT / "docs"

# 确保目录存在
for dir_path in [PTRADE_BACKTEST_DIR, PTRADE_TRADES_DIR, 
                 QMT_BACKTEST_DIR, QMT_TRADES_DIR,
                 QC_BACKTEST_DIR, QC_TRADES_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

DOC_CATEGORY_CONFIG = [
    {
        "key": "platform_overview",
        "name": "平台总览与架构",
        "description": "平台定位、总体架构、开发路线与投研流程蓝图。",
        "keywords": ["architecture", "arch", "overview", "platform", "项目", "方案", "implementation", "bridge", "分析", "workflow"]
    },
    {
        "key": "strategy_research",
        "name": "策略研究与回测",
        "description": "策略模板、回测结果、因子研究与工作流规范。",
        "keywords": ["strategy", "策略", "backtest", "test", "alpha", "factor", "workflow", "research", "report", "quant", "分析"]
    },
    {
        "key": "live_trading",
        "name": "实盘交易与券商集成",
        "description": "PTrade/QMT/IBKR等券商接口、风控与实盘联调方案。",
        "keywords": ["ptrade", "qmt", "ibkr", "live", "trading", "broker", "execution", "bridge", "risk", "交易"]
    },
    {
        "key": "deployment_ops",
        "name": "部署运维与环境",
        "description": "Docker/安装脚本/备份与自动化运维等文档。",
        "keywords": ["docker", "install", "部署", "运维", "guide", "环境", "backup", "安装", "setup", "run"]
    },
    {
        "key": "research_manual",
        "name": "投研手册与业务资料",
        "description": "市场研究、手册、指南及业务知识库。",
        "keywords": ["manual", "handbook", "指南", "投研", "market", "report", "文档", "research", "study"]
    },
    {
        "key": "others",
        "name": "其他研究资料",
        "description": "尚未归类的其他参考资料。",
        "keywords": []
    }
]


def _build_doc_entry(doc_file: Path) -> Dict:
    """构建文档条目"""
    relative_path = doc_file.relative_to(DOCS_DIR)
    project_relative = doc_file.relative_to(PROJECT_ROOT)
    modified = datetime.fromtimestamp(doc_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    entry = {
        "name": doc_file.stem,
        "file": doc_file.name,
        "path": str(project_relative),
        "docs_path": relative_path.as_posix(),
        "type": doc_file.suffix[1:].upper(),
        "modified": modified,
        "size": f"{doc_file.stat().st_size / 1024:.1f} KB",
        "url": f"/docs/view/{relative_path.as_posix()}"
    }
    entry["category"] = _categorize_document(entry)
    return entry


def _categorize_document(entry: Dict) -> str:
    """根据关键字匹配文档类别"""
    text = f"{entry['name']} {entry['path']}".lower()
    for config in DOC_CATEGORY_CONFIG:
        if config["key"] == "others":
            continue
        if any(keyword.lower() in text for keyword in config["keywords"]):
            return config["key"]
    return "others"


def _collect_docs() -> List[Dict]:
    """收集文档列表"""
    docs = []
    if DOCS_DIR.exists():
        for ext in ['*.md', '*.pdf', '*.docx', '*.html']:
            for doc_file in DOCS_DIR.rglob(ext):
                try:
                    docs.append(_build_doc_entry(doc_file))
                except Exception as e:
                    print(f"读取文档 {doc_file} 失败: {e}")
    docs.sort(key=lambda x: x["modified"], reverse=True)
    return docs


def _build_doc_categories(docs: List[Dict]) -> List[Dict]:
    """根据配置构建分类列表"""
    category_map = {
        cfg["key"]: {
            "key": cfg["key"],
            "name": cfg["name"],
            "description": cfg["description"],
            "docs": []
        }
        for cfg in DOC_CATEGORY_CONFIG
    }
    
    for doc in docs:
        key = doc.get("category", "others")
        if key not in category_map:
            key = "others"
        category_map[key]["docs"].append(doc)
    
    # 仅返回包含文档的分类，并按配置顺序排序
    ordered = []
    for cfg in DOC_CATEGORY_CONFIG:
        cat = category_map[cfg["key"]]
        if cat["docs"]:
            ordered.append(cat)
    return ordered


def _render_markdown_basic(md_text: str) -> str:
    """简易Markdown转HTML（无第三方依赖时使用）"""
    lines = md_text.splitlines()
    html_lines = []
    in_code = False
    in_list = False
    
    def close_list():
        nonlocal in_list
        if in_list:
            html_lines.append("</ul>")
            in_list = False
    
    for line in lines:
        if line.strip().startswith("```"):
            if not in_code:
                close_list()
                html_lines.append("<pre><code>")
                in_code = True
            else:
                html_lines.append("</code></pre>")
                in_code = False
            continue
        
        if in_code:
            html_lines.append(html.escape(line))
            continue
        
        stripped = line.strip()
        if not stripped:
            close_list()
            html_lines.append("<br>")
            continue
        
        if stripped.startswith("#"):
            close_list()
            level = len(stripped) - len(stripped.lstrip("#"))
            content = stripped[level:].strip()
            content = html.escape(content)
            html_lines.append(f"<h{min(level,6)}>{content}</h{min(level,6)}>")
            continue
        
        if stripped.startswith(("- ", "* ")):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = stripped[2:].strip()
            html_lines.append(f"<li>{html.escape(content)}</li>")
            continue
        
        close_list()
        text = html.escape(stripped)
        # 简单处理 [text](url)
        text = _convert_links(text)
        html_lines.append(f"<p>{text}</p>")
    
    close_list()
    return "\n".join(html_lines)


def _convert_links(text: str) -> str:
    """将 [text](url) 转为链接"""
    result = ""
    i = 0
    while i < len(text):
        if text[i] == "[":
            end = text.find("]", i)
            if end != -1 and end + 1 < len(text) and text[end+1] == "(":
                close = text.find(")", end+2)
                if close != -1:
                    label = text[i+1:end]
                    url = text[end+2:close]
                    result += f'<a href="{url}" target="_blank">{label}</a>'
                    i = close + 1
                    continue
        result += text[i]
        i += 1
    return result

bridge_service = None
if PTradeBridgeService:
    try:
        bridge_service = PTradeBridgeService(PTradeBridgeConfig())
    except Exception as e:
        print(f"[Dashboard] 无法加载PTrade Bridge数据: {e}")


def get_strategy_count():
    """获取策略数量"""
    return len(list(get_strategy_inventory()))


def get_strategy_inventory():
    """整合策略清单（本地示例 + PTrade + QMT + QuantConnect+IBKR）"""
    strategies = []
    seen = set()
    
    # 平台映射
    platform_map = {
        "examples": "本地",
        "ptrade": "PTrade",
        "qmt": "QMT",
        "quantconnect": "QuantConnect+IBKR"
    }
    
    for dir_path in STRATEGY_DIRS:
        if not dir_path.exists():
            continue
        
        # 识别平台
        platform = "本地"
        platform_key = "examples"
        for key, name in platform_map.items():
            if key in str(dir_path):
                platform = name
                platform_key = key
                break
        
        for py_file in dir_path.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            strategy_id = py_file.stem
            if strategy_id in seen:
                continue
            seen.add(strategy_id)
            
            # 读取策略文件的前几行获取描述
            description = py_file.stem.replace("_", " ").title()
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:30]
                    for line in lines:
                        if '"""' in line or "'''" in line:
                            continue
                        if 'description' in line.lower() or '策略' in line:
                            # 尝试提取描述
                            if ':' in line:
                                desc_part = line.split(':')[-1].strip().strip('"').strip("'")
                                if desc_part and len(desc_part) > 5:
                                    description = desc_part[:100]
                                    break
            except:
                pass
            
            strategies.append({
                "id": strategy_id,
                "name": py_file.stem,
                "file": py_file.name,
                "source": platform_key,
                "platform": platform,
                "description": description,
                "modified": datetime.fromtimestamp(py_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": f"{py_file.stat().st_size / 1024:.1f} KB"
            })
    
    # PTrade Bridge策略
    if bridge_service:
        try:
            for strategy in bridge_service.get_strategies():
                if strategy.id in seen:
                    continue
                seen.add(strategy.id)
                strategies.append({
                    "id": strategy.id,
                    "name": strategy.name,
                    "file": Path(strategy.code_path).name if strategy.code_path else f"{strategy.id}.py",
                    "source": "ptrade",
                    "platform": "PTrade",
                    "description": strategy.description or "PTrade策略",
                    "modified": strategy.updated_at.split("T")[0] if strategy.updated_at else "",
                    "size": "--"
                })
        except Exception as e:
            print(f"加载PTrade Bridge策略失败: {e}")
    
    strategies.sort(key=lambda x: x["modified"], reverse=True)
    return strategies


def get_report_count():
    """获取报告数量"""
    counts = {"html": 0, "json": 0, "ptrade": 0, "total": 0}
    
    if RESULTS_DIR.exists():
        counts["html"] = len(list(RESULTS_DIR.glob("*_report*.html")))
        counts["json"] = len(list(RESULTS_DIR.glob("backtest_*.json")))
    
    if PTRADE_BACKTEST_DIR.exists():
        counts["ptrade"] = len(list(PTRADE_BACKTEST_DIR.glob("*.json")))
    
    counts["total"] = counts["html"] + counts["json"] + counts["ptrade"]
    return counts


def get_backtest_statistics():
    """获取回测统计数据"""
    stats = {
        "total_backtests": 0,
        "ptrade_backtests": 0,
        "avg_win_rate": 0,
        "avg_profit_ratio": 0,
        "avg_sharpe": 0,
        "total_trades": 0,
        "backtests": []
    }
    
    if not RESULTS_DIR.exists():
        return stats
    
    json_files = list(RESULTS_DIR.glob("backtest_*.json"))
    
    win_rates = []
    profit_ratios = []
    sharpe_ratios = []
    
    for json_file in sorted(json_files, key=lambda x: x.stat().st_mtime, reverse=True):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            summary = data.get('summary', {})
            metrics = data.get('metrics', {})
            
            backtest_info = {
                "file": json_file.name,
                "strategy": data.get('strategy', 'unknown'),
                "start_date": data.get('start_date', ''),
                "end_date": data.get('end_date', ''),
                "total_return": summary.get('total_profit_rate', 0) * 100,
                "annual_return": metrics.get('annual_return', 0) * 100,
                "sharpe_ratio": metrics.get('sharpe_ratio', 0),
                "max_drawdown": metrics.get('max_drawdown', 0) * 100,
                "total_trades": metrics.get('total_trades', 0),
                "win_rate": metrics.get('win_rate', 0.5) * 100,
            }
            
            stats["backtests"].append(backtest_info)
            stats["total_backtests"] += 1
            stats["total_trades"] += backtest_info["total_trades"]
            
            # 收集用于计算平均值的数据
            if backtest_info["win_rate"] > 0:
                win_rates.append(backtest_info["win_rate"])
            if backtest_info["sharpe_ratio"] != 0:
                sharpe_ratios.append(backtest_info["sharpe_ratio"])
            
            # 计算盈亏比 (假设从交易记录计算)
            trade_history = data.get('trade_history', [])
            if trade_history:
                profits = [t.get('profit', 0) for t in trade_history if t.get('profit', 0) > 0]
                losses = [abs(t.get('profit', 0)) for t in trade_history if t.get('profit', 0) < 0]
                if profits and losses:
                    avg_profit = sum(profits) / len(profits)
                    avg_loss = sum(losses) / len(losses)
                    if avg_loss > 0:
                        profit_ratios.append(avg_profit / avg_loss)
                        
        except Exception as e:
            print(f"读取 {json_file} 失败: {e}")
    
    # 追加PTrade回测
    if PTRADE_BACKTEST_DIR.exists():
        for json_file in sorted(PTRADE_BACKTEST_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                backtest_info = {
                    "file": json_file.name,
                    "strategy": data.get('strategy_name', json_file.stem),
                    "start_date": data.get('start_date', ''),
                    "end_date": data.get('end_date', ''),
                    "total_return": data.get('total_return', 0) * 100,
                    "annual_return": data.get('annual_return', 0) * 100,
                    "sharpe_ratio": data.get('sharpe_ratio', 0),
                    "max_drawdown": data.get('max_drawdown', 0) * 100,
                    "total_trades": data.get('total_trades', 0),
                    "win_rate": data.get('win_rate', 0) * 100,
                    "source": "ptrade"
                }
                
                stats["backtests"].append(backtest_info)
                stats["total_backtests"] += 1
                stats["ptrade_backtests"] += 1
                stats["total_trades"] += backtest_info["total_trades"]
                
                if backtest_info["win_rate"] > 0:
                    win_rates.append(backtest_info["win_rate"])
                if backtest_info["sharpe_ratio"] != 0:
                    sharpe_ratios.append(backtest_info["sharpe_ratio"])
                
                if data.get("metrics", {}).get("profit_loss_ratio"):
                    profit_ratios.append(data["metrics"]["profit_loss_ratio"])
            except Exception as e:
                print(f"读取 {json_file} 失败: {e}")
    
    # 计算平均值
    if win_rates:
        stats["avg_win_rate"] = sum(win_rates) / len(win_rates)
    if profit_ratios:
        stats["avg_profit_ratio"] = sum(profit_ratios) / len(profit_ratios)
    if sharpe_ratios:
        stats["avg_sharpe"] = sum(sharpe_ratios) / len(sharpe_ratios)
    
    return stats


def get_workflow_progress():
    """获取工作流程进度"""
    strategy_count = get_strategy_count()
    report_count = get_report_count()
    backtest_stats = get_backtest_statistics()
    ptrade_ready = backtest_stats["ptrade_backtests"] > 0
    trades_ready = len(get_latest_trades(1)) > 0
    
    # 根据实际数据计算进度
    progress = {
        "research": {
            "status": "completed" if strategy_count > 0 else "pending",
            "count": strategy_count,
            "desc": f"策略库：{strategy_count} 个 | PTrade {backtest_stats['ptrade_backtests']} 个回测"
        },
        "backtest": {
            "status": "completed" if backtest_stats["total_backtests"] > 0 else "pending",
            "count": backtest_stats["total_backtests"],
            "desc": f"{backtest_stats['total_backtests']} 次已完成"
        },
        "report": {
            "status": "completed" if report_count["total"] > 0 else "pending",
            "count": report_count["total"],
            "desc": f"{report_count['total']} 份报告（含PTrade {report_count['ptrade']}）"
        },
        "paper_trade": {
            "status": "completed" if ptrade_ready else "in_progress",
            "count": backtest_stats["ptrade_backtests"],
            "desc": "PTrade回测联通" if ptrade_ready else "等待PTrade回测"
        },
        "live_trade": {
            "status": "completed" if trades_ready else "pending",
            "count": 1 if trades_ready else 0,
            "desc": "交易日志实时回传" if trades_ready else "等待实盘数据"
        }
    }
    
    return progress


def get_live_readiness():
    """计算实盘准备度"""
    strategy_count = get_strategy_count()
    report_count = get_report_count()
    backtest_stats = get_backtest_statistics()
    has_trades = len(get_latest_trades(1)) > 0
    
    # 计算各项得分
    scores = {
        "strategy": min(strategy_count * 10, 20),  # 最多20分
        "backtest": min(backtest_stats["total_backtests"] * 10, 30),  # 最多30分
        "report": min(report_count["html"] * 2, 20),  # 最多20分
        "win_rate": 15 if backtest_stats["avg_win_rate"] > 50 else 0,  # 胜率>50%得15分
        "sharpe": 10 if backtest_stats["avg_sharpe"] > 1 else 0,  # 夏普>1得分
        "ptrade": 10 if backtest_stats["ptrade_backtests"] > 0 else 0,
        "trades": 5 if has_trades else 0,
    }
    
    total_score = sum(scores.values())
    
    return {
        "score": total_score,
        "max_score": 100,
        "percentage": total_score,
        "details": scores,
        "avg_win_rate": backtest_stats["avg_win_rate"],
        "avg_profit_ratio": backtest_stats["avg_profit_ratio"],
        "ready": total_score >= 60,
        "message": "已满足实盘联调条件，可进入模拟或小额实盘验证阶段。" if total_score >= 60 else "请继续完善策略和回测。"
    }


def get_reports_list():
    """获取报告列表"""
    reports = []
    
    if RESULTS_DIR.exists():
        # HTML报告
        for html_file in sorted(RESULTS_DIR.glob("*_report*.html"), key=lambda x: x.stat().st_mtime, reverse=True):
            if html_file.name in ['view_report.html', 'report_template.html']:
                continue
            
            strategy = "策略报告"
            if 'adaptive_momentum' in html_file.name.lower():
                strategy = "自适应动量策略"
            elif 'ma_cross' in html_file.name.lower():
                strategy = "均线交叉策略"
            
            reports.append({
                "type": "html",
                "file": html_file.name,
                "strategy": strategy,
                "modified": datetime.fromtimestamp(html_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": f"{html_file.stat().st_size / 1024:.1f} KB",
                "source": "backtest"
            })
    
    if PTRADE_BACKTEST_DIR.exists():
        for json_file in sorted(PTRADE_BACKTEST_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                reports.append({
                    "type": "ptrade",
                    "file": json_file.name,
                    "strategy": data.get("strategy_name", json_file.stem),
                    "modified": datetime.fromtimestamp(json_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "size": f"{json_file.stat().st_size / 1024:.1f} KB",
                    "total_return": data.get("total_return", 0) * 100,
                    "max_drawdown": data.get("max_drawdown", 0) * 100,
                    "sharpe_ratio": data.get("sharpe_ratio", 0),
                    "source": "ptrade"
                })
            except Exception:
                continue
    
    return reports[:20]  # 最多返回20个


def get_latest_trades(limit=20):
    """获取最新的交易记录"""
    trades = []
    
    if bridge_service:
        try:
            for trade in bridge_service.get_trades(limit=limit):
                trades.append({
                    "strategy_id": trade.strategy_id,
                    "symbol": trade.symbol,
                    "side": trade.side.value if hasattr(trade.side, "value") else trade.side,
                    "price": trade.price,
                    "volume": trade.volume,
                    "trade_time": trade.trade_time,
                    "pnl": trade.pnl,
                })
        except Exception as e:
            print(f"读取PTrade Bridge交易失败: {e}")
    
    if not trades and PTRADE_TRADES_DIR.exists():
        for json_file in sorted(PTRADE_TRADES_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                records = data if isinstance(data, list) else data.get("trades", [])
                for record in records:
                    trades.append({
                        "strategy_id": record.get("strategy_id", json_file.stem.replace("_trades", "")),
                        "symbol": record.get("symbol", record.get("stock")),
                        "side": record.get("side", record.get("action")),
                        "price": record.get("price"),
                        "volume": record.get("volume", record.get("quantity")),
                        "trade_time": record.get("trade_time", record.get("date")),
                        "pnl": record.get("pnl", record.get("profit")),
                    })
            except Exception:
                continue
    
    trades.sort(key=lambda x: x.get("trade_time", ""), reverse=True)
    return trades[:limit]


@app.route('/')
def index():
    """主页"""
    return render_template('dashboard.html')


@app.route('/api/overview')
def api_overview():
    """概览数据API"""
    strategy_count = get_strategy_count()
    report_count = get_report_count()
    backtest_stats = get_backtest_statistics()
    strategy_inventory = get_strategy_inventory()
    ptrade_strategies = len([s for s in strategy_inventory if "ptrade" in s.get("source", "")])
    
    return jsonify({
        "strategy_count": strategy_count,
        "ptrade_strategy_count": ptrade_strategies,
        "report_count": report_count["total"],
        "ptrade_report_count": report_count["ptrade"],
        "backtest_count": backtest_stats["total_backtests"],
        "ptrade_backtest_count": backtest_stats["ptrade_backtests"],
        "avg_win_rate": round(backtest_stats["avg_win_rate"], 1),
        "avg_profit_ratio": round(backtest_stats["avg_profit_ratio"], 2),
        "avg_sharpe": round(backtest_stats["avg_sharpe"], 2),
        "total_trades": backtest_stats["total_trades"],
        "backend_status": "运行正常",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


@app.route('/api/workflow')
def api_workflow():
    """工作流程进度API"""
    return jsonify(get_workflow_progress())


@app.route('/api/readiness')
def api_readiness():
    """实盘准备度API"""
    return jsonify(get_live_readiness())


@app.route('/api/reports')
def api_reports():
    """报告列表API"""
    return jsonify(get_reports_list())


@app.route('/api/backtests')
def api_backtests():
    """回测结果API"""
    stats = get_backtest_statistics()
    return jsonify(stats["backtests"][:10])


@app.route('/reports/<path:filename>')
def serve_report(filename):
    """提供报告文件"""
    target = RESULTS_DIR / filename
    if target.exists():
        return send_from_directory(RESULTS_DIR, filename)
    abort(404)


@app.route('/ptrade/reports/<path:filename>')
def serve_ptrade_report(filename):
    """提供PTrade回测文件"""
    target = PTRADE_BACKTEST_DIR / filename
    if target.exists():
        return send_from_directory(PTRADE_BACKTEST_DIR, filename)
    abort(404)


@app.route('/reports/<path:filepath>')
def serve_generated_report(filepath):
    """提供工作流生成的报告"""
    reports_dir = PROJECT_ROOT / "reports"
    target = reports_dir / filepath
    if target.exists():
        return send_from_directory(reports_dir, filepath)
    abort(404)


@app.route('/docs/view/<path:filepath>')
def serve_doc_file(filepath):
    """提供研究文档下载"""
    docs_root = DOCS_DIR.resolve()
    requested_path = (DOCS_DIR / filepath).resolve()
    
    if docs_root not in requested_path.parents and requested_path != docs_root:
        abort(403)
    
    relative_path = requested_path.relative_to(docs_root)
    suffix = requested_path.suffix.lower()
    
    if suffix in [".md", ".markdown"]:
        try:
            with open(requested_path, 'r', encoding='utf-8') as f:
                md_text = f.read()
            if markdown:
                html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc'])
            else:
                html_content = _render_markdown_basic(md_text)
            return render_template(
                'doc_viewer.html',
                title=relative_path.name,
                breadcrumbs=relative_path.parts,
                html_content=html_content
            )
        except Exception as e:
            return f"<h3>文档渲染失败</h3><pre>{e}</pre>", 500
    
    return send_from_directory(docs_root, relative_path.as_posix())


@app.route('/api/strategies')
def api_strategies():
    """策略列表API"""
    return jsonify(get_strategy_inventory())


def _find_strategy_file(name: str) -> Optional[Path]:
    """在策略目录中定位文件"""
    for dir_path in STRATEGY_DIRS:
        strategy_file = dir_path / f"{name}.py"
        if strategy_file.exists():
            return strategy_file
    return None


def _get_platform_from_path(file_path: Path) -> str:
    """从文件路径识别平台"""
    path_str = str(file_path)
    if "quantconnect" in path_str:
        return "QuantConnect+IBKR"
    elif "qmt" in path_str:
        return "QMT"
    elif "ptrade" in path_str:
        return "PTrade"
    else:
        return "本地"


@app.route('/api/strategy/<name>')
def api_strategy_detail(name):
    """获取策略详情（支持多平台）"""
    strategy_file = _find_strategy_file(name)
    
    # 本地策略（包括所有平台）
    if strategy_file and strategy_file.exists():
        try:
            with open(strategy_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            platform = _get_platform_from_path(strategy_file)
            
            return jsonify({
                "name": name,
                "content": content,
                "platform": platform,
                "modified": datetime.fromtimestamp(strategy_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": f"{strategy_file.stat().st_size / 1024:.1f} KB",
                "file_path": str(strategy_file.relative_to(PROJECT_ROOT))
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # PTrade Bridge策略
    if bridge_service:
        try:
            strategy = next((s for s in bridge_service.get_strategies() if s.id == name or s.name == name), None)
            if strategy and strategy.code_path and Path(strategy.code_path).exists():
                with open(strategy.code_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return jsonify({
                    "name": strategy.name,
                    "content": content,
                    "platform": "PTrade",
                    "modified": strategy.updated_at,
                    "size": "--",
                    "source": "ptrade"
                })
        except Exception as e:
            print(f"加载PTrade策略失败: {e}")
    
    return jsonify({"error": "策略不存在"}), 404


@app.route('/api/docs')
def api_docs():
    """研究文档列表（按核心目标分类）"""
    docs = _collect_docs()
    categories = _build_doc_categories(docs)
    return jsonify({
        "flat": docs[:40],
        "categories": categories
    })


@app.route('/api/factors')
def api_factors():
    """量化因子列表"""
    factors = [
        {
            "category": "动量因子",
            "factors": [
                {"name": "ROC", "description": "价格变动率", "period": "10/20/60日"},
                {"name": "MACD", "description": "指数平滑异同移动平均线", "period": "12-26-9"},
                {"name": "RSI", "description": "相对强弱指标", "period": "14日"},
            ]
        },
        {
            "category": "价值因子",
            "factors": [
                {"name": "PE", "description": "市盈率", "period": "TTM"},
                {"name": "PB", "description": "市净率", "period": "最新"},
                {"name": "PS", "description": "市销率", "period": "TTM"},
            ]
        },
        {
            "category": "质量因子",
            "factors": [
                {"name": "ROE", "description": "净资产收益率", "period": "TTM"},
                {"name": "ROA", "description": "总资产收益率", "period": "TTM"},
                {"name": "GPM", "description": "毛利率", "period": "TTM"},
            ]
        },
        {
            "category": "波动因子",
            "factors": [
                {"name": "ATR", "description": "平均真实波幅", "period": "14日"},
                {"name": "VOLATILITY", "description": "历史波动率", "period": "20日"},
                {"name": "BETA", "description": "贝塔系数", "period": "60日"},
            ]
        }
    ]
    return jsonify(factors)


@app.route('/api/trades/latest')
def api_latest_trades():
    """最新交易记录"""
    limit = int(request.args.get('limit', 20))
    return jsonify(get_latest_trades(limit))


def run_server(host='127.0.0.1', port=5000, debug=False):
    """启动服务器"""
    print(f"\n{'='*60}")
    print(f"  韬睿量化 - 量化投资文件管理系统")
    print(f"{'='*60}")
    print(f"  服务地址: http://{host}:{port}")
    print(f"  在浏览器中打开上述地址访问文件管理系统")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)

