# 同步共用模块到Git（Windows端）
# 用途: 将共用模块的更改提交并推送到远程仓库

$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
Set-Location $PROJECT_ROOT

# 共用模块列表
$COMMON_MODULES = @(
    "core",
    "mcp_servers",
    "notebooks",
    "scripts",
    "strategies",
    "data_sources",
    "utils",
    "docs",
    ".trquant\dev\knowledge"
)

Write-Host "=========================================="
Write-Host "同步共用模块到Git"
Write-Host "=========================================="

# 检查是否有未提交的更改
$status = git status --porcelain
if ([string]::IsNullOrEmpty($status)) {
    Write-Host "✅ 没有未提交的更改"
    exit 0
}

# 添加共用模块
foreach ($module in $COMMON_MODULES) {
    if (Test-Path $module) {
        Write-Host "添加 $module..."
        git add $module
    }
}

# 添加知识库文件
$KB_JSON = ".trquant\dev\knowledge\knowledge_base.json"
if (Test-Path $KB_JSON) {
    Write-Host "添加知识库..."
    git add $KB_JSON
    $KB_STRATEGY = ".trquant\dev\knowledge\strategy_knowledge"
    if (Test-Path $KB_STRATEGY) {
        git add $KB_STRATEGY
    }
}

# 检查是否有更改
$staged = git diff --cached --name-only
if ([string]::IsNullOrEmpty($staged)) {
    Write-Host "✅ 没有需要提交的更改"
    exit 0
}

# 提交
$COMMIT_MSG = Read-Host "请输入提交信息 (默认: sync: 同步共用模块)"
if ([string]::IsNullOrEmpty($COMMIT_MSG)) {
    $COMMIT_MSG = "sync: 同步共用模块"
}

git commit -m $COMMIT_MSG

# 推送到远程
$remotes = git remote
if ($remotes -match "origin") {
    $confirm = Read-Host "是否推送到远程仓库? (y/n)"
    if ($confirm -eq "y") {
        $CURRENT_BRANCH = git branch --show-current
        git push origin $CURRENT_BRANCH
        Write-Host "✅ 已推送到远程仓库 (分支: $CURRENT_BRANCH)"
    }
} else {
    Write-Host "⚠️  未配置远程仓库，跳过推送"
}

Write-Host "✅ 共用模块同步完成"
