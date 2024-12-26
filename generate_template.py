import argparse
import os
from src.ppt_template_generator import PPTTemplateGenerator

def main():
    parser = argparse.ArgumentParser(description='Generate PowerPoint template with specified theme and layout')
    
    parser.add_argument('--theme', 
                       choices=['modern', 'classic', 'minimal'],
                       default='modern',
                       help='Theme style for the template')
    
    parser.add_argument('--output', 
                       default='template.pptx',
                       help='Output path for the template file')
    
    parser.add_argument('--width',
                       type=float,
                       default=13.33,
                       help='Slide width in inches (default: 13.33 for 16:9)')
    
    parser.add_argument('--height',
                       type=float,
                       default=7.5,
                       help='Slide height in inches (default: 7.5 for 16:9)')
    
    args = parser.parse_args()
    
    # 创建输出目录（如果不存在）
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # 生成模板
    generator = PPTTemplateGenerator()
    
    # 设置幻灯片大小
    generator.set_slide_size(args.width, args.height)
    
    # 生成模板
    output_path = generator.generate_template(
        theme=args.theme,
        output_path=args.output
    )
    
    print(f"Template generated successfully: {output_path}")
    print(f"Theme: {args.theme}")
    print(f"Slide size: {args.width}\" x {args.height}\"")

if __name__ == "__main__":
    main() 