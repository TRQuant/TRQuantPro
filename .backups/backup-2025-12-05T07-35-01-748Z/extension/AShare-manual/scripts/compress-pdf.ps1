# PDF压缩脚本
# 支持多种压缩策略，大幅减小PDF文件大小

param(
    [Parameter(Mandatory=$true)]
    [string]$InputPath,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("low", "medium", "high", "extreme")]
    [string]$CompressionLevel = "medium",
    
    [Parameter(Mandatory=$false)]
    [string]$OutputPath = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$KeepOriginal = $false
)

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# 检查文件是否存在
function Test-PDFFile {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        Write-ColorOutput "❌ 文件不存在: $Path" "Red"
        return $false
    }
    
    $extension = [System.IO.Path]::GetExtension($Path)
    if ($extension -ne ".pdf") {
        Write-ColorOutput "❌ 文件不是PDF格式: $Path" "Red"
        return $false
    }
    
    return $true
}

# 获取文件大小
function Get-FileSize {
    param([string]$Path)
    
    $file = Get-Item $Path
    $sizeInMB = [math]::Round($file.Length / 1MB, 2)
    return $sizeInMB
}

# 检查Ghostscript是否安装
function Test-Ghostscript {
    try {
        $gsVersion = gs --version 2>$null
        if ($gsVersion) {
            Write-ColorOutput "✅ Ghostscript版本: $gsVersion" "Green"
            return $true
        }
    }
    catch {
        Write-ColorOutput "⚠️  Ghostscript未安装，将使用在线压缩服务" "Yellow"
        return $false
    }
    return $false
}

# 使用Ghostscript压缩PDF
function Compress-PDFWithGhostscript {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [string]$Level
    )
    
    $settings = switch ($Level) {
        "low" { 
            @{
                dPDFSETTINGS = "/printer"
                dCompatibilityLevel = "1.4"
                dAutoFilterColorImages = "false"
                dColorImageFilter = "/DCTEncode"
                dGrayImageFilter = "/DCTEncode"
                dMonoImageFilter = "/CCITTFaxEncode"
                dColorImageResolution = "150"
                dGrayImageResolution = "150"
                dMonoImageResolution = "150"
            }
        }
        "medium" { 
            @{
                dPDFSETTINGS = "/ebook"
                dCompatibilityLevel = "1.4"
                dAutoFilterColorImages = "false"
                dColorImageFilter = "/DCTEncode"
                dGrayImageFilter = "/DCTEncode"
                dMonoImageFilter = "/CCITTFaxEncode"
                dColorImageResolution = "150"
                dGrayImageResolution = "150"
                dMonoImageResolution = "150"
            }
        }
        "high" { 
            @{
                dPDFSETTINGS = "/screen"
                dCompatibilityLevel = "1.4"
                dAutoFilterColorImages = "false"
                dColorImageFilter = "/DCTEncode"
                dGrayImageFilter = "/DCTEncode"
                dMonoImageFilter = "/CCITTFaxEncode"
                dColorImageResolution = "72"
                dGrayImageResolution = "72"
                dMonoImageResolution = "72"
            }
        }
        "extreme" { 
            @{
                dPDFSETTINGS = "/screen"
                dCompatibilityLevel = "1.4"
                dAutoFilterColorImages = "false"
                dColorImageFilter = "/DCTEncode"
                dGrayImageFilter = "/DCTEncode"
                dMonoImageFilter = "/CCITTFaxEncode"
                dColorImageResolution = "72"
                dGrayImageResolution = "72"
                dMonoImageResolution = "72"
                dOptimize = "true"
                dDownsampleColorImages = "true"
                dDownsampleGrayImages = "true"
                dDownsampleMonoImages = "true"
            }
        }
    }
    
    $gsArgs = @(
        "-sDEVICE=pdfwrite",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH"
    )
    
    foreach ($key in $settings.Keys) {
        $gsArgs += "-$key", $settings[$key]
    }
    
    $gsArgs += "-sOutputFile=`"$OutputPath`"", "`"$InputPath`""
    
    Write-ColorOutput "🔧 使用Ghostscript压缩PDF..." "Yellow"
    Write-ColorOutput "压缩级别: $Level" "White"
    
    try {
        $process = Start-Process -FilePath "gs" -ArgumentList $gsArgs -NoNewWindow -PassThru -Wait
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "✅ Ghostscript压缩完成" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Ghostscript压缩失败，退出代码: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Ghostscript执行失败: $_" "Red"
        return $false
    }
}

