# 更好的AVGO PDF内容提取脚本
Write-Host "🔍 正在提取AVGO PDF中的有用内容..." -ForegroundColor Green

$contentPath = "scripts\avgo-pdf-content.txt"

if (-not (Test-Path $contentPath)) {
    Write-Host "❌ 未找到提取的文本文件" -ForegroundColor Red
    exit 1
}

# 读取文件内容
$content = Get-Content $contentPath -Raw

# 查找更长的中文文本片段
Write-Host "📖 提取中文内容..." -ForegroundColor Green
$chinesePattern = '[\u4e00-\u9fff\s\d\.\,\，\。\、\：\；\！\？\（\）\【\】\""\''\-\+]{50,}'
$chineseMatches = [regex]::Matches($content, $chinesePattern)

$usefulContent = @()

if ($chineseMatches.Count -gt 0) {
    Write-Host "✅ 找到 $($chineseMatches.Count) 个中文文本片段" -ForegroundColor Green
    
    foreach ($match in $chineseMatches) {
        $text = $match.Value.Trim()
        # 过滤掉包含太多数字或特殊字符的片段
        $chineseRatio = ([regex]::Matches($text, '[\u4e00-\u9fff]')).Count / $text.Length
        if ($chineseRatio -gt 0.3) {  # 至少30%是中文
            $usefulContent += $text
        }
    }
}

# 查找Broadcom相关信息
Write-Host "🏢 查找Broadcom相关信息..." -ForegroundColor Green
$broadcomPatterns = @(
    "Broadcom.*[\u4e00-\u9fff]+",
    "[\u4e00-\u9fff]+.*Broadcom",
    "AVGO.*[\u4e00-\u9fff]+",
    "[\u4e00-\u9fff]+.*AVGO"
)

foreach ($pattern in $broadcomPatterns) {
    $matches = [regex]::Matches($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    foreach ($match in $matches) {
        $usefulContent += $match.Value
    }
}

# 查找财务分析相关内容
Write-Host "📊 查找财务分析内容..." -ForegroundColor Green
$financialPatterns = @(
    "收入.*[\u4e00-\u9fff]+",
    "利润.*[\u4e00-\u9fff]+",
    "增长.*[\u4e00-\u9fff]+",
    "估值.*[\u4e00-\u9fff]+",
    "财务.*[\u4e00-\u9fff]+",
    "分析.*[\u4e00-\u9fff]+"
)

foreach ($pattern in $financialPatterns) {
    $matches = [regex]::Matches($content, $pattern)
    foreach ($match in $matches) {
        $usefulContent += $match.Value
    }
}

# 去重并保存
$uniqueContent = $usefulContent | Sort-Object | Get-Unique

# 保存提取的内容
$outputPath = "scripts\avgo-useful-content.txt"
$uniqueContent | Out-File -FilePath $outputPath -Encoding UTF8

Write-Host "✅ 提取完成，共找到 $($uniqueContent.Count) 个有用内容片段" -ForegroundColor Green
Write-Host "📝 内容已保存到: $outputPath" -ForegroundColor Green

# 显示一些示例
Write-Host ""
Write-Host "📖 内容示例:" -ForegroundColor Yellow
for ($i = 0; $i -lt [math]::Min(5, $uniqueContent.Count); $i++) {
    Write-Host "片段 $($i+1):"
    Write-Host $uniqueContent[$i].Substring(0, [math]::Min(150, $uniqueContent[$i].Length))
    Write-Host ""
}

Write-Host "🎯 现在可以开始生成章节内容了！" -ForegroundColor Green 