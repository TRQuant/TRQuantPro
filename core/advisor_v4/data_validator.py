#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证和清洗模块
==================

功能：
1. 验证高收益案例数据的完整性、一致性和合理性
2. 清洗异常数据、重复数据、缺失数据
3. 数据质量报告

设计原则：
- 数据可靠性优先：确保训练数据质量
- 常识性检查：收益率、市值、估值等指标应在合理范围
- 可追溯性：记录所有清洗操作，便于审计
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    total_records: int
    valid_records: int
    invalid_records: int
    issues: List[Dict[str, any]] = field(default_factory=list)
    cleaned_data: Optional[pd.DataFrame] = None
    report: str = ""


@dataclass
class DataQualityConfig:
    """数据质量配置"""
    # 收益率范围（常识性检查）
    min_return_pct: float = 5.0   # 最小收益率（%）
    max_return_pct: float = 100.0  # 最大收益率（%），超过100%需要特别验证
    
    # 市值范围（常识性检查）
    min_market_cap: float = 1.0   # 最小市值（亿元）
    max_market_cap: float = 50000.0  # 最大市值（亿元）
    
    # PE/PB范围（常识性检查）
    min_pe: float = -100.0   # 允许负PE（亏损公司）
    max_pe: float = 1000.0   # 最大PE
    min_pb: float = 0.1      # 最小PB
    max_pb: float = 50.0     # 最大PB
    
    # 缺失值处理
    max_missing_ratio: float = 0.3  # 最大缺失值比例（30%）
    
    # 重复数据
    remove_duplicates: bool = True
    
    # 异常值检测
    use_iqr_outlier_detection: bool = True  # 使用IQR方法检测异常值
    iqr_factor: float = 3.0  # IQR倍数


