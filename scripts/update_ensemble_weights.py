#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据验证结果更新集成模型权重
================================

从验证报告中提取各模型的准确率，并更新EnsembleMarketTrendAnalyzer的权重。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import re
from pathlib import Path
from typing import Dict, Optional

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

def extract_accuracies_from_report(report_path: Path) -> Dict[str, float]:
    """
    从验证报告中提取各模型的准确率
    
    Args:
        report_path: 验证报告文件路径
    
    Returns:
        Dict: {模型名: 准确率}
    """
    if not report_path.exists():
        print(f"❌ 报告文件不存在: {report_path}")
        return {}
    
    content = report_path.read_text(encoding='utf-8')
    accuracies = {}
    
    # 匹配模式：模型名: XX.X% 或 准确率: XX.X%
    patterns = [
        r'##\s+(\w+)\s+模型.*?准确率[：:]\s*(\d+\.?\d*)%',
        r'###\s+(\w+).*?准确率[：:]\s*(\d+\.?\d*)%',
        r'(\w+)\s+模型.*?准确率[：:]\s*(\d+\.?\d*)%',
        r'(\w+).*?准确率[：:]\s*(\d+\.?\d*)%',
    ]
    
    # 模型名称映射
    model_name_map = {
        'HMM': 'HMM',
        'Technical': 'Technical',
        'Trend': 'Technical',
        'Breadth': 'Breadth',
        'MarketBreadth': 'Breadth',
        'Sentiment': 'Sentiment',
        'JQDataSentiment': 'Sentiment',
    }
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            model_name = match.group(1)
            accuracy_str = match.group(2)
            
            # 映射模型名称
            for key, value in model_name_map.items():
                if key.lower() in model_name.lower():
                    model_name = value
                    break
            
            try:
                accuracy = float(accuracy_str) / 100.0
                if model_name in ['HMM', 'Technical', 'Breadth', 'Sentiment']:
                    if model_name not in accuracies or accuracy > accuracies[model_name]:
                        accuracies[model_name] = accuracy
            except ValueError:
                continue
    
    # 如果没找到，尝试查找表格
    if not accuracies:
        # 查找表格格式
        table_pattern = r'\|\s*(\w+)\s*\|.*?\|.*?\|.*?(\d+\.?\d*)%'
        matches = re.finditer(table_pattern, content, re.IGNORECASE)
        for match in matches:
            model_name = match.group(1)
            accuracy_str = match.group(2)
            
            for key, value in model_name_map.items():
                if key.lower() in model_name.lower():
                    model_name = value
                    break
            
            try:
                accuracy = float(accuracy_str) / 100.0
                if model_name in ['HMM', 'Technical', 'Breadth', 'Sentiment']:
                    accuracies[model_name] = accuracy
            except ValueError:
                continue
    
    return accuracies


def update_ensemble_weights(accuracies: Dict[str, float]):
    """
    更新集成模型的权重
    
    Args:
        accuracies: {模型名: 准确率}
    """
    ensemble_file = PROJECT_ROOT / "core" / "ensemble_market_trend.py"
    
    if not ensemble_file.exists():
        print(f"❌ 文件不存在: {ensemble_file}")
        return False
    
    content = ensemble_file.read_text(encoding='utf-8')
    
    # 更新model_accuracies字典
    for model_name, accuracy in accuracies.items():
        # 查找并替换
        pattern = f"'{model_name}':\\s*\\d+\\.?\\d*"
        replacement = f"'{model_name}': {accuracy:.3f}"
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"✅ 更新 {model_name} 准确率: {accuracy:.1%}")
        else:
            print(f"⚠️  未找到 {model_name} 的准确率配置")
    
    # 保存文件
    ensemble_file.write_text(content, encoding='utf-8')
    print(f"\n✅ 已更新 {ensemble_file}")
    
    return True


def main():
    """主函数"""
    output_dir = PROJECT_ROOT / "output" / "model_validation"
    
    # 查找最新的验证报告
    report_files = sorted(output_dir.glob("individual_models_validation_*.md"), reverse=True)
    
    if not report_files:
        print("❌ 未找到验证报告文件")
        print(f"   请检查目录: {output_dir}")
        return
    
    latest_report = report_files[0]
    print(f"📄 使用最新报告: {latest_report.name}")
    print("")
    
    # 提取准确率
    accuracies = extract_accuracies_from_report(latest_report)
    
    if not accuracies:
        print("❌ 未能从报告中提取准确率")
        print("   请手动检查报告文件并更新")
        return
    
    print("📊 提取的准确率:")
    for model_name, accuracy in accuracies.items():
        print(f"   {model_name}: {accuracy:.1%}")
    print("")
    
    # 更新权重
    if update_ensemble_weights(accuracies):
        print("\n✅ 权重更新完成！")
        print("\n下一步: 运行回测验证脚本")
        print("   python scripts/backtest_ensemble_model.py")
    else:
        print("\n❌ 权重更新失败")


if __name__ == '__main__':
    main()
