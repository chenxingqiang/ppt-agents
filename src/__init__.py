"""
PPT Agents - A Python-based tool for generating PowerPoint presentations from markdown files.

This module provides components for:
- Reading and parsing markdown files
- Analyzing content layout
- Generating PowerPoint presentations with various themes and templates
"""

from src.md_reader import MarkdownReader
from src.layout_analyzer import LayoutAnalyzer, ContentElement, SlideLayout
from src.ppt_generator import PPTGenerator
from src.ppt_template_generator import PPTTemplateGenerator
from src.ppt_template_reader import PPTTemplateReader
from src.ppt_gen import DetailedPPTGenerator

__all__ = [
    'MarkdownReader',
    'LayoutAnalyzer',
    'ContentElement',
    'SlideLayout',
    'PPTGenerator',
    'PPTTemplateGenerator',
    'PPTTemplateReader',
    'DetailedPPTGenerator',
]

__version__ = '1.0.0'
