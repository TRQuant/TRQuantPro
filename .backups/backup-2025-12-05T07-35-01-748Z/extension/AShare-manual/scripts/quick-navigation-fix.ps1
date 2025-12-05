# 快速导航修复脚本
# 为剩余的小节页面添加导航功能

$baseDir = "src/pages/book1"

# 定义需要处理的文件（第四章到第七章）
$chapterFiles = @(
    # 第四章剩余
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

Write-Host "开始快速处理导航功能..." -ForegroundColor Green
Write-Host "总计需要处理 $($chapterFiles.Count) 个文件" -ForegroundColor Yellow

$processedCount = 0
$skippedCount = 0

foreach ($file in $chapterFiles) {
    $fullPath = Join-Path $baseDir $file
    
    if (Test-Path $fullPath) {
        Write-Host "处理文件: $file" -ForegroundColor Yellow
        
        try {
            $content = Get-Content $fullPath -Raw -Encoding UTF8
            
            # 检查是否已经有导航脚本
            if ($content -notmatch "function scrollToSection") {
                # 查找章节概览部分
                if ($content -match '## 📋 章节概览' -or $content -match '## 🗺️ 章节导览') {
                    Write-Host "  ✓ 找到章节概览部分" -ForegroundColor Green
                    
                    # 添加导航脚本和样式
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

                    # 添加导航脚本和样式
                    $content = $content -replace '## 📋 章节概览', "## 📋 章节概览`n`n$navigationScript`n$navigationStyle"
                    $content = $content -replace '## 🗺️ 章节导览', "## 🗺️ 章节导览`n`n$navigationScript`n$navigationStyle"
                    
                    # 保存文件
                    $content | Set-Content $fullPath -Encoding UTF8
                    $processedCount++
                    Write-Host "  ✓ 已添加导航功能" -ForegroundColor Green
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
            $skippedCount++
        }
    } else {
        Write-Host "  ❌ 文件不存在: $file" -ForegroundColor Red
        $skippedCount++
    }
}

Write-Host "`n快速处理完成！" -ForegroundColor Green
Write-Host "处理成功: $processedCount 个文件" -ForegroundColor Green
Write-Host "跳过文件: $skippedCount 个文件" -ForegroundColor Yellow 