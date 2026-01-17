#!/usr/bin/env python3
"""
JQData Finance表字段测试脚本

测试STK_CASHFLOW_STATEMENT和STK_BALANCE_SHEET的所有字段
检查权限限制和字段名正确性

Author: TRQuant Team
Date: 2025-12-20
"""

import sys
import os
from datetime import datetime
import traceback
import json

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from jqdata.client import JQDataClient
from config.config_manager import get_config_manager
from jqdatasdk import query, finance, get_fundamentals, auth, get_account_info

# ==================== 配置 ====================

# 测试股票
TEST_SYMBOL = "000001.XSHE"  # 平安银行

# 现金流量表字段（基于官方文档和测试）
CASHFLOW_FIELDS = {
    # 基础字段
    "code": {"name": "股票代码", "category": "基础字段"},
    "pub_date": {"name": "发布日期", "category": "基础字段"},
    "stat_date": {"name": "报告期", "category": "基础字段"},
    
    # 经营活动现金流
    "net_operate_cash_flow": {"name": "经营活动产生的现金流量净额", "category": "经营活动"},
    "operating_cash_inflow": {"name": "经营活动现金流入小计", "category": "经营活动"},
    "operating_cash_outflow": {"name": "经营活动现金流出小计", "category": "经营活动"},
    "cash_received_from_sales": {"name": "销售商品、提供劳务收到的现金", "category": "经营活动"},
    "cash_paid_for_goods": {"name": "购买商品、接受劳务支付的现金", "category": "经营活动"},
    
    # 投资活动现金流
    "net_invest_cash_flow": {"name": "投资活动产生的现金流量净额", "category": "投资活动"},
    "invest_cash_inflow": {"name": "投资活动现金流入小计", "category": "投资活动"},
    "invest_cash_outflow": {"name": "投资活动现金流出小计", "category": "投资活动"},
    
    # 筹资活动现金流
    "net_finance_cash_flow": {"name": "筹资活动产生的现金流量净额", "category": "筹资活动"},
    "finance_cash_inflow": {"name": "筹资活动现金流入小计", "category": "筹资活动"},
    "finance_cash_outflow": {"name": "筹资活动现金流出小计", "category": "筹资活动"},
    
    # 其他
    "cash_equivalents": {"name": "现金及现金等价物净增加额", "category": "其他"},
    "beginning_cash_equivalents": {"name": "期初现金及现金等价物余额", "category": "其他"},
    "ending_cash_equivalents": {"name": "期末现金及现金等价物余额", "category": "其他"},
}

# 资产负债表字段（基于官方文档和测试）
BALANCE_SHEET_FIELDS = {
    # 基础字段
    "code": {"name": "股票代码", "category": "基础字段"},
    "pub_date": {"name": "发布日期", "category": "基础字段"},
    "stat_date": {"name": "报告期", "category": "基础字段"},
    
    # 资产
    "total_assets": {"name": "资产总计", "category": "资产"},
    "total_current_assets": {"name": "流动资产合计", "category": "资产"},
    "total_non_current_assets": {"name": "非流动资产合计", "category": "资产"},
    "monetary_funds": {"name": "货币资金", "category": "资产"},
    "accounts_receivable": {"name": "应收账款", "category": "资产"},
    "inventory": {"name": "存货", "category": "资产"},
    "fixed_assets": {"name": "固定资产", "category": "资产"},
    
    # 负债
    "total_liability": {"name": "负债合计", "category": "负债"},
    "total_current_liability": {"name": "流动负债合计", "category": "负债"},
    "total_non_current_liability": {"name": "非流动负债合计", "category": "负债"},
    "short_term_loan": {"name": "短期借款", "category": "负债"},
    "accounts_payable": {"name": "应付账款", "category": "负债"},
    
    # 所有者权益
    "total_equity": {"name": "所有者权益合计", "category": "所有者权益"},
    "total_shareholders_equity": {"name": "股东权益合计", "category": "所有者权益"},
    "paid_in_capital": {"name": "实收资本", "category": "所有者权益"},
    "retained_profit": {"name": "未分配利润", "category": "所有者权益"},
}

# ==================== 测试函数 ====================

