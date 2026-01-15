# PPT Agents

A Python-based tool for automatically generating PowerPoint presentations from markdown files. This tool uses intelligent layout analysis to format and structure content, making it easy to create professional presentations from markdown documentation.

## Features

- **Markdown to PowerPoint Conversion**: Convert markdown files to professional PPT presentations
- **Automatic Content Layout**: Smart analysis and positioning of content elements
- **Table Support**: Academic-style table formatting with alternating row colors
- **Multiple Themes**: Support for modern, tech, nature, elegant, vibrant, corporate, creative, dark themes
- **Template System**: Customizable PowerPoint templates
- **Batch Processing**: Process multiple markdown files at once
- **Reference Management**: Automatic reference numbering and formatting
- **Unified CLI**: Single command-line interface for all operations

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ppt-agents.git
cd ppt-agents
```

2. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Generate default template:

```bash
python main.py template
```

## Quick Start

### Check Environment

Verify your environment and dependencies are set up correctly:

```bash
python main.py check
```

### Generate Templates

Generate the default modern template:

```bash
python main.py template
```

Generate a specific theme template:

```bash
python main.py template --theme dark --output templates/dark_template.pptx
```

Generate all theme templates:

```bash
python main.py template --all
```

### Generate Presentations from Markdown

Process iEchor BP markdown files:

```bash
python main.py generate -i iechor-bp-md -o iechor-bp-ppt
```

Process LLM lecture markdown files with detailed mode:

```bash
python main.py generate -i llm-lecture-md -o llm-lecture-ppt --mode detailed
```

Clean existing files before generating:

```bash
python main.py generate -i iechor-bp-md -o iechor-bp-ppt --clean
```

Use a custom template:

```bash
python main.py generate -i input-md -o output-ppt --template templates/dark_template.pptx
```

### Programmatic Usage

```python
from src import PPTGenerator, MarkdownReader

# Simple generation from markdown
generator = PPTGenerator("templates/modern_template.pptx")
generator.process_markdown_file("input.md", "output.pptx")

# Detailed generation with template reader
from src import PPTTemplateReader, DetailedPPTGenerator

template_reader = PPTTemplateReader("templates/modern_template.pptx")
markdown_reader = MarkdownReader("input.md")
ppt_gen = DetailedPPTGenerator(template_reader, markdown_reader, "output/")
ppt_gen.generate_ppt()
```

## CLI Reference

```
usage: ppt-agents [-h] {generate,template,check} ...

Generate PowerPoint presentations from markdown files

positional arguments:
  {generate,template,check}
                        Available commands
    generate            Generate PPT from markdown files
    template            Generate PowerPoint templates
    check               Check environment and dependencies

Examples:
  ppt-agents generate -i iechor-bp-md -o iechor-bp-ppt
  ppt-agents generate -i llm-lecture-md -o llm-lecture-ppt --mode detailed
  ppt-agents template --theme modern --output templates/modern.pptx
  ppt-agents template --all
  ppt-agents check
```

### Generate Command Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input directory with markdown files (required) |
| `-o, --output` | Output directory for PPT files (required) |
| `-t, --template` | Template path (default: templates/modern_template.pptx) |
| `-m, --mode` | Generation mode: `simple` or `detailed` (default: simple) |
| `-c, --clean` | Clean existing PPT files first |

### Template Command Options

| Option | Description |
|--------|-------------|
| `--theme` | Theme name: modern, tech, nature, elegant, vibrant, corporate, creative, dark |
| `--output` | Output path for template |
| `--all` | Generate all theme templates |
| `--width` | Slide width in inches (default: 13.33) |
| `--height` | Slide height in inches (default: 7.5) |

## Project Structure

```
ppt-agents/
├── src/
│   ├── __init__.py           # Module exports
│   ├── layout_analyzer.py    # Content layout analysis
│   ├── md_reader.py          # Markdown file parsing
│   ├── ppt_gen.py            # Detailed PPT generator
│   ├── ppt_generator.py      # Core PPT generation
│   ├── ppt_template_generator.py  # Template creation
│   └── ppt_template_reader.py     # Template reading
├── templates/
│   └── modern_template.pptx  # Default template
├── iechor-bp-md/             # Input: iEchor BP markdown files
├── iechor-bp-ppt/            # Output: Generated presentations
├── llm-lecture-md/           # Input: LLM lecture markdown files
├── llm-lecture-ppt/          # Output: Generated presentations
├── main.py                   # Unified CLI entry point
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # This file
```

## Markdown Format

The tool supports standard markdown with the following features:

### Headings
- `#` - Main title (creates title slide)
- `##` - Section headers (creates section slides)
- `###` - Subsection headers

### Content Elements
- Bullet lists (`-` or `*`)
- Numbered lists (`1.`, `2.`, etc.)
- Tables (pipe-delimited format)
- Code blocks (fenced with triple backticks)
- Links and references

### Slide Separation
Use `---` to separate slides in a single markdown file.

### Example Markdown

```markdown
# Presentation Title

---

## Introduction

- First point
- Second point
- Third point

---

## Data Overview

| Category | Value | Notes |
|----------|-------|-------|
| A        | 100   | High  |
| B        | 75    | Medium|
| C        | 50    | Low   |

---

## Conclusion

Key takeaways:
- Summary point 1
- Summary point 2
```

## Available Themes

| Theme | Description |
|-------|-------------|
| **modern** | Clean, professional look with blue accents |
| **tech** | Futuristic theme with neon colors on dark background |
| **nature** | Green eco-friendly theme |
| **elegant** | Sophisticated with warm tones |
| **vibrant** | Colorful and energetic |
| **corporate** | Business professional with navy blue |
| **creative** | Artistic with pink and orange accents |
| **dark** | Dark mode with high contrast cyan and magenta |

## Configuration

### Font Sizes

Font sizes can be configured in `src/ppt_generator.py`:

```python
font_sizes = {
    1: Pt(40),      # Heading 1
    2: Pt(32),      # Heading 2
    3: Pt(28),      # Heading 3
    'body': Pt(18), # Normal text
    'table_header': Pt(16),
    'table_cell': Pt(14),
}
```

### Table Styles

Table appearance can be customized in the `table_styles` dictionary.

## Dependencies

- `python-pptx>=0.6.21` - PowerPoint file creation
- `markdown>=3.4.3` - Markdown parsing
- `beautifulsoup4>=4.12.0` - HTML/XML parsing
- `PyYAML>=6.0.1` - YAML configuration
- `python-frontmatter>=1.0.0` - Frontmatter parsing
- `python-dotenv>=1.0.0` - Environment variables
- `lxml>=4.9.0` - XML processing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
