# 提取AVGO PDF中的有用内容
Write-Host "🔍 正在提取AVGO PDF中的有用内容..." -ForegroundColor Green

$contentPath = "scripts\avgo-pdf-content.txt"

if (-not (Test-Path $contentPath)) {
    Write-Host "❌ 未找到提取的文本文件，请先运行 read-avgo-pdf.ps1" -ForegroundColor Red
    exit 1
}

# 读取文件内容
$content = Get-Content $contentPath -Raw

# 提取中文段落
Write-Host "📖 提取中文段落..." -ForegroundColor Green
$chinesePattern = '[\u4e00-\u9fff\s]{20,}'
$chineseParagraphs = [regex]::Matches($content, $chinesePattern)

$extractedContent = @()

if ($chineseParagraphs.Count -gt 0) {
    Write-Host "✅ 找到 $($chineseParagraphs.Count) 个中文段落" -ForegroundColor Green
    
    foreach ($paragraph in $chineseParagraphs) {
        $text = $paragraph.Value.Trim()
        if ($text.Length -gt 30) {  # 只保留较长的段落
            $extractedContent += $text
        }
    }
}

# 查找财务数据
Write-Host "📊 提取财务数据..." -ForegroundColor Green
$financialPatterns = @{
    "收入" = "\d+\.?\d*\s*[万亿]?元"
    "利润" = "\d+\.?\d*\s*[万亿]?元"
    "增长率" = "\d+\.?\d*%"
    "股价" = "\$\d+\.?\d*"
    "市值" = "\d+\.?\d*\s*[万亿]?美元"
}

$financialData = @{}

foreach ($key in $financialPatterns.Keys) {
    $pattern = $financialPatterns[$key]
    $matches = [regex]::Matches($content, $pattern)
    if ($matches.Count -gt 0) {
        $financialData[$key] = @()
        foreach ($match in $matches[0..([math]::Min(10, $matches.Count-1))]) {
            $financialData[$key] += $match.Value
        }
    }
}

# 查找公司信息
Write-Host "🏢 提取公司信息..." -ForegroundColor Green
$companyInfo = @{
    "公司名称" = @()
    "业务领域" = @()
    "技术优势" = @()
    "市场地位" = @()
}

# 查找可能的公司信息片段
$companyPatterns = @(
    "Broadcom.*公司",
    "半导体.*业务",
    "技术.*领先",
    "市场.*份额",
    "全球.*第一"
)

foreach ($pattern in $companyPatterns) {
    $matches = [regex]::Matches($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($match in $matches) {
        $extractedContent += $match.Value
    }
}

# 保存提取的内容
Write-Host "📝 保存提取的内容..." -ForegroundColor Green

# 保存中文段落
$paragraphsOutput = "scripts\avgo-paragraphs.txt"
$extractedContent | Out-File -FilePath $paragraphsOutput -Encoding UTF8
Write-Host "✅ 中文段落已保存到: $paragraphsOutput" -ForegroundColor Green

# 保存财务数据
$financialOutput = "scripts\avgo-financial-data.txt"
$financialText = "AVGO财务数据提取结果`n" + "=" * 50 + "`n`n"

foreach ($key in $financialData.Keys) {
    if ($financialData[$key].Count -gt 0) {
        $financialText += "$key`:`n"
        foreach ($value in $financialData[$key]) {
            $financialText += "  $value`n"
        }
        $financialText += "`n"
    }
}

$financialText | Out-File -FilePath $financialOutput -Encoding UTF8
Write-Host "✅ 财务数据已保存到: $financialOutput" -ForegroundColor Green

# 显示提取结果摘要
Write-Host ""
Write-Host "📊 提取结果摘要:" -ForegroundColor Yellow
Write-Host "中文段落数: $($extractedContent.Count)"
Write-Host "财务数据类型: $($financialData.Keys.Count)"

foreach ($key in $financialData.Keys) {
    if ($financialData[$key].Count -gt 0) {
        Write-Host "  $key`: $($financialData[$key].Count) 个数据点"
    }
}

# 显示一些提取的段落示例
Write-Host ""
Write-Host "📖 提取的段落示例:" -ForegroundColor Yellow
for ($i = 0; $i -lt [math]::Min(3, $extractedContent.Count); $i++) {
    Write-Host "段落 $($i+1):"
    Write-Host $extractedContent[$i].Substring(0, [math]::Min(200, $extractedContent[$i].Length))
    Write-Host ""
}

Write-Host ""
Write-Host "💡 下一步建议:" -ForegroundColor Cyan
Write-Host "1. 检查提取的段落内容质量" -ForegroundColor White
Write-Host "2. 根据内容组织章节结构" -ForegroundColor White
Write-Host "3. 提取关键数据和图表信息" -ForegroundColor White
Write-Host "4. 整理成第三册章节内容" -ForegroundColor White 