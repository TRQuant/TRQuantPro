# -*- coding: utf-8 -*-
"""
A股策略管理API
==============

为Web仪表盘提供A股策略管理相关的API接口：
- 工作流程数据（市场趋势、投资主线、候选池、因子推荐）
- 回测历史
- 生成的报告和策略
"""

from flask import Blueprint, jsonify, request
from pathlib import Path
from datetime import datetime
import json

# 创建Blueprint
astock_bp = Blueprint('astock', __name__, url_prefix='/api/astock')

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


def get_mongodb():
    """获取MongoDB连接"""
    try:
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
        return client['trquant']
    except:
        return None


@astock_bp.route('/workflow')
def api_workflow():
    """获取工作流程产生的数据"""
    try:
        db = get_mongodb()
        if db is None:
            return jsonify({"success": False, "error": "MongoDB未连接"})
        
        # 获取市场趋势
        market_trend = db.market_trend.find_one(sort=[("date", -1)])
        
        # 获取投资主线
        mainlines = list(db.mainline_scores.find().sort("composite_score", -1).limit(20))
        for m in mainlines:
            m['_id'] = str(m['_id'])
            if 'timestamp' in m and hasattr(m['timestamp'], 'isoformat'):
                m['timestamp'] = m['timestamp'].isoformat()
        
        # 获取候选池
        candidate_pool = db.candidate_pool.find_one({"type": "latest"})
        if candidate_pool:
            candidate_pool['_id'] = str(candidate_pool['_id'])
            if 'timestamp' in candidate_pool and hasattr(candidate_pool['timestamp'], 'isoformat'):
                candidate_pool['timestamp'] = candidate_pool['timestamp'].isoformat()
        
        # 获取因子推荐
        factor_rec = db.factor_recommendations.find_one({"type": "latest"})
        if factor_rec:
            factor_rec['_id'] = str(factor_rec['_id'])
        
        return jsonify({
            "success": True,
            "data": {
                "market_trend": {
                    "phase": market_trend.get("market_phase", "未知") if market_trend else "未知",
                    "score": market_trend.get("composite_score", 0) if market_trend else 0,
                    "date": market_trend.get("date", "") if market_trend else "",
                    "short_term": market_trend.get("trend_short", "") if market_trend else "",
                    "mid_term": market_trend.get("trend_mid", "") if market_trend else "",
                    "long_term": market_trend.get("trend_long", "") if market_trend else ""
                },
                "mainlines": mainlines,
                "candidate_pool": {
                    "total": candidate_pool.get("total_count", 0) if candidate_pool else 0,
                    "stocks": candidate_pool.get("stocks", [])[:30] if candidate_pool else [],
                    "sources": candidate_pool.get("sources", []) if candidate_pool else []
                },
                "factor_recommendation": {
                    "factors": factor_rec.get("recommended_factors", []) if factor_rec else [],
                    "reasoning": factor_rec.get("reasoning", "") if factor_rec else "",
                    "market_environment": factor_rec.get("market_environment", "") if factor_rec else ""
                }
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@astock_bp.route('/backtests')
def api_backtests():
    """获取回测历史"""
    try:
        db = get_mongodb()
        if db is None:
            return jsonify({"success": False, "error": "MongoDB未连接"})
        
        backtests = list(db.backtest_results.find().sort("timestamp", -1).limit(50))
        for bt in backtests:
            bt['_id'] = str(bt['_id'])
            if 'timestamp' in bt and hasattr(bt['timestamp'], 'isoformat'):
                bt['timestamp'] = bt['timestamp'].isoformat()
        
        # 统计
        stats = {
            "total_count": len(backtests),
            "avg_return": sum(bt.get("total_return", 0) for bt in backtests) / max(len(backtests), 1),
            "best_return": max((bt.get("total_return", 0) for bt in backtests), default=0),
            "avg_sharpe": sum(bt.get("sharpe_ratio", 0) for bt in backtests) / max(len(backtests), 1)
        }
        
        return jsonify({"success": True, "data": backtests, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@astock_bp.route('/reports')
def api_reports():
    """获取工作流生成的报告"""
    reports = []
    reports_dir = PROJECT_ROOT / "reports"
    
    if reports_dir.exists():
        for f in sorted(reports_dir.rglob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)[:30]:
            rel_path = f.relative_to(PROJECT_ROOT)
            report_type = "趋势报告" if "trend" in f.name else "主线报告" if "mainline" in f.name else "报告"
            reports.append({
                "name": f.stem,
                "file": f.name,
                "path": str(rel_path),
                "type": report_type,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": f"{f.stat().st_size / 1024:.1f} KB",
                "url": f"/reports/{rel_path.as_posix()}"
            })
    
    return jsonify({"success": True, "data": reports, "total": len(reports)})


@astock_bp.route('/strategies')
def api_strategies():
    """获取工作流生成的策略"""
    strategies = []
    ptrade_dir = PROJECT_ROOT / "strategies" / "ptrade"
    
    if ptrade_dir.exists():
        for f in sorted(ptrade_dir.glob("*.py"), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.name.startswith("__"):
                continue
            
            # 读取策略元数据
            meta_file = f.with_name(f.stem + "_meta.json")
            meta = {}
            if meta_file.exists():
                try:
                    with open(meta_file, 'r', encoding='utf-8') as mf:
                        meta = json.load(mf)
                except:
                    pass
            
            strategies.append({
                "name": f.stem,
                "file": f.name,
                "path": str(f.relative_to(PROJECT_ROOT)),
                "type": meta.get("type", "ptrade"),
                "description": meta.get("description", ""),
                "factors": meta.get("factors", []),
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": f"{f.stat().st_size / 1024:.1f} KB"
            })
    
    # 统计
    stats = {
        "total": len(strategies),
        "ptrade": sum(1 for s in strategies if "strategy_" in s["name"]),
        "multi_factor": sum(1 for s in strategies if "multi_factor" in s["name"]),
        "other": sum(1 for s in strategies if "strategy_" not in s["name"] and "multi_factor" not in s["name"])
    }
    
    return jsonify({"success": True, "data": strategies, "stats": stats})


@astock_bp.route('/strategy/<name>')
def api_strategy_detail(name):
    """获取策略详情"""
    ptrade_dir = PROJECT_ROOT / "strategies" / "ptrade"
    strategy_file = ptrade_dir / f"{name}.py"
    
    if not strategy_file.exists():
        return jsonify({"success": False, "error": "策略不存在"})
    
    try:
        with open(strategy_file, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 读取元数据
        meta_file = strategy_file.with_name(f"{name}_meta.json")
        meta = {}
        if meta_file.exists():
            try:
                with open(meta_file, 'r', encoding='utf-8') as mf:
                    meta = json.load(mf)
            except:
                pass
        
        return jsonify({
            "success": True,
            "data": {
                "name": name,
                "code": code,
                "meta": meta,
                "modified": datetime.fromtimestamp(strategy_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": f"{strategy_file.stat().st_size / 1024:.1f} KB"
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@astock_bp.route('/summary')
def api_summary():
    """获取A股策略管理概览"""
    try:
        db = get_mongodb()
        
        # 统计各类数据
        summary = {
            "workflow": {
                "has_trend": False,
                "has_mainlines": False,
                "has_pool": False,
                "has_factors": False
            },
            "strategies": {"total": 0, "generated": 0},
            "reports": {"total": 0, "trend": 0, "mainline": 0},
            "backtests": {"total": 0, "avg_return": 0}
        }
        
        if db is not None:
            # 检查工作流数据
            summary["workflow"]["has_trend"] = db.market_trend.count_documents({}) > 0
            summary["workflow"]["has_mainlines"] = db.mainline_scores.count_documents({}) > 0
            summary["workflow"]["has_pool"] = db.candidate_pool.count_documents({}) > 0
            summary["workflow"]["has_factors"] = db.factor_recommendations.count_documents({}) > 0
            
            # 回测统计
            backtests = list(db.backtest_results.find())
            summary["backtests"]["total"] = len(backtests)
            if backtests:
                summary["backtests"]["avg_return"] = sum(bt.get("total_return", 0) for bt in backtests) / len(backtests)
        
        # 策略统计
        ptrade_dir = PROJECT_ROOT / "strategies" / "ptrade"
        if ptrade_dir.exists():
            all_strategies = list(ptrade_dir.glob("*.py"))
            summary["strategies"]["total"] = len([s for s in all_strategies if not s.name.startswith("__")])
            summary["strategies"]["generated"] = len(list(ptrade_dir.glob("strategy_*.py")))
        
        # 报告统计
        reports_dir = PROJECT_ROOT / "reports"
        if reports_dir.exists():
            all_reports = list(reports_dir.rglob("*.html"))
            summary["reports"]["total"] = len(all_reports)
            summary["reports"]["trend"] = len([r for r in all_reports if "trend" in r.name])
            summary["reports"]["mainline"] = len([r for r in all_reports if "mainline" in r.name])
        
        return jsonify({"success": True, "data": summary})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