# 使用Python压缩PDF（备用方案）
function Compress-PDFWithPython {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [string]$Level
    )
    
    $pythonScript = @"
import fitz  # PyMuPDF
import sys

def compress_pdf(input_path, output_path, compression_level):
    try:
        # 打开PDF
        doc = fitz.open(input_path)
        
        # 根据压缩级别设置参数
        if compression_level == "low":
            image_quality = 85
            image_dpi = 150
        elif compression_level == "medium":
            image_quality = 70
            image_dpi = 120
        elif compression_level == "high":
            image_quality = 50
            image_dpi = 96
        else:  # extreme
            image_quality = 30
            image_dpi = 72
        
        # 创建新的PDF文档
        new_doc = fitz.open()
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # 获取页面内容
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1))
            
            # 压缩图像
            img_data = pix.tobytes("jpeg", quality=image_quality)
            
            # 创建新页面
            new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
            
            # 插入压缩后的图像
            new_page.insert_image(page.rect, stream=img_data)
        
        # 保存压缩后的PDF
        new_doc.save(output_path, garbage=4, deflate=True)
        new_doc.close()
        doc.close()
        
        print("✅ Python压缩完成")
        return True
        
    except Exception as e:
        print(f"❌ Python压缩失败: {e}")
        return False

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    level = sys.argv[3]
    
    success = compress_pdf(input_file, output_file, level)
    sys.exit(0 if success else 1)
"@
    
    $tempScriptPath = Join-Path $env:TEMP "compress_pdf_temp.py"
    $pythonScript | Out-File -FilePath $tempScriptPath -Encoding UTF8
    
    Write-ColorOutput "🔧 使用Python压缩PDF..." "Yellow"
    Write-ColorOutput "压缩级别: $Level" "White"
    
    try {
        $process = Start-Process -FilePath "python" -ArgumentList $tempScriptPath, $InputPath, $OutputPath, $Level -NoNewWindow -PassThru -Wait
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "✅ Python压缩完成" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ Python压缩失败，退出代码: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Python执行失败: $_" "Red"
        return $false
    }
    finally {
        if (Test-Path $tempScriptPath) {
            Remove-Item $tempScriptPath -Force
        }
    }
}

# 显示压缩结果
function Show-CompressionResult {
    param(
        [string]$OriginalPath,
        [string]$CompressedPath
    )
    
    $originalSize = Get-FileSize $OriginalPath
    $compressedSize = Get-FileSize $CompressedPath
    
    $savings = $originalSize - $compressedSize
    $savingsPercent = [math]::Round(($savings / $originalSize) * 100, 1)
    
    Write-ColorOutput ""
    Write-ColorOutput "📊 压缩结果:" "Cyan"
    Write-ColorOutput "原始大小: ${originalSize}MB" "White"
    Write-ColorOutput "压缩后: ${compressedSize}MB" "White"
    Write-ColorOutput "节省空间: ${savings}MB (${savingsPercent}%)" "Green"
    Write-ColorOutput ""
}