def get_table_fields(table_obj):
    """获取表的所有字段"""
    fields = []
    for attr in dir(table_obj):
        if not attr.startswith('_') and not callable(getattr(table_obj, attr)):
            fields.append(attr)
    return fields

def test_finance_field(table_name, field_name, jq_client, test_date):
    """
    测试单个finance字段
    
    Returns:
        {
            "table": 表名,
            "field": 字段名,
            "success": 是否成功,
            "error": 错误信息,
            "error_type": 错误类型 (permission/field_not_found/other),
            "value": 返回值
        }
    """
    result = {
        "table": table_name,
        "field": field_name,
        "success": False,
        "error": None,
        "error_type": None,
        "value": None
    }
    
    try:
        # 获取表对象
        table_obj = getattr(finance, table_name, None)
        if table_obj is None:
            result["error"] = f"表不存在: finance.{table_name}"
            result["error_type"] = "table_not_found"
            return result
        
        # 获取字段属性
        field_attr = getattr(table_obj, field_name, None)
        if field_attr is None:
            result["error"] = f"字段不存在: {table_name}.{field_name}"
            result["error_type"] = "field_not_found"
            return result
        
        # 构建查询
        q = query(
            table_obj.code,
            field_attr
        ).filter(
            table_obj.code == TEST_SYMBOL
        )
        
        # 执行查询
        df = jq_client.get_fundamentals(q, date=test_date)
        
        # 检查错误
        if df is None:
            result["error"] = "查询返回None"
            result["error_type"] = "query_failed"
            return result
        
        if df.empty:
            result["error"] = "查询返回空数据"
            result["error_type"] = "empty_result"
            return result
        
        # 检查是否有"非法查询"错误
        if isinstance(df, str) and "非法查询" in df:
            result["error"] = "非法查询（权限限制）"
            result["error_type"] = "permission"
            return result
        
        # 获取字段值
        if field_name in df.columns:
            value = df[field_name].iloc[0]
            result["value"] = str(value) if value is not None else None
            result["success"] = True
        else:
            result["error"] = f"字段不在返回结果中: {list(df.columns)}"
            result["error_type"] = "field_not_in_result"
            
    except AttributeError as e:
        result["error"] = f"属性错误: {str(e)}"
        result["error_type"] = "attribute_error"
    except Exception as e:
        error_msg = str(e)
        if "非法查询" in error_msg:
            result["error"] = "非法查询（权限限制）"
            result["error_type"] = "permission"
        else:
            result["error"] = f"查询异常: {error_msg}"
            result["error_type"] = "other"
        result["traceback"] = traceback.format_exc()
    
    return result

# ==================== 主测试流程 ====================

