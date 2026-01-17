# 知识库每日自动同步脚本（Windows端）
# 用途: 每天自动同步知识库到Git
# 添加到任务计划程序: 每天9点运行

$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
$LOG_FILE = "$PROJECT_ROOT\.sync_kb_daily.log"

Set-Location $PROJECT_ROOT

Add-Content -Path $LOG_FILE -Value "=========================================="
Add-Content -Path $LOG_FILE -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] 开始每日知识库同步"
Add-Content -Path $LOG_FILE -Value "=========================================="

# 检查知识库文件
$KB_JSON = ".trquant\dev\knowledge\knowledge_base.json"

if (-not (Test-Path $KB_JSON)) {
    Add-Content -Path $LOG_FILE -Value "❌ 知识库JSON文件不存在: $KB_JSON"
    exit 1
}

# 添加知识库文件
git add $KB_JSON
git add .trquant\dev\knowledge\strategy_knowledge\ 2>$null

# 检查是否有更改
$staged = git diff --cached --name-only
if ([string]::IsNullOrEmpty($staged)) {
    Add-Content -Path $LOG_FILE -Value "✅ 知识库没有更改"
    exit 0
}

# 提交
$COMMIT_MSG = "sync: 知识库每日自动同步 $(Get-Date -Format 'yyyy-MM-dd')"
git commit -m $COMMIT_MSG

# 推送到远程
$remotes = git remote
if ($remotes -match "origin") {
    git push origin windows
    Add-Content -Path $LOG_FILE -Value "✅ 知识库已推送到远程仓库"
} else {
    Add-Content -Path $LOG_FILE -Value "⚠️  未配置远程仓库，跳过推送"
}

Add-Content -Path $LOG_FILE -Value "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] 知识库同步完成"
