"""
隐藏/显示Notebook代码的工具
在Notebook第一个cell运行此代码即可添加按钮
"""

from IPython.display import display, HTML

def add_hide_code_button():
    """添加隐藏/显示代码的按钮"""
    html = '''
    <style>
    .hide-code-btn {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
        padding: 8px 16px;
        background: #6366F1;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .hide-code-btn:hover {
        background: #4F46E5;
    }
    .code-hidden .jp-Cell-inputWrapper,
    .code-hidden .input {
        display: none !important;
    }
    </style>
    
    <button class="hide-code-btn" onclick="toggleCode()">🔒 隐藏代码</button>
    
    <script>
    var codeHidden = false;
    function toggleCode() {
        var btn = document.querySelector('.hide-code-btn');
        var body = document.body;
        
        if (codeHidden) {
            body.classList.remove('code-hidden');
            btn.innerHTML = '🔒 隐藏代码';
            btn.style.background = '#6366F1';
        } else {
            body.classList.add('code-hidden');
            btn.innerHTML = '👁️ 显示代码';
            btn.style.background = '#10B981';
        }
        codeHidden = !codeHidden;
    }
    </script>
    '''
    display(HTML(html))
    print("✅ 代码隐藏按钮已添加（右上角）")

# 直接调用
if __name__ != "__main__":
    pass
