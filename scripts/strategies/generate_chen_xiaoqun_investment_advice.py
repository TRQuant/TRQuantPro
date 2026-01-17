#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成陈小群战法投资建议
====================

基于知识库和市场数据，生成陈小群战法的投资建议
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_search


def get_market_data():
    """获取当前市场数据"""
    try:
        import jqdatasdk as jq
        from config.config_manager import get_config_manager
        
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        
        # 获取最近交易日
        today = datetime.now()
        trade_days = jq.get_trade_days(end_date=today, count=10)
        
        if not trade_days:
            return None
        
        latest_day = trade_days[-1]
        prev_day = trade_days[-2] if len(trade_days) > 1 else trade_days[-1]
        
        # 获取涨停板数据（使用AKShare更准确）
        limit_up_count = 0
        try:
            import akshare as ak
            limit_up_data = ak.stock_zt_pool_em(date=latest_day.strftime('%Y%m%d'))
            if limit_up_data is not None and not limit_up_data.empty:
                limit_up_count = len(limit_up_data)
        except Exception as e:
            print(f"      ⚠️  AKShare数据获取失败: {e}")
            limit_up_count = 0
        
        # 获取指数数据
        market_info = {
            'latest_date': latest_day.strftime('%Y-%m-%d'),
            'prev_date': prev_day.strftime('%Y-%m-%d'),
            'limit_up_count': limit_up_count,
            'index_data': {}
        }
        
        try:
            index_codes = ['000300.XSHG', '000905.XSHG']
            for code in index_codes:
                try:
                    data = jq.get_price(code, start_date=prev_day, end_date=latest_day,
                                       frequency='daily', fields=['close', 'volume'])
                    if not data.empty:
                        market_info['index_data'][code] = {
                            'close': float(data['close'].iloc[-1]),
                            'volume': float(data['volume'].iloc[-1]) if 'volume' in data.columns else 0
                        }
                except:
                    pass
        except Exception as e:
            print(f"      ⚠️  指数数据获取失败: {e}")
        
        return market_info
        
    except Exception as e:
        print(f"⚠️  数据获取失败: {e}")
        return None


def judge_emotion_cycle(market_info):
    """判断情绪周期"""
    if not market_info:
        return "待确认"
    
    limit_up_count = market_info.get('limit_up_count', 0)
    
    if limit_up_count < 10:
        return "退潮期"
    elif limit_up_count < 30:
        return "启动期"
    elif limit_up_count < 60:
        return "加速期"
    else:
        return "过热期"


def generate_investment_advice(market_info, emotion_cycle):
    """生成投资建议"""
    
    advice = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "market_status": emotion_cycle,
        "market_data": market_info,
        "strategy_recommendation": "",
        "position_suggestion": "",
        "key_points": [],
        "risk_warnings": [],
        "next_steps": []
    }
    
    # 如果没有市场数据，给出通用建议
    if not market_info or emotion_cycle == "待确认":
        advice["strategy_recommendation"] = "等待市场数据确认"
        advice["position_suggestion"] = "轻仓观察（建议10%以内）"
        advice["key_points"] = [
            "当前无法获取实时市场数据，建议等待数据确认后再操作",
            "每日早盘9:35前扫描涨停股票，关注涨停家数",
            "如果涨停家数<10只，建议空仓等待",
            "如果涨停家数10-30只，可以使用首板卡位术（10%试错仓）",
            "如果涨停家数30-60只，可以使用龙头战法（50%+重仓）",
            "如果涨停家数>60只，建议逐步减仓（30-50%）"
        ]
        advice["risk_warnings"] = [
            "市场数据未确认，建议谨慎操作",
            "严格按照止损策略执行",
            "不要超过70%总仓位",
            "及时止盈，避免贪婪"
        ]
        advice["next_steps"] = [
            "每日早盘9:35前扫描涨停股票",
            "统计涨停家数和连板高度",
            "根据情绪周期判断选择合适的策略",
            "等待市场数据确认后再操作"
        ]
        return advice
    
    if emotion_cycle == "退潮期":
        advice["strategy_recommendation"] = "空仓等待"
        advice["position_suggestion"] = "0%仓位"
        advice["key_points"] = [
            "退潮期不适合游资战法",
            "涨停家数<10只，市场情绪低迷",
            "建议空仓等待更好的机会",
            "可以关注市场情绪指标的改善"
        ]
        advice["risk_warnings"] = [
            "退潮期操作风险极高",
            "即使符合条件，成功率也会大幅降低",
            "建议等待情绪周期转换"
        ]
        advice["next_steps"] = [
            "每日监控涨停家数和连板高度",
            "等待涨停家数>20只再考虑操作",
            "关注板块效应的出现"
        ]
        
    elif emotion_cycle == "启动期":
        advice["strategy_recommendation"] = "陈小群三板斧战法 - 首板卡位术"
        advice["position_suggestion"] = "轻仓试错（10%）"
        advice["key_points"] = [
            "涨停家数10-30只，市场情绪开始启动",
            "适合使用首板卡位术（10%试错仓）",
            "选股条件：早盘9:35前涨停，流通市值<30亿，封单量>2%",
            "板块内至少3只跟风股涨停形成板块效应",
            "严格止损：次日不涨停立即止损（-5%）"
        ]
        advice["risk_warnings"] = [
            "启动期仍有一定风险，需要严格止损",
            "不要重仓，保持10%试错仓",
            "如果板块效应不强，不建议操作"
        ]
        advice["next_steps"] = [
            "每日早盘9:35前扫描涨停股票",
            "筛选符合首板条件的股票",
            "确认板块效应后再介入",
            "设置严格止损，控制风险"
        ]
        
    elif emotion_cycle == "加速期":
        advice["strategy_recommendation"] = "陈小群龙头战法 - 重仓持有"
        advice["position_suggestion"] = "重仓持有（50%+）"
        advice["key_points"] = [
            "涨停家数30-60只，市场情绪高涨",
            "适合使用龙头战法，重仓持有龙头股",
            "选股标准：板块内涨幅最大或最早涨停的股票",
            "持有策略：不爱做T，看准就坚定持有到巅峰",
            "板块内至少3只跟风股涨停形成梯队效应"
        ]
        advice["risk_warnings"] = [
            "加速期虽然机会多，但也要控制总仓位不超过70%",
            "重点关注龙头股，避免跟风股",
            "如果板块效应减弱，及时减仓"
        ]
        advice["next_steps"] = [
            "识别市场总龙头",
            "在龙头启动期重仓介入",
            "坚定持有，不因短期波动而离场",
            "关注板块效应是否持续"
        ]
        
    elif emotion_cycle == "过热期":
        advice["strategy_recommendation"] = "陈小群合力情绪战法 - 逐步减仓"
        advice["position_suggestion"] = "逐步减仓（30%-50%）"
        advice["key_points"] = [
            "涨停家数>60只，市场情绪极度高涨",
            "适合使用合力情绪战法，跟随市场合力",
            "操作策略：逐步减仓，保留部分仓位享受最后涨幅",
            "重点关注：炸板率>30%时，风险极高",
            "及时止盈：出现见顶信号立即止盈"
        ]
        advice["risk_warnings"] = [
            "过热期风险极高，随时可能见顶",
            "炸板率>30%时，建议大幅减仓",
            "不要贪心，及时止盈保住收益"
        ]
        advice["next_steps"] = [
            "监控炸板率，如果>30%大幅减仓",
            "关注连板高度的变化",
            "如果板块效应减弱，立即止盈",
            "准备空仓等待退潮期结束"
        ]
    
    return advice


