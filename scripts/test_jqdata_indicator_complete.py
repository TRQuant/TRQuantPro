#!/usr/bin/env python3
"""
JQData Indicator表完整字段测试脚本

测试indicator表的所有字段，记录成功和失败的字段，生成HTML报告

Author: TRQuant Team
Date: 2025-12-20
"""

import sys
import os
from datetime import datetime, timedelta
import traceback
import json

# 添加项目路径
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from jqdata.client import JQDataClient
from config.config_manager import get_config_manager
from jqdatasdk import query, indicator, get_fundamentals, auth, get_account_info

# ==================== 配置 ====================

# Indicator表所有字段定义（基于官方文档）
INDICATOR_FIELDS = {
    # 基础字段
    "code": {"name": "股票代码", "category": "基础字段", "type": "string"},
    "day": {"name": "日期", "category": "基础字段", "type": "date"},
    "id": {"name": "记录ID", "category": "基础字段", "type": "int"},
    "pubDate": {"name": "发布日期", "category": "基础字段", "type": "date"},
    "statDate": {"name": "报告期", "category": "基础字段", "type": "string"},
    
    # 盈利能力指标
    "roe": {"name": "净资产收益率", "category": "盈利能力", "type": "float"},
    "roa": {"name": "总资产收益率", "category": "盈利能力", "type": "float"},
    "net_profit_margin": {"name": "净利率", "category": "盈利能力", "type": "float"},
    "gross_profit_margin": {"name": "毛利率", "category": "盈利能力", "type": "float"},
    "operating_profit": {"name": "营业利润", "category": "盈利能力", "type": "float"},
    "adjusted_profit": {"name": "调整后净利润", "category": "盈利能力", "type": "float"},
    
    # 增长率指标
    "inc_revenue_year_on_year": {"name": "营收同比增长", "category": "增长率", "type": "float"},
    "inc_revenue_annual": {"name": "营收年增长率", "category": "增长率", "type": "float"},
    "inc_net_profit_year_on_year": {"name": "净利润同比增长", "category": "增长率", "type": "float"},
    "inc_net_profit_annual": {"name": "净利润年增长率", "category": "增长率", "type": "float"},
    "inc_operation_profit_year_on_year": {"name": "营业利润同比增长", "category": "增长率", "type": "float"},
    "inc_operation_profit_annual": {"name": "营业利润年增长率", "category": "增长率", "type": "float"},
    "inc_total_revenue_year_on_year": {"name": "总收入同比增长", "category": "增长率", "type": "float"},
    "inc_total_revenue_annual": {"name": "总收入年增长率", "category": "增长率", "type": "float"},
    "inc_net_profit_to_shareholders_year_on_year": {"name": "归属净利润同比增长", "category": "增长率", "type": "float"},
    "inc_net_profit_to_shareholders_annual": {"name": "归属净利润年增长率", "category": "增长率", "type": "float"},
    
    # 每股指标
    "eps": {"name": "每股收益", "category": "每股指标", "type": "float"},
    
    # 比率指标
    "adjusted_profit_to_profit": {"name": "调整后净利润/净利润", "category": "比率指标", "type": "float"},
    "expense_to_total_revenue": {"name": "费用/总收入", "category": "比率指标", "type": "float"},
    "financing_expense_to_total_revenue": {"name": "财务费用/总收入", "category": "比率指标", "type": "float"},
    "ga_expense_to_total_revenue": {"name": "管理费用/总收入", "category": "比率指标", "type": "float"},
    "operating_expense_to_total_revenue": {"name": "营业费用/总收入", "category": "比率指标", "type": "float"},
    "net_profit_to_total_revenue": {"name": "净利润/总收入", "category": "比率指标", "type": "float"},
    "operation_profit_to_total_revenue": {"name": "营业利润/总收入", "category": "比率指标", "type": "float"},
    "operating_profit_to_profit": {"name": "营业利润/利润总额", "category": "比率指标", "type": "float"},
    "invesment_profit_to_profit": {"name": "投资收益/利润总额", "category": "比率指标", "type": "float"},
    
    # 现金流相关
    "ocf_to_operating_profit": {"name": "经营现金流/营业利润", "category": "现金流", "type": "float"},
    "ocf_to_revenue": {"name": "经营现金流/营业收入", "category": "现金流", "type": "float"},
    
    # 其他指标
    "goods_sale_and_service_to_revenue": {"name": "商品销售和服务/营业收入", "category": "其他", "type": "float"},
    "value_change_profit": {"name": "公允价值变动收益", "category": "其他", "type": "float"},
    "inc_return": {"name": "收益率", "category": "其他", "type": "float"},
}

