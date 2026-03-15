#!/usr/bin/env python3
"""
切片元数据增强脚本
将基础切片升级为符合 content-slice-rules.md 规范的完整切片
"""

import re
import os
import yaml
from pathlib import Path
from datetime import datetime


def extract_content_info(content: str) -> dict:
    """从内容中提取信息用于生成元数据"""
    info = {
        'title': '',
        'exam_points': [],
        'difficulty': 'medium',
        'tags': []
    }
    
    # 提取标题（第一个 # 开头的行）
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        info['title'] = title_match.group(1).strip()
    
    # 提取关键词作为 tags
    keywords = [
        'enzyme', 'catalyst', 'protein', 'substrate', 'active site',
        'cell', 'membrane', 'structure', 'function', 'DNA', 'RNA',
        'gene', 'expression', 'transcription', 'translation'
    ]
    content_lower = content.lower()
    for keyword in keywords:
        if keyword in content_lower:
            info['tags'].append(keyword)
    
    # 根据内容长度判断难度
    word_count = len(content.split())
    if word_count < 800:
        info['difficulty'] = 'easy'
    elif word_count > 1500:
        info['difficulty'] = 'hard'
    else:
        info['difficulty'] = 'medium'
    
    return info


def generate_exam_points(content: str, topic: str) -> list:
    """根据内容生成考点列表"""
    exam_points = []
    content_lower = content.lower()
    
    # 基于主题和内容的考点识别
    topic_keywords = {
        'enzyme': [
            '酶的定义和特性',
            '酶的作用机制',
            '影响酶活性的因素',
            '酶的动力学参数'
        ],
        'cell-structure': [
            '细胞结构识别',
            '细胞器功能',
            '原核与真核细胞比较'
        ],
        'biological-molecules': [
            '生物大分子结构',
            '生物分子检测',
            '分子功能'
        ],
        'gene-expression': [
            '基因表达调控',
            '转录和翻译',
            '表观遗传学'
        ]
    }
    
    # 根据内容匹配考点
    if 'enzyme' in topic or 'enzyme' in content_lower:
        if 'catalyst' in content_lower or 'cataly' in content_lower:
            exam_points.append('酶作为生物催化剂的特点')
        if 'active site' in content_lower or 'substrate' in content_lower:
            exam_points.append('酶的活性位点和底物结合')
        if 'temperature' in content_lower or 'ph' in content_lower:
            exam_points.append('温度和pH对酶活性的影响')
        if 'inhibitor' in content_lower:
            exam_points.append('酶抑制剂的类型和作用')
        if 'km' in content_lower or 'vmax' in content_lower:
            exam_points.append('酶动力学参数Km和Vmax')
    
    # 如果没有识别到考点，使用通用考点
    if not exam_points:
        exam_points = ['理解核心概念', '应用知识解决问题']
    
    return exam_points


