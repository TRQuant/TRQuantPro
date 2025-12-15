# 为所有小节页面添加统一的章节导航功能
# 目标：为每个小节页面的章节概览添加点击导航功能

$baseDir = "src/pages/book1"

# 定义所有需要处理的小节文件
$chapterFiles = @(
    # 第一章
    "001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN.md",
    "001_Chapter1/1.2_Understanding_the_World_CN.md", 
    "001_Chapter1/1.3_From_Cognition_to_Action_CN.md",
    
    # 第二章
    "002_Chapter2/2.1_Personalized_Risk_Tolerance_Model_CN.md",
    "002_Chapter2/2.2_Stop_Loss_and_Risk_Control_CN.md",
    "002_Chapter2/2.3_Investment_Emotions_and_Decision_Traps_CN.md",
    "002_Chapter2/2.4_Maintaining_Discipline_in_Volatile_Markets_CN.md",
    
    # 第三章
    "003_Chapter3/3.1_Definition_and_Time_Dimensions_CN.md",
    "003_Chapter3/3.2_Industry_Distribution_and_Characteristics_CN.md",
    "003_Chapter3/3.3_Historical_Patterns_and_Investment_Strategies_CN.md",
    
    # 第四章
    "004_Chapter4/4.1_Track_Screening_Methods_CN.md",
    "004_Chapter4/4.2_AI_and_Big_Data_Revolution_CN.md",
    "004_Chapter4/4.3_New_Energy_and_EV_Golden_Decade_CN.md",
    
    # 第五章
    "005_Chapter5/5.1_Stock_Screening_Methods_CN.md",
    "005_Chapter5/5.2_Fundamental_Screening_Parameters_CN.md",
    "005_Chapter5/5.3_Technical_Analysis_CN.md",
    
    # 第六章
    "006_Chapter6/6.1_Long_term_vs_Short_term_CN.md",
    "006_Chapter6/6.2_Position_Management_CN.md",
    "006_Chapter6/6.3_ETF_Optimization_CN.md",
    
    # 第七章
    "007_Chapter7/7.1_GuruFocus_Morningstar_CN.md",
    "007_Chapter7/7.2_Technical_Analysis_Tools_CN.md",
    "007_Chapter7/7.3_Data_Driven_Decision_CN.md",
    
    # 第八章
    "008_Chapter8/8.1_Broadcom_Case_Study_CN.md",
    "008_Chapter8/8.2_NVIDIA_Case_Study_CN.md",
    "008_Chapter8/8.3_Case_Review_Methodology_CN.md",
    
    # 第九章
    "009_Chapter9/9.1_Efficient_Investment_Lifestyle_CN.md",
    "009_Chapter9/9.2_Strategy_Review_Optimization_CN.md",
    "009_Chapter9/9.3_Personal_Investment_System_CN.md",
    
    # 第十章
    "010_Chapter10/10.1_Preparation_CN.md",
    "010_Chapter10/10.2_Gurufocus_Screening_CN.md",
    "010_Chapter10/10.3_Trading_Execution_CN.md"
)

# 导航脚本模板
$navigationScript = @"
<script>
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    const targetPosition = element.offsetTop + 88;
    
    window.scrollTo({
      top: Math.max(0, targetPosition),
      behavior: 'smooth'
    });
  }
}
</script>
"@

# 导航样式模板
$navigationStyle = @"
<style>
.chapter-overview .overview-item {
  transition: all 0.3s ease;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  cursor: pointer;
}

.chapter-overview .overview-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--primary-color);
}

.chapter-overview .overview-item h4 {
  margin: 0 0 8px 0;
  color: var(--text-primary);
  font-size: 1.1rem;
  font-weight: 600;
}

.chapter-overview .overview-item p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .chapter-overview {
    grid-template-columns: 1fr;
  }
  
  .chapter-overview .overview-item {
    padding: 12px;
  }
  
  .chapter-overview .overview-item h4 {
    font-size: 1rem;
  }
}
</style>
"@

Write-Host "开始为小节页面添加导航功能..." -ForegroundColor Green

foreach ($file in $chapterFiles) {
    $fullPath = Join-Path $baseDir $file
    
    if (Test-Path $fullPath) {
        Write-Host "处理文件: $file" -ForegroundColor Yellow
        
        $content = Get-Content $fullPath -Raw -Encoding UTF8
        
        # 检查是否已经有导航脚本
        if ($content -notmatch "function scrollToSection") {
            # 查找章节概览部分
            if ($content -match '## 📋 章节概览') {
                # 为overview-item添加onclick属性
                $content = $content -replace '<div class="overview-item">', '<div class="overview-item" onclick="scrollToSection(''section-$1'')" style="cursor: pointer;">'
                
                # 添加导航脚本和样式
                $content = $content -replace '## 📋 章节概览', "## 📋 章节概览`n`n$navigationScript`n$navigationStyle"
                
                # 保存文件
                $content | Set-Content $fullPath -Encoding UTF8
                Write-Host "  ✓ 已添加导航功能" -ForegroundColor Green
            } else {
                Write-Host "  ⚠ 未找到章节概览部分" -ForegroundColor Yellow
            }
        } else {
            Write-Host "  ⚠ 已有导航功能，跳过" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ❌ 文件不存在: $file" -ForegroundColor Red
    }
}

Write-Host "完成！" -ForegroundColor Green 