# 测试股票（使用活跃股票）
TEST_SYMBOL = "000001.XSHE"  # 平安银行

# ==================== 测试函数 ====================

def test_indicator_field(field_name: str, jq_client: JQDataClient, test_date: str) -> dict:
    """
    测试单个indicator字段
    
    Returns:
        {
            "field": 字段名,
            "success": 是否成功,
            "error": 错误信息,
            "value": 返回值,
            "data_type": 数据类型
        }
    """
    result = {
        "field": field_name,
        "success": False,
        "error": None,
        "value": None,
        "data_type": None
    }
    
    try:
        # 获取字段属性
        field_attr = getattr(indicator, field_name, None)
        if field_attr is None:
            result["error"] = f"字段不存在: indicator.{field_name}"
            return result
        
        # 构建查询
        q = query(
            indicator.code,
            field_attr
        ).filter(
            indicator.code == TEST_SYMBOL
        )
        
        # 执行查询
        df = jq_client.get_fundamentals(q, date=test_date)
        
        if df is None or df.empty:
            result["error"] = "查询返回空数据"
            return result
        
        # 获取字段值
        if field_name in df.columns:
            value = df[field_name].iloc[0]
            result["value"] = value
            result["data_type"] = str(type(value).__name__)
            result["success"] = True
        else:
            result["error"] = f"字段不在返回结果中: {list(df.columns)}"
            
    except AttributeError as e:
        result["error"] = f"属性错误: {str(e)}"
    except Exception as e:
        result["error"] = f"查询异常: {str(e)}"
        result["traceback"] = traceback.format_exc()
    
    return result

# ==================== 主测试流程 ====================

