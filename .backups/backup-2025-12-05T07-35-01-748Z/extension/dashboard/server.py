# -*- coding: utf-8 -*-
"""
TRQuant Extension Dashboard - 文件管理系统
==========================================

独立的Flask Web服务，用于管理：
- 策略代码（PTrade/QMT/示例）
- 回测报告
- 研究文档
- 数据库（MongoDB）
- 投资流程数据

此Dashboard独立于桌面系统，可随扩展件打包部署
"""
import sys
import json
import os
import html
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# Flask相关
try:
    from flask import Flask, render_template, jsonify, send_from_directory, request, abort, Response
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("警告: Flask未安装，请运行 pip install flask flask-cors")

# Markdown渲染
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    markdown = None
    MARKDOWN_AVAILABLE = False

# MongoDB
try:
    from pymongo import MongoClient
    MONGO_AVAILABLE = True
except ImportError:
    MongoClient = None
    MONGO_AVAILABLE = False

# ============================================================
# 路径配置 - 相对于extension目录
# ============================================================

EXTENSION_ROOT = Path(__file__).parent.parent
DATA_ROOT = EXTENSION_ROOT / "data"

# 策略目录
STRATEGY_DIRS = {
    "ptrade": DATA_ROOT / "strategies" / "ptrade",
    "qmt": DATA_ROOT / "strategies" / "qmt",
    "examples": DATA_ROOT / "strategies" / "examples",
}

# 其他数据目录
REPORTS_DIR = DATA_ROOT / "reports"
BACKTESTS_DIR = DATA_ROOT / "backtests"
DOCS_DIR = DATA_ROOT / "docs"
CONFIG_DIR = DATA_ROOT / "config"

# 确保目录存在
for dir_path in [REPORTS_DIR, BACKTESTS_DIR, DOCS_DIR, CONFIG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
for dir_path in STRATEGY_DIRS.values():
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================================
# Flask应用
# ============================================================

if FLASK_AVAILABLE:
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    CORS(app)
else:
    app = None

# MongoDB连接
db = None
if MONGO_AVAILABLE:
    try:
        client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
        client.server_info()  # 测试连接
        db = client['trquant_extension']
        print("✅ MongoDB连接成功")
    except Exception as e:
        print(f"⚠️ MongoDB连接失败: {e}")
        db = None


# ============================================================
# 文档分类配置
# ============================================================

DOC_CATEGORIES = [
    {
        "key": "strategy_research",
        "name": "📊 策略研究与回测",
        "description": "策略模板、回测结果、因子研究",
        "keywords": ["strategy", "策略", "backtest", "factor", "alpha", "回测"]
    },
    {
        "key": "trading_integration",
        "name": "🔗 实盘交易与集成",
        "description": "PTrade/QMT/IBKR接口与实盘方案",
        "keywords": ["ptrade", "qmt", "ibkr", "trading", "broker", "交易"]
    },
    {
        "key": "investment_manual",
        "name": "📚 投研手册",
        "description": "A股实操指南、市场研究",
        "keywords": ["manual", "handbook", "指南", "手册", "研究"]
    },
    {
        "key": "system_docs",
        "name": "⚙️ 系统文档",
        "description": "安装、部署、配置说明",
        "keywords": ["install", "setup", "config", "docker", "部署"]
    },
    {
        "key": "others",
        "name": "📁 其他资料",
        "description": "其他研究资料",
        "keywords": []
    }
]


# ============================================================
# 工具函数
# ============================================================

def _render_markdown_basic(md_text: str) -> str:
    """简易Markdown转HTML（无markdown库时使用）"""
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
        html_lines.append(f"<p>{text}</p>")
    
    close_list()
    return "\n".join(html_lines)


def _categorize_document(name: str, path: str) -> str:
    """根据关键字分类文档"""
    text = f"{name} {path}".lower()
    for cat in DOC_CATEGORIES:
        if cat["key"] == "others":
            continue
        if any(kw.lower() in text for kw in cat["keywords"]):
            return cat["key"]
    return "others"


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1024 / 1024:.1f} MB"


# ============================================================
# 策略管理
# ============================================================