def main():
    print("=" * 70)
    print("JQData Finance表字段测试")
    print("=" * 70)
    print()
    
    # 1. 连接JQData
    print("📡 Step 1: 连接JQData...")
    jq_client = JQDataClient()
    cm = get_config_manager()
    jq_config = cm.get_jqdata_config()
    
    if not jq_config:
        print("❌ 未找到JQData配置")
        return
    
    jq_client.authenticate(jq_config['username'], jq_config['password'])
    auth(jq_config['username'], jq_config['password'])
    
    if not jq_client.is_authenticated():
        print("❌ JQData认证失败")
        return
    
    # 获取账号信息
    try:
        account_info = get_account_info()
        print(f"  ✅ 已连接")
        print(f"     账号: {account_info.get('mob', 'N/A')}")
        print(f"     账号类型: {'试用账户' if account_info.get('license') == 1 else '正式账户'}")
        print(f"     每日流量限制: {account_info.get('query_count_limit', 'N/A'):,} 条")
    except Exception as e:
        print(f"  ⚠️ 获取账号信息失败: {e}")
        account_info = {}
    
    print()
    
    # 2. 获取测试日期
    print("📅 Step 2: 确定测试日期...")
    test_date = jq_client.get_available_end_date()
    print(f"  使用日期: {test_date} (权限范围内的最新日期)")
    print()
    
    # 3. 获取表的实际字段
    print("🔍 Step 3: 获取表的实际字段...")
    
    # 现金流量表
    cf_table = getattr(finance, "STK_CASHFLOW_STATEMENT", None)
    if cf_table:
        cf_actual_fields = get_table_fields(cf_table)
        print(f"  STK_CASHFLOW_STATEMENT: {len(cf_actual_fields)} 个字段")
        print(f"    示例字段: {cf_actual_fields[:10]}")
    else:
        print(f"  ⚠️ STK_CASHFLOW_STATEMENT 表不存在")
        cf_actual_fields = []
    
    # 资产负债表
    bs_table = getattr(finance, "STK_BALANCE_SHEET", None)
    if bs_table:
        bs_actual_fields = get_table_fields(bs_table)
        print(f"  STK_BALANCE_SHEET: {len(bs_actual_fields)} 个字段")
        print(f"    示例字段: {bs_actual_fields[:10]}")
    else:
        print(f"  ⚠️ STK_BALANCE_SHEET 表不存在")
        bs_actual_fields = []
    
    print()
    
    # 4. 测试现金流量表字段
    print("💧 Step 4: 测试现金流量表字段...")
    print(f"  测试股票: {TEST_SYMBOL}")
    print(f"  测试字段数: {len(CASHFLOW_FIELDS)}")
    print()
    
    cf_results = []
    cf_success = 0
    cf_permission_error = 0
    cf_field_not_found = 0
    
    for i, (field_name, field_info) in enumerate(CASHFLOW_FIELDS.items(), 1):
        print(f"  [{i}/{len(CASHFLOW_FIELDS)}] 测试 {field_name} ({field_info['name']})...", end=" ")
        
        result = test_finance_field("STK_CASHFLOW_STATEMENT", field_name, jq_client, test_date)
        result.update(field_info)
        cf_results.append(result)
        
        if result["success"]:
            cf_success += 1
            print(f"✅ 成功")
        elif result["error_type"] == "permission":
            cf_permission_error += 1
            print(f"🚫 权限限制")
        elif result["error_type"] == "field_not_found":
            cf_field_not_found += 1
            print(f"❌ 字段不存在")
        else:
            print(f"⚠️ {result['error']}")
    
    print()
    
    # 5. 测试资产负债表字段
    print("📊 Step 5: 测试资产负债表字段...")
    print(f"  测试字段数: {len(BALANCE_SHEET_FIELDS)}")
    print()
    
    bs_results = []
    bs_success = 0
    bs_permission_error = 0
    bs_field_not_found = 0
    
    for i, (field_name, field_info) in enumerate(BALANCE_SHEET_FIELDS.items(), 1):
        print(f"  [{i}/{len(BALANCE_SHEET_FIELDS)}] 测试 {field_name} ({field_info['name']})...", end=" ")
        
        result = test_finance_field("STK_BALANCE_SHEET", field_name, jq_client, test_date)
        result.update(field_info)
        bs_results.append(result)
        
        if result["success"]:
            bs_success += 1
            print(f"✅ 成功")
        elif result["error_type"] == "permission":
            bs_permission_error += 1
            print(f"🚫 权限限制")
        elif result["error_type"] == "field_not_found":
            bs_field_not_found += 1
            print(f"❌ 字段不存在")
        else:
            print(f"⚠️ {result['error']}")
    
    print()
    print("=" * 70)
    print("📊 测试结果统计")
    print("=" * 70)
    print()
    print("现金流量表 (STK_CASHFLOW_STATEMENT):")
    print(f"  总字段数: {len(CASHFLOW_FIELDS)}")
    print(f"  ✅ 成功: {cf_success}")
    print(f"  🚫 权限限制: {cf_permission_error}")
    print(f"  ❌ 字段不存在: {cf_field_not_found}")
    print()
    print("资产负债表 (STK_BALANCE_SHEET):")
    print(f"  总字段数: {len(BALANCE_SHEET_FIELDS)}")
    print(f"  ✅ 成功: {bs_success}")
    print(f"  🚫 权限限制: {bs_permission_error}")
    print(f"  ❌ 字段不存在: {bs_field_not_found}")
    print()
    
    # 6. 生成HTML报告
    print("📝 Step 6: 生成HTML报告...")
    html_report = generate_html_report(
        cf_results, bs_results, 
        cf_actual_fields, bs_actual_fields,
        account_info, test_date
    )
    
    report_path = "/home/taotao/dev/QuantTest/TRQuant/docs/JQDATA_FINANCE_TABLES_TEST_REPORT.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"  ✅ HTML报告已保存: {report_path}")
    print()
    print("测试完成!")