def main():
    print("=" * 70)
    print("JQData Indicator表完整字段测试")
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
    
    if not jq_client.is_authenticated():
        print("❌ JQData认证失败")
        return
    
    # 获取账号信息
    try:
        auth(jq_config['username'], jq_config['password'])
        account_info = get_account_info()
        print(f"  ✅ 已连接")
        print(f"     账号: {account_info.get('mob', 'N/A')}")
        print(f"     每日流量限制: {account_info.get('query_count_limit', 'N/A'):,} 条")
        print(f"     数据范围: {account_info.get('date_range_start', 'N/A')[:10]} 至 {account_info.get('date_range_end', 'N/A')[:10]}")
    except Exception as e:
        print(f"  ⚠️ 获取账号信息失败: {e}")
    
    print()
    
    # 2. 获取测试日期
    print("📅 Step 2: 确定测试日期...")
    test_date = jq_client.get_available_end_date()
    print(f"  使用日期: {test_date} (权限范围内的最新日期)")
    print()
    
    # 3. 测试所有字段
    print("🔍 Step 3: 测试Indicator表字段...")
    print(f"  测试股票: {TEST_SYMBOL}")
    print(f"  总字段数: {len(INDICATOR_FIELDS)}")
    print()
    
    results = []
    success_count = 0
    fail_count = 0
    
    for i, (field_name, field_info) in enumerate(INDICATOR_FIELDS.items(), 1):
        print(f"  [{i}/{len(INDICATOR_FIELDS)}] 测试 {field_name} ({field_info['name']})...", end=" ")
        
        result = test_indicator_field(field_name, jq_client, test_date)
        result.update(field_info)
        results.append(result)
        
        if result["success"]:
            success_count += 1
            print(f"✅ 成功 (值: {result['value']})")
        else:
            fail_count += 1
            print(f"❌ 失败: {result['error']}")
    
    print()
    print("=" * 70)
    print("📊 测试结果统计")
    print("=" * 70)
    print(f"  总字段数: {len(INDICATOR_FIELDS)}")
    print(f"  ✅ 成功: {success_count}")
    print(f"  ❌ 失败: {fail_count}")
    print(f"  成功率: {success_count/len(INDICATOR_FIELDS)*100:.1f}%")
    print()
    
    # 4. 生成HTML报告
    print("📝 Step 4: 生成HTML报告...")
    html_report = generate_html_report(results, account_info, test_date)
    
    report_path = "/home/taotao/dev/QuantTest/TRQuant/docs/JQDATA_INDICATOR_TEST_REPORT.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"  ✅ HTML报告已保存: {report_path}")
    
    # 5. 生成JSON报告
    json_path = "/home/taotao/dev/QuantTest/TRQuant/docs/JQDATA_INDICATOR_TEST_REPORT.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            "test_date": test_date,
            "test_symbol": TEST_SYMBOL,
            "account_info": account_info,
            "summary": {
                "total": len(INDICATOR_FIELDS),
                "success": success_count,
                "failed": fail_count,
                "success_rate": success_count/len(INDICATOR_FIELDS)*100
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ JSON报告已保存: {json_path}")
    print()
    print("测试完成!")

# ==================== HTML报告生成 ====================

def generate_html_report(results: list, account_info: dict, test_date: str) -> str:
    """生成HTML格式的测试报告"""
    
    success_count = sum(1 for r in results if r["success"])
    fail_count = len(results) - success_count
    
    # 按类别分组
    by_category = {}
    for result in results:
        category = result.get("category", "未知")
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(result)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JQData Indicator表字段测试报告</title>
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
            max-width: 1200px;
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
        .summary-card.failed {{
            background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);
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
        .status-failed {{
            color: #e74c3c;
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
        <h1>📊 JQData Indicator表字段测试报告</h1>
        
        <div class="info-box">
            <strong>测试信息:</strong><br>
            测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            测试股票: {TEST_SYMBOL}<br>
            测试日期: {test_date}<br>
            账号类型: {'试用账户' if account_info.get('license') == 1 else '正式账户'}<br>
            每日流量限制: {account_info.get('query_count_limit', 'N/A'):,} 条
        </div>
        
        <h2>📈 测试结果概览</h2>
        <div class="summary">
            <div class="summary-card">
                <h3>总字段数</h3>
                <div class="number">{len(results)}</div>
            </div>
            <div class="summary-card success">
                <h3>✅ 成功</h3>
                <div class="number">{success_count}</div>
            </div>
            <div class="summary-card failed">
                <h3>❌ 失败</h3>
                <div class="number">{fail_count}</div>
            </div>
            <div class="summary-card">
                <h3>成功率</h3>
                <div class="number">{success_count/len(results)*100:.1f}%</div>
            </div>
        </div>
        
        <h2>📚 官方文档引用</h2>
        <div class="info-box">
            <strong>JQData官方文档:</strong><br>
            <a href="https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9885&keyword=Indicator" target="_blank">
                https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9885&keyword=Indicator
            </a><br><br>
            <strong>API说明:</strong><br>
            Indicator表提供财务指标数据，包括盈利能力、增长率、每股指标等。所有字段在试用账户中均可访问，无权限限制。
        </div>
        
        <h2>💻 完整测试代码</h2>
        <div class="code-block">
<code>#!/usr/bin/env python3
from jqdatasdk import query, indicator, get_fundamentals, auth

# 1. 认证
auth('your_username', 'your_password')

# 2. 测试单个字段
def test_field(field_name, symbol='000001.XSHE', date='2025-09-18'):
    try:
        field_attr = getattr(indicator, field_name)
        q = query(indicator.code, field_attr).filter(
            indicator.code == symbol
        )
        df = get_fundamentals(q, date=date)
        if df is not None and not df.empty:
            return True, df[field_name].iloc[0]
        return False, "无数据"
    except Exception as e:
        return False, str(e)

# 3. 测试所有字段
fields = ['roe', 'roa', 'gross_profit_margin', 'inc_revenue_year_on_year']
for fn in fns:
    success, result = test_field(field)
    print(f"{{field_name}}: {{status}} {{result}}")
</code>
        </div>
        
        <h2>📋 详细测试结果</h2>
"""
    
    # 按类别显示结果
    for category, category_results in sorted(by_category.items()):
        html += f"""
        <div class="category-section">
            <h3>{category} ({len(category_results)}个字段)</h3>
            <table>
                <thead>
                    <tr>
                        <th>字段名</th>
                        <th>中文名称</th>
                        <th>状态</th>
                        <th>返回值</th>
                        <th>数据类型</th>
                        <th>错误信息</th>
                    </tr>
                </thead>
                <tbody>
"""
        for result in category_results:
            status_class = "status-success" if result["success"] else "status-failed"
            status_text = "✅ 成功" if result["success"] else "❌ 失败"
            value_display = str(result["value"]) if result["value"] is not None else "-"
            error_display = result["error"] if result["error"] else "-"
            data_type_display = result["data_type"] if result["data_type"] else "-"
            
            html += f"""
                    <tr>
                        <td><code>{result["field"]}</code></td>
                        <td>{result["name"]}</td>
                        <td class="{status_class}">{status_text}</td>
                        <td>{value_display}</td>
                        <td>{data_type_display}</td>
                        <td>{error_display}</td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
        </div>
"""
    
    # 失败字段汇总
    failed_fields = [r for r in results if not r["success"]]
    if failed_fields:
        html += f"""
        <h2>⚠️ 失败字段分析</h2>
        <div class="warning-box">
            <strong>共 {len(failed_fields)} 个字段测试失败:</strong>
            <ul style="margin-top: 10px;">
"""
        for result in failed_fields:
            html += f"<li><code>{result['field']}</code> ({result['name']}): {result['error']}</li>"
        html += """
            </ul>
        </div>
"""
    
    # 使用建议
    html += f"""
        <h2>💡 使用建议</h2>
        <div class="info-box">
            <h3>1. 推荐使用的字段</h3>
            <p>以下字段测试成功，建议在项目中使用:</p>
            <ul>
"""
    for result in results:
        if result["success"]:
            html += f"<li><code>indicator.{result['field']}</code> - {result['name']}</li>"
    html += """
            </ul>
            
            <h3>2. 数据获取示例</h3>
            <div class="code-block">
<code>from jqdatasdk import query, indicator, get_fundamentals

# 查询多个字段
q = query(
    indicator.code,
    indicator.roe,
    indicator.roa,
    indicator.gross_profit_margin,
    indicator.inc_revenue_year_on_year,
    indicator.inc_net_profit_year_on_year,
    indicator.eps
).filter(
    indicator.code == '000001.XSHE'
)

df = get_fundamentals(q, date='2025-09-18')
print(df)</code>
            </div>
            
            <h3>3. 注意事项</h3>
            <ul>
                <li>所有indicator表字段在试用账户中均可访问，无权限限制</li>
                <li>建议使用权限范围内的日期进行查询</li>
                <li>部分字段可能返回None，需要做空值处理</li>
                <li>字段值的数据类型可能因股票而异，建议统一转换</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>TRQuant Team | JQData Indicator表字段测试</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    main()

