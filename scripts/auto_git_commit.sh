#!/usr/bin/env bash
# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac






# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac




# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac

# ============================================================
# 韬睿量化专业版 - Git自动提交脚本
# 监控文件变化并自动commit
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

# 配置
WATCH_INTERVAL="${GIT_WATCH_INTERVAL:-300}"  # 默认5分钟检查一次
AUTO_PUSH="${GIT_AUTO_PUSH:-false}"          # 是否自动push
COMMIT_PREFIX="${GIT_COMMIT_PREFIX:-[Auto]}" # commit消息前缀

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"
}

# 检查是否有未提交的更改
check_changes() {
    git status --porcelain | grep -v "^??" | head -1
}

# 获取更改摘要
get_change_summary() {
    local added modified deleted
    added=$(git status --porcelain | grep "^A" | wc -l)
    modified=$(git status --porcelain | grep "^M" | wc -l)
    deleted=$(git status --porcelain | grep "^D" | wc -l)
    
    local parts=()
    [[ $added -gt 0 ]] && parts+=("新增${added}个文件")
    [[ $modified -gt 0 ]] && parts+=("修改${modified}个文件")
    [[ $deleted -gt 0 ]] && parts+=("删除${deleted}个文件")
    
    if [[ ${#parts[@]} -gt 0 ]]; then
        IFS=', ' ; echo "${parts[*]}"
    else
        echo "更新"
    fi
}

# 执行提交
do_commit() {
    local summary
    summary=$(get_change_summary)
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M')
    local message="${COMMIT_PREFIX} ${summary} (${timestamp})"
    
    log "${GREEN}📝 提交更改: ${message}${NC}"
    
    git add -A
    git commit -m "${message}"
    
    if [[ "${AUTO_PUSH}" == "true" ]]; then
        log "${YELLOW}📤 推送到远程...${NC}"
        git push || log "${YELLOW}⚠️ 推送失败，请手动处理${NC}"
    fi
}

# 单次检查并提交
single_commit() {
    if [[ -n "$(check_changes)" ]]; then
        do_commit
    else
        log "没有需要提交的更改"
    fi
}

# 守护模式：持续监控
daemon_mode() {
    log "🔄 启动Git自动提交守护进程"
    log "   检查间隔: ${WATCH_INTERVAL}秒"
    log "   自动推送: ${AUTO_PUSH}"
    log "   按 Ctrl+C 停止"
    echo ""
    
    while true; do
        if [[ -n "$(check_changes)" ]]; then
            do_commit
        fi
        sleep "${WATCH_INTERVAL}"
    done
}

# 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  commit    立即检查并提交更改"
    echo "  daemon    启动守护进程持续监控"
    echo "  status    显示当前Git状态"
    echo "  help      显示此帮助"
    echo ""
    echo "环境变量:"
    echo "  GIT_WATCH_INTERVAL  检查间隔秒数 (默认: 300)"
    echo "  GIT_AUTO_PUSH       是否自动push (默认: false)"
    echo "  GIT_COMMIT_PREFIX   commit消息前缀 (默认: [Auto])"
}

# 主入口
case "${1:-commit}" in
    commit)
        single_commit
        ;;
    daemon)
        daemon_mode
        ;;
    status)
        git status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "未知命令: $1"
        show_help
        exit 1
        ;;
esac














