"""
PowerPoint Generator module for creating presentations from markdown content.

This module provides the PPTGenerator class which handles:
- Template-based slide generation with intelligent layout selection
- Automatic slide type detection (title, toc, section, content, closing)
- Proper font sizing and content formatting
- Table formatting with academic style
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.dml.color import RGBColor
from typing import Dict, List, Tuple, Optional
import re


class PPTGenerator:
    """Generate PowerPoint presentations from markdown content."""
    
    # Keywords for detecting slide types
    TITLE_KEYWORDS = []  # First slide is always title
    TOC_KEYWORDS = ['目录', '大纲', 'contents', 'outline', 'agenda']
    SECTION_KEYWORDS = ['章节', '部分', 'section', 'part']
    CLOSING_KEYWORDS = ['总结', '结束', '谢谢', '感谢', 'summary', 'conclusion', 
                        'thank', 'q&a', '问答', '引用', '参考']
    
    def __init__(self, template_path: str = None):
        self.template_path = template_path or "templates/modern_template.pptx"
        self.prs = Presentation(self.template_path)
        
        # Remove any existing slides from template (keep only layouts)
        self._clear_existing_slides()
        
        self.slide_layouts = self._get_layouts_by_name()
        self.slide_index = 0  # Track slide position
    
    def _clear_existing_slides(self):
        """Remove all existing slides from the presentation, keeping only layouts."""
        # Get list of slide IDs to delete
        slide_ids = [slide.slide_id for slide in self.prs.slides]
        for slide_id in slide_ids:
            # Find the slide by ID and remove it
            rId = self.prs.slides._sldIdLst[0].rId
            self.prs.part.drop_rel(rId)
            del self.prs.slides._sldIdLst[0]
        
        # Font sizes - increased for better readability
        self.font_sizes = {
            'title_main': Pt(44),       # Main title on title page
            'title_subtitle': Pt(28),   # Subtitle on title page
            'section_title': Pt(40),    # Section header title
            'slide_title': Pt(36),      # Regular slide title
            'body': Pt(24),             # Normal body text
            'bullet_l1': Pt(24),        # Level 1 bullets
            'bullet_l2': Pt(22),        # Level 2 bullets  
            'bullet_l3': Pt(20),        # Level 3 bullets
            'toc_item': Pt(26),         # TOC items
            'table_header': Pt(20),     # Table headers
            'table_cell': Pt(18),       # Table cells
        }
        
        # Table styles
        self.table_styles = {
            'academic': {
                'header_bg': RGBColor(69, 69, 69),
                'header_font': RGBColor(255, 255, 255),
                'row_bg_even': RGBColor(242, 242, 242),
                'row_bg_odd': RGBColor(255, 255, 255),
                'cell_font': RGBColor(0, 0, 0),
                'border_color': RGBColor(128, 128, 128),
            }
        }

    def _get_layouts_by_name(self) -> Dict:
        """Get slide layouts by their exact names."""
        layouts = {}
        for layout in self.prs.slide_layouts:
            name = layout.name.lower().strip()
            layouts[name] = layout
            # Also map common variations
            if 'title' in name and 'content' not in name:
                layouts['title'] = layout
            elif 'toc' in name or 'contents' in name:
                layouts['toc'] = layout
            elif 'section' in name:
                layouts['section'] = layout
            elif 'closing' in name or 'end' in name:
                layouts['closing'] = layout
            elif 'content' in name:
                layouts['content'] = layout
        return layouts

    def _detect_slide_type(self, title: str, content: str, is_first: bool) -> str:
        """
        Detect the appropriate slide type based on title and content.
        
        Returns: 'title', 'toc', 'section', 'content', or 'closing'
        """
        title_lower = title.lower() if title else ''
        
        # First slide is always title
        if is_first:
            return 'title'
        
        # Check for TOC
        for kw in self.TOC_KEYWORDS:
            if kw in title_lower:
                return 'toc'
        
        # Check for closing/summary
        for kw in self.CLOSING_KEYWORDS:
            if kw in title_lower:
                return 'closing'
        
        # Check for section headers (short title, minimal content)
        content_lines = [l for l in content.split('\n') if l.strip() and not l.startswith('**')]
        if len(content_lines) <= 1 and len(title) < 30:
            # Could be a section header
            for kw in self.SECTION_KEYWORDS:
                if kw in title_lower:
                    return 'section'
        
        # Default to content
        return 'content'

    def _get_layout(self, slide_type: str):
        """Get the appropriate layout for a slide type."""
        # Try exact match first
        if slide_type in self.slide_layouts:
            return self.slide_layouts[slide_type]
        
        # Fallback chain
        fallbacks = {
            'title': ['title', 'content'],
            'toc': ['toc', 'content'],
            'section': ['section', 'title', 'content'],
            'closing': ['closing', 'section', 'content'],
            'content': ['content'],
        }
        
        for fb in fallbacks.get(slide_type, ['content']):
            if fb in self.slide_layouts:
                return self.slide_layouts[fb]
        
        # Last resort: use first layout with content placeholder
        return self.prs.slide_layouts[1]

    def _clean_title(self, raw_title: str) -> str:
        """Clean up title text."""
        # Remove markdown heading markers
        title = raw_title.lstrip('#').strip()
        # Remove leading numbers (e.g., "2. 目录页" -> "目录页")
        title = re.sub(r'^\d+\.\s*', '', title)
        return title

    def _extract_subtitle(self, lines: List[str], start_idx: int) -> Tuple[str, int]:
        """Extract subtitle from content lines."""
        subtitle = ""
        new_start = start_idx
        
        for i, line in enumerate(lines[start_idx:], start_idx):
            stripped = line.strip()
            if stripped.startswith('- **副标题**') or stripped.startswith('- **Subtitle**'):
                subtitle = stripped.split(':', 1)[-1].strip() if ':' in stripped else ''
                new_start = i + 1
            elif stripped.startswith('- **日期**') or stripped.startswith('- **演讲者**'):
                # Skip metadata lines
                new_start = i + 1
            elif stripped and not stripped.startswith('-'):
                break
        
        return subtitle, new_start

    def _format_content_for_type(self, content: str, slide_type: str) -> List[dict]:
        """Format content based on slide type."""
        lines = content.strip().split('\n')
        formatted = []
        
        # Filter out reference sections
        filtered_lines = []
        skip_refs = False
        for line in lines:
            if '**参考文献**' in line or '**参考资料**' in line:
                skip_refs = True
                continue
            if skip_refs:
                if line.strip() and not line.strip()[0].isdigit():
                    skip_refs = False
                else:
                    continue
            filtered_lines.append(line)
        
        for line in filtered_lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Determine item properties
            item = {'text': stripped, 'level': 0, 'is_bullet': False, 'bold': False}
            
            # Handle numbered list (for TOC)
            if slide_type == 'toc' and re.match(r'^\d+\.', stripped):
                item['text'] = stripped
                item['is_bullet'] = False
                item['font_size'] = self.font_sizes['toc_item']
            # Handle bullet points
            elif stripped.startswith('- ') or stripped.startswith('* '):
                indent = len(line) - len(line.lstrip())
                item['text'] = stripped[2:].strip()
                item['level'] = min(indent // 2, 2)
                item['is_bullet'] = True
                item['font_size'] = self.font_sizes[f'bullet_l{item["level"]+1}']
            # Handle bold text markers
            elif stripped.startswith('**') and stripped.endswith('**'):
                item['text'] = stripped.strip('*')
                item['bold'] = True
                item['font_size'] = self.font_sizes['body']
            else:
                item['font_size'] = self.font_sizes['body']
            
            # Clean markdown formatting
            item['text'] = re.sub(r'\*\*([^*]+)\*\*', r'\1', item['text'])
            
            if item['text']:
                formatted.append(item)
        
        return formatted

    def _apply_content_to_placeholder(self, placeholder, items: List[dict], slide_type: str):
        """Apply formatted content to a placeholder shape."""
        if not placeholder or not items:
            return
        
        tf = placeholder.text_frame
        tf.clear()
        tf.word_wrap = True
        
        for i, item in enumerate(items):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            
            p.text = item['text']
            p.level = item.get('level', 0)
            
            # Set bullet
            if item.get('is_bullet', False):
                p.bullet = True
            
            # Set font
            if p.runs:
                run = p.runs[0]
            else:
                run = p.add_run()
                run.text = item['text']
            
            run.font.size = item.get('font_size', self.font_sizes['body'])
            if item.get('bold', False):
                run.font.bold = True

    def create_slide(self, markdown_content: str, is_first: bool = False):
        """Create a single slide from markdown content."""
        lines = markdown_content.strip().split('\n')
        
        # Find title
        title = None
        content_start = 0
        
        for i, line in enumerate(lines):
            if line.startswith('#'):
                title = self._clean_title(line)
                content_start = i + 1
                break
        
        if not title:
            return None
            
        # Get content and detect slide type
        content = '\n'.join(lines[content_start:])
        slide_type = self._detect_slide_type(title, content, is_first)
        
        # Get appropriate layout
        layout = self._get_layout(slide_type)
        slide = self.prs.slides.add_slide(layout)
        
        # Apply title
        if slide.shapes.title:
            slide.shapes.title.text = title
            tf = slide.shapes.title.text_frame
            for para in tf.paragraphs:
                if slide_type == 'title':
                    para.font.size = self.font_sizes['title_main']
                elif slide_type == 'section':
                    para.font.size = self.font_sizes['section_title']
                else:
                    para.font.size = self.font_sizes['slide_title']
                para.font.bold = True
        
        # Handle title slide subtitle
        if slide_type == 'title':
            subtitle, content_start_new = self._extract_subtitle(lines, content_start)
            if subtitle:
                # Find subtitle placeholder (idx=1 for subtitle)
                for shape in slide.placeholders:
                    if shape.placeholder_format.idx == 1:
                        shape.text = subtitle
                        for para in shape.text_frame.paragraphs:
                            para.font.size = self.font_sizes['title_subtitle']
                        break
            return slide
        
        # Handle section slide (no body content needed)
        if slide_type == 'section':
            return slide
        
        # Handle closing slide
        if slide_type == 'closing':
            # Minimal content for closing
            return slide
        
        # Format and apply content for content/toc slides
        formatted_items = self._format_content_for_type(content, slide_type)
        
        # Find body placeholder
        body_placeholder = None
            for shape in slide.placeholders:
            if shape.placeholder_format.idx == 1:  # Body placeholder
                body_placeholder = shape
                    break
        
        if body_placeholder and formatted_items:
            self._apply_content_to_placeholder(body_placeholder, formatted_items, slide_type)
        
        return slide

    def _split_into_slides(self, content: str) -> List[str]:
        """Split markdown content into individual slides."""
        # Try --- separator first
        if '\n---\n' in content or content.startswith('---'):
            slides = content.split('---')
            slides = [s.strip() for s in slides if s.strip()]
            if len(slides) > 1:
                return slides
        
        # Split by heading levels
        slides = []
        current_slide = []
        lines = content.split('\n')
        
        # Detect primary heading level
        h2_count = sum(1 for line in lines if line.startswith('## '))
        h3_count = sum(1 for line in lines if line.startswith('### '))
        section_pattern = '### ' if h3_count > h2_count else '## '
        
        for line in lines:
            # New slide on section heading or main title
            if line.startswith(section_pattern) or (line.startswith('# ') and not line.startswith('## ')):
                if current_slide:
                    slides.append('\n'.join(current_slide))
                current_slide = [line]
            else:
                current_slide.append(line)
        
        if current_slide:
            slides.append('\n'.join(current_slide))
        
        return slides

    def process_markdown_file(self, markdown_path: str, output_path: str):
        """Process a markdown file and generate PowerPoint presentation."""
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        slides_content = self._split_into_slides(content)
        
        for i, slide_content in enumerate(slides_content):
            if slide_content.strip():
                self.create_slide(slide_content.strip(), is_first=(i == 0))
        
        self.prs.save(output_path)

    def apply_theme(self, theme_name: str):
        """Apply a predefined theme to the presentation."""
        theme_settings = {
            'modern': {
                'background_color': 'FFFFFF',
                'title_font': 'Arial',
                'body_font': 'Arial',
                'accent_color': '4472C4'
            },
            'classic': {
                'background_color': 'F2F2F2',
                'title_font': 'Times New Roman',
                'body_font': 'Calibri',
                'accent_color': '8B0000'
            }
        }
        
        if theme_name in theme_settings:
            theme = theme_settings[theme_name]
            for layout in self.prs.slide_layouts:
                for shape in layout.shapes:
                    if shape.has_text_frame:
                        for para in shape.text_frame.paragraphs:
                            for run in para.runs:
                                if 'title' in layout.name.lower():
                                    run.font.name = theme['title_font']
                                else:
                                    run.font.name = theme['body_font'] 
