# 简化的PDF内容提取调用脚本
param(
    [Parameter(Mandatory=$true)]
    [string]$PdfFile,
    [string]$OutputFolder = "extracted_content"
)

Write-Host "=== PDF内容提取工具 ===" -ForegroundColor Cyan
Write-Host "正在调用综合提取脚本..." -ForegroundColor Yellow

# 获取脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 调用主提取脚本
$mainScript = Join-Path $scriptDir "comprehensive-pdf-extractor.ps1"

if (Test-Path $mainScript) {
    & $mainScript -PdfPath $PdfFile -OutputDir $OutputFolder
} else {
    Write-Error "找不到主提取脚本: $mainScript"
    Write-Host "请确保 comprehensive-pdf-extractor.ps1 文件存在于同一目录中" -ForegroundColor Red
}

Write-Host "`n使用示例:" -ForegroundColor Green
Write-Host "  .\extract-pdf.ps1 -PdfFile 'C:\path\to\your\file.pdf'" -ForegroundColor Gray
Write-Host "  .\extract-pdf.ps1 -PdfFile 'document.pdf' -OutputFolder 'my_output'" -ForegroundColor Gray 