class DataValidator:
    """数据验证器"""
    
    def __init__(self, config: Optional[DataQualityConfig] = None, verbose: bool = True):
        self.config = config or DataQualityConfig()
        self.verbose = verbose
    
    def validate_and_clean(
        self,
        df: pd.DataFrame,
        required_columns: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        验证和清洗数据
        
        Args:
            df: 原始数据
            required_columns: 必需列（如果为None，使用默认必需列）
        
        Returns:
            ValidationResult
        """
        if self.verbose:
            print(f"\n{'='*70}")
            print("【数据验证和清洗】")
            print(f"{'='*70}")
            print(f"原始记录数: {len(df)}")
        
        result = ValidationResult(
            is_valid=False,
            total_records=len(df),
            valid_records=0,
            invalid_records=0,
        )
        
        issues = []
        cleaned_df = df.copy()
        
        # 1. 检查必需列
        if required_columns is None:
            required_columns = ['code', 'date', 'return_5d']
        
        missing_cols = [col for col in required_columns if col not in cleaned_df.columns]
        if missing_cols:
            issues.append({
                'type': 'missing_columns',
                'severity': 'error',
                'message': f'缺少必需列: {missing_cols}',
                'count': len(missing_cols)
            })
            if self.verbose:
                print(f"❌ 缺少必需列: {missing_cols}")
            result.issues = issues
            return result
        
        # 2. 检查重复数据
        if self.config.remove_duplicates:
            duplicates = cleaned_df.duplicated(subset=['code', 'date'], keep='first')
            dup_count = duplicates.sum()
            if dup_count > 0:
                issues.append({
                    'type': 'duplicates',
                    'severity': 'warning',
                    'message': f'发现 {dup_count} 条重复记录',
                    'count': dup_count
                })
                cleaned_df = cleaned_df[~duplicates].reset_index(drop=True)
                if self.verbose:
                    print(f"⚠️ 移除 {dup_count} 条重复记录")
        
        # 3. 常识性检查：收益率范围
        if 'return_5d' in cleaned_df.columns:
            invalid_returns = (
                (cleaned_df['return_5d'] < self.config.min_return_pct) |
                (cleaned_df['return_5d'] > self.config.max_return_pct)
            )
            invalid_count = invalid_returns.sum()
            if invalid_count > 0:
                issues.append({
                    'type': 'invalid_return_range',
                    'severity': 'error',
                    'message': f'收益率超出合理范围 [{self.config.min_return_pct}%, {self.config.max_return_pct}%]',
                    'count': invalid_count,
                    'examples': cleaned_df[invalid_returns][['code', 'date', 'return_5d']].head(5).to_dict('records')
                })
                cleaned_df = cleaned_df[~invalid_returns].reset_index(drop=True)
                if self.verbose:
                    print(f"❌ 移除 {invalid_count} 条收益率异常记录")
        
        # 4. 常识性检查：市值范围
        if 'market_cap' in cleaned_df.columns:
            invalid_caps = (
                (cleaned_df['market_cap'] < self.config.min_market_cap) |
                (cleaned_df['market_cap'] > self.config.max_market_cap)
            )
            invalid_count = invalid_caps.sum()
            if invalid_count > 0:
                issues.append({
                    'type': 'invalid_market_cap',
                    'severity': 'warning',
                    'message': f'市值超出合理范围 [{self.config.min_market_cap}, {self.config.max_market_cap}] 亿元',
                    'count': invalid_count
                })
                cleaned_df = cleaned_df[~invalid_caps].reset_index(drop=True)
                if self.verbose:
                    print(f"⚠️ 移除 {invalid_count} 条市值异常记录")
        
        # 5. 常识性检查：PE/PB范围
        if 'pe' in cleaned_df.columns:
            invalid_pe = (
                (cleaned_df['pe'] < self.config.min_pe) |
                (cleaned_df['pe'] > self.config.max_pe)
            )
            invalid_count = invalid_pe.sum()
            if invalid_count > 0:
                issues.append({
                    'type': 'invalid_pe',
                    'severity': 'warning',
                    'message': f'PE超出合理范围 [{self.config.min_pe}, {self.config.max_pe}]',
                    'count': invalid_count
                })
                # PE异常不直接删除，标记为异常值
                cleaned_df.loc[invalid_pe, 'pe'] = np.nan
        
        if 'pb' in cleaned_df.columns:
            invalid_pb = (
                (cleaned_df['pb'] < self.config.min_pb) |
                (cleaned_df['pb'] > self.config.max_pb)
            )
            invalid_count = invalid_pb.sum()
            if invalid_count > 0:
                issues.append({
                    'type': 'invalid_pb',
                    'severity': 'warning',
                    'message': f'PB超出合理范围 [{self.config.min_pb}, {self.config.max_pb}]',
                    'count': invalid_count
                })
                cleaned_df.loc[invalid_pb, 'pb'] = np.nan
        
        # 6. 缺失值检查
        missing_stats = cleaned_df.isnull().sum()
        high_missing_cols = missing_stats[missing_stats / len(cleaned_df) > self.config.max_missing_ratio]
        if len(high_missing_cols) > 0:
            issues.append({
                'type': 'high_missing_ratio',
                'severity': 'warning',
                'message': f'以下列缺失值比例超过 {self.config.max_missing_ratio:.0%}',
                'columns': high_missing_cols.to_dict()
            })
            if self.verbose:
                print(f"⚠️ 高缺失值列: {list(high_missing_cols.index)}")
        
        # 7. 异常值检测（IQR方法）
        if self.config.use_iqr_outlier_detection:
            numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col in ['code', 'date']:
                    continue
                Q1 = cleaned_df[col].quantile(0.25)
                Q3 = cleaned_df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - self.config.iqr_factor * IQR
                upper_bound = Q3 + self.config.iqr_factor * IQR
                
                outliers = (cleaned_df[col] < lower_bound) | (cleaned_df[col] > upper_bound)
                outlier_count = outliers.sum()
                
                if outlier_count > 0 and outlier_count / len(cleaned_df) < 0.1:  # 异常值比例<10%才标记
                    issues.append({
                        'type': 'outliers',
                        'severity': 'info',
                        'message': f'列 {col} 检测到 {outlier_count} 个异常值',
                        'column': col,
                        'count': outlier_count
                    })
        
        # 8. 日期格式检查
        if 'date' in cleaned_df.columns:
            try:
                cleaned_df['date'] = pd.to_datetime(cleaned_df['date'])
            except Exception as e:
                issues.append({
                    'type': 'date_format_error',
                    'severity': 'error',
                    'message': f'日期格式错误: {e}',
                })
        
        # 9. 股票代码格式检查
        if 'code' in cleaned_df.columns:
            # 使用非捕获组避免警告
            invalid_codes = ~cleaned_df['code'].str.contains(r'\.X(?:SHE|SHG)', regex=True, na=False)
            invalid_count = invalid_codes.sum()
            if invalid_count > 0:
                issues.append({
                    'type': 'invalid_code_format',
                    'severity': 'error',
                    'message': f'股票代码格式错误: {invalid_count} 条',
                    'count': invalid_count
                })
                cleaned_df = cleaned_df[~invalid_codes].reset_index(drop=True)
                if self.verbose:
                    print(f"❌ 移除 {invalid_count} 条代码格式错误记录")
        
        # 生成报告
        result.valid_records = len(cleaned_df)
        result.invalid_records = result.total_records - result.valid_records
        result.cleaned_data = cleaned_df
        result.issues = issues
        result.is_valid = len([i for i in issues if i['severity'] == 'error']) == 0
        
        # 生成文本报告
        result.report = self._generate_report(result)
        
        if self.verbose:
            print(f"\n✅ 验证完成:")
            print(f"   有效记录: {result.valid_records} / {result.total_records}")
            print(f"   移除记录: {result.invalid_records}")
            print(f"   发现问题: {len(issues)} 个")
            if result.is_valid:
                print(f"   ✅ 数据质量: 通过")
            else:
                print(f"   ❌ 数据质量: 未通过（存在严重错误）")
        
        return result
    
    def _generate_report(self, result: ValidationResult) -> str:
        """生成验证报告"""
        lines = [
            f"数据验证报告",
            f"=" * 70,
            f"总记录数: {result.total_records}",
            f"有效记录: {result.valid_records}",
            f"无效记录: {result.invalid_records}",
            f"数据保留率: {result.valid_records/result.total_records:.1%}",
            f"",
            f"问题统计:",
        ]
        
        error_count = len([i for i in result.issues if i['severity'] == 'error'])
        warning_count = len([i for i in result.issues if i['severity'] == 'warning'])
        info_count = len([i for i in result.issues if i['severity'] == 'info'])
        
        lines.append(f"  严重错误: {error_count}")
        lines.append(f"  警告: {warning_count}")
        lines.append(f"  信息: {info_count}")
        lines.append("")
        
        if result.issues:
            lines.append("详细问题:")
            for i, issue in enumerate(result.issues, 1):
                lines.append(f"  {i}. [{issue['severity'].upper()}] {issue['message']}")
                if 'count' in issue:
                    lines.append(f"     影响记录数: {issue['count']}")
        
        return "\n".join(lines)


def validate_high_return_cases(
    cases_file: str,
    output_file: Optional[str] = None,
    config: Optional[DataQualityConfig] = None
) -> ValidationResult:
    """
    验证高收益案例数据文件
    
    Args:
        cases_file: 输入文件路径
        output_file: 清洗后输出文件路径（可选）
        config: 验证配置
    
    Returns:
        ValidationResult
    """
    # 读取数据
    df = pd.read_csv(cases_file)
    
    # 验证和清洗
    validator = DataValidator(config=config, verbose=True)
    result = validator.validate_and_clean(df)
    
    # 保存清洗后的数据
    if output_file and result.cleaned_data is not None:
        result.cleaned_data.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 清洗后数据已保存: {output_file}")
    
    # 保存验证报告
    if output_file:
        report_file = output_file.replace('.csv', '_validation_report.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(result.report)
        print(f"✅ 验证报告已保存: {report_file}")
    
    return result


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="验证和清洗高收益案例数据")
    parser.add_argument('--input', type=str, required=True, help='输入文件路径')
    parser.add_argument('--output', type=str, help='输出文件路径（可选）')
    parser.add_argument('--config', type=str, help='配置文件路径（可选）')
    
    args = parser.parse_args()
    
    result = validate_high_return_cases(args.input, args.output)
    
    if not result.is_valid:
        print("\n❌ 数据验证未通过，请检查并修复问题后重试")
        sys.exit(1)
    else:
        print("\n✅ 数据验证通过")
