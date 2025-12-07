"""PDF读取和解构工具

提供统一的PDF处理接口，支持多种提取方式，便于大模型使用。
"""
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    logger.warning("pdfplumber未安装，部分功能不可用")

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    logger.warning("PyPDF2未安装，元数据提取功能不可用")

try:
    from pdfminer.high_level import extract_text as pdfminer_extract
    from pdfminer.layout import LAParams
    PDFMINER_AVAILABLE = True
except ImportError:
    PDFMINER_AVAILABLE = False
    logger.warning("pdfminer未安装，详细文本提取功能不可用")


class PDFReader:
    """PDF读取器，支持多种提取方式
    
    特性：
    - 文本提取（pdfplumber + pdfminer）
    - 表格提取（pdfplumber）
    - 元数据提取（PyPDF2）
    - 结构化输出，便于大模型使用
    """
    
    def __init__(self, pdf_path: str):
        """初始化PDF读取器
        
        Args:
            pdf_path: PDF文件路径
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        self.metadata: Dict = {}
        self._extracted_text: Optional[str] = None
        self._extracted_tables: List[Dict] = []
    
    def extract_metadata(self) -> Dict:
        """提取PDF元数据
        
        Returns:
            包含标题、作者、页数等信息的字典
        """
        if not PYPDF2_AVAILABLE:
            logger.warning("PyPDF2未安装，无法提取元数据")
            return {}
        
        try:
            with open(self.pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                self.metadata = {
                    'total_pages': len(reader.pages),
                    'title': '',
                    'author': '',
                    'subject': '',
                    'creator': '',
                    'producer': '',
                    'creation_date': '',
                    'modification_date': ''
                }
                
                if reader.metadata:
                    info = reader.metadata
                    self.metadata.update({
                        'title': info.get('/Title', ''),
                        'author': info.get('/Author', ''),
                        'subject': info.get('/Subject', ''),
                        'creator': info.get('/Creator', ''),
                        'producer': info.get('/Producer', ''),
                        'creation_date': str(info.get('/CreationDate', '')),
                        'modification_date': str(info.get('/ModDate', ''))
                    })
                
                logger.info(f"提取元数据成功，共 {self.metadata['total_pages']} 页")
                return self.metadata
                
        except Exception as e:
            logger.error(f"提取元数据失败: {e}")
            return {}
    
    def extract_text(
        self, 
        method: str = 'pdfplumber',
        page_range: Optional[Tuple[int, int]] = None
    ) -> str:
        """提取PDF文本内容
        
        Args:
            method: 提取方法，'pdfplumber' 或 'pdfminer'
            page_range: 页码范围，如 (1, 10) 表示提取1-10页
            
        Returns:
            提取的文本内容
        """
        if method == 'pdfplumber':
            return self._extract_with_pdfplumber(page_range)
        elif method == 'pdfminer':
            return self._extract_with_pdfminer()
        else:
            raise ValueError(f"不支持的提取方法: {method}")
    
    def _extract_with_pdfplumber(
        self, 
        page_range: Optional[Tuple[int, int]] = None
    ) -> str:
        """使用pdfplumber提取文本（推荐）"""
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber未安装，请运行: pip install pdfplumber")
        
        text_parts = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                start_page = page_range[0] if page_range else 1
                end_page = page_range[1] if page_range else len(pdf.pages)
                
                for i in range(start_page - 1, min(end_page, len(pdf.pages))):
                    page = pdf.pages[i]
                    page_text = page.extract_text()
                    
                    if page_text:
                        text_parts.append(f"=== 第 {i + 1} 页 ===\n{page_text}")
                
                self._extracted_text = "\n\n".join(text_parts)
                logger.info(f"使用pdfplumber提取文本成功，共 {len(text_parts)} 页")
                return self._extracted_text
                
        except Exception as e:
            logger.error(f"pdfplumber提取失败: {e}")
            raise
    
    def _extract_with_pdfminer(self) -> str:
        """使用pdfminer提取详细文本"""
        if not PDFMINER_AVAILABLE:
            raise ImportError("pdfminer未安装，请运行: pip install pdfminer.six")
        
        try:
            text = pdfminer_extract(
                str(self.pdf_path),
                laparams=LAParams()
            )
            self._extracted_text = text
            logger.info("使用pdfminer提取文本成功")
            return text
        except Exception as e:
            logger.error(f"pdfminer提取失败: {e}")
            raise
    
    def extract_tables(self, page_num: Optional[int] = None) -> List[Dict]:
        """提取PDF中的表格
        
        Args:
            page_num: 指定页码，None表示提取所有页
            
        Returns:
            表格列表，每个表格包含数据和位置信息
        """
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber未安装，请运行: pip install pdfplumber")
        
        tables = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                pages = [pdf.pages[page_num - 1]] if page_num else pdf.pages
                
                for page_idx, page in enumerate(pages, 1):
                    page_tables = page.extract_tables()
                    
                    for table_idx, table in enumerate(page_tables, 1):
                        if table:
                            tables.append({
                                'page': page_idx if not page_num else page_num,
                                'table_index': table_idx,
                                'data': table,
                                'rows': len(table),
                                'cols': len(table[0]) if table else 0
                            })
                
                self._extracted_tables = tables
                logger.info(f"提取表格成功，共 {len(tables)} 个")
                return tables
                
        except Exception as e:
            logger.error(f"提取表格失败: {e}")
            return []
    
    def extract_code_blocks(
        self,
        page_num: Optional[int] = None,
        preserve_formatting: bool = True,
        detect_language: bool = True
    ) -> List[Dict]:
        """提取PDF中的代码块（专门用于代码提取）
        
        特点：
        - 保持代码格式（缩进、换行）
        - 识别等宽字体区域（通常是代码）
        - 检测代码语言（Python、JavaScript等）
        - 提取代码块位置信息
        
        Args:
            page_num: 指定页码，None表示提取所有页
            preserve_formatting: 是否保持格式（使用layout模式）
            detect_language: 是否尝试检测代码语言
            
        Returns:
            代码块列表，每个代码块包含：
            - code: 代码内容
            - page: 页码
            - language: 检测到的语言（如果启用）
            - position: 位置信息
        """
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber未安装，请运行: pip install pdfplumber")
        
        code_blocks = []
        
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                pages = [pdf.pages[page_num - 1]] if page_num else pdf.pages
                
                for page_idx, page in enumerate(pages, 1):
                    if preserve_formatting:
                        # 使用layout模式保持格式
                        chars = page.chars
                        words = page.extract_words()
                        
                        # 识别等宽字体区域（代码通常使用等宽字体）
                        monospace_regions = self._find_monospace_regions(chars)
                        
                        # 提取代码块
                        for region in monospace_regions:
                            code_text = self._extract_text_from_region(chars, region)
                            if self._is_likely_code(code_text):
                                language = self._detect_language(code_text) if detect_language else None
                                code_blocks.append({
                                    'code': code_text,
                                    'page': page_idx if not page_num else page_num,
                                    'language': language,
                                    'position': region,
                                    'lines': len(code_text.split('\n'))
                                })
                    else:
                        # 简单模式：从文本中提取代码块
                        text = page.extract_text()
                        if text:
                            # 查找代码块标记（```、```python等）
                            blocks = self._extract_code_from_text(text)
                            for block in blocks:
                                language = self._detect_language(block['code']) if detect_language else None
                                code_blocks.append({
                                    'code': block['code'],
                                    'page': page_idx if not page_num else page_num,
                                    'language': language,
                                    'marker': block.get('marker'),
                                    'lines': len(block['code'].split('\n'))
                                })
                
                logger.info(f"提取代码块成功，共 {len(code_blocks)} 个")
                return code_blocks
                
        except Exception as e:
            logger.error(f"提取代码块失败: {e}")
            return []
    
    def _find_monospace_regions(self, chars: List) -> List[Dict]:
        """查找等宽字体区域（通常是代码）"""
        if not chars:
            return []
        
        # 按字体分组
        font_groups = {}
        for char in chars:
            font_name = char.get('fontname', '')
            if 'mono' in font_name.lower() or 'courier' in font_name.lower():
                if font_name not in font_groups:
                    font_groups[font_name] = []
                font_groups[font_name].append(char)
        
        regions = []
        for font_name, font_chars in font_groups.items():
            if len(font_chars) > 10:  # 至少10个字符才认为是代码块
                # 计算区域边界
                x0 = min(c['x0'] for c in font_chars)
                y0 = min(c['top'] for c in font_chars)
                x1 = max(c['x1'] for c in font_chars)
                y1 = max(c['bottom'] for c in font_chars)
                
                regions.append({
                    'x0': x0,
                    'y0': y0,
                    'x1': x1,
                    'y1': y1,
                    'font': font_name
                })
        
        return regions
    
    def _extract_text_from_region(self, chars: List, region: Dict) -> str:
        """从指定区域提取文本，保持格式"""
        region_chars = [
            c for c in chars
            if (region['x0'] <= c['x0'] <= region['x1'] and
                region['y0'] <= c['top'] <= region['y1'])
        ]
        
        if not region_chars:
            return ""
        
        # 按行排序
        region_chars.sort(key=lambda c: (-c['top'], c['x0']))
        
        # 构建文本，保持换行和缩进
        lines = []
        current_line = []
        current_y = None
        
        for char in region_chars:
            char_y = round(char['top'], 1)
            
            if current_y is None:
                current_y = char_y
            elif abs(char_y - current_y) > 2:  # 新行
                if current_line:
                    lines.append(''.join(current_line))
                current_line = []
                current_y = char_y
            
            current_line.append(char['text'])
        
        if current_line:
            lines.append(''.join(current_line))
        
        return '\n'.join(lines)
    
    def _is_likely_code(self, text: str) -> bool:
        """判断文本是否可能是代码"""
        if not text or len(text.strip()) < 10:
            return False
        
        # 代码特征：
        # 1. 包含常见关键字
        code_keywords = [
            'def ', 'class ', 'import ', 'from ', 'return ',
            'function ', 'const ', 'let ', 'var ',
            'if ', 'for ', 'while ', 'try ', 'except ',
            'print(', 'console.log', 'public ', 'private '
        ]
        
        text_lower = text.lower()
        keyword_count = sum(1 for kw in code_keywords if kw in text_lower)
        
        # 2. 包含常见符号
        code_symbols = ['()', '[]', '{}', '=>', '->', '::', '==', '!=', '&&', '||']
        symbol_count = sum(1 for sym in code_symbols if sym in text)
        
        # 3. 行数较多且每行较短（代码特征）
        lines = text.split('\n')
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        
        # 判断标准
        is_code = (
            keyword_count >= 2 or  # 至少2个关键字
            (symbol_count >= 3 and len(lines) > 3) or  # 多个符号且多行
            (len(lines) > 5 and avg_line_length < 80)  # 多行且平均行长短
        )
        
        return is_code
    
    def _detect_language(self, code: str) -> Optional[str]:
        """检测代码语言"""
        code_lower = code.lower()
        
        # Python特征
        if any(kw in code for kw in ['def ', 'import ', 'from ', 'print(', '__init__']):
            return 'python'
        
        # JavaScript/TypeScript特征
        if any(kw in code for kw in ['function ', 'const ', 'let ', 'var ', 'console.log', '=>']):
            return 'javascript'
        
        # Java特征
        if any(kw in code for kw in ['public class', 'private ', 'public ', 'System.out']):
            return 'java'
        
        # C/C++特征
        if any(kw in code for kw in ['#include', 'int main', 'printf', 'cout']):
            return 'cpp'
        
        # SQL特征
        if any(kw in code_lower for kw in ['select ', 'from ', 'where ', 'insert ', 'update ']):
            return 'sql'
        
        # Shell/Bash特征
        if code.startswith('#!') or any(kw in code for kw in ['#!/bin/', 'echo ', 'grep ', 'awk ']):
            return 'shell'
        
        return None
    
    def _extract_code_from_text(self, text: str) -> List[Dict]:
        """从文本中提取代码块（查找```标记）"""
        import re
        
        code_blocks = []
        
        # 查找 ```language 或 ``` 标记的代码块
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            language = match.group(1) or None
            code = match.group(2).strip()
            if code:
                code_blocks.append({
                    'code': code,
                    'marker': f'```{language or ""}'
                })
        
        return code_blocks
    
    def to_llm_format(
        self, 
        include_metadata: bool = True,
        include_tables: bool = False,
        max_length: Optional[int] = None
    ) -> str:
        """转换为大模型友好的格式
        
        Args:
            include_metadata: 是否包含元数据
            include_tables: 是否包含表格
            max_length: 最大长度限制（字符数）
            
        Returns:
            格式化后的文本，可直接传给大模型
        """
        parts = []
        
        # 元数据
        if include_metadata:
            if not self.metadata:
                self.extract_metadata()
            
            if self.metadata:
                parts.append("=== PDF元数据 ===")
                parts.append(f"标题: {self.metadata.get('title', '未知')}")
                parts.append(f"作者: {self.metadata.get('author', '未知')}")
                parts.append(f"总页数: {self.metadata.get('total_pages', 0)}")
                parts.append("")
        
        # 文本内容
        if not self._extracted_text:
            self.extract_text()
        
        parts.append("=== PDF文本内容 ===")
        text = self._extracted_text or ""
        
        # 长度限制
        if max_length and len(text) > max_length:
            text = text[:max_length] + "\n\n[内容已截断...]"
        
        parts.append(text)
        
        # 表格内容
        if include_tables:
            if not self._extracted_tables:
                self.extract_tables()
            
            if self._extracted_tables:
                parts.append("\n=== PDF表格内容 ===")
                for table in self._extracted_tables:
                    parts.append(f"\n表格 {table['table_index']} (第 {table['page']} 页):")
                    parts.append(f"行数: {table['rows']}, 列数: {table['cols']}")
                    # 表格数据可以转换为Markdown格式
                    parts.append(self._table_to_markdown(table['data']))
        
        result = "\n".join(parts)
        
        # 最终长度检查
        if max_length and len(result) > max_length:
            result = result[:max_length] + "\n\n[内容已截断...]"
        
        return result
    
    def _table_to_markdown(self, table_data: List[List]) -> str:
        """将表格数据转换为Markdown格式"""
        if not table_data:
            return ""
        
        lines = []
        for i, row in enumerate(table_data):
            # 转义管道符
            row_str = " | ".join(str(cell or "").replace("|", "\\|") for cell in row)
            lines.append(f"| {row_str} |")
            
            # 添加表头分隔符
            if i == 0:
                separator = "| " + " | ".join(["---"] * len(row)) + " |"
                lines.append(separator)
        
        return "\n".join(lines)
    
    def save_extracted_content(
        self, 
        output_dir: str,
        include_tables: bool = True
    ) -> Dict[str, str]:
        """保存提取的内容到文件
        
        Args:
            output_dir: 输出目录
            include_tables: 是否保存表格
            
        Returns:
            保存的文件路径字典
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = {}
        
        # 保存文本
        if not self._extracted_text:
            self.extract_text()
        
        text_file = output_path / "extracted_text.txt"
        text_file.write_text(self._extracted_text or "", encoding='utf-8')
        saved_files['text'] = str(text_file)
        
        # 保存元数据
        if not self.metadata:
            self.extract_metadata()
        
        metadata_file = output_path / "metadata.json"
        metadata_file.write_text(
            json.dumps(self.metadata, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        saved_files['metadata'] = str(metadata_file)
        
        # 保存表格
        if include_tables:
            if not self._extracted_tables:
                self.extract_tables()
            
            tables_file = output_path / "tables.json"
            tables_file.write_text(
                json.dumps(self._extracted_tables, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            saved_files['tables'] = str(tables_file)
        
        # 保存LLM格式
        llm_file = output_path / "llm_format.txt"
        llm_file.write_text(
            self.to_llm_format(include_tables=include_tables),
            encoding='utf-8'
        )
        saved_files['llm_format'] = str(llm_file)
        
        logger.info(f"内容已保存到: {output_dir}")
        return saved_files


def read_pdf_for_llm(
    pdf_path: str,
    max_length: Optional[int] = None,
    include_tables: bool = False
) -> str:
    """快速函数：读取PDF并转换为大模型格式
    
    Args:
        pdf_path: PDF文件路径
        max_length: 最大长度限制
        include_tables: 是否包含表格
        
    Returns:
        格式化后的文本
    """
    reader = PDFReader(pdf_path)
    return reader.to_llm_format(
        include_metadata=True,
        include_tables=include_tables,
        max_length=max_length
    )


def extract_code_from_pdf(
    pdf_path: str,
    preserve_formatting: bool = True,
    detect_language: bool = True
) -> List[Dict]:
    """快速函数：从PDF中提取代码块
    
    Args:
        pdf_path: PDF文件路径
        preserve_formatting: 是否保持格式（推荐True）
        detect_language: 是否检测代码语言
        
    Returns:
        代码块列表，每个代码块包含：
        - code: 代码内容
        - page: 页码
        - language: 检测到的语言
        - lines: 代码行数
        
    Example:
        >>> code_blocks = extract_code_from_pdf("strategy_guide.pdf")
        >>> for block in code_blocks:
        ...     print(f"第{block['page']}页 - {block['language']}代码:")
        ...     print(block['code'])
    """
    reader = PDFReader(pdf_path)
    return reader.extract_code_blocks(
        preserve_formatting=preserve_formatting,
        detect_language=detect_language
    )

