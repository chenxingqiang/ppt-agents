import os
from src.ppt_gen import MarkdownReader
from src.ppt_gen import PPTTemplateReader
from src.ppt_gen import DetailedPPTGenerator

template_path = "template.pptx"

markdown_paths = ["medical_imgame_sam-md/1.md"]

output_dir = "medical_imgame_sam-ppt/"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

for markdown_path in markdown_paths:
    template_reader = PPTTemplateReader(template_path)
    markdown_reader = MarkdownReader(markdown_path)
    ppt_generator = DetailedPPTGenerator(template_reader, markdown_reader, output_dir)
    ppt_generator.generate_ppt()
