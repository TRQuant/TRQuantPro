# 从Git拉取共用模块更新（Windows端）

$PROJECT_ROOT = "C:\Users\Administrator\.cursor\worktrees\TRQuantPro\ope"
Set-Location $PROJECT_ROOT

Write-Host "=========================================="
Write-Host "从Git拉取共用模块更新"
Write-Host "=========================================="

# 检查远程仓库
$remotes = git remote
if ($remotes -notmatch "origin") {
    Write-Host "❌ 未配置远程仓库"
    exit 1
}

# 获取当前分支
$CURRENT_BRANCH = git branch --show-current
if ([string]::IsNullOrEmpty($CURRENT_BRANCH)) {
    Write-Host "❌ 未在Git分支上，请先创建分支"
    exit 1
}

# 拉取更新
Write-Host "拉取远程更新 (分支: $CURRENT_BRANCH)..."
git fetch origin $CURRENT_BRANCH

# 检查是否有冲突
$status = git status --porcelain
if (-not [string]::IsNullOrEmpty($status)) {
    Write-Host "⚠️  有未提交的本地更改，请先提交或暂存"
    git status
    $confirm = Read-Host "是否继续合并? (y/n)"
    if ($confirm -ne "y") {
        exit 1
    }
}

# 合并
Write-Host "合并远程更新..."
try {
    git merge "origin/$CURRENT_BRANCH"
    Write-Host "✅ 合并成功"
    
    # 如果知识库有更新，重建向量索引
    $kbChanged = git diff HEAD@{1} HEAD --name-only 2>$null | Select-String "knowledge_base.json"
    if ($kbChanged) {
        Write-Host "知识库已更新，重建向量索引..."
        if (Get-Command python -ErrorAction SilentlyContinue) {
            python scripts\kb\kb_manager.py build-index 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ 向量索引重建成功"
            } else {
                Write-Host "⚠️  向量索引重建失败（可能需要手动重建）"
            }
        } else {
            Write-Host "⚠️  未找到Python，请手动重建向量索引"
        }
    }
} catch {
    Write-Host "❌ 合并失败，请手动解决冲突"
    exit 1
}

Write-Host "✅ 共用模块更新完成"