def format_advice_report(advice):
    """格式化建议报告"""
    report = []
    report.append("=" * 70)
    report.append("📊 陈小群战法投资建议")
    report.append("=" * 70)
    report.append("")
    report.append(f"📅 生成时间: {advice['date']}")
    report.append(f"📈 市场状态: {advice['market_status']}")
    
    if advice.get('market_data'):
        md = advice['market_data']
        report.append(f"📊 最新交易日: {md.get('latest_date', '未知')}")
        report.append(f"📊 涨停家数: {md.get('limit_up_count', 0)}只")
    
    report.append("")
    report.append("🎯 策略建议:")
    report.append(f"   {advice['strategy_recommendation']}")
    report.append("")
    report.append("💰 仓位建议:")
    report.append(f"   {advice['position_suggestion']}")
    report.append("")
    report.append("🔑 关键要点:")
    for point in advice['key_points']:
        report.append(f"   • {point}")
    report.append("")
    report.append("⚠️  风险提示:")
    for warning in advice['risk_warnings']:
        report.append(f"   • {warning}")
    report.append("")
    report.append("📝 后续步骤:")
    for step in advice['next_steps']:
        report.append(f"   {len(report) - len(advice['next_steps']) + advice['next_steps'].index(step)}. {step}")
    report.append("")
    report.append("=" * 70)
    
    return "\n".join(report)


def main():
    """主函数"""
    print("=" * 70)
    print("📊 生成陈小群战法投资建议")
    print("=" * 70)
    print()
    
    # 1. 获取市场数据
    print("1️⃣ 获取市场数据...")
    market_info = get_market_data()
    if market_info:
        print(f"   ✅ 获取成功")
        print(f"   📅 最新交易日: {market_info['latest_date']}")
        print(f"   📊 涨停家数: {market_info['limit_up_count']}只")
    else:
        print("   ⚠️  获取失败，将使用默认建议")
    print()
    
    # 2. 判断情绪周期
    print("2️⃣ 判断情绪周期...")
    emotion_cycle = judge_emotion_cycle(market_info)
    print(f"   ✅ 当前情绪周期: {emotion_cycle}")
    print()
    
    # 3. 生成投资建议
    print("3️⃣ 生成投资建议...")
    advice = generate_investment_advice(market_info, emotion_cycle)
    print("   ✅ 生成成功")
    print()
    
    # 4. 输出报告
    report = format_advice_report(advice)
    print(report)
    print()
    
    # 5. 保存报告
    output_file = TRQUANT_ROOT / "docs" / "strategies" / f"chen_xiaoqun_advice_{datetime.now().strftime('%Y%m%d')}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 陈小群战法投资建议\n\n")
        f.write(f"> **生成时间**: {advice['date']}\n\n")
        f.write(report)
        f.write("\n\n")
        f.write("## 详细说明\n\n")
        f.write("本建议基于以下知识库内容生成：\n\n")
        f.write("1. 陈小群三板斧战法\n")
        f.write("2. 陈小群龙头战法\n")
        f.write("3. 陈小群合力情绪战法\n")
        f.write("4. 情绪周期把控\n")
        f.write("5. 选股三高筛龙\n\n")
        f.write("---\n\n")
        f.write("**注意**: 本建议仅供参考，不构成投资建议。投资有风险，入市需谨慎。\n")
    
    print(f"💾 报告已保存到: {output_file}")
    print()
    
    # 6. 保存JSON格式
    json_file = TRQUANT_ROOT / "docs" / "strategies" / f"chen_xiaoqun_advice_{datetime.now().strftime('%Y%m%d')}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(advice, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"💾 JSON格式已保存到: {json_file}")
    print()


if __name__ == '__main__':
    main()