def get_strategies() -> List[Dict]:
    """获取所有策略"""
    strategies = []
    platform_names = {
        "ptrade": "PTrade",
        "qmt": "QMT",
        "examples": "示例"
    }
    
    for platform_key, dir_path in STRATEGY_DIRS.items():
        if not dir_path.exists():
            continue
        
        for py_file in sorted(dir_path.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True):
            if py_file.name.startswith("__"):
                continue
            
            # 读取描述
            description = py_file.stem.replace("_", " ").title()
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    if '"""' in content:
                        start = content.find('"""') + 3
                        end = content.find('"""', start)
                        if end > start:
                            description = content[start:end].strip()[:100]
            except:
                pass
            
            strategies.append({
                "id": py_file.stem,
                "name": py_file.stem,
                "file": py_file.name,
                "platform": platform_names.get(platform_key, platform_key),
                "platform_key": platform_key,
                "description": description,
                "path": str(py_file.relative_to(EXTENSION_ROOT)),
                "size": _format_size(py_file.stat().st_size),
                "modified": datetime.fromtimestamp(py_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    
    return strategies


def get_strategy_content(name: str) -> Optional[Dict]:
    """获取策略内容"""
    for platform_key, dir_path in STRATEGY_DIRS.items():
        strategy_file = dir_path / f"{name}.py"
        if strategy_file.exists():
            try:
                with open(strategy_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {
                    "name": name,
                    "content": content,
                    "platform": platform_key,
                    "path": str(strategy_file.relative_to(EXTENSION_ROOT)),
                    "size": _format_size(strategy_file.stat().st_size),
                    "modified": datetime.fromtimestamp(strategy_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                }
            except Exception as e:
                return {"error": str(e)}
    return None


# ============================================================
# 报告管理
# ============================================================

def get_reports() -> List[Dict]:
    """获取所有报告"""
    reports = []
    
    if REPORTS_DIR.exists():
        for report_file in sorted(REPORTS_DIR.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True):
            if report_file.is_file() and report_file.suffix.lower() in ['.html', '.json', '.pdf']:
                # 识别报告类型
                report_type = "其他"
                if "trend" in report_file.name.lower():
                    report_type = "市场趋势"
                elif "mainline" in report_file.name.lower():
                    report_type = "投资主线"
                elif "backtest" in report_file.name.lower():
                    report_type = "回测报告"
                elif "investment" in report_file.name.lower():
                    report_type = "投资报告"
                
                reports.append({
                    "name": report_file.stem,
                    "file": report_file.name,
                    "type": report_type,
                    "format": report_file.suffix[1:].upper(),
                    "path": str(report_file.relative_to(EXTENSION_ROOT)),
                    "size": _format_size(report_file.stat().st_size),
                    "modified": datetime.fromtimestamp(report_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                })
    
    return reports[:50]  # 最多50个


# ============================================================
# 回测结果管理
# ============================================================

def get_backtests() -> List[Dict]:
    """获取回测结果"""
    backtests = []
    
    if BACKTESTS_DIR.exists():
        for bt_file in sorted(BACKTESTS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                with open(bt_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                backtests.append({
                    "file": bt_file.name,
                    "strategy": data.get("strategy_name", bt_file.stem),
                    "start_date": data.get("start_date", ""),
                    "end_date": data.get("end_date", ""),
                    "total_return": data.get("total_return", 0) * 100,
                    "annual_return": data.get("annual_return", 0) * 100,
                    "sharpe_ratio": data.get("sharpe_ratio", 0),
                    "max_drawdown": data.get("max_drawdown", 0) * 100,
                    "win_rate": data.get("win_rate", 0) * 100,
                    "total_trades": data.get("total_trades", 0),
                    "modified": datetime.fromtimestamp(bt_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                })
            except Exception as e:
                print(f"读取回测文件 {bt_file} 失败: {e}")
    
    # 也从MongoDB获取
    if db is not None:
        try:
            for doc in db.backtest_results.find().sort("timestamp", -1).limit(20):
                backtests.append({
                    "file": doc.get("file", "MongoDB"),
                    "strategy": doc.get("strategy_name", "未知"),
                    "start_date": doc.get("start_date", ""),
                    "end_date": doc.get("end_date", ""),
                    "total_return": doc.get("total_return", 0) * 100,
                    "annual_return": doc.get("annual_return", 0) * 100,
                    "sharpe_ratio": doc.get("sharpe_ratio", 0),
                    "max_drawdown": doc.get("max_drawdown", 0) * 100,
                    "win_rate": doc.get("win_rate", 0) * 100,
                    "total_trades": doc.get("total_trades", 0),
                    "modified": doc.get("timestamp", datetime.now()).strftime("%Y-%m-%d %H:%M") if hasattr(doc.get("timestamp"), 'strftime') else str(doc.get("timestamp", ""))[:16],
                    "source": "mongodb"
                })
        except Exception as e:
            print(f"从MongoDB获取回测记录失败: {e}")
    
    return backtests[:30]


def get_backtest_statistics() -> Dict:
    """计算回测统计"""
    backtests = get_backtests()
    
    if not backtests:
        return {
            "total_count": 0,
            "avg_return": 0,
            "avg_sharpe": 0,
            "avg_win_rate": 0,
            "avg_drawdown": 0
        }
    
    returns = [bt["total_return"] for bt in backtests if bt.get("total_return")]
    sharpes = [bt["sharpe_ratio"] for bt in backtests if bt.get("sharpe_ratio")]
    win_rates = [bt["win_rate"] for bt in backtests if bt.get("win_rate")]
    drawdowns = [bt["max_drawdown"] for bt in backtests if bt.get("max_drawdown")]
    
    return {
        "total_count": len(backtests),
        "avg_return": sum(returns) / len(returns) if returns else 0,
        "avg_sharpe": sum(sharpes) / len(sharpes) if sharpes else 0,
        "avg_win_rate": sum(win_rates) / len(win_rates) if win_rates else 0,
        "avg_drawdown": sum(drawdowns) / len(drawdowns) if drawdowns else 0
    }


# ============================================================
# 文档管理
# ============================================================

def get_documents() -> Dict:
    """获取所有文档（按分类）"""
    docs = []
    
    if DOCS_DIR.exists():
        for ext in ['*.md', '*.pdf', '*.html', '*.docx']:
            for doc_file in DOCS_DIR.rglob(ext):
                if doc_file.is_file():
                    rel_path = doc_file.relative_to(DOCS_DIR)
                    category = _categorize_document(doc_file.stem, str(rel_path))
                    
                    docs.append({
                        "name": doc_file.stem,
                        "file": doc_file.name,
                        "path": str(rel_path),
                        "full_path": str(doc_file.relative_to(EXTENSION_ROOT)),
                        "type": doc_file.suffix[1:].upper(),
                        "category": category,
                        "size": _format_size(doc_file.stat().st_size),
                        "modified": datetime.fromtimestamp(doc_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                    })
    
    # 按修改时间排序
    docs.sort(key=lambda x: x["modified"], reverse=True)
    
    # 按分类组织
    categories = {}
    for cat in DOC_CATEGORIES:
        categories[cat["key"]] = {
            "key": cat["key"],
            "name": cat["name"],
            "description": cat["description"],
            "docs": []
        }
    
    for doc in docs:
        cat_key = doc.get("category", "others")
        if cat_key in categories:
            categories[cat_key]["docs"].append(doc)
    
    # 过滤空分类
    result = [cat for cat in categories.values() if cat["docs"]]
    
    return {
        "flat": docs[:50],
        "categories": result
    }


# ============================================================
# 数据库管理
# ============================================================

def get_database_info() -> Dict:
    """获取数据库信息"""
    if db is None:
        return {
            "connected": False,
            "message": "MongoDB未连接",
            "collections": []
        }
    
    try:
        collections = []
        for coll_name in db.list_collection_names():
            coll = db[coll_name]
            doc_count = coll.count_documents({})
            
            # 获取最后更新时间
            last_doc = coll.find_one(sort=[("timestamp", -1)])
            last_update = "-"
            if last_doc and "timestamp" in last_doc:
                ts = last_doc["timestamp"]
                last_update = ts.strftime('%Y-%m-%d %H:%M') if hasattr(ts, 'strftime') else str(ts)[:16]
            
            collections.append({
                "name": coll_name,
                "count": doc_count,
                "last_update": last_update
            })
        
        return {
            "connected": True,
            "database": "trquant_extension",
            "collections": collections,
            "total_collections": len(collections)
        }
    except Exception as e:
        return {
            "connected": False,
            "message": str(e),
            "collections": []
        }


def export_database() -> Dict:
    """导出数据库"""
    if db is None:
        return {"ok": False, "error": "MongoDB未连接"}
    
    try:
        export_dir = DATA_ROOT / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        export_file = export_dir / f"db_export_{timestamp}.json"
        
        export_data = {}
        for coll_name in db.list_collection_names():
            docs = list(db[coll_name].find().limit(1000))
            for doc in docs:
                doc['_id'] = str(doc['_id'])
                for k, v in doc.items():
                    if hasattr(v, 'isoformat'):
                        doc[k] = v.isoformat()
            export_data[coll_name] = docs
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return {
            "ok": True,
            "file": str(export_file),
            "collections": len(export_data),
            "total_docs": sum(len(docs) for docs in export_data.values())
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ============================================================
# 概览统计
# ============================================================

def get_overview() -> Dict:
    """获取概览数据"""
    strategies = get_strategies()
    reports = get_reports()
    backtests = get_backtests()
    bt_stats = get_backtest_statistics()
    db_info = get_database_info()
    
    return {
        "strategy_count": len(strategies),
        "report_count": len(reports),
        "backtest_count": len(backtests),
        "avg_return": round(bt_stats["avg_return"], 2),
        "avg_sharpe": round(bt_stats["avg_sharpe"], 2),
        "avg_win_rate": round(bt_stats["avg_win_rate"], 1),
        "db_connected": db_info["connected"],
        "db_collections": db_info.get("total_collections", 0),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ============================================================
# 工作流数据
# ============================================================

def get_workflow_data() -> Dict:
    """获取工作流步骤的数据"""
    workflow_steps = {
        "market_trend": {"name": "市场趋势", "files": [], "db_count": 0},
        "mainlines": {"name": "投资主线", "files": [], "db_count": 0},
        "candidate_pool": {"name": "候选池", "files": [], "db_count": 0},
        "factors": {"name": "因子推荐", "files": [], "db_count": 0},
        "strategies": {"name": "策略生成", "files": [], "db_count": 0},
        "backtests": {"name": "回测验证", "files": [], "db_count": 0}
    }
    
    # 从报告目录获取
    if REPORTS_DIR.exists():
        for f in sorted(REPORTS_DIR.glob("trend_*.html"), reverse=True)[:5]:
            workflow_steps["market_trend"]["files"].append({
                "name": f.name,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
        
        for f in sorted(REPORTS_DIR.glob("mainline_*.html"), reverse=True)[:5]:
            workflow_steps["mainlines"]["files"].append({
                "name": f.name,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    
    # 从策略目录获取
    ptrade_dir = STRATEGY_DIRS.get("ptrade")
    if ptrade_dir and ptrade_dir.exists():
        for f in sorted(ptrade_dir.glob("strategy_*.py"), reverse=True)[:5]:
            workflow_steps["strategies"]["files"].append({
                "name": f.name,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    
    # 从回测目录获取
    if BACKTESTS_DIR.exists():
        for f in sorted(BACKTESTS_DIR.glob("*.json"), reverse=True)[:5]:
            workflow_steps["backtests"]["files"].append({
                "name": f.name,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    
    # 从MongoDB获取计数
    if db is not None:
        try:
            workflow_steps["market_trend"]["db_count"] = db.market_trend.count_documents({})
            workflow_steps["mainlines"]["db_count"] = db.mainline_scores.count_documents({})
            workflow_steps["candidate_pool"]["db_count"] = db.candidate_pool.count_documents({})
            workflow_steps["factors"]["db_count"] = db.factor_recommendations.count_documents({})
            workflow_steps["strategies"]["db_count"] = db.strategies.count_documents({})
            workflow_steps["backtests"]["db_count"] = db.backtest_results.count_documents({})
        except:
            pass
    
    return workflow_steps


# ============================================================
# Flask路由
# ============================================================

if app:
    @app.route('/')
    def index():
        """主页"""
        return render_template('dashboard.html')
    
    @app.route('/api/overview')
    def api_overview():
        """概览API"""
        return jsonify(get_overview())
    
    @app.route('/api/strategies')
    def api_strategies():
        """策略列表API"""
        return jsonify(get_strategies())
    
    # 策略详情API移至下方策略管理模块
    
    @app.route('/api/reports')
    def api_reports():
        """报告列表API"""
        return jsonify(get_reports())
    
    @app.route('/api/backtests')
    def api_backtests():
        """回测列表API"""
        return jsonify(get_backtests())
    
    @app.route('/api/backtest/stats')
    def api_backtest_stats():
        """回测统计API"""
        return jsonify(get_backtest_statistics())
    
    @app.route('/api/docs')
    def api_docs():
        """文档列表API"""
        return jsonify(get_documents())
    
    @app.route('/api/database')
    def api_database():
        """数据库信息API"""
        return jsonify(get_database_info())
    
    @app.route('/api/database/export', methods=['POST'])
    def api_database_export():
        """导出数据库API"""
        return jsonify(export_database())
    
    @app.route('/api/workflow')
    def api_workflow():
        """工作流数据API"""
        return jsonify(get_workflow_data())
    
    # 静态文件服务
    @app.route('/reports/<path:filename>')
    def serve_report(filename):
        """提供报告文件"""
        return send_from_directory(REPORTS_DIR, filename)
    
    @app.route('/docs/view/<path:filepath>')
    def serve_doc(filepath):
        """提供文档文件（MD自动渲染）"""
        doc_path = DOCS_DIR / filepath
        
        if not doc_path.exists():
            abort(404)
        
        if doc_path.suffix.lower() in ['.md', '.markdown']:
            try:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()
                
                if MARKDOWN_AVAILABLE:
                    html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc'])
                else:
                    html_content = _render_markdown_basic(md_text)
                
                return render_template('doc_viewer.html',
                    title=doc_path.stem,
                    html_content=html_content
                )
            except Exception as e:
                return f"<h3>文档渲染失败</h3><pre>{e}</pre>", 500
        
        return send_from_directory(DOCS_DIR, filepath)
    
    @app.route('/backtests/<path:filename>')
    def serve_backtest(filename):
        """提供回测文件"""
        return send_from_directory(BACKTESTS_DIR, filename)
    
    # ============================================================
    # 策略管理API
    # ============================================================
    
    @app.route('/api/strategy/list')
    def api_strategy_list():
        """策略列表（支持平台筛选）"""
        from .strategy_manager import get_all_strategies
        platform = request.args.get('platform')
        return jsonify(get_all_strategies(platform))
    
    @app.route('/api/strategy/<name>')
    def api_strategy_detail(name):
        """策略详情"""
        from .strategy_manager import get_strategy_detail
        result = get_strategy_detail(name)
        if result:
            return jsonify(result)
        return jsonify({"error": "策略不存在"}), 404
    
    @app.route('/api/strategy/create', methods=['POST'])
    def api_strategy_create():
        """创建策略"""
        from .strategy_manager import create_new_strategy
        data = request.json or {}
        return jsonify(create_new_strategy(
            name=data.get('name', ''),
            platform=data.get('platform', 'ptrade'),
            template=data.get('template'),
            description=data.get('description', ''),
            params=data.get('params')
        ))
    
    @app.route('/api/strategy/update', methods=['POST'])
    def api_strategy_update():
        """更新策略"""
        from .strategy_manager import update_existing_strategy
        data = request.json or {}
        return jsonify(update_existing_strategy(
            name=data.get('name', ''),
            code=data.get('code', '')
        ))
    
    @app.route('/api/strategy/delete', methods=['POST'])
    def api_strategy_delete():
        """删除策略"""
        from .strategy_manager import delete_existing_strategy
        data = request.json or {}
        return jsonify(delete_existing_strategy(
            name=data.get('name', ''),
            archive=data.get('archive', True)
        ))
    
    @app.route('/api/strategy/validate/<name>')
    def api_strategy_validate(name):
        """验证策略"""
        from .strategy_manager import validate_strategy_code
        return jsonify(validate_strategy_code(name))
    
    @app.route('/api/strategy/templates')
    def api_strategy_templates():
        """获取模板列表"""
        from .strategy_manager import get_strategy_templates
        return jsonify(get_strategy_templates())
    
    @app.route('/api/strategy/copy', methods=['POST'])
    def api_strategy_copy():
        """复制策略"""
        from .strategy_manager import copy_existing_strategy
        data = request.json or {}
        return jsonify(copy_existing_strategy(
            name=data.get('name', ''),
            new_name=data.get('new_name', ''),
            platform=data.get('platform')
        ))


# ============================================================
# 服务器启动
# ============================================================

def run_server(host='127.0.0.1', port=5000, debug=False):
    """启动Dashboard服务器"""
    if not FLASK_AVAILABLE:
        print("错误: Flask未安装，无法启动服务器")
        print("请运行: pip install flask flask-cors")
        return
    
    print(f"\n{'='*60}")
    print(f"  🐉 韬睿量化 - Extension Dashboard")
    print(f"{'='*60}")
    print(f"  📁 数据目录: {DATA_ROOT}")
    print(f"  🌐 服务地址: http://{host}:{port}")
    print(f"  📊 MongoDB: {'已连接' if db is not None else '未连接'}")
    print(f"{'='*60}\n")
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)