# 主函数
function Main {
    Write-ColorOutput "=== PDF压缩工具 ===" "Cyan"
    Write-ColorOutput ""
    
    # 检查输入文件
    if (-not (Test-PDFFile $InputPath)) {
        exit 1
    }
    
    # 设置输出路径
    if ([string]::IsNullOrEmpty($OutputPath)) {
        $inputDir = Split-Path $InputPath -Parent
        $inputName = [System.IO.Path]::GetFileNameWithoutExtension($InputPath)
        $OutputPath = Join-Path $inputDir "${inputName}_compressed.pdf"
    }
    
    # 显示原始文件信息
    $originalSize = Get-FileSize $InputPath
    Write-ColorOutput "📄 原始文件: $InputPath" "White"
    Write-ColorOutput "📏 文件大小: ${originalSize}MB" "White"
    Write-ColorOutput "🎯 压缩级别: $CompressionLevel" "White"
    Write-ColorOutput "📁 输出文件: $OutputPath" "White"
    Write-ColorOutput ""
    
    # 检查Ghostscript
    $hasGhostscript = Test-Ghostscript
    
    # 执行压缩
    $success = $false
    
    if ($hasGhostscript) {
        $success = Compress-PDFWithGhostscript -InputPath $InputPath -OutputPath $OutputPath -Level $CompressionLevel
    }
    
    if (-not $success) {
        Write-ColorOutput "🔄 尝试使用Python压缩..." "Yellow"
        $success = Compress-PDFWithPython -InputPath $InputPath -OutputPath $OutputPath -Level $CompressionLevel
    }
    
    if ($success) {
        # 显示压缩结果
        Show-CompressionResult -OriginalPath $InputPath -CompressedPath $OutputPath
        
        # 删除原文件（如果指定）
        if (-not $KeepOriginal) {
            Write-ColorOutput "🗑️  删除原始文件..." "Yellow"
            Remove-Item $InputPath -Force
            Write-ColorOutput "✅ 原始文件已删除" "Green"
        }
        
        Write-ColorOutput "🎉 PDF压缩完成！" "Green"
        Write-ColorOutput "输出文件: $OutputPath" "White"
    } else {
        Write-ColorOutput "💥 PDF压缩失败！" "Red"
        exit 1
    }
}

# 显示帮助信息
if ($InputPath -eq "help" -or $InputPath -eq "-h" -or $InputPath -eq "--help") {
    Write-ColorOutput "=== PDF压缩工具帮助 ===" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "使用方法:" "Yellow"
    Write-ColorOutput "  .\compress-pdf.ps1 -InputPath 'file.pdf' -CompressionLevel medium" "White"
    Write-ColorOutput "  .\compress-pdf.ps1 -InputPath 'file.pdf' -CompressionLevel high -KeepOriginal" "White"
    Write-ColorOutput ""
    Write-ColorOutput "参数说明:" "Yellow"
    Write-ColorOutput "  -InputPath: 输入PDF文件路径" "White"
    Write-ColorOutput "  -CompressionLevel: 压缩级别 (low/medium/high/extreme)" "White"
    Write-ColorOutput "  -OutputPath: 输出文件路径（可选）" "White"
    Write-ColorOutput "  -KeepOriginal: 保留原始文件" "White"
    Write-ColorOutput ""
    Write-ColorOutput "压缩级别说明:" "Yellow"
    Write-ColorOutput "  low: 轻微压缩，保持高质量" "White"
    Write-ColorOutput "  medium: 中等压缩，平衡质量和大小" "White"
    Write-ColorOutput "  high: 高压缩，显著减小文件大小" "White"
    Write-ColorOutput "  extreme: 极限压缩，最大程度减小文件大小" "White"
    Write-ColorOutput ""
    Write-ColorOutput "示例:" "Yellow"
    Write-ColorOutput "  .\compress-pdf.ps1 -InputPath 'book1_CN_Complete.pdf' -CompressionLevel medium" "White"
    Write-ColorOutput "  .\compress-pdf.ps1 -InputPath 'large.pdf' -CompressionLevel extreme -KeepOriginal" "White"
    return
}

# 执行主函数
Main 