# ==================== HTML报告生成 ====================

def generate_html_report(cf_results, bs_results, cf_actual_fields, bs_actual_fields, account_info, test_date):
    """生成HTML格式的测试报告"""
    
    cf_success = sum(1 for r in cf_results if r["success"])
    cf_permission = sum(1 for r in cf_results if r["error_type"] == "permission")
    cf_not_found = sum(1 for r in cf_results if r["error_type"] == "field_not_found")
    
    bs_success = sum(1 for r in bs_results if r["success"])
    bs_permission = sum(1 for r in bs_results if r["error_type"] == "permission")
    bs_not_found = sum(1 for r in bs_results if r["error_type"] == "field_not_found")
    
    # 按类别分组
    cf_by_category = {}
    for r in cf_results:
        cat = r.get("category", "未知")
        if cat not in cf_by_category:
            cf_by_category[cat] = []
        cf_by_category[cat].append(r)
    
    bs_by_category = {}
    for r in bs_results:
        cat = r.get("category", "未知")
        if cat not in bs_by_category:
            bs_by_category[cat] = []
        bs_by_category[cat].append(r)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JQData Finance表字段测试报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-left: 10px;
            border-left: 4px solid #3498db;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-card.success {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        .summary-card.permission {{
            background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
        }}
        .summary-card.notfound {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .summary-card h3 {{
            color: white;
            margin: 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .summary-card .number {{
            font-size: 36px;
            font-weight: bold;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .status-success {{
            color: #27ae60;
            font-weight: bold;
        }}
        .status-permission {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .status-notfound {{
            color: #f39c12;
            font-weight: bold;
        }}
        .code-block {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
        }}
        .code-block code {{
            color: #f8f8f2;
        }}
        .info-box {{
            background: #e8f4f8;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .warning-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .error-box {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .category-section {{
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #777;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 JQData Finance表字段测试报告</h1>
        
        <div class="info-box">
            <strong>测试信息:</strong><br>
            测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            测试股票: {TEST_SYMBOL}<br>
            测试日期: {test_date}<br>
            账号类型: {'试用账户' if account_info.get('license') == 1 else '正式账户'}<br>
            每日流量限制: {account_info.get('query_count_limit', 'N/A'):,} 条
        </div>
        
        <h2>📈 测试结果概览</h2>
        
        <h3>现金流量表 (STK_CASHFLOW_STATEMENT)</h3>
        <div class="summary">
            <div class="summary-card">
                <h3>总字段数</h3>
                <div class="number">{len(cf_results)}</div>
            </div>
            <div class="summary-card success">
                <h3>✅ 成功</h3>
                <div class="number">{cf_success}</div>
            </div>
            <div class="summary-card permission">
                <h3>🚫 权限限制</h3>
                <div class="number">{cf_permission}</div>
            </div>
            <div class="summary-card notfound">
                <h3>❌ 字段不存在</h3>
                <div class="number">{cf_not_found}</div>
            </div>
        </div>
        
        <h3>资产负债表 (STK_BALANCE_SHEET)</h3>
        <div class="summary">
            <div class="summary-card">
                <h3>总字段数</h3>
                <div class="number">{len(bs_results)}</div>
            </div>
            <div class="summary-card success">
                <h3>✅ 成功</h3>
                <div class="number">{bs_success}</div>
            </div>
            <div class="summary-card permission">
                <h3>🚫 权限限制</h3>
                <div class="number">{bs_permission}</div>
            </div>
            <div class="summary-card notfound">
                <h3>❌ 字段不存在</h3>
                <div class="number">{bs_not_found}</div>
            </div>
        </div>
        
        <h2>📚 官方文档引用</h2>
        <div class="info-box">
            <strong>JQData官方文档:</strong><br>
            <a href="https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9886" target="_blank">
                现金流量表: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9886
            </a><br>
            <a href="https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9887" target="_blank">
                资产负债表: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9887
            </a><br>
            <a href="https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9898" target="_blank">
                现金流量表详细说明: https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9898
            </a><br><br>
            <strong>API说明:</strong><br>
            Finance表提供上市公司财务数据，包括现金流量表、资产负债表、利润表等。
            部分表在试用账户中可能受权限限制。
        </div>
        
        <h2>💻 完整测试代码</h2>
        <div class="code-block">
<code>#!/usr/bin/env python3
from jqdatasdk import query, finance, get_fundamentals, auth

# 1. 认证
auth('your_username', 'your_password')

# 2. 测试现金流量表字段
def test_cashflow_field(field_name, symbol='000001.XSHE', date='2025-09-18'):
    try:
        field_attr = getattr(finance.STK_CASHFLOW_STATEMENT, field_name)
        q = query(
            finance.STK_CASHFLOW_STATEMENT.code,
            field_attr
        ).filter(
            finance.STK_CASHFLOW_STATEMENT.code == symbol
        )
        df = get_fundamentals(q, date=date)
        if df is not None and not df.empty:
            return True, df[field_name].iloc[0]
        return False, "无数据或权限限制"
    except Exception as e:
        return False, str(e)

# 3. 测试资产负债表字段
def test_balance_field(field_name, symbol='000001.XSHE', date='2025-09-18'):
    try:
        field_attr = getattr(finance.STK_BALANCE_SHEET, field_name)
        q = query(
            finance.STK_BALANCE_SHEET.code,
            field_attr
        ).filter(
            finance.STK_BALANCE_SHEET.code == symbol
        )
        df = get_fundamentals(q, date=date)
        if df is not None and not df.empty:
            return True, df[field_name].iloc[0]
        return False, "无数据或权限限制"
    except Exception as e:
        return False, str(e)

# 4. 测试示例
cf_fields = ['net_operate_cash_flow', 'net_invest_cash_flow']
for field in cf_fields:
    success, result = test_cashflow_field(field)
    status = '✅' if success else '❌'
    print(f"{{field}}: {{status}} {{result}}")
</code>
        </div>
        
        <h2>📋 详细测试结果</h2>
        
        <h3>现金流量表 (STK_CASHFLOW_STATEMENT)</h3>
"""
    
    # 显示实际字段列表
    if cf_actual_fields:
        html += f"""
        <div class="info-box">
            <strong>表的实际字段 ({len(cf_actual_fields)}个):</strong><br>
            {', '.join(cf_actual_fields[:20])}
            {f'... 等共{len(cf_actual_fields)}个字段' if len(cf_actual_fields) > 20 else ''}
        </div>
"""
    
    # 按类别显示结果
    for category, category_results in sorted(cf_by_category.items()):
        html += f"""
        <div class="category-section">
            <h4>{category} ({len(category_results)}个字段)</h4>
            <table>
                <thead>
                    <tr>
                        <th>字段名</th>
                        <th>中文名称</th>
                        <th>状态</th>
                        <th>返回值</th>
                        <th>错误信息</th>
                    </tr>
                </thead>
                <tbody>
"""
        for result in category_results:
            if result["success"]:
                status_class = "status-success"
                status_text = "✅ 成功"
            elif result["error_type"] == "permission":
                status_class = "status-permission"
                status_text = "🚫 权限限制"
            elif result["error_type"] == "field_not_found":
                status_class = "status-notfound"
                status_text = "❌ 字段不存在"
            else:
                status_class = "status-notfound"
                status_text = "⚠️ 其他错误"
            
            value_display = result["value"] if result["value"] else "-"
            error_display = result["error"] if result["error"] else "-"
            
            html += f"""
                    <tr>
                        <td><code>{result["field"]}</code></td>
                        <td>{result["name"]}</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>{value_display}</td>
                        <td>{error_display}</td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
        </div>
"""
    
    html += """
        <h3>资产负债表 (STK_BALANCE_SHEET)</h3>
"""
    
    # 显示实际字段列表
    if bs_actual_fields:
        html += f"""
        <div class="info-box">
            <strong>表的实际字段 ({len(bs_actual_fields)}个):</strong><br>
            {', '.join(bs_actual_fields[:20])}
            {f'... 等共{len(bs_actual_fields)}个字段' if len(bs_actual_fields) > 20 else ''}
        </div>
"""
    
    # 按类别显示结果
    for category, category_results in sorted(bs_by_category.items()):
        html += f"""
        <div class="category-section">
            <h4>{category} ({len(category_results)}个字段)</h4>
            <table>
                <thead>
                    <tr>
                        <th>字段名</th>
                        <th>中文名称</th>
                        <th>状态</th>
                        <th>返回值</th>
                        <th>错误信息</th>
                    </tr>
                </thead>
                <tbody>
"""
        for result in category_results:
            if result["success"]:
                status_class = "status-success"
                status_text = "✅ 成功"
            elif result["error_type"] == "permission":
                status_class = "status-permission"
                status_text = "🚫 权限限制"
            elif result["error_type"] == "field_not_found":
                status_class = "status-notfound"
                status_text = "❌ 字段不存在"
            else:
                status_class = "status-notfound"
                status_text = "⚠️ 其他错误"
            
            value_display = result["value"] if result["value"] else "-"
            error_display = result["error"] if result["error"] else "-"
            
            html += f"""
                    <tr>
                        <td><code>{result["field"]}</code></td>
                        <td>{result["name"]}</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>{value_display}</td>
                        <td>{error_display}</td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
        </div>
"""
    
    # 权限限制说明
    if cf_permission > 0 or bs_permission > 0:
        html += f"""
        <h2>⚠️ 权限限制说明</h2>
        <div class="warning-box">
            <strong>权限限制字段:</strong><br>
            <ul style="margin-top: 10px;">
"""
        for r in cf_results + bs_results:
            if r["error_type"] == "permission":
                html += f"<li><code>{r['table']}.{r['field']}</code> ({r['name']}): {r['error']}</li>"
        html += """
            </ul>
            <p style="margin-top: 10px;">
                <strong>说明:</strong> 试用账户访问finance表的现金流量表和资产负债表时，可能返回"非法查询"错误。
                这是试用账户的功能限制，需要升级到正式账户才能访问完整数据。
            </p>
        </div>
"""
    
    # 字段不存在说明
    if cf_not_found > 0 or bs_not_found > 0:
        html += f"""
        <h2>❌ 字段不存在说明</h2>
        <div class="error-box">
            <strong>字段不存在 ({cf_not_found + bs_not_found}个):</strong><br>
            <ul style="margin-top: 10px;">
"""
        for r in cf_results + bs_results:
            if r["error_type"] == "field_not_found":
                html += f"<li><code>{r['table']}.{r['field']}</code> ({r['name']}): 字段不存在</li>"
        html += """
            </ul>
            <p style="margin-top: 10px;">
                <strong>说明:</strong> 这些字段在表中不存在，可能是字段名错误或已废弃。
                请参考官方文档使用正确的字段名。
            </p>
        </div>
"""
    
    # 使用建议
    html += f"""
        <h2>💡 使用建议</h2>
        <div class="info-box">
            <h3>1. 字段名规范</h3>
            <p>JQData使用<strong>snake_case</strong>（下划线命名）规范：</p>
            <ul>
                <li>✅ 正确: <code>net_operate_cash_flow</code>, <code>total_assets</code></li>
                <li>❌ 错误: <code>N_CASHFLOW_ACT_OPERATE</code>, <code>TOTAL_ASSETS</code></li>
            </ul>
            
            <h3>2. 权限限制处理</h3>
            <p>如果遇到权限限制，可以使用替代方案：</p>
            <ul>
                <li>使用indicator表的代理指标（如<code>ocf_to_operating_profit</code>）</li>
                <li>使用默认值或估算值</li>
                <li>升级到正式账户获取完整数据</li>
            </ul>
            
            <h3>3. 字段查找方法</h3>
            <div class="code-block">
<code>from jqdatasdk import finance

# 查看表的所有字段
cf_fields = [attr for attr in dir(finance.STK_CASHFLOW_STATEMENT) 
             if not attr.startswith('_')]
bs_fields = [attr for attr in dir(finance.STK_BALANCE_SHEET) 
             if not attr.startswith('_')]

print("现金流量表字段:", cf_fields)
print("资产负债表字段:", bs_fields)</code>
            </div>
        </div>
        
        <div class="footer">
            <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>TRQuant Team | JQData Finance表字段测试</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    main()

