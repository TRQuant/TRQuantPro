#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
代码格式转换工具
================

功能：
1. Python代码 → HTML格式化显示
2. 支持语法高亮（使用Pygments）
3. 支持行号显示
4. 支持代码折叠
5. 支持多种主题

代码位置: utils/code_to_html.py

使用方法：
```python
from utils.code_to_html import CodeToHtml

converter = CodeToHtml()
html = converter.convert_file('/path/to/file.py', title='策略代码')
html = converter.convert_code(code_string, language='python', title='核心算法')
```
"""

import re
import html as html_lib
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# 尝试导入Pygments用于高级语法高亮
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    logger.warning("Pygments未安装，使用简单语法高亮")


class CodeToHtml:
    """代码转HTML工具"""
    
    # Python关键字
    PYTHON_KEYWORDS = {
        'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except',
        'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'raise',
        'pass', 'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'lambda',
        'True', 'False', 'None', 'global', 'nonlocal', 'assert', 'del', 'async', 'await'
    }
    
    # 内置函数
    PYTHON_BUILTINS = {
        'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
        'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool', 'type',
        'isinstance', 'hasattr', 'getattr', 'setattr', 'open', 'abs', 'min', 'max',
        'sum', 'any', 'all', 'round', 'input', 'id', 'hex', 'bin', 'oct', 'ord', 'chr'
    }
    
    # 主题配置
    THEMES = {
        'monokai': {
            'background': '#272822',
            'text': '#f8f8f2',
            'comment': '#75715e',
            'keyword': '#f92672',
            'string': '#e6db74',
            'function': '#a6e22e',
            'number': '#ae81ff',
            'builtin': '#66d9ef',
            'decorator': '#66d9ef',
            'class': '#a6e22e',
            'line_number': '#75715e',
            'line_bg': '#3e3d32'
        },
        'github': {
            'background': '#ffffff',
            'text': '#24292e',
            'comment': '#6a737d',
            'keyword': '#d73a49',
            'string': '#032f62',
            'function': '#6f42c1',
            'number': '#005cc5',
            'builtin': '#005cc5',
            'decorator': '#6f42c1',
            'class': '#6f42c1',
            'line_number': '#6a737d',
            'line_bg': '#f6f8fa'
        },
        'dracula': {
            'background': '#282a36',
            'text': '#f8f8f2',
            'comment': '#6272a4',
            'keyword': '#ff79c6',
            'string': '#f1fa8c',
            'function': '#50fa7b',
            'number': '#bd93f9',
            'builtin': '#8be9fd',
            'decorator': '#ff79c6',
            'class': '#8be9fd',
            'line_number': '#6272a4',
            'line_bg': '#44475a'
        },
        'nord': {
            'background': '#2e3440',
            'text': '#d8dee9',
            'comment': '#616e88',
            'keyword': '#81a1c1',
            'string': '#a3be8c',
            'function': '#88c0d0',
            'number': '#b48ead',
            'builtin': '#8fbcbb',
            'decorator': '#d08770',
            'class': '#8fbcbb',
            'line_number': '#4c566a',
            'line_bg': '#3b4252'
        }
    }
    
    def __init__(self, theme: str = 'monokai', show_line_numbers: bool = True):
        """
        初始化转换器
        
        Args:
            theme: 主题名称 (monokai/github/dracula/nord)
            show_line_numbers: 是否显示行号
        """
        self.theme = self.THEMES.get(theme, self.THEMES['monokai'])
        self.theme_name = theme
        self.show_line_numbers = show_line_numbers
    
    def convert_file(self, file_path: str, title: str = None, 
                     start_line: int = None, end_line: int = None,
                     collapsible: bool = True) -> str:
        """
        转换文件为HTML
        
        Args:
            file_path: 文件路径
            title: 代码块标题
            start_line: 起始行号（可选）
            end_line: 结束行号（可选）
            collapsible: 是否可折叠
        """
        path = Path(file_path)
        if not path.exists():
            return f'<div class="code-error">文件不存在: {file_path}</div>'
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 提取指定行
        if start_line is not None or end_line is not None:
            start = (start_line or 1) - 1
            end = end_line or len(lines)
            lines = lines[start:end]
            line_offset = start
        else:
            line_offset = 0
        
        code = ''.join(lines)
        
        if title is None:
            title = path.name
        
        return self.convert_code(
            code, 
            language=self._detect_language(path.suffix),
            title=title,
            collapsible=collapsible,
            line_offset=line_offset
        )
    
    def convert_code(self, code: str, language: str = 'python', 
                     title: str = None, collapsible: bool = True,
                     line_offset: int = 0) -> str:
        """
        转换代码字符串为HTML
        
        Args:
            code: 代码字符串
            language: 语言类型
            title: 代码块标题
            collapsible: 是否可折叠
            line_offset: 行号偏移
        """
        if PYGMENTS_AVAILABLE:
            return self._convert_with_pygments(code, language, title, collapsible, line_offset)
        else:
            return self._convert_simple(code, language, title, collapsible, line_offset)
    
    def _convert_with_pygments(self, code: str, language: str, 
                                title: str, collapsible: bool, 
                                line_offset: int) -> str:
        """使用Pygments转换"""
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = PythonLexer()
        
        formatter = HtmlFormatter(
            linenos=self.show_line_numbers,
            cssclass='highlight',
            style=self.theme_name if self.theme_name in ['monokai', 'github'] else 'monokai',
            linenostart=line_offset + 1
        )
        
        highlighted = highlight(code, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        
        # 构建HTML
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            {css}
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .highlight {{
                background: {self.theme['background']} !important;
                padding: 15px;
                overflow-x: auto;
                margin: 0;
            }}
            .highlight pre {{
                margin: 0;
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                {highlighted}
            </div>
        </div>
        '''
    
    def _convert_simple(self, code: str, language: str, 
                        title: str, collapsible: bool,
                        line_offset: int) -> str:
        """简单语法高亮（无Pygments）"""
        
        lines = code.split('\n')
        highlighted_lines = []
        
        for i, line in enumerate(lines, start=line_offset + 1):
            highlighted = self._highlight_line(line)
            
            if self.show_line_numbers:
                line_num = f'<span class="line-number">{i:4d}</span>'
                highlighted_lines.append(f'{line_num}{highlighted}')
            else:
                highlighted_lines.append(highlighted)
        
        code_html = '\n'.join(highlighted_lines)
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .code-body {{
                background: {self.theme['background']};
                padding: 15px;
                overflow-x: auto;
            }}
            .code-body pre {{
                margin: 0;
                font-size: 13px;
                line-height: 1.6;
                color: {self.theme['text']};
            }}
            .line-number {{
                color: {self.theme['line_number']};
                padding-right: 15px;
                user-select: none;
                border-right: 1px solid rgba(255,255,255,0.1);
                margin-right: 15px;
            }}
            .keyword {{ color: {self.theme['keyword']}; font-weight: bold; }}
            .builtin {{ color: {self.theme['builtin']}; }}
            .string {{ color: {self.theme['string']}; }}
            .comment {{ color: {self.theme['comment']}; font-style: italic; }}
            .number {{ color: {self.theme['number']}; }}
            .function {{ color: {self.theme['function']}; }}
            .decorator {{ color: {self.theme['decorator']}; }}
            .class-name {{ color: {self.theme['class']}; font-weight: bold; }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                <pre>{code_html}</pre>
            </div>
        </div>
        '''
    
    def _highlight_line(self, line: str) -> str:
        """高亮单行代码"""
        # 转义HTML
        escaped = html_lib.escape(line)
        
        # 注释
        if '#' in escaped:
            idx = escaped.index('#')
            return escaped[:idx] + f'<span class="comment">{escaped[idx:]}</span>'
        
        # 装饰器
        if escaped.strip().startswith('@'):
            return f'<span class="decorator">{escaped}</span>'
        
        # 字符串 (简化处理)
        escaped = re.sub(
            r'([\"\'])(.*?)\1',
            r'<span class="string">\1\2\1</span>',
            escaped
        )
        
        # 数字
        escaped = re.sub(
            r'\b(\d+\.?\d*)\b',
            r'<span class="number">\1</span>',
            escaped
        )
        
        # 关键字
        for kw in self.PYTHON_KEYWORDS:
            escaped = re.sub(
                rf'\b({kw})\b',
                r'<span class="keyword">\1</span>',
                escaped
            )
        
        # 内置函数
        for bf in self.PYTHON_BUILTINS:
            escaped = re.sub(
                rf'\b({bf})\b(?=\s*\()',
                r'<span class="builtin">\1</span>',
                escaped
            )
        
        # 函数定义
        escaped = re.sub(
            r'def\s+(\w+)',
            r'<span class="keyword">def</span> <span class="function">\1</span>',
            escaped
        )
        
        # 类定义
        escaped = re.sub(
            r'class\s+(\w+)',
            r'<span class="keyword">class</span> <span class="class-name">\1</span>',
            escaped
        )
        
        return escaped
    
    def _detect_language(self, suffix: str) -> str:
        """检测文件语言"""
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bash': 'bash',
        }
        return mapping.get(suffix.lower(), 'python')
    
    def get_javascript(self) -> str:
        """获取JavaScript代码（用于复制和折叠功能）"""
        return '''
        <script>
        function copyCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body pre, .highlight pre');
            if (codeBody) {
                const text = codeBody.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    const btn = container.querySelector('.code-btn');
                    if (btn) {
                        const original = btn.innerText;
                        btn.innerText = '✅ 已复制';
                        setTimeout(() => btn.innerText = original, 2000);
                    }
                });
            }
        }
        
        function toggleCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body');
            const btn = container.querySelectorAll('.code-btn')[1];
            
            if (codeBody.style.display === 'none') {
                codeBody.style.display = 'block';
                if (btn) btn.innerText = '▼ 折叠';
            } else {
                codeBody.style.display = 'none';
                if (btn) btn.innerText = '▶ 展开';
            }
        }
        </script>
        '''
    
    @staticmethod
    def extract_function(file_path: str, function_name: str) -> str:
        """从文件中提取指定函数的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取函数
        pattern = rf'(def\s+{function_name}\s*\([^)]*\):.*?)(?=\ndef\s|\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""
    
    @staticmethod
    def extract_class(file_path: str, class_name: str) -> str:
        """从文件中提取指定类的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取类
        pattern = rf'(class\s+{class_name}\s*(?:\([^)]*\))?:.*?)(?=\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""


def convert_code_to_html(code: str, **kwargs) -> str:
    """便捷函数：转换代码为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_code(code, **kwargs)


