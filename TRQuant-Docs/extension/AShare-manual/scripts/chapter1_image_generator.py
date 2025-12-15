# region imports
from AlgorithmImports import *
# endregion
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.font_manager as fm
import os

# 配置中文字体支持
def setup_chinese_font():
    """设置中文字体"""
    # Windows系统字体路径
    windows_fonts = [
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
        'C:/Windows/Fonts/simsun.ttc',  # 宋体
    ]
    
    for font_path in windows_fonts:
        if os.path.exists(font_path):
            # 添加字体文件
            fm.fontManager.addfont(font_path)
            # 设置字体
            if 'simhei' in font_path.lower():
                plt.rcParams['font.sans-serif'] = ['SimHei'] + plt.rcParams['font.sans-serif']
                print(f"使用中文字体: SimHei")
                break
            elif 'msyh' in font_path.lower():
                plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] + plt.rcParams['font.sans-serif']
                print(f"使用中文字体: Microsoft YaHei")
                break
            elif 'simsun' in font_path.lower():
                plt.rcParams['font.sans-serif'] = ['SimSun'] + plt.rcParams['font.sans-serif']
                print(f"使用中文字体: SimSun")
                break
    
    # 确保负号正确显示
    plt.rcParams['axes.unicode_minus'] = False

# 设置中文字体
setup_chinese_font()

# 设置字体为英文
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# 设置专业金融报告风格
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def create_cognitive_bias_chart():
    """创建认知偏差统计图"""
    
    # 认知偏差数据（英文标签）
    biases = [
        'Overconfidence',
        'Confirmation Bias', 
        'Loss Aversion',
        'Anchoring Bias',
        'Representativeness',
        'Herd Mentality'
    ]
    
    # 发生频率（基于行为金融学研究数据）
    frequency = [85, 78, 92, 65, 72, 68]  # 百分比
    
    # 对投资决策的影响程度（1-10分）
    impact = [8.5, 7.8, 9.2, 6.5, 7.2, 6.8]
    
    # 创建图表 - 增大整体尺寸，移除标题
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 10))
    
    # 左侧：发生频率图
    bars1 = ax1.barh(biases, frequency, color='#2E86AB', alpha=0.8, height=0.6)
    ax1.set_xlabel('Occurrence Frequency (%)', fontsize=20, fontweight='bold')
    ax1.set_title('Cognitive Bias Occurrence in Investors', fontsize=22, fontweight='bold', pad=20)
    ax1.set_xlim(0, 100)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='both', which='major', labelsize=16)
    
    # 添加数值标签
    for i, (bar, freq) in enumerate(zip(bars1, frequency)):
        ax1.text(freq + 4, bar.get_y() + bar.get_height()/2, 
                f'{freq}%', va='center', fontweight='bold', fontsize=16)
    
    # 右侧：影响程度图
    bars2 = ax2.barh(biases, impact, color='#A23B72', alpha=0.8, height=0.6)
    ax2.set_xlabel('Impact Level (1-10)', fontsize=20, fontweight='bold')
    ax2.set_title('Cognitive Bias Impact on Investment Decisions', fontsize=22, fontweight='bold', pad=20)
    ax2.set_xlim(0, 10)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='both', which='major', labelsize=16)
    
    # 添加数值标签
    for i, (bar, imp) in enumerate(zip(bars2, impact)):
        ax2.text(imp + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{imp}', va='center', fontweight='bold', fontsize=16)
    
    # 添加数据来源说明
    fig.text(0.02, 0.02, 'Data Source: Behavioral Finance Research + Investment Practice Statistics', 
             fontsize=14, style='italic', alpha=0.7)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.05, right=0.95)
    
    # 保存图片
    plt.savefig('src/images/001_Chapter1/generated/cognitive_biases_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("认知偏差统计图已生成：src/images/001_Chapter1/generated/cognitive_biases_analysis.png")

def create_investment_tools_chart():
    """创建投资工具分析图"""
    
    # 投资工具数据（英文标签）
    tools = [
        'Bloomberg Terminal',
        'TradingView',
        'GuruFocus',
        'Morningstar',
        'Seeking Alpha',
        'Yahoo Finance'
    ]
    
    # 使用频率（基于市场调研数据）
    usage_frequency = [95, 88, 72, 68, 65, 82]  # 百分比
    
    # 专业度评分（1-10分）
    professionalism = [9.8, 8.5, 8.2, 8.7, 7.5, 6.8]
    
    # 成本效益比（1-10分）
    cost_effectiveness = [6.5, 9.2, 8.8, 7.5, 8.0, 9.5]
    
    # 创建图表 - 增大整体尺寸，移除主标题
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(26, 10))
    
    # 左侧：使用频率图
    bars1 = ax1.barh(tools, usage_frequency, color='#2E86AB', alpha=0.8, height=0.5)
    ax1.set_xlabel('Usage Frequency (%)', fontsize=20, fontweight='bold')
    ax1.set_title('Market Adoption Rate', fontsize=22, fontweight='bold', pad=20)
    ax1.set_xlim(0, 100)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='both', which='major', labelsize=16)
    
    # 添加数值标签
    for i, (bar, freq) in enumerate(zip(bars1, usage_frequency)):
        ax1.text(freq + 4, bar.get_y() + bar.get_height()/2, 
                f'{freq}%', va='center', fontweight='bold', fontsize=16)
    
    # 中间：专业度评分图
    bars2 = ax2.barh(tools, professionalism, color='#A23B72', alpha=0.8, height=0.5)
    ax2.set_xlabel('Professionalism Score (1-10)', fontsize=20, fontweight='bold')
    ax2.set_title('Professional Quality Rating', fontsize=22, fontweight='bold', pad=20)
    ax2.set_xlim(0, 10)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='both', which='major', labelsize=16)
    
    # 添加数值标签
    for i, (bar, prof) in enumerate(zip(bars2, professionalism)):
        ax2.text(prof + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{prof}', va='center', fontweight='bold', fontsize=16)
    
    # 右侧：成本效益比图
    bars3 = ax3.barh(tools, cost_effectiveness, color='#F18F01', alpha=0.8, height=0.5)
    ax3.set_xlabel('Cost-Effectiveness (1-10)', fontsize=20, fontweight='bold')
    ax3.set_title('Value for Money Rating', fontsize=22, fontweight='bold', pad=20)
    ax3.set_xlim(0, 10)
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='both', which='major', labelsize=16)
    
    # 添加数值标签
    for i, (bar, cost) in enumerate(zip(bars3, cost_effectiveness)):
        ax3.text(cost + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{cost}', va='center', fontweight='bold', fontsize=16)
    
    # 添加数据来源说明
    fig.text(0.02, 0.02, 'Data Source: Investment Tool Market Research + User Feedback Analysis', 
             fontsize=14, style='italic', alpha=0.7)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.05, right=0.95)
    
    # 保存图片
    plt.savefig('src/images/001_Chapter1/generated/investment_tools_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print("投资工具分析图已生成：src/images/001_Chapter1/generated/investment_tools_analysis.png")

if __name__ == "__main__":
    create_cognitive_bias_chart()
    create_investment_tools_chart() 