# 读取AVGO PDF文件脚本
Write-Host "🔍 正在读取个股研究AVGO.pdf文件..." -ForegroundColor Green

$pdfPath = "public\documents\个股研究AVGO.pdf"

# 检查文件是否存在
if (-not (Test-Path $pdfPath)) {
    Write-Host "❌ 文件不存在: $pdfPath" -ForegroundColor Red
    exit 1
}

# 显示文件信息
Write-Host "📄 文件信息:" -ForegroundColor Cyan
$fileInfo = Get-ChildItem $pdfPath
Write-Host "文件名: $($fileInfo.Name)"
Write-Host "文件大小: $([math]::Round($fileInfo.Length / 1MB, 2)) MB"
Write-Host "修改时间: $($fileInfo.LastWriteTime)"
Write-Host ""

# 尝试读取文件内容
Write-Host "📖 尝试读取文件内容..." -ForegroundColor Green

try {
    # 方法1: 直接读取（如果是文本PDF）
    $content = Get-Content $pdfPath -Raw -ErrorAction SilentlyContinue
    
    if ($content) {
        Write-Host "✅ 成功读取文本内容" -ForegroundColor Green
        Write-Host "内容长度: $($content.Length) 字符"
        
        # 保存到文本文件
        $outputPath = "scripts\avgo-pdf-content.txt"
        $content | Out-File -FilePath $outputPath -Encoding UTF8
        Write-Host "📝 内容已保存到: $outputPath"
        
        # 显示前1000个字符
        Write-Host ""
        Write-Host "📖 内容预览:" -ForegroundColor Yellow
        Write-Host "=" * 60
        Write-Host $content.Substring(0, [math]::Min(1000, $content.Length))
        Write-Host "=" * 60
        
    } else {
        Write-Host "⚠️ 无法直接读取文本内容" -ForegroundColor Yellow
        Write-Host "这可能是一个图像PDF，需要OCR工具" -ForegroundColor Yellow
        
        # 方法2: 尝试使用二进制读取
        Write-Host ""
        Write-Host "🔍 尝试二进制读取..." -ForegroundColor Green
        $bytes = [System.IO.File]::ReadAllBytes($pdfPath)
        Write-Host "文件字节数: $($bytes.Length)"
        
        # 查找PDF头部信息
        $header = [System.Text.Encoding]::ASCII.GetString($bytes[0..100])
        Write-Host "PDF头部: $header"
        
        # 查找可能的文本内容
        $textContent = [System.Text.Encoding]::UTF8.GetString($bytes)
        $textMatches = [regex]::Matches($textContent, '[a-zA-Z\u4e00-\u9fff]{3,}')
        
        if ($textMatches.Count -gt 0) {
            Write-Host "✅ 找到 $($textMatches.Count) 个文本片段" -ForegroundColor Green
            
            # 保存找到的文本
            $outputPath = "scripts\avgo-extracted-text.txt"
            $textMatches | ForEach-Object { $_.Value } | Out-File -FilePath $outputPath -Encoding UTF8
            Write-Host "📝 提取的文本已保存到: $outputPath"
            
            # 显示一些文本片段
            Write-Host ""
            Write-Host "📖 提取的文本片段:" -ForegroundColor Yellow
            for ($i = 0; $i -lt [math]::Min(10, $textMatches.Count); $i++) {
                Write-Host "  $($textMatches[$i].Value)"
            }
        }
    }
}
catch {
    Write-Host "❌ 读取文件时出错: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 建议:" -ForegroundColor Cyan
Write-Host "1. 如果是图像PDF，可以使用在线OCR工具" -ForegroundColor White
Write-Host "2. 或者使用专业的PDF阅读器提取文本" -ForegroundColor White
Write-Host "3. 检查提取的文本文件: scripts\avgo-pdf-content.txt" -ForegroundColor White 