def convert_file_to_html(file_path: str, **kwargs) -> str:
    """便捷函数：转换文件为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_file(file_path, **kwargs)


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    # 测试代码
    test_code = '''
def calculate_momentum(prices, period=20):
    """
    计算动量因子
    
    Args:
        prices: 价格序列
        period: 周期
    """
    if len(prices) < period:
        return None
    
    momentum = (prices[-1] / prices[-period] - 1) * 100
    return momentum


class TenbaggerStrategy:
    """十倍股策略"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.max_holdings = 2
    
    @property
    def is_ready(self):
        return True
    
    def generate_signals(self, data):
        # 计算动量
        momentum = calculate_momentum(data['close'])
        
        if momentum > 10:
            return "BUY"
        elif momentum < -5:
            return "SELL"
        return "HOLD"
'''
    
    converter = CodeToHtml(theme='monokai')
    html = converter.convert_code(test_code, title='策略示例代码')
    
    # 保存测试输出
    output_path = Path(__file__).parent.parent / "reports" / "code_highlight_test.html"
    output_path.parent.mkdir(exist_ok=True)
    
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>代码高亮测试</title>
</head>
<body style="background: #1a1a2e; padding: 30px;">
    <h1 style="color: white;">代码格式转换工具测试</h1>
    {html}
    {converter.get_javascript()}
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 测试输出: {output_path}")


"""
代码格式转换工具
================

功能：
1. Python代码 → HTML格式化显示
2. 支持语法高亮（使用Pygments）
3. 支持行号显示
4. 支持代码折叠
5. 支持多种主题

代码位置: utils/code_to_html.py

使用方法：
```python
from utils.code_to_html import CodeToHtml

converter = CodeToHtml()
html = converter.convert_file('/path/to/file.py', title='策略代码')
html = converter.convert_code(code_string, language='python', title='核心算法')
```
"""

import re
import html as html_lib
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# 尝试导入Pygments用于高级语法高亮
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    logger.warning("Pygments未安装，使用简单语法高亮")


class CodeToHtml:
    """代码转HTML工具"""
    
    # Python关键字
    PYTHON_KEYWORDS = {
        'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except',
        'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'raise',
        'pass', 'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'lambda',
        'True', 'False', 'None', 'global', 'nonlocal', 'assert', 'del', 'async', 'await'
    }
    
    # 内置函数
    PYTHON_BUILTINS = {
        'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
        'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool', 'type',
        'isinstance', 'hasattr', 'getattr', 'setattr', 'open', 'abs', 'min', 'max',
        'sum', 'any', 'all', 'round', 'input', 'id', 'hex', 'bin', 'oct', 'ord', 'chr'
    }
    
    # 主题配置
    THEMES = {
        'monokai': {
            'background': '#272822',
            'text': '#f8f8f2',
            'comment': '#75715e',
            'keyword': '#f92672',
            'string': '#e6db74',
            'function': '#a6e22e',
            'number': '#ae81ff',
            'builtin': '#66d9ef',
            'decorator': '#66d9ef',
            'class': '#a6e22e',
            'line_number': '#75715e',
            'line_bg': '#3e3d32'
        },
        'github': {
            'background': '#ffffff',
            'text': '#24292e',
            'comment': '#6a737d',
            'keyword': '#d73a49',
            'string': '#032f62',
            'function': '#6f42c1',
            'number': '#005cc5',
            'builtin': '#005cc5',
            'decorator': '#6f42c1',
            'class': '#6f42c1',
            'line_number': '#6a737d',
            'line_bg': '#f6f8fa'
        },
        'dracula': {
            'background': '#282a36',
            'text': '#f8f8f2',
            'comment': '#6272a4',
            'keyword': '#ff79c6',
            'string': '#f1fa8c',
            'function': '#50fa7b',
            'number': '#bd93f9',
            'builtin': '#8be9fd',
            'decorator': '#ff79c6',
            'class': '#8be9fd',
            'line_number': '#6272a4',
            'line_bg': '#44475a'
        },
        'nord': {
            'background': '#2e3440',
            'text': '#d8dee9',
            'comment': '#616e88',
            'keyword': '#81a1c1',
            'string': '#a3be8c',
            'function': '#88c0d0',
            'number': '#b48ead',
            'builtin': '#8fbcbb',
            'decorator': '#d08770',
            'class': '#8fbcbb',
            'line_number': '#4c566a',
            'line_bg': '#3b4252'
        }
    }
    
    def __init__(self, theme: str = 'monokai', show_line_numbers: bool = True):
        """
        初始化转换器
        
        Args:
            theme: 主题名称 (monokai/github/dracula/nord)
            show_line_numbers: 是否显示行号
        """
        self.theme = self.THEMES.get(theme, self.THEMES['monokai'])
        self.theme_name = theme
        self.show_line_numbers = show_line_numbers
    
    def convert_file(self, file_path: str, title: str = None, 
                     start_line: int = None, end_line: int = None,
                     collapsible: bool = True) -> str:
        """
        转换文件为HTML
        
        Args:
            file_path: 文件路径
            title: 代码块标题
            start_line: 起始行号（可选）
            end_line: 结束行号（可选）
            collapsible: 是否可折叠
        """
        path = Path(file_path)
        if not path.exists():
            return f'<div class="code-error">文件不存在: {file_path}</div>'
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 提取指定行
        if start_line is not None or end_line is not None:
            start = (start_line or 1) - 1
            end = end_line or len(lines)
            lines = lines[start:end]
            line_offset = start
        else:
            line_offset = 0
        
        code = ''.join(lines)
        
        if title is None:
            title = path.name
        
        return self.convert_code(
            code, 
            language=self._detect_language(path.suffix),
            title=title,
            collapsible=collapsible,
            line_offset=line_offset
        )
    
    def convert_code(self, code: str, language: str = 'python', 
                     title: str = None, collapsible: bool = True,
                     line_offset: int = 0) -> str:
        """
        转换代码字符串为HTML
        
        Args:
            code: 代码字符串
            language: 语言类型
            title: 代码块标题
            collapsible: 是否可折叠
            line_offset: 行号偏移
        """
        if PYGMENTS_AVAILABLE:
            return self._convert_with_pygments(code, language, title, collapsible, line_offset)
        else:
            return self._convert_simple(code, language, title, collapsible, line_offset)
    
    def _convert_with_pygments(self, code: str, language: str, 
                                title: str, collapsible: bool, 
                                line_offset: int) -> str:
        """使用Pygments转换"""
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = PythonLexer()
        
        formatter = HtmlFormatter(
            linenos=self.show_line_numbers,
            cssclass='highlight',
            style=self.theme_name if self.theme_name in ['monokai', 'github'] else 'monokai',
            linenostart=line_offset + 1
        )
        
        highlighted = highlight(code, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        
        # 构建HTML
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            {css}
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .highlight {{
                background: {self.theme['background']} !important;
                padding: 15px;
                overflow-x: auto;
                margin: 0;
            }}
            .highlight pre {{
                margin: 0;
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                {highlighted}
            </div>
        </div>
        '''
    
    def _convert_simple(self, code: str, language: str, 
                        title: str, collapsible: bool,
                        line_offset: int) -> str:
        """简单语法高亮（无Pygments）"""
        
        lines = code.split('\n')
        highlighted_lines = []
        
        for i, line in enumerate(lines, start=line_offset + 1):
            highlighted = self._highlight_line(line)
            
            if self.show_line_numbers:
                line_num = f'<span class="line-number">{i:4d}</span>'
                highlighted_lines.append(f'{line_num}{highlighted}')
            else:
                highlighted_lines.append(highlighted)
        
        code_html = '\n'.join(highlighted_lines)
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .code-body {{
                background: {self.theme['background']};
                padding: 15px;
                overflow-x: auto;
            }}
            .code-body pre {{
                margin: 0;
                font-size: 13px;
                line-height: 1.6;
                color: {self.theme['text']};
            }}
            .line-number {{
                color: {self.theme['line_number']};
                padding-right: 15px;
                user-select: none;
                border-right: 1px solid rgba(255,255,255,0.1);
                margin-right: 15px;
            }}
            .keyword {{ color: {self.theme['keyword']}; font-weight: bold; }}
            .builtin {{ color: {self.theme['builtin']}; }}
            .string {{ color: {self.theme['string']}; }}
            .comment {{ color: {self.theme['comment']}; font-style: italic; }}
            .number {{ color: {self.theme['number']}; }}
            .function {{ color: {self.theme['function']}; }}
            .decorator {{ color: {self.theme['decorator']}; }}
            .class-name {{ color: {self.theme['class']}; font-weight: bold; }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                <pre>{code_html}</pre>
            </div>
        </div>
        '''
    
    def _highlight_line(self, line: str) -> str:
        """高亮单行代码"""
        # 转义HTML
        escaped = html_lib.escape(line)
        
        # 注释
        if '#' in escaped:
            idx = escaped.index('#')
            return escaped[:idx] + f'<span class="comment">{escaped[idx:]}</span>'
        
        # 装饰器
        if escaped.strip().startswith('@'):
            return f'<span class="decorator">{escaped}</span>'
        
        # 字符串 (简化处理)
        escaped = re.sub(
            r'([\"\'])(.*?)\1',
            r'<span class="string">\1\2\1</span>',
            escaped
        )
        
        # 数字
        escaped = re.sub(
            r'\b(\d+\.?\d*)\b',
            r'<span class="number">\1</span>',
            escaped
        )
        
        # 关键字
        for kw in self.PYTHON_KEYWORDS:
            escaped = re.sub(
                rf'\b({kw})\b',
                r'<span class="keyword">\1</span>',
                escaped
            )
        
        # 内置函数
        for bf in self.PYTHON_BUILTINS:
            escaped = re.sub(
                rf'\b({bf})\b(?=\s*\()',
                r'<span class="builtin">\1</span>',
                escaped
            )
        
        # 函数定义
        escaped = re.sub(
            r'def\s+(\w+)',
            r'<span class="keyword">def</span> <span class="function">\1</span>',
            escaped
        )
        
        # 类定义
        escaped = re.sub(
            r'class\s+(\w+)',
            r'<span class="keyword">class</span> <span class="class-name">\1</span>',
            escaped
        )
        
        return escaped
    
    def _detect_language(self, suffix: str) -> str:
        """检测文件语言"""
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bash': 'bash',
        }
        return mapping.get(suffix.lower(), 'python')
    
    def get_javascript(self) -> str:
        """获取JavaScript代码（用于复制和折叠功能）"""
        return '''
        <script>
        function copyCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body pre, .highlight pre');
            if (codeBody) {
                const text = codeBody.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    const btn = container.querySelector('.code-btn');
                    if (btn) {
                        const original = btn.innerText;
                        btn.innerText = '✅ 已复制';
                        setTimeout(() => btn.innerText = original, 2000);
                    }
                });
            }
        }
        
        function toggleCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body');
            const btn = container.querySelectorAll('.code-btn')[1];
            
            if (codeBody.style.display === 'none') {
                codeBody.style.display = 'block';
                if (btn) btn.innerText = '▼ 折叠';
            } else {
                codeBody.style.display = 'none';
                if (btn) btn.innerText = '▶ 展开';
            }
        }
        </script>
        '''
    
    @staticmethod
    def extract_function(file_path: str, function_name: str) -> str:
        """从文件中提取指定函数的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取函数
        pattern = rf'(def\s+{function_name}\s*\([^)]*\):.*?)(?=\ndef\s|\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""
    
    @staticmethod
    def extract_class(file_path: str, class_name: str) -> str:
        """从文件中提取指定类的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取类
        pattern = rf'(class\s+{class_name}\s*(?:\([^)]*\))?:.*?)(?=\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""


def convert_code_to_html(code: str, **kwargs) -> str:
    """便捷函数：转换代码为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_code(code, **kwargs)


def convert_file_to_html(file_path: str, **kwargs) -> str:
    """便捷函数：转换文件为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_file(file_path, **kwargs)


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    # 测试代码
    test_code = '''
