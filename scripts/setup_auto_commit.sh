#!/bin/bash
# 设置自动提交和推送

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

echo "🔧 设置TRQuant自动提交..."

# 1. 创建git alias
git config alias.acp '!f() { python3 scripts/auto_commit_push.py; }; f'
echo "✅ Git alias 'acp' 已创建（使用: git acp）"

# 2. 设置post-commit hook（可选）
read -p "是否启用自动推送？(y/N): " enable_auto_push
if [ "$enable_auto_push" = "y" ] || [ "$enable_auto_push" = "Y" ]; then
    cat > "$PROJECT_ROOT/.git/hooks/post-commit" << 'HOOK_EOF'
#!/bin/bash
# 自动推送
git push origin main 2>&1 | grep -v "Everything up-to-date"
HOOK_EOF
    chmod +x "$PROJECT_ROOT/.git/hooks/post-commit"
    echo "✅ 自动推送已启用（每次commit后自动push）"
else
    echo "ℹ️  自动推送未启用，可手动使用: git acp 或 python3 scripts/auto_commit_push.py"
fi

echo ""
echo "📖 使用方法:"
echo "  1. 手动提交: python3 scripts/auto_commit_push.py"
echo "  2. Git alias: git acp"
echo "  3. Shell脚本: ./scripts/auto_commit_push.sh"

