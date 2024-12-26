from src.ppt_template_generator import PPTTemplateGenerator
import os

def main():
    # 创建templates目录（如果不存在）
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 初始化模板生成器
    generator = PPTTemplateGenerator()
    
    # 所有主题列表
    themes = [
        'modern',    # 现代主题
        'tech',      # 科技主题
        'nature',    # 自然主题
        'elegant',   # 优雅主题
        'vibrant',   # 活力主题
        'corporate', # 企业主题
        'creative',  # 创意主题
        'dark'       # 暗黑主题
    ]
    
    # 生成所有主题的模板
    for theme in themes:
        output_path = f'templates/{theme}_template.pptx'
        print(f'正在生成 {theme} 主题模板...')
        generator.generate_template(theme=theme, output_path=output_path)
        print(f'已生成模板: {output_path}')
    
    print('\n所有模板生成完成！')

if __name__ == '__main__':
    main() 