def calculate_momentum(prices, period=20):
    """
    计算动量因子
    
    Args:
        prices: 价格序列
        period: 周期
    """
    if len(prices) < period:
        return None
    
    momentum = (prices[-1] / prices[-period] - 1) * 100
    return momentum


class TenbaggerStrategy:
    """十倍股策略"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.max_holdings = 2
    
    @property
    def is_ready(self):
        return True
    
    def generate_signals(self, data):
        # 计算动量
        momentum = calculate_momentum(data['close'])
        
        if momentum > 10:
            return "BUY"
        elif momentum < -5:
            return "SELL"
        return "HOLD"
'''
    
    converter = CodeToHtml(theme='monokai')
    html = converter.convert_code(test_code, title='策略示例代码')
    
    # 保存测试输出
    output_path = Path(__file__).parent.parent / "reports" / "code_highlight_test.html"
    output_path.parent.mkdir(exist_ok=True)
    
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>代码高亮测试</title>
</head>
<body style="background: #1a1a2e; padding: 30px;">
    <h1 style="color: white;">代码格式转换工具测试</h1>
    {html}
    {converter.get_javascript()}
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 测试输出: {output_path}")


"""
代码格式转换工具
================

功能：
1. Python代码 → HTML格式化显示
2. 支持语法高亮（使用Pygments）
3. 支持行号显示
4. 支持代码折叠
5. 支持多种主题

