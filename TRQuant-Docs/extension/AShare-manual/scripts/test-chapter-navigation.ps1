# 测试脚本：为单个小节页面添加导航功能
# 目标：验证导航功能是否正确

$baseDir = "src/pages/book1"
$testFile = "001_Chapter1/1.1_Self_Awareness_and_Investment_Wisdom_CN.md"
$fullPath = Join-Path $baseDir $testFile

Write-Host "测试文件: $testFile" -ForegroundColor Yellow

if (Test-Path $fullPath) {
    $content = Get-Content $fullPath -Raw -Encoding UTF8
    
    # 检查是否已经有导航脚本
    if ($content -notmatch "function scrollToSection") {
        Write-Host "  ✓ 文件存在且无导航脚本" -ForegroundColor Green
        
        # 查找章节概览部分
        if ($content -match '## 📋 章节概览') {
            Write-Host "  ✓ 找到章节概览部分" -ForegroundColor Green
            
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

            # 为overview-item添加onclick属性
            $content = $content -replace '<div class="overview-item">', '<div class="overview-item" onclick="scrollToSection(''section-1-1-1'')" style="cursor: pointer;">'
            $content = $content -replace '<div class="overview-item" onclick="scrollToSection(''section-1-1-1'')" style="cursor: pointer;">', '<div class="overview-item" onclick="scrollToSection(''section-1-1-2'')" style="cursor: pointer;">'
            $content = $content -replace '<div class="overview-item" onclick="scrollToSection(''section-1-1-2'')" style="cursor: pointer;">', '<div class="overview-item" onclick="scrollToSection(''section-1-1-3'')" style="cursor: pointer;">'
            
            # 添加导航脚本和样式
            $content = $content -replace '## 📋 章节概览', "## 📋 章节概览`n`n$navigationScript`n$navigationStyle"
            
            # 保存文件
            $content | Set-Content $fullPath -Encoding UTF8
            Write-Host "  ✓ 已添加导航功能" -ForegroundColor Green
            Write-Host "  ✓ 文件已保存" -ForegroundColor Green
        } else {
            Write-Host "  ❌ 未找到章节概览部分" -ForegroundColor Red
        }
    } else {
        Write-Host "  ⚠ 已有导航功能，跳过" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ 文件不存在: $testFile" -ForegroundColor Red
}

Write-Host "测试完成！" -ForegroundColor Green 