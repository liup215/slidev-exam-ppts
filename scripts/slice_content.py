#!/usr/bin/env python3
"""
教材内容分片脚本
将教材内容按 1000 词为一片进行分片
"""

import re
import os
from pathlib import Path


def count_words(text: str) -> int:
    """统计文本中的词数（英文单词）"""
    # 移除 markdown 标记，只保留实际文本
    # 移除代码块、图片标记等
    clean_text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 图片
    clean_text = re.sub(r'\[.*?\]\(.*?\)', '', clean_text)  # 链接
    clean_text = re.sub(r'[#*_`]', '', clean_text)  # markdown 标记
    clean_text = re.sub(r'\d+', '', clean_text)  # 数字
    
    # 统计英文单词
    words = re.findall(r'[a-zA-Z]+', clean_text)
    return len(words)


def split_into_paragraphs(text: str) -> list:
    """将文本分割成段落"""
    # 按空行分割段落
    paragraphs = re.split(r'\n\s*\n', text)
    # 清理每个段落
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs


def split_paragraph_into_sentences(paragraph: str) -> list:
    """将段落分割成句子"""
    # 使用正则表达式分割句子，考虑常见的句末标点
    sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=\?\n)|(?<=!\n)|(?<=\.\n)'
    sentences = re.split(sentence_pattern, paragraph)
    # 清理每个句子
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


def create_slice_metadata(slice_num: int, word_count: int, start_pos: int, end_pos: int, 
                          source_file: str) -> str:
    """创建分片文件的元数据"""
    return f"""---
slice_number: {slice_num:03d}
word_count: {word_count}
source_file: {source_file}
start_position: paragraph_{start_pos}
end_position: paragraph_{end_pos}
created_at: auto-generated
---

"""


def slice_content(input_file: str, output_dir: str, target_words: int = 1000):
    """
    将内容按目标词数分片
    
    分片规则：
    1. 尽量在段落边界处分割
    2. 如果段落超过目标词数，则在句子边界处分割
    """
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割成段落
    paragraphs = split_into_paragraphs(content)
    
    slices = []
    current_slice = []
    current_word_count = 0
    start_para_idx = 0
    
    for i, paragraph in enumerate(paragraphs):
        para_word_count = count_words(paragraph)
        
        # 如果当前段落本身超过目标词数，需要分割
        if para_word_count > target_words:
            # 如果当前切片已有内容，先保存
            if current_slice:
                slices.append({
                    'content': '\n\n'.join(current_slice),
                    'word_count': current_word_count,
                    'start_pos': start_para_idx,
                    'end_pos': i - 1
                })
                current_slice = []
                current_word_count = 0
                start_para_idx = i
            
            # 分割大段落
            sentences = split_paragraph_into_sentences(paragraph)
            temp_slice = []
            temp_word_count = 0
            
            for sentence in sentences:
                sent_word_count = count_words(sentence)
                
                if temp_word_count + sent_word_count > target_words and temp_slice:
                    # 保存当前句子切片
                    slices.append({
                        'content': ' '.join(temp_slice),
                        'word_count': temp_word_count,
                        'start_pos': i,
                        'end_pos': i
                    })
                    temp_slice = [sentence]
                    temp_word_count = sent_word_count
                else:
                    temp_slice.append(sentence)
                    temp_word_count += sent_word_count
            
            # 保存剩余的句子
            if temp_slice:
                slices.append({
                    'content': ' '.join(temp_slice),
                    'word_count': temp_word_count,
                    'start_pos': i,
                    'end_pos': i
                })
            
            start_para_idx = i + 1
        
        # 如果添加当前段落后超过目标词数，且当前切片不为空
        elif current_word_count + para_word_count > target_words and current_slice:
            # 保存当前切片
            slices.append({
                'content': '\n\n'.join(current_slice),
                'word_count': current_word_count,
                'start_pos': start_para_idx,
                'end_pos': i - 1
            })
            # 开始新切片
            current_slice = [paragraph]
            current_word_count = para_word_count
            start_para_idx = i
        else:
            # 添加到当前切片
            current_slice.append(paragraph)
            current_word_count += para_word_count
    
    # 保存最后一个切片
    if current_slice:
        slices.append({
            'content': '\n\n'.join(current_slice),
            'word_count': current_word_count,
            'start_pos': start_para_idx,
            'end_pos': len(paragraphs) - 1
        })
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 写入分片文件
    for idx, slice_data in enumerate(slices, 1):
        filename = f"slice_{idx:03d}.md"
        filepath = os.path.join(output_dir, filename)
        
        metadata = create_slice_metadata(
            slice_num=idx,
            word_count=slice_data['word_count'],
            start_pos=slice_data['start_pos'],
            end_pos=slice_data['end_pos'],
            source_file=input_file
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(metadata)
            f.write(slice_data['content'])
        
        print(f"Created: {filename} ({slice_data['word_count']} words)")
    
    print(f"\nTotal slices created: {len(slices)}")
    return len(slices)


def main():
    # 配置
    input_file = "data/cie-9700/textbook_by_chapter/Chapter_3.md"
    output_dir = "slices/chapter_3"
    target_words = 1000
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        return 1
    
    print(f"Slicing content from: {input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Target words per slice: {target_words}")
    print("-" * 50)
    
    # 执行分片
    num_slices = slice_content(input_file, output_dir, target_words)
    
    print("-" * 50)
    print(f"Slicing complete! {num_slices} slices created in {output_dir}/")
    return 0


if __name__ == "__main__":
    exit(main())
