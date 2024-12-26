from dataclasses import dataclass
from typing import List, Dict, Optional
import re

@dataclass
class ContentElement:
    type: str  # 'title', 'bullet_list', 'table', 'numbered_list', 'paragraph'
    content: str
    level: int
    children: List['ContentElement']

@dataclass
class SlideLayout:
    layout_type: str  # 'title', 'content', 'two_column', 'comparison', 'image_text'
    title_position: tuple  # (x, y, width, height)
    content_positions: List[tuple]  # [(x, y, width, height), ...]
    notes_position: tuple

class LayoutAnalyzer:
    def __init__(self):
        self.layout_patterns = {
            'bullet_list': r'^\s*[-*]\s+(.+)$',
            'numbered_list': r'^\s*\d+\.\s+(.+)$',
            'table': r'^\|.+\|$',
            'heading': r'^#{1,6}\s+(.+)$'
        }
        
        self.slide_templates = {
            'title': {
                'max_title_length': 50,
                'max_content_blocks': 1
            },
            'content': {
                'max_title_length': 40,
                'max_bullet_points': 6,
                'max_content_blocks': 2
            },
            'two_column': {
                'max_title_length': 40,
                'max_items_per_column': 4,
                'max_content_blocks': 2
            },
            'comparison': {
                'max_title_length': 40,
                'max_rows': 4,
                'max_content_blocks': 2
            }
        }

    def parse_markdown_section(self, content: str) -> List[ContentElement]:
        """Parse markdown content into structured elements."""
        elements = []
        current_element = None
        
        for line in content.split('\n'):
            element_type = self._identify_element_type(line)
            if element_type:
                if current_element and current_element.type != element_type:
                    elements.append(current_element)
                    current_element = None
                
                if not current_element:
                    current_element = ContentElement(
                        type=element_type,
                        content=line,
                        level=self._get_indent_level(line),
                        children=[]
                    )
                else:
                    current_element.content += '\n' + line
                    
        if current_element:
            elements.append(current_element)
            
        return elements

    def _identify_element_type(self, line: str) -> Optional[str]:
        """Identify the type of content element from a line."""
        for pattern_type, pattern in self.layout_patterns.items():
            if re.match(pattern, line):
                return pattern_type
        return None

    def _get_indent_level(self, line: str) -> int:
        """Calculate the indentation level of a line."""
        return len(line) - len(line.lstrip())

    def analyze_slide_content(self, elements: List[ContentElement]) -> str:
        """Determine the best slide layout based on content elements."""
        if not elements:
            return 'content'

        # Count different types of elements
        element_types = [e.type for e in elements]
        
        if 'table' in element_types:
            return 'comparison'
        
        if len(elements) > 3:
            return 'two_column'
            
        if all(e.type == 'bullet_list' for e in elements):
            return 'content'
            
        return 'content'  # default layout

    def get_layout_instructions(self, slide_type: str, elements: List[ContentElement]) -> Dict:
        """Generate specific layout instructions for the slide."""
        template = self.slide_templates[slide_type]
        instructions = {
            'layout_type': slide_type,
            'title': {
                'position': (0.1, 0.1, 0.8, 0.15),
                'max_length': template['max_title_length']
            },
            'content_blocks': []
        }

        if slide_type == 'two_column':
            instructions['content_blocks'] = [
                {'position': (0.1, 0.3, 0.4, 0.6)},
                {'position': (0.5, 0.3, 0.4, 0.6)}
            ]
        elif slide_type == 'comparison':
            instructions['content_blocks'] = [
                {'position': (0.1, 0.3, 0.8, 0.6)}
            ]
        else:
            instructions['content_blocks'] = [
                {'position': (0.1, 0.3, 0.8, 0.6)}
            ]

        return instructions

    def optimize_content_distribution(self, elements: List[ContentElement], layout_type: str) -> List[Dict]:
        """Optimize how content is distributed across the slide."""
        template = self.slide_templates[layout_type]
        distributions = []

        if layout_type == 'two_column':
            # Split elements between columns
            mid_point = len(elements) // 2
            distributions = [
                {
                    'position': (0.1, 0.3, 0.4, 0.6),
                    'elements': elements[:mid_point]
                },
                {
                    'position': (0.5, 0.3, 0.4, 0.6),
                    'elements': elements[mid_point:]
                }
            ]
        else:
            distributions = [
                {
                    'position': (0.1, 0.3, 0.8, 0.6),
                    'elements': elements
                }
            ]

        return distributions

    def process_slide(self, markdown_content: str) -> Dict:
        """Process a complete slide and return layout instructions."""
        elements = self.parse_markdown_section(markdown_content)
        layout_type = self.analyze_slide_content(elements)
        layout_instructions = self.get_layout_instructions(layout_type, elements)
        content_distribution = self.optimize_content_distribution(elements, layout_type)
        
        return {
            'layout_type': layout_type,
            'layout_instructions': layout_instructions,
            'content_distribution': content_distribution
        } 