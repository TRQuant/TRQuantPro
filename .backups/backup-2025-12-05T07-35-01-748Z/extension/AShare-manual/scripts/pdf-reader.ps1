# PDF读取和分析脚本
# 用于读取个股研究AVGO.pdf文件内容

param(
    [string]$PdfPath = "public\documents\个股研究AVGO.pdf",
    [string]$OutputPath = "scripts\pdf-content.txt",
    [switch]$ExtractText,
    [switch]$AnalyzeContent,
    [switch]$ShowInfo
)

# 检查PDF文件是否存在
if (-not (Test-Path $PdfPath)) {
    Write-Host "❌ PDF文件不存在: $PdfPath" -ForegroundColor Red
    Write-Host "请确保文件路径正确" -ForegroundColor Yellow
    exit 1
}

# 显示文件信息
if ($ShowInfo) {
    Write-Host "📄 PDF文件信息:" -ForegroundColor Green
    $fileInfo = Get-ChildItem $PdfPath
    Write-Host "文件名: $($fileInfo.Name)" -ForegroundColor Cyan
    Write-Host "文件大小: $([math]::Round($fileInfo.Length / 1MB, 2)) MB" -ForegroundColor Cyan
    Write-Host "创建时间: $($fileInfo.CreationTime)" -ForegroundColor Cyan
    Write-Host "修改时间: $($fileInfo.LastWriteTime)" -ForegroundColor Cyan
    Write-Host ""
}

# 提取文本内容
if ($ExtractText) {
    Write-Host "🔍 正在提取PDF文本内容..." -ForegroundColor Green
    
    try {
        # 使用PowerShell的Get-Content尝试读取（如果是文本PDF）
        $content = Get-Content $PdfPath -Raw -ErrorAction SilentlyContinue
        
        if ($content) {
            Write-Host "✅ 成功读取PDF文本内容" -ForegroundColor Green
            Write-Host "内容长度: $($content.Length) 字符" -ForegroundColor Cyan
            
            # 保存到文件
            $content | Out-File -FilePath $OutputPath -Encoding UTF8
            Write-Host "📝 内容已保存到: $OutputPath" -ForegroundColor Green
            
            # 显示前500个字符作为预览
            Write-Host "📖 内容预览:" -ForegroundColor Yellow
            Write-Host "=" * 50
            Write-Host $content.Substring(0, [math]::Min(500, $content.Length))
            Write-Host "=" * 50
        } else {
            Write-Host "⚠️ 无法直接读取PDF文本内容" -ForegroundColor Yellow
            Write-Host "这可能是一个图像PDF，需要OCR工具来提取文本" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "❌ 读取PDF时出错: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# 分析内容
if ($AnalyzeContent) {
    Write-Host "📊 正在分析PDF内容..." -ForegroundColor Green
    
    if (Test-Path $OutputPath) {
        $content = Get-Content $OutputPath -Raw
        
        # 基本统计
        $lines = ($content -split "`n").Count
        $words = ($content -split '\s+').Count
        $chars = $content.Length
        
        Write-Host "📈 内容统计:" -ForegroundColor Cyan
        Write-Host "行数: $lines" -ForegroundColor White
        Write-Host "单词数: $words" -ForegroundColor White
        Write-Host "字符数: $chars" -ForegroundColor White
        
        # 查找关键词
        $keywords = @("Broadcom", "AVGO", "半导体", "芯片", "财务", "估值", "投资", "分析")
        Write-Host "🔍 关键词分析:" -ForegroundColor Cyan
        
        foreach ($keyword in $keywords) {
            $count = ([regex]::Matches($content, $keyword, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)).Count
            if ($count -gt 0) {
                Write-Host "  $keyword`: $count 次" -ForegroundColor White
            }
        }
        
        # 查找章节结构
        Write-Host "📚 章节结构分析:" -ForegroundColor Cyan
        $chapterPatterns = @(
            "第[一二三四五六七八九十]+章",
            "Chapter\s+\d+",
            "^\d+\.\s+",
            "^[一二三四五六七八九十]+、"
        )
        
        foreach ($pattern in $chapterPatterns) {
            $matches = [regex]::Matches($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
            if ($matches.Count -gt 0) {
                Write-Host "  找到 $($matches.Count) 个可能的章节标题" -ForegroundColor White
                foreach ($match in $matches[0..([math]::Min(5, $matches.Count-1))]) {
                    Write-Host "    - $($match.Value)" -ForegroundColor Gray
                }
                break
            }
        }
        
    } else {
        Write-Host "❌ 未找到提取的文本文件，请先运行 -ExtractText" -ForegroundColor Red
    }
}

# 如果没有指定任何操作，显示帮助信息
if (-not ($ExtractText -or $AnalyzeContent -or $ShowInfo)) {
    Write-Host "📖 PDF读取脚本使用说明:" -ForegroundColor Green
    Write-Host ""
    Write-Host "用法:" -ForegroundColor Yellow
    Write-Host "  .\pdf-reader.ps1 [参数]" -ForegroundColor White
    Write-Host ""
    Write-Host "参数:" -ForegroundColor Yellow
    Write-Host "  -PdfPath <路径>     指定PDF文件路径 (默认: public\documents\个股研究AVGO.pdf)" -ForegroundColor White
    Write-Host "  -OutputPath <路径>  指定输出文件路径 (默认: scripts\pdf-content.txt)" -ForegroundColor White
    Write-Host "  -ExtractText        提取PDF文本内容" -ForegroundColor White
    Write-Host "  -AnalyzeContent     分析提取的内容" -ForegroundColor White
    Write-Host "  -ShowInfo           显示PDF文件信息" -ForegroundColor White
    Write-Host ""
    Write-Host "示例:" -ForegroundColor Yellow
    Write-Host "  .\pdf-reader.ps1 -ShowInfo" -ForegroundColor White
    Write-Host "  .\pdf-reader.ps1 -ExtractText" -ForegroundColor White
    Write-Host "  .\pdf-reader.ps1 -AnalyzeContent" -ForegroundColor White
    Write-Host "  .\pdf-reader.ps1 -ExtractText -AnalyzeContent" -ForegroundColor White
}

Write-Host ""
Write-Host "💡 提示: 如果PDF是图像格式，可能需要使用OCR工具来提取文本" -ForegroundColor Cyan 