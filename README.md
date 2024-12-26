# PPT Agents

A Python-based tool for automatically generating PowerPoint presentations from markdown files. This tool uses AI agents to intelligently format and structure content, making it easy to create professional presentations from markdown documentation.

## Features

- Convert markdown files to PowerPoint presentations
- Automatic content layout and formatting
- Support for tables, lists, and references
- Multiple theme templates
- Smart content sizing and positioning
- Academic-style table formatting

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ppt-agents.git
cd ppt-agents
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your markdown files in the `iechor-bp-md` directory
2. Run the main script:

```bash
python iechor_bp_main.py
```

3. Generated PowerPoint files will be saved in the `iechor-bp-ppt` directory

## Project Structure

```
ppt-agents/
├── src/
│   ├── __init__.py
│   ├── layout_analyzer.py
│   ├── md_reader.py
│   └── ppt_generator.py
├── templates/
├── iechor-bp-md/
├── iechor-bp-ppt/
├── requirements.txt
└── iechor_bp_main.py
```

## Configuration

- Templates can be customized in the `templates` directory
- Font sizes and styles can be configured in `src/ppt_generator.py`
- Table styles can be modified in the `table_styles` dictionary

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