代码位置: utils/code_to_html.py

使用方法：
```python
from utils.code_to_html import CodeToHtml

converter = CodeToHtml()
html = converter.convert_file('/path/to/file.py', title='策略代码')
html = converter.convert_code(code_string, language='python', title='核心算法')
```
"""

import re
import html as html_lib
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# 尝试导入Pygments用于高级语法高亮
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    logger.warning("Pygments未安装，使用简单语法高亮")


class CodeToHtml:
    """代码转HTML工具"""
    
    # Python关键字
    PYTHON_KEYWORDS = {
        'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except',
        'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'raise',
        'pass', 'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'lambda',
        'True', 'False', 'None', 'global', 'nonlocal', 'assert', 'del', 'async', 'await'
    }
    
    # 内置函数
    PYTHON_BUILTINS = {
        'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
        'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool', 'type',
        'isinstance', 'hasattr', 'getattr', 'setattr', 'open', 'abs', 'min', 'max',
        'sum', 'any', 'all', 'round', 'input', 'id', 'hex', 'bin', 'oct', 'ord', 'chr'
    }
    
    # 主题配置
    THEMES = {
        'monokai': {
            'background': '#272822',
            'text': '#f8f8f2',
            'comment': '#75715e',
            'keyword': '#f92672',
            'string': '#e6db74',
            'function': '#a6e22e',
            'number': '#ae81ff',
            'builtin': '#66d9ef',
            'decorator': '#66d9ef',
            'class': '#a6e22e',
            'line_number': '#75715e',
            'line_bg': '#3e3d32'
        },
        'github': {
            'background': '#ffffff',
            'text': '#24292e',
            'comment': '#6a737d',
            'keyword': '#d73a49',
            'string': '#032f62',
            'function': '#6f42c1',
            'number': '#005cc5',
            'builtin': '#005cc5',
            'decorator': '#6f42c1',
            'class': '#6f42c1',
            'line_number': '#6a737d',
            'line_bg': '#f6f8fa'
        },
        'dracula': {
            'background': '#282a36',
            'text': '#f8f8f2',
            'comment': '#6272a4',
            'keyword': '#ff79c6',
            'string': '#f1fa8c',
            'function': '#50fa7b',
            'number': '#bd93f9',
            'builtin': '#8be9fd',
            'decorator': '#ff79c6',
            'class': '#8be9fd',
            'line_number': '#6272a4',
            'line_bg': '#44475a'
        },
        'nord': {
            'background': '#2e3440',
            'text': '#d8dee9',
            'comment': '#616e88',
            'keyword': '#81a1c1',
            'string': '#a3be8c',
            'function': '#88c0d0',
            'number': '#b48ead',
            'builtin': '#8fbcbb',
            'decorator': '#d08770',
            'class': '#8fbcbb',
            'line_number': '#4c566a',
            'line_bg': '#3b4252'
        }
    }
    
    def __init__(self, theme: str = 'monokai', show_line_numbers: bool = True):
        """
        初始化转换器
        
        Args:
            theme: 主题名称 (monokai/github/dracula/nord)
            show_line_numbers: 是否显示行号
        """
        self.theme = self.THEMES.get(theme, self.THEMES['monokai'])
        self.theme_name = theme
        self.show_line_numbers = show_line_numbers
    
    def convert_file(self, file_path: str, title: str = None, 
                     start_line: int = None, end_line: int = None,
                     collapsible: bool = True) -> str:
        """
        转换文件为HTML
        
        Args:
            file_path: 文件路径
            title: 代码块标题
            start_line: 起始行号（可选）
            end_line: 结束行号（可选）
            collapsible: 是否可折叠
        """
        path = Path(file_path)
        if not path.exists():
            return f'<div class="code-error">文件不存在: {file_path}</div>'
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 提取指定行
        if start_line is not None or end_line is not None:
            start = (start_line or 1) - 1
            end = end_line or len(lines)
            lines = lines[start:end]
            line_offset = start
        else:
            line_offset = 0
        
        code = ''.join(lines)
        
        if title is None:
            title = path.name
        
        return self.convert_code(
            code, 
            language=self._detect_language(path.suffix),
            title=title,
            collapsible=collapsible,
            line_offset=line_offset
        )
    
    def convert_code(self, code: str, language: str = 'python', 
                     title: str = None, collapsible: bool = True,
                     line_offset: int = 0) -> str:
        """
        转换代码字符串为HTML
        
        Args:
            code: 代码字符串
            language: 语言类型
            title: 代码块标题
            collapsible: 是否可折叠
            line_offset: 行号偏移
        """
        if PYGMENTS_AVAILABLE:
            return self._convert_with_pygments(code, language, title, collapsible, line_offset)
        else:
            return self._convert_simple(code, language, title, collapsible, line_offset)
    
    def _convert_with_pygments(self, code: str, language: str, 
                                title: str, collapsible: bool, 
                                line_offset: int) -> str:
        """使用Pygments转换"""
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = PythonLexer()
        
        formatter = HtmlFormatter(
            linenos=self.show_line_numbers,
            cssclass='highlight',
            style=self.theme_name if self.theme_name in ['monokai', 'github'] else 'monokai',
            linenostart=line_offset + 1
        )
        
        highlighted = highlight(code, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        
        # 构建HTML
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            {css}
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .highlight {{
                background: {self.theme['background']} !important;
                padding: 15px;
                overflow-x: auto;
                margin: 0;
            }}
            .highlight pre {{
                margin: 0;
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                {highlighted}
            </div>
        </div>
        '''
    
    def _convert_simple(self, code: str, language: str, 
                        title: str, collapsible: bool,
                        line_offset: int) -> str:
        """简单语法高亮（无Pygments）"""
        
        lines = code.split('\n')
        highlighted_lines = []
        
        for i, line in enumerate(lines, start=line_offset + 1):
            highlighted = self._highlight_line(line)
            
            if self.show_line_numbers:
                line_num = f'<span class="line-number">{i:4d}</span>'
                highlighted_lines.append(f'{line_num}{highlighted}')
            else:
                highlighted_lines.append(highlighted)
        
        code_html = '\n'.join(highlighted_lines)
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .code-body {{
                background: {self.theme['background']};
                padding: 15px;
                overflow-x: auto;
            }}
            .code-body pre {{
                margin: 0;
                font-size: 13px;
                line-height: 1.6;
                color: {self.theme['text']};
            }}
            .line-number {{
                color: {self.theme['line_number']};
                padding-right: 15px;
                user-select: none;
                border-right: 1px solid rgba(255,255,255,0.1);
                margin-right: 15px;
            }}
            .keyword {{ color: {self.theme['keyword']}; font-weight: bold; }}
            .builtin {{ color: {self.theme['builtin']}; }}
            .string {{ color: {self.theme['string']}; }}
            .comment {{ color: {self.theme['comment']}; font-style: italic; }}
            .number {{ color: {self.theme['number']}; }}
            .function {{ color: {self.theme['function']}; }}
            .decorator {{ color: {self.theme['decorator']}; }}
            .class-name {{ color: {self.theme['class']}; font-weight: bold; }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                <pre>{code_html}</pre>
            </div>
        </div>
        '''
    
    def _highlight_line(self, line: str) -> str:
        """高亮单行代码"""
        # 转义HTML
        escaped = html_lib.escape(line)
        
        # 注释
        if '#' in escaped:
            idx = escaped.index('#')
            return escaped[:idx] + f'<span class="comment">{escaped[idx:]}</span>'
        
        # 装饰器
        if escaped.strip().startswith('@'):
            return f'<span class="decorator">{escaped}</span>'
        
        # 字符串 (简化处理)
        escaped = re.sub(
            r'([\"\'])(.*?)\1',
            r'<span class="string">\1\2\1</span>',
            escaped
        )
        
        # 数字
        escaped = re.sub(
            r'\b(\d+\.?\d*)\b',
            r'<span class="number">\1</span>',
            escaped
        )
        
        # 关键字
        for kw in self.PYTHON_KEYWORDS:
            escaped = re.sub(
                rf'\b({kw})\b',
                r'<span class="keyword">\1</span>',
                escaped
            )
        
        # 内置函数
        for bf in self.PYTHON_BUILTINS:
            escaped = re.sub(
                rf'\b({bf})\b(?=\s*\()',
                r'<span class="builtin">\1</span>',
                escaped
            )
        
        # 函数定义
        escaped = re.sub(
            r'def\s+(\w+)',
            r'<span class="keyword">def</span> <span class="function">\1</span>',
            escaped
        )
        
        # 类定义
        escaped = re.sub(
            r'class\s+(\w+)',
            r'<span class="keyword">class</span> <span class="class-name">\1</span>',
            escaped
        )
        
        return escaped
    
    def _detect_language(self, suffix: str) -> str:
        """检测文件语言"""
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bash': 'bash',
        }
        return mapping.get(suffix.lower(), 'python')
    
    def get_javascript(self) -> str:
        """获取JavaScript代码（用于复制和折叠功能）"""
        return '''
        <script>
        function copyCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body pre, .highlight pre');
            if (codeBody) {
                const text = codeBody.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    const btn = container.querySelector('.code-btn');
                    if (btn) {
                        const original = btn.innerText;
                        btn.innerText = '✅ 已复制';
                        setTimeout(() => btn.innerText = original, 2000);
                    }
                });
            }
        }
        
        function toggleCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body');
            const btn = container.querySelectorAll('.code-btn')[1];
            
            if (codeBody.style.display === 'none') {
                codeBody.style.display = 'block';
                if (btn) btn.innerText = '▼ 折叠';
            } else {
                codeBody.style.display = 'none';
                if (btn) btn.innerText = '▶ 展开';
            }
        }
        </script>
        '''
    
    @staticmethod
    def extract_function(file_path: str, function_name: str) -> str:
        """从文件中提取指定函数的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取函数
        pattern = rf'(def\s+{function_name}\s*\([^)]*\):.*?)(?=\ndef\s|\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""
    
    @staticmethod
    def extract_class(file_path: str, class_name: str) -> str:
        """从文件中提取指定类的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取类
        pattern = rf'(class\s+{class_name}\s*(?:\([^)]*\))?:.*?)(?=\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""


def convert_code_to_html(code: str, **kwargs) -> str:
    """便捷函数：转换代码为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_code(code, **kwargs)


