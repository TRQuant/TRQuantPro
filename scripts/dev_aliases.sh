# TRQuant 开发别名
# 添加到 ~/.bashrc 或 ~/.zshrc

alias trquant='cd /home/taotao/dev/QuantTest/TRQuant && source venv/bin/activate'
alias trdev='cd /home/taotao/dev/QuantTest/TRQuant && source venv/bin/activate && python scripts/dev_workflow.py check'
alias trstart='python scripts/dev_workflow.py start'
alias trlog='python scripts/dev_workflow.py log'
alias trcomplete='python scripts/dev_workflow.py complete'
alias trstatus='python scripts/dev_workflow.py status'
alias trsearch='python scripts/dev_workflow.py search'
