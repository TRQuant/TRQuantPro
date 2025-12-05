# 分析AVGO PDF文件内容结构
Write-Host "🔍 正在分析个股研究AVGO.pdf内容结构..." -ForegroundColor Green

$contentPath = "scripts\avgo-pdf-content.txt"

if (-not (Test-Path $contentPath)) {
    Write-Host "❌ 未找到提取的文本文件，请先运行 read-avgo-pdf.ps1" -ForegroundColor Red
    exit 1
}

# 读取文件内容
$content = Get-Content $contentPath -Raw
Write-Host "📄 文件大小: $([math]::Round($content.Length / 1MB, 2)) MB" -ForegroundColor Cyan

# 查找中文内容
Write-Host ""
Write-Host "🔍 查找中文内容..." -ForegroundColor Green
$chinesePattern = '[\u4e00-\u9fff]+'
$chineseMatches = [regex]::Matches($content, $chinesePattern)

if ($chineseMatches.Count -gt 0) {
    Write-Host "✅ 找到 $($chineseMatches.Count) 个中文字符片段" -ForegroundColor Green
    
    # 提取较长的中文片段
    $longChineseTexts = $chineseMatches | Where-Object { $_.Value.Length -gt 10 } | Select-Object -First 20
    
    Write-Host ""
    Write-Host "📖 中文内容片段:" -ForegroundColor Yellow
    foreach ($text in $longChineseTexts) {
        Write-Host "  $($text.Value)"
    }
} else {
    Write-Host "❌ 未找到中文内容" -ForegroundColor Red
}

# 查找章节结构
Write-Host ""
Write-Host "📚 查找章节结构..." -ForegroundColor Green
$chapterPatterns = @(
    "第[一二三四五六七八九十]+章",
    "Chapter\s+\d+",
    "^\d+\.\s+",
    "^[一二三四五六七八九十]+、",
    "^\d+、"
)

foreach ($pattern in $chapterPatterns) {
    $matches = [regex]::Matches($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if ($matches.Count -gt 0) {
        Write-Host "✅ 找到 $($matches.Count) 个章节标题 (模式: $pattern)" -ForegroundColor Green
        foreach ($match in $matches[0..([math]::Min(5, $matches.Count-1))]) {
            Write-Host "  $($match.Value)"
        }
        break
    }
}

# 查找关键词
Write-Host ""
Write-Host "🔍 查找关键词..." -ForegroundColor Green
$keywords = @("Broadcom", "AVGO", "半导体", "芯片", "财务", "估值", "投资", "分析", "收入", "利润", "增长")
$keywordResults = @{}

foreach ($keyword in $keywords) {
    $count = ([regex]::Matches($content, $keyword, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)).Count
    if ($count -gt 0) {
        $keywordResults[$keyword] = $count
    }
}

if ($keywordResults.Count -gt 0) {
    Write-Host "✅ 关键词统计:" -ForegroundColor Green
    $keywordResults.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object {
        Write-Host "  $($_.Key): $($_.Value) 次"
    }
}

# 查找表格数据
Write-Host ""
Write-Host "📊 查找表格数据..." -ForegroundColor Green
$tablePatterns = @(
    "\d+\.\d+%",  # 百分比
    "\$\d+\.\d+", # 美元金额
    "\d{4}-\d{2}-\d{2}", # 日期
    "\d+\.\d+",   # 小数
    "\d{4}"       # 年份
)

foreach ($pattern in $tablePatterns) {
    $matches = [regex]::Matches($content, $pattern)
    if ($matches.Count -gt 0) {
        Write-Host "✅ 找到 $($matches.Count) 个数据项 (模式: $pattern)" -ForegroundColor Green
        foreach ($match in $matches[0..([math]::Min(10, $matches.Count-1))]) {
            Write-Host "  $($match.Value)"
        }
        break
    }
}

# 保存分析结果
$analysisResult = @"
AVGO PDF文件分析结果
====================
文件大小: $([math]::Round($content.Length / 1MB, 2)) MB
中文字符片段数: $($chineseMatches.Count)
关键词统计: $($keywordResults.Count) 个关键词
"@

$analysisResult | Out-File -FilePath "scripts\avgo-pdf-analysis.txt" -Encoding UTF8
Write-Host ""
Write-Host "📝 分析结果已保存到: scripts\avgo-pdf-analysis.txt" -ForegroundColor Green

Write-Host ""
Write-Host "💡 建议:" -ForegroundColor Cyan
Write-Host "1. 检查提取的中文内容是否完整" -ForegroundColor White
Write-Host "2. 根据章节结构组织内容" -ForegroundColor White
Write-Host "3. 提取关键数据和表格信息" -ForegroundColor White 