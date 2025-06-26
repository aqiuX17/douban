#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试解析逻辑
"""

import requests
from bs4 import BeautifulSoup

def test_parsing():
    """测试解析逻辑"""
    print("测试解析逻辑...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get('https://movie.douban.com/top250', headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有电影链接
        movie_link_elements = soup.find_all('a', href=lambda x: x and '/subject/' in x)
        
        print(f"找到 {len(movie_link_elements)} 个电影链接")
        
        # 测试解析逻辑
        seen_urls = set()
        valid_links = []
        
        for i, link in enumerate(movie_link_elements[:10], 1):  # 只测试前10个
            url = link.get('href')
            title = link.get_text(strip=True)
            
            print(f"\n链接 {i}:")
            print(f"  URL: {url}")
            print(f"  标题: '{title}'")
            print(f"  标题长度: {len(title)}")
            
            if url and url not in seen_urls:
                seen_urls.add(url)
                
                if title and len(title) > 1:
                    valid_links.append({
                        'url': url,
                        'title': title
                    })
                    print(f"  ✓ 有效链接")
                else:
                    print(f"  ✗ 标题无效")
            else:
                print(f"  ✗ 重复链接或无效URL")
        
        print(f"\n有效链接数量: {len(valid_links)}")
        
        # 显示有效链接
        for i, link in enumerate(valid_links, 1):
            print(f"{i}. {link['title']} - {link['url']}")
        
        return len(valid_links) > 0
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False

def main():
    """主函数"""
    print("解析逻辑测试")
    print("=" * 50)
    
    success = test_parsing()
    
    if success:
        print("\n✓ 解析逻辑正常")
    else:
        print("\n✗ 解析逻辑有问题")

if __name__ == "__main__":
    main() 