def create_enhanced_metadata(slice_num: int, word_count: int, source_file: str,
                            content: str, chapter: str = "3", subject: str = "biology") -> str:
    """创建增强的元数据"""
    
    # 提取内容信息
    info = extract_content_info(content)
    exam_points = generate_exam_points(content, f"chapter-{chapter}")
    
    # 生成 ID
    topic = f"chapter-{chapter}"
    slice_id = f"bio-{topic}-{slice_num:03d}"
    
    # 计算预计时长（基于词数，假设每分钟150词）
    duration = max(5, min(20, word_count // 150))
    
    # 构建元数据
    metadata = {
        'id': slice_id,
        'topic': topic,
        'source': f"CIE Biology 9700 Chapter {chapter}",
        'exam_points': exam_points,
        'difficulty': info['difficulty'],
        'duration': duration,
        'tags': info['tags'][:5],  # 最多5个标签
        'sequence': slice_num,
        'part_of_series': True,
        'subject': subject,
        'grade': 'A-Level',
        'word_count': word_count,
        'created_at': datetime.now().strftime('%Y-%m-%d'),
        'updated_at': datetime.now().strftime('%Y-%m-%d')
    }
    
    # 转换为 YAML 格式
    yaml_content = yaml.dump(metadata, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    return f"---\n{yaml_content}---\n\n"


def enhance_slice_file(input_path: Path, output_path: Path, chapter: str = "3"):
    """增强单个切片文件"""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取现有元数据
    existing_metadata_match = re.match(r'^---\n(.*?)\n---\n\n', content, re.DOTALL)
    
    if existing_metadata_match:
        # 解析现有元数据
        existing_yaml = existing_metadata_match.group(1)
        existing_data = yaml.safe_load(existing_yaml)
        
        slice_num = existing_data.get('slice_number', 1)
        word_count = existing_data.get('word_count', 0)
        source_file = existing_data.get('source_file', '')
        
        # 提取正文内容
        body_content = content[existing_metadata_match.end():]
    else:
        # 没有元数据，从文件名推断
        slice_num = int(input_path.stem.split('_')[-1])
        word_count = len(content.split())
        source_file = str(input_path)
        body_content = content
    
    # 生成增强的元数据
    enhanced_metadata = create_enhanced_metadata(
        slice_num=slice_num,
        word_count=word_count,
        source_file=source_file,
        content=body_content,
        chapter=chapter
    )
    
    # 组合新文件内容
    new_content = enhanced_metadata + body_content
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Enhanced: {input_path.name} -> {output_path.name}")
    return slice_num


def enhance_all_slices(input_dir: str, output_dir: str, chapter: str = "3"):
    """增强目录中的所有切片"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # 创建输出目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 获取所有切片文件
    slice_files = sorted(input_path.glob('slice_*.md'))
    
    if not slice_files:
        print(f"No slice files found in {input_dir}")
        return 0
    
    print(f"Found {len(slice_files)} slice files")
    print(f"Enhancing slices from {input_dir} to {output_dir}")
    print("-" * 60)
    
    enhanced_count = 0
    for slice_file in slice_files:
        output_file = output_path / slice_file.name
        enhance_slice_file(slice_file, output_file, chapter)
        enhanced_count += 1
    
    print("-" * 60)
    print(f"Enhanced {enhanced_count} slices")
    
    # 生成切片索引文件
    generate_slice_index(output_path, chapter)
    
    return enhanced_count


def generate_slice_index(slice_dir: Path, chapter: str):
    """生成切片索引文件"""
    
    slice_files = sorted(slice_dir.glob('slice_*.md'))
    
    index_content = f"""# Chapter {chapter} - Content Slices Index

This directory contains {len(slice_files)} content slices for Chapter {chapter}.

## Slice Overview

| Slice | ID | Topic | Difficulty | Duration | Word Count |
|-------|-----|-------|------------|----------|------------|
"""
    
    for slice_file in slice_files:
        with open(slice_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取元数据
        metadata_match = re.match(r'^---\n(.*?)\n---\n\n', content, re.DOTALL)
        if metadata_match:
            metadata = yaml.safe_load(metadata_match.group(1))
            index_content += f"| [{slice_file.stem}]({slice_file.name}) | {metadata.get('id', 'N/A')} | {metadata.get('topic', 'N/A')} | {metadata.get('difficulty', 'N/A')} | {metadata.get('duration', 'N/A')} min | {metadata.get('word_count', 'N/A')} |\n"
    
    index_content += f"""
## Quick Links

- [Chapter {chapter} Slides](../../slides/cie-9700/chapter-{chapter}/)
- [Chapter {chapter} Notes](../../docs/cie/as/chapter{chapter}.md)

---

*Generated on {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    index_file = slice_dir / 'README.md'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\nGenerated index: {index_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhance slice metadata')
    parser.add_argument('--input', '-i', default='slices/chapter_3',
                       help='Input directory containing slices')
    parser.add_argument('--output', '-o', default='slices/chapter_3_enhanced',
                       help='Output directory for enhanced slices')
    parser.add_argument('--chapter', '-c', default='3',
                       help='Chapter number')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Slice Metadata Enhancement Tool")
    print("=" * 60)
    print()
    
    # 检查输入目录
    if not os.path.exists(args.input):
        print(f"Error: Input directory not found: {args.input}")
        return 1
    
    # 执行增强
    count = enhance_all_slices(args.input, args.output, args.chapter)
    
    print()
    print("=" * 60)
    print(f"Enhancement complete! {count} slices enhanced.")
    print(f"Output directory: {args.output}")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
