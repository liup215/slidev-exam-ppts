#!/usr/bin/env python3
"""
下载飞书云盘 CIE 9700 资料
"""

import os
import requests
import json

# 配置
APP_ID = "cli_a9907814ddbb1013"
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')

# 文件夹 tokens
FOLDERS = {
    "note-for-each-chapter": "XGjtfmfyOlMVAGdg8TPcj4LAnEf",
    "textbook_by_chapter": "EWYkfWCMqlmjdkdVWUDcNFQGnOc",
    "must-remember-question-by-chapter": "K2vXfi5MxlouPqdliJ8cR5wknIb"
}

# 下载目录
DOWNLOAD_DIR = "data/cie-9700"

def get_token():
    """获取 tenant_access_token"""
    resp = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return resp.json()['tenant_access_token']

def list_files(token, folder_token):
    """列出文件夹内容"""
    resp = requests.get(
        'https://open.feishu.cn/open-apis/drive/v1/files',
        headers={'Authorization': f'Bearer {token}'},
        params={'folder_token': folder_token, 'page_size': 50}
    )
    return resp.json()

def download_file(token, file_token, save_path):
    """下载文件"""
    resp = requests.get(
        f'https://open.feishu.cn/open-apis/drive/v1/files/{file_token}/download',
        headers={'Authorization': f'Bearer {token}'},
        stream=True
    )
    
    with open(save_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return save_path

def main():
    if not APP_SECRET:
        print("错误: FEISHU_APP_SECRET 环境变量未设置")
        return
    
    print("获取飞书 token...")
    token = get_token()
    print("Token 获取成功")
    
    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    for folder_name, folder_token in FOLDERS.items():
        print(f"\n处理文件夹: {folder_name}")
        
        # 创建子目录
        subdir = os.path.join(DOWNLOAD_DIR, folder_name)
        os.makedirs(subdir, exist_ok=True)
        
        # 列出文件
        data = list_files(token, folder_token)
        if data.get('code') != 0:
            print(f"  错误: {data.get('msg')}")
            continue
        
        files = data.get('data', {}).get('files', [])
        print(f"  找到 {len(files)} 个文件")
        
        # 下载每个文件
        for item in files:
            name = item.get('name')
            file_token = item.get('token')
            file_type = item.get('type')
            
            if file_type != 'file':
                continue
            
            save_path = os.path.join(subdir, name)
            print(f"  下载: {name} -> {save_path}")
            
            try:
                download_file(token, file_token, save_path)
                print(f"    ✓ 完成")
            except Exception as e:
                print(f"    ✗ 失败: {e}")
    
    print(f"\n下载完成！文件保存在: {DOWNLOAD_DIR}")

if __name__ == "__main__":
    main()