def convert_file_to_html(file_path: str, **kwargs) -> str:
    """便捷函数：转换文件为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_file(file_path, **kwargs)


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    # 测试代码
    test_code = '''
def calculate_momentum(prices, period=20):
    """
    计算动量因子
    
    Args:
        prices: 价格序列
        period: 周期
    """
    if len(prices) < period:
        return None
    
    momentum = (prices[-1] / prices[-period] - 1) * 100
    return momentum


class TenbaggerStrategy:
    """十倍股策略"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.max_holdings = 2
    
    @property
    def is_ready(self):
        return True
    
    def generate_signals(self, data):
        # 计算动量
        momentum = calculate_momentum(data['close'])
        
        if momentum > 10:
            return "BUY"
        elif momentum < -5:
            return "SELL"
        return "HOLD"
'''
    
    converter = CodeToHtml(theme='monokai')
    html = converter.convert_code(test_code, title='策略示例代码')
    
    # 保存测试输出
    output_path = Path(__file__).parent.parent / "reports" / "code_highlight_test.html"
    output_path.parent.mkdir(exist_ok=True)
    
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>代码高亮测试</title>
</head>
<body style="background: #1a1a2e; padding: 30px;">
    <h1 style="color: white;">代码格式转换工具测试</h1>
    {html}
    {converter.get_javascript()}
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 测试输出: {output_path}")


"""
代码格式转换工具
================

功能：
1. Python代码 → HTML格式化显示
2. 支持语法高亮（使用Pygments）
3. 支持行号显示
4. 支持代码折叠
5. 支持多种主题

代码位置: utils/code_to_html.py

使用方法：
```python
from utils.code_to_html import CodeToHtml

converter = CodeToHtml()
html = converter.convert_file('/path/to/file.py', title='策略代码')
html = converter.convert_code(code_string, language='python', title='核心算法')
```
"""

import re
import html as html_lib
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

# 尝试导入Pygments用于高级语法高亮
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer, get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_style_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    logger.warning("Pygments未安装，使用简单语法高亮")


class CodeToHtml:
    """代码转HTML工具"""
    
    # Python关键字
    PYTHON_KEYWORDS = {
        'def', 'class', 'if', 'elif', 'else', 'for', 'while', 'try', 'except',
        'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'raise',
        'pass', 'break', 'continue', 'and', 'or', 'not', 'in', 'is', 'lambda',
        'True', 'False', 'None', 'global', 'nonlocal', 'assert', 'del', 'async', 'await'
    }
    
    # 内置函数
    PYTHON_BUILTINS = {
        'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
        'list', 'dict', 'set', 'tuple', 'str', 'int', 'float', 'bool', 'type',
        'isinstance', 'hasattr', 'getattr', 'setattr', 'open', 'abs', 'min', 'max',
        'sum', 'any', 'all', 'round', 'input', 'id', 'hex', 'bin', 'oct', 'ord', 'chr'
    }
    
    # 主题配置
    THEMES = {
        'monokai': {
            'background': '#272822',
            'text': '#f8f8f2',
            'comment': '#75715e',
            'keyword': '#f92672',
            'string': '#e6db74',
            'function': '#a6e22e',
            'number': '#ae81ff',
            'builtin': '#66d9ef',
            'decorator': '#66d9ef',
            'class': '#a6e22e',
            'line_number': '#75715e',
            'line_bg': '#3e3d32'
        },
        'github': {
            'background': '#ffffff',
            'text': '#24292e',
            'comment': '#6a737d',
            'keyword': '#d73a49',
            'string': '#032f62',
            'function': '#6f42c1',
            'number': '#005cc5',
            'builtin': '#005cc5',
            'decorator': '#6f42c1',
            'class': '#6f42c1',
            'line_number': '#6a737d',
            'line_bg': '#f6f8fa'
        },
        'dracula': {
            'background': '#282a36',
            'text': '#f8f8f2',
            'comment': '#6272a4',
            'keyword': '#ff79c6',
            'string': '#f1fa8c',
            'function': '#50fa7b',
            'number': '#bd93f9',
            'builtin': '#8be9fd',
            'decorator': '#ff79c6',
            'class': '#8be9fd',
            'line_number': '#6272a4',
            'line_bg': '#44475a'
        },
        'nord': {
            'background': '#2e3440',
            'text': '#d8dee9',
            'comment': '#616e88',
            'keyword': '#81a1c1',
            'string': '#a3be8c',
            'function': '#88c0d0',
            'number': '#b48ead',
            'builtin': '#8fbcbb',
            'decorator': '#d08770',
            'class': '#8fbcbb',
            'line_number': '#4c566a',
            'line_bg': '#3b4252'
        }
    }
    
    def __init__(self, theme: str = 'monokai', show_line_numbers: bool = True):
        """
        初始化转换器
        
        Args:
            theme: 主题名称 (monokai/github/dracula/nord)
            show_line_numbers: 是否显示行号
        """
        self.theme = self.THEMES.get(theme, self.THEMES['monokai'])
        self.theme_name = theme
        self.show_line_numbers = show_line_numbers
    
    def convert_file(self, file_path: str, title: str = None, 
                     start_line: int = None, end_line: int = None,
                     collapsible: bool = True) -> str:
        """
        转换文件为HTML
        
        Args:
            file_path: 文件路径
            title: 代码块标题
            start_line: 起始行号（可选）
            end_line: 结束行号（可选）
            collapsible: 是否可折叠
        """
        path = Path(file_path)
        if not path.exists():
            return f'<div class="code-error">文件不存在: {file_path}</div>'
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 提取指定行
        if start_line is not None or end_line is not None:
            start = (start_line or 1) - 1
            end = end_line or len(lines)
            lines = lines[start:end]
            line_offset = start
        else:
            line_offset = 0
        
        code = ''.join(lines)
        
        if title is None:
            title = path.name
        
        return self.convert_code(
            code, 
            language=self._detect_language(path.suffix),
            title=title,
            collapsible=collapsible,
            line_offset=line_offset
        )
    
    def convert_code(self, code: str, language: str = 'python', 
                     title: str = None, collapsible: bool = True,
                     line_offset: int = 0) -> str:
        """
        转换代码字符串为HTML
        
        Args:
            code: 代码字符串
            language: 语言类型
            title: 代码块标题
            collapsible: 是否可折叠
            line_offset: 行号偏移
        """
        if PYGMENTS_AVAILABLE:
            return self._convert_with_pygments(code, language, title, collapsible, line_offset)
        else:
            return self._convert_simple(code, language, title, collapsible, line_offset)
    
    def _convert_with_pygments(self, code: str, language: str, 
                                title: str, collapsible: bool, 
                                line_offset: int) -> str:
        """使用Pygments转换"""
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except:
            lexer = PythonLexer()
        
        formatter = HtmlFormatter(
            linenos=self.show_line_numbers,
            cssclass='highlight',
            style=self.theme_name if self.theme_name in ['monokai', 'github'] else 'monokai',
            linenostart=line_offset + 1
        )
        
        highlighted = highlight(code, lexer, formatter)
        css = formatter.get_style_defs('.highlight')
        
        # 构建HTML
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            {css}
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .highlight {{
                background: {self.theme['background']} !important;
                padding: 15px;
                overflow-x: auto;
                margin: 0;
            }}
            .highlight pre {{
                margin: 0;
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                {highlighted}
            </div>
        </div>
        '''
    
    def _convert_simple(self, code: str, language: str, 
                        title: str, collapsible: bool,
                        line_offset: int) -> str:
        """简单语法高亮（无Pygments）"""
        
        lines = code.split('\n')
        highlighted_lines = []
        
        for i, line in enumerate(lines, start=line_offset + 1):
            highlighted = self._highlight_line(line)
            
            if self.show_line_numbers:
                line_num = f'<span class="line-number">{i:4d}</span>'
                highlighted_lines.append(f'{line_num}{highlighted}')
            else:
                highlighted_lines.append(highlighted)
        
        code_html = '\n'.join(highlighted_lines)
        container_id = f"code_{hash(code) % 10000}"
        
        header_html = ""
        if title:
            header_html = f'''
            <div class="code-header">
                <span class="code-title">{html_lib.escape(title)}</span>
                <div class="code-actions">
                    <button onclick="copyCode('{container_id}')" class="code-btn">📋 复制</button>
                    {('<button onclick="toggleCode(' + "'" + container_id + "'" + ')" class="code-btn">▼ 折叠</button>') if collapsible else ''}
                </div>
            </div>
            '''
        
        return f'''
        <style>
            .code-container {{
                margin: 15px 0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
            }}
            .code-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: {self.theme['line_bg']};
                padding: 8px 15px;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .code-title {{
                color: {self.theme['text']};
                font-weight: 600;
                font-size: 0.9em;
            }}
            .code-actions {{
                display: flex;
                gap: 10px;
            }}
            .code-btn {{
                background: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: {self.theme['text']};
                padding: 4px 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
            }}
            .code-btn:hover {{
                background: rgba(255,255,255,0.1);
            }}
            .code-body {{
                background: {self.theme['background']};
                padding: 15px;
                overflow-x: auto;
            }}
            .code-body pre {{
                margin: 0;
                font-size: 13px;
                line-height: 1.6;
                color: {self.theme['text']};
            }}
            .line-number {{
                color: {self.theme['line_number']};
                padding-right: 15px;
                user-select: none;
                border-right: 1px solid rgba(255,255,255,0.1);
                margin-right: 15px;
            }}
            .keyword {{ color: {self.theme['keyword']}; font-weight: bold; }}
            .builtin {{ color: {self.theme['builtin']}; }}
            .string {{ color: {self.theme['string']}; }}
            .comment {{ color: {self.theme['comment']}; font-style: italic; }}
            .number {{ color: {self.theme['number']}; }}
            .function {{ color: {self.theme['function']}; }}
            .decorator {{ color: {self.theme['decorator']}; }}
            .class-name {{ color: {self.theme['class']}; font-weight: bold; }}
        </style>
        <div class="code-container" id="{container_id}">
            {header_html}
            <div class="code-body">
                <pre>{code_html}</pre>
            </div>
        </div>
        '''
    
    def _highlight_line(self, line: str) -> str:
        """高亮单行代码"""
        # 转义HTML
        escaped = html_lib.escape(line)
        
        # 注释
        if '#' in escaped:
            idx = escaped.index('#')
            return escaped[:idx] + f'<span class="comment">{escaped[idx:]}</span>'
        
        # 装饰器
        if escaped.strip().startswith('@'):
            return f'<span class="decorator">{escaped}</span>'
        
        # 字符串 (简化处理)
        escaped = re.sub(
            r'([\"\'])(.*?)\1',
            r'<span class="string">\1\2\1</span>',
            escaped
        )
        
        # 数字
        escaped = re.sub(
            r'\b(\d+\.?\d*)\b',
            r'<span class="number">\1</span>',
            escaped
        )
        
        # 关键字
        for kw in self.PYTHON_KEYWORDS:
            escaped = re.sub(
                rf'\b({kw})\b',
                r'<span class="keyword">\1</span>',
                escaped
            )
        
        # 内置函数
        for bf in self.PYTHON_BUILTINS:
            escaped = re.sub(
                rf'\b({bf})\b(?=\s*\()',
                r'<span class="builtin">\1</span>',
                escaped
            )
        
        # 函数定义
        escaped = re.sub(
            r'def\s+(\w+)',
            r'<span class="keyword">def</span> <span class="function">\1</span>',
            escaped
        )
        
        # 类定义
        escaped = re.sub(
            r'class\s+(\w+)',
            r'<span class="keyword">class</span> <span class="class-name">\1</span>',
            escaped
        )
        
        return escaped
    
    def _detect_language(self, suffix: str) -> str:
        """检测文件语言"""
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bash': 'bash',
        }
        return mapping.get(suffix.lower(), 'python')
    
    def get_javascript(self) -> str:
        """获取JavaScript代码（用于复制和折叠功能）"""
        return '''
        <script>
        function copyCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body pre, .highlight pre');
            if (codeBody) {
                const text = codeBody.innerText;
                navigator.clipboard.writeText(text).then(() => {
                    const btn = container.querySelector('.code-btn');
                    if (btn) {
                        const original = btn.innerText;
                        btn.innerText = '✅ 已复制';
                        setTimeout(() => btn.innerText = original, 2000);
                    }
                });
            }
        }
        
        function toggleCode(containerId) {
            const container = document.getElementById(containerId);
            const codeBody = container.querySelector('.code-body');
            const btn = container.querySelectorAll('.code-btn')[1];
            
            if (codeBody.style.display === 'none') {
                codeBody.style.display = 'block';
                if (btn) btn.innerText = '▼ 折叠';
            } else {
                codeBody.style.display = 'none';
                if (btn) btn.innerText = '▶ 展开';
            }
        }
        </script>
        '''
    
    @staticmethod
    def extract_function(file_path: str, function_name: str) -> str:
        """从文件中提取指定函数的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取函数
        pattern = rf'(def\s+{function_name}\s*\([^)]*\):.*?)(?=\ndef\s|\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""
    
    @staticmethod
    def extract_class(file_path: str, class_name: str) -> str:
        """从文件中提取指定类的代码"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则提取类
        pattern = rf'(class\s+{class_name}\s*(?:\([^)]*\))?:.*?)(?=\nclass\s|\Z)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            return match.group(1).strip()
        return ""


