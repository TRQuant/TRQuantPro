# 智能章节导航脚本
# 自动识别章节结构并添加导航功能

$baseDir = "src/pages/book1"

# 定义需要处理的文件
$chapterFiles = @(
    # 第三章
    "003_Chapter3/3.2_Industry_Distribution_and_Characteristics_CN.md",
    "003_Chapter3/3.3_Driving_Factors_CN.md",
    "003_Chapter3/3.4_Case_Studies_CN.md",
    
    # 第四章
    "004_Chapter4/4.1_Track_Screening_Methods_CN.md",
    "004_Chapter4/4.2_AI_and_Big_Data_Revolution_CN.md",
    "004_Chapter4/4.3_New_Energy_and_EV_Golden_Decade_CN.md",
    "004_Chapter4/4.4_Biotech_and_Precision_Medicine_CN.md",
    "004_Chapter4/4.5_Semiconductor_and_Metaverse_CN.md",
    "004_Chapter4/4.6_Chinese_Stocks_Opportunities_CN.md",
    
    # 第五章
    "005_Chapter5/5.1_Stock_Screening_Methods_CN.md",
    "005_Chapter5/5.2_Fundamental_Screening_Parameters_CN.md",
    "005_Chapter5/5.3_Technical_Analysis_CN.md",
    "005_Chapter5/5.4_Valuation_Methodology_CN.md",
    "005_Chapter5/5.5_Stock_Screening_Practice_CN.md",
    "005_Chapter5/5.6_Derivatives_Enhancement_CN.md",
    
    # 第六章
    "006_Chapter6/6.1_Long_term_vs_Short_term_CN.md",
    "006_Chapter6/6.2_Position_Management_CN.md",
    "006_Chapter6/6.3_ETF_Optimization_CN.md",
    "006_Chapter6/6.4_Dynamic_Adjustment_CN.md",
    "006_Chapter6/6.5_Growth_Stock_Exit_CN.md",
    "006_Chapter6/6.6_Strategy_Execution_CN.md",
    
    # 第七章（排除7.2已完成的）
    "007_Chapter7/7.1_GuruFocus_Morningstar_CN.md",
    "007_Chapter7/7.3_Data_Driven_Decision_CN.md"
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

Write-Host "开始智能处理章节导航功能..." -ForegroundColor Green
Write-Host "总计需要处理 $($chapterFiles.Count) 个文件" -ForegroundColor Yellow

$processedCount = 0
$skippedCount = 0
$errorCount = 0

foreach ($file in $chapterFiles) {
    $fullPath = Join-Path $baseDir $file
    
    if (Test-Path $fullPath) {
        Write-Host "处理文件: $file" -ForegroundColor Yellow
        
        try {
            $content = Get-Content $fullPath -Raw -Encoding UTF8
            
            # 检查是否已经有导航脚本
            if ($content -notmatch "function scrollToSection") {
                # 查找章节概览部分（支持多种标题格式）
                if ($content -match '## 📋 章节概览' -or $content -match '## 📋 章节导航') {
                    # 提取章节编号
                    $chapterMatch = [regex]::Match($file, '(\d+)_Chapter(\d+)/(\d+)\.(\d+)')
                    if ($chapterMatch.Success) {
                        $chapterNum = $chapterMatch.Groups[2].Value
                        $subChapterNum = $chapterMatch.Groups[3].Value
                        
                        # 为overview-item添加onclick属性
                        $sectionId1 = "section-$chapterNum-$subChapterNum-1"
                        $sectionId2 = "section-$chapterNum-$subChapterNum-2"
                        $sectionId3 = "section-$chapterNum-$subChapterNum-3"
                        $sectionId4 = "section-$chapterNum-$subChapterNum-4"
                        $sectionId5 = "section-$chapterNum-$subChapterNum-5"
                        $sectionId6 = "section-$chapterNum-$subChapterNum-6"
                        
                        $content = $content -replace '<div class="overview-item">', "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId1')`" style=`"cursor: pointer;`">"
                        $content = $content -replace "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId1')`" style=`"cursor: pointer;`">", "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId2')`" style=`"cursor: pointer;`">"
                        $content = $content -replace "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId2')`" style=`"cursor: pointer;`">", "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId3')`" style=`"cursor: pointer;`">"
                        $content = $content -replace "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId3')`" style=`"cursor: pointer;`">", "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId4')`" style=`"cursor: pointer;`">"
                        $content = $content -replace "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId4')`" style=`"cursor: pointer;`">", "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId5')`" style=`"cursor: pointer;`">"
                        $content = $content -replace "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId5')`" style=`"cursor: pointer;`">", "<div class=`"overview-item`" onclick=`"scrollToSection('$sectionId6')`" style=`"cursor: pointer;`">"
                        
                        # 添加导航脚本和样式
                        $content = $content -replace '## 📋 章节概览', "## 📋 章节概览`n`n$navigationScript`n$navigationStyle"
                        $content = $content -replace '## 📋 章节导航', "## 📋 章节导航`n`n$navigationScript`n$navigationStyle"
                        
                        # 保存文件
                        $content | Set-Content $fullPath -Encoding UTF8
                        $processedCount++
                        Write-Host "  ✓ 已添加导航功能" -ForegroundColor Green
                    } else {
                        Write-Host "  ⚠ 无法解析章节编号" -ForegroundColor Yellow
                        $skippedCount++
                    }
                } else {
                    Write-Host "  ⚠ 未找到章节概览部分" -ForegroundColor Yellow
                    $skippedCount++
                }
            } else {
                Write-Host "  ⚠ 已有导航功能，跳过" -ForegroundColor Yellow
                $skippedCount++
            }
        } catch {
            Write-Host "  ❌ 处理失败: $($_.Exception.Message)" -ForegroundColor Red
            $errorCount++
        }
    } else {
        Write-Host "  ❌ 文件不存在: $file" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host "`n智能处理完成！" -ForegroundColor Green
Write-Host "处理成功: $processedCount 个文件" -ForegroundColor Green
Write-Host "跳过文件: $skippedCount 个文件" -ForegroundColor Yellow
Write-Host "处理失败: $errorCount 个文件" -ForegroundColor Red 