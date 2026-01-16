# 知识库同步脚本（Windows端）
# 用途: 将知识库更改提交并推送到Git

$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
Set-Location $PROJECT_ROOT

Write-Host "=========================================="
Write-Host "同步知识库到Git"
Write-Host "=========================================="

# 检查知识库文件
$KB_JSON = ".trquant\dev\knowledge\knowledge_base.json"
$KB_STRATEGY = ".trquant\dev\knowledge\strategy_knowledge"

if (-not (Test-Path $KB_JSON)) {
    Write-Host "❌ 知识库JSON文件不存在: $KB_JSON"
    exit 1
}

# 添加知识库文件
Write-Host "添加知识库文件..."
git add $KB_JSON
if (Test-Path $KB_STRATEGY) {
    git add $KB_STRATEGY
}

# 检查是否有更改
$staged = git diff --cached --name-only
if ([string]::IsNullOrEmpty($staged)) {
    Write-Host "✅ 知识库没有更改"
    exit 0
}

# 提交
$COMMIT_MSG = Read-Host "请输入提交信息 (默认: sync: 知识库更新)"
if ([string]::IsNullOrEmpty($COMMIT_MSG)) {
    $COMMIT_MSG = "sync: 知识库更新"
}

git commit -m $COMMIT_MSG

# 推送到远程
$remotes = git remote
if ($remotes -match "origin") {
    $confirm = Read-Host "是否推送到远程仓库? (y/n)"
    if ($confirm -eq "y") {
        $CURRENT_BRANCH = git branch --show-current
        git push origin $CURRENT_BRANCH
        Write-Host "✅ 知识库已推送到远程仓库 (分支: $CURRENT_BRANCH)"
    }
} else {
    Write-Host "⚠️  未配置远程仓库，跳过推送"
}

Write-Host "✅ 知识库同步完成"