def convert_code_to_html(code: str, **kwargs) -> str:
    """便捷函数：转换代码为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_code(code, **kwargs)


def convert_file_to_html(file_path: str, **kwargs) -> str:
    """便捷函数：转换文件为HTML"""
    converter = CodeToHtml(**kwargs)
    return converter.convert_file(file_path, **kwargs)


# ============================================================
# 测试
# ============================================================

if __name__ == "__main__":
    # 测试代码
    test_code = '''
def calculate_momentum(prices, period=20):
    """
    计算动量因子
    
    Args:
        prices: 价格序列
        period: 周期
    """
    if len(prices) < period:
        return None
    
    momentum = (prices[-1] / prices[-period] - 1) * 100
    return momentum


class TenbaggerStrategy:
    """十倍股策略"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.max_holdings = 2
    
    @property
    def is_ready(self):
        return True
    
    def generate_signals(self, data):
        # 计算动量
        momentum = calculate_momentum(data['close'])
        
        if momentum > 10:
            return "BUY"
        elif momentum < -5:
            return "SELL"
        return "HOLD"
'''
    
    converter = CodeToHtml(theme='monokai')
    html = converter.convert_code(test_code, title='策略示例代码')
    
    # 保存测试输出
    output_path = Path(__file__).parent.parent / "reports" / "code_highlight_test.html"
    output_path.parent.mkdir(exist_ok=True)
    
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>代码高亮测试</title>
</head>
<body style="background: #1a1a2e; padding: 30px;">
    <h1 style="color: white;">代码格式转换工具测试</h1>
    {html}
    {converter.get_javascript()}
</body>
</html>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 测试输出: {output_path}")

