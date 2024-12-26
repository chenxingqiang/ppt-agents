import os
import logging
import glob
from datetime import datetime
from src.ppt_generator import PPTGenerator
from src.layout_analyzer import LayoutAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def clean_old_files(directory: str, pattern: str):
    """Clean up old PPT files."""
    old_files = glob.glob(os.path.join(directory, pattern))
    for file in old_files:
        try:
            os.remove(file)
            logger.info(f"Cleaned up old file: {file}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file}: {e}")

def process_markdown_files(input_dir: str, output_dir: str, template_path: str):
    """Process all markdown files in the input directory."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Clean up old files
    clean_old_files(output_dir, "*.pptx")

    # Initialize generator with template
    ppt_generator = PPTGenerator(template_path)
    
    # Get all markdown files
    md_files = glob.glob(os.path.join(input_dir, "*.md"))
    successful_count = 0
    
    for md_file in md_files:
        try:
            logger.info(f"Processing markdown file: {md_file}")
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Extract title from markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                title = content.split('\n')[0].strip('# ').replace(':', '-')
            
            output_file = os.path.join(
                output_dir,
                f"{timestamp}-{base_name}-{title.replace(' ', '')}.pptx"
            )
            
            # Process the file
            ppt_generator.process_markdown_file(md_file, output_file)
            
            # Apply modern theme
            ppt_generator.apply_theme('modern')
            
            # Verify file was created
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                logger.info(f"Successfully generated PPT: {output_file}")
                successful_count += 1
            else:
                logger.error(f"Failed to generate PPT: {output_file}")
                
        except Exception as e:
            logger.error(f"Error processing file {md_file}: {e}")
    
    logger.info(f"Processing complete. Successfully generated {successful_count} out of {len(md_files)} presentations.")

if __name__ == "__main__":
    # Define directories
    input_dir = "iechor-bp-md"
    output_dir = "iechor-bp-ppt"
    template_path = "templates/modern_template.pptx"  # Use modern template
    
    # Process files
    process_markdown_files(input_dir, output_dir, template_path)




