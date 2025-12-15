# 语言版本PDF生成脚本
# 支持按中文(CN)或英文(EN)分别生成PDF

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("CN", "EN")]
    [string]$Language,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("single", "chapter", "book", "all")]
    [string]$Type = "all",
    
    [Parameter(Mandatory=$false)]
    [string]$Path = "",
    
    [Parameter(Mandatory=$false)]
    [string]$URL = ""
)

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# 显示帮助信息
function Show-Help {
    Write-ColorOutput "=== 语言版本PDF生成工具 ===" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "使用方法:" "Yellow"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language CN -Type all" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language EN -Type book -Path book1" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language CN -Type chapter -Path book1/001_Chapter1" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language EN -Type single -URL /book1/001_Chapter1/1.1_xxx_EN" "White"
    Write-ColorOutput ""
    Write-ColorOutput "参数说明:" "Yellow"
    Write-ColorOutput "  -Language: 语言版本 (CN/EN)" "White"
    Write-ColorOutput "  -Type: 生成类型 (single/chapter/book/all)" "White"
    Write-ColorOutput "  -Path: 路径参数 (用于chapter/book类型)" "White"
    Write-ColorOutput "  -URL: URL参数 (用于single类型)" "White"
    Write-ColorOutput ""
    Write-ColorOutput "示例:" "Yellow"
    Write-ColorOutput "  # 生成所有书籍的中文版PDF" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language CN -Type all" "White"
    Write-ColorOutput ""
    Write-ColorOutput "  # 生成book1的英文版PDF" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language EN -Type book -Path book1" "White"
    Write-ColorOutput ""
    Write-ColorOutput "  # 生成第一章的中文版PDF" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language CN -Type chapter -Path book1/001_Chapter1" "White"
    Write-ColorOutput ""
    Write-ColorOutput "  # 生成单个页面的英文版PDF" "White"
    Write-ColorOutput "  .\generate-pdf-by-language.ps1 -Language EN -Type single -URL /book1/001_Chapter1/1.1_xxx_EN" "White"
}

# 检查Node.js环境
function Test-NodeEnvironment {
    try {
        $nodeVersion = node --version
        Write-ColorOutput "✅ Node.js版本: $nodeVersion" "Green"
    }
    catch {
        Write-ColorOutput "❌ 未找到Node.js，请先安装Node.js" "Red"
        exit 1
    }
}

# 检查npm脚本
function Test-NpmScripts {
    $packageJson = Get-Content "package.json" | ConvertFrom-Json
    
    $requiredScripts = @(
        "pdf:lang:single",
        "pdf:lang:chapter", 
        "pdf:lang:book",
        "pdf:lang:all"
    )
    
    $missingScripts = @()
    
    foreach ($script in $requiredScripts) {
        if (-not $packageJson.scripts.PSObject.Properties.Name.Contains($script)) {
            $missingScripts += $script
        }
    }
    
    if ($missingScripts.Count -gt 0) {
        Write-ColorOutput "❌ 缺少以下npm脚本: $($missingScripts -join ', ')" "Red"
        Write-ColorOutput "请确保已正确配置package.json中的PDF生成脚本" "Yellow"
        exit 1
    }
    
    Write-ColorOutput "✅ npm脚本检查通过" "Green"
}

# 检查开发服务器
function Test-DevServer {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:4321" -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "✅ 开发服务器运行正常" "Green"
            return $true
        }
    }
    catch {
        Write-ColorOutput "⚠️  开发服务器未运行，正在启动..." "Yellow"
        return $false
    }
}

# 启动开发服务器
function Start-DevServer {
    Write-ColorOutput "🚀 正在启动开发服务器..." "Yellow"
    
    # 在后台启动开发服务器
    Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Hidden
    
    # 等待服务器启动
    $maxAttempts = 30
    $attempt = 0
    
    while ($attempt -lt $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:4321" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput "✅ 开发服务器已启动" "Green"
                return $true
            }
        }
        catch {
            # 继续等待
        }
        
        $attempt++
        Start-Sleep -Seconds 2
        Write-ColorOutput "⏳ 等待服务器启动... ($attempt/$maxAttempts)" "Yellow"
    }
    
    Write-ColorOutput "❌ 开发服务器启动超时" "Red"
    return $false
}

# 生成PDF
function Generate-PDF {
    param(
        [string]$Type,
        [string]$Language,
        [string]$Path = "",
        [string]$URL = ""
    )
    
    $scriptPath = "scripts/astro-pdf-generator-lang.mjs"
    
    if (-not (Test-Path $scriptPath)) {
        Write-ColorOutput "❌ PDF生成脚本不存在: $scriptPath" "Red"
        return $false
    }
    
    $arguments = @("node", $scriptPath, $Type)
    
    switch ($Type) {
        "single" {
            if ([string]::IsNullOrEmpty($URL)) {
                Write-ColorOutput "❌ 单页生成需要提供URL参数" "Red"
                return $false
            }
            $arguments += $URL, $Language
        }
        "chapter" {
            if ([string]::IsNullOrEmpty($Path)) {
                Write-ColorOutput "❌ 章节生成需要提供Path参数" "Red"
                return $false
            }
            $arguments += $Path, $Language
        }
        "book" {
            if ([string]::IsNullOrEmpty($Path)) {
                Write-ColorOutput "❌ 整册生成需要提供Path参数" "Red"
                return $false
            }
            $arguments += $Path, $Language
        }
        "all" {
            $arguments += $Language
        }
    }
    
    Write-ColorOutput "📄 开始生成 $Language 版本的 $Type PDF..." "Cyan"
    Write-ColorOutput "命令: $($arguments -join ' ')" "Gray"
    Write-ColorOutput ""
    
    try {
        $process = Start-Process -FilePath "node" -ArgumentList $arguments[1..($arguments.Length-1)] -NoNewWindow -PassThru -Wait
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "✅ PDF生成完成" "Green"
            return $true
        } else {
            Write-ColorOutput "❌ PDF生成失败，退出代码: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ PDF生成过程中出现错误: $_" "Red"
        return $false
    }
}

# 主函数
function Main {
    # 显示帮助信息
    if ($Language -eq "help" -or $Language -eq "-h" -or $Language -eq "--help") {
        Show-Help
        return
    }
    
    Write-ColorOutput "=== 语言版本PDF生成工具 ===" "Cyan"
    Write-ColorOutput "语言: $Language" "White"
    Write-ColorOutput "类型: $Type" "White"
    if ($Path) { Write-ColorOutput "路径: $Path" "White" }
    if ($URL) { Write-ColorOutput "URL: $URL" "White" }
    Write-ColorOutput ""
    
    # 检查环境
    Test-NodeEnvironment
    Test-NpmScripts
    
    # 检查开发服务器
    if (-not (Test-DevServer)) {
        if (-not (Start-DevServer)) {
            Write-ColorOutput "❌ 无法启动开发服务器，请手动运行: npm run dev" "Red"
            exit 1
        }
    }
    
    Write-ColorOutput ""
    
    # 生成PDF
    $success = Generate-PDF -Type $Type -Language $Language -Path $Path -URL $URL
    
    if ($success) {
        Write-ColorOutput ""
        Write-ColorOutput "🎉 PDF生成任务完成！" "Green"
        Write-ColorOutput "输出目录: dist/pdf/" "White"
    } else {
        Write-ColorOutput ""
        Write-ColorOutput "💥 PDF生成任务失败！" "Red"
        exit 1
    }
}

# 执行主函数
Main 