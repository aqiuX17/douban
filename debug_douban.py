#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣页面调试工具
用于查看豆瓣页面的实际HTML结构
"""

import requests
from bs4 import BeautifulSoup
import json

def debug_movie_list():
    """调试电影列表页面"""
    print("调试豆瓣Top250页面...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get('https://movie.douban.com/top250', headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有可能的电影容器
        print("\n查找电影容器...")
        
        # 方法1: 查找 class='item' 的div
        items = soup.find_all('div', class_='item')
        print(f"找到 {len(items)} 个 class='item' 的div")
        
        # 方法2: 查找包含电影链接的元素
        movie_links = soup.find_all('a', href=lambda x: x and '/subject/' in x)
        print(f"找到 {len(movie_links)} 个电影链接")
        
        # 方法3: 查找包含评分的元素
        ratings = soup.find_all('span', class_='rating_num')
        print(f"找到 {len(ratings)} 个评分元素")
        
        # 显示前3个电影的信息
        print("\n前3个电影信息:")
        for i, item in enumerate(items[:3], 1):
            print(f"\n电影 {i}:")
            
            # 查找标题
            title_element = item.find('span', class_='title')
            if title_element:
                print(f"  标题: {title_element.text.strip()}")
            
            # 查找链接
            link_element = item.find('a')
            if link_element:
                print(f"  链接: {link_element.get('href')}")
            
            # 查找评分
            rating_element = item.find('span', class_='rating_num')
            if rating_element:
                print(f"  评分: {rating_element.text.strip()}")
        
        # 保存HTML到文件以便查看
        with open('douban_debug.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\nHTML已保存到 douban_debug.html")
        
        return len(items) > 0
        
    except Exception as e:
        print(f"调试失败: {e}")
        return False

def debug_movie_detail():
    """调试电影详情页面"""
    print("\n调试电影详情页面...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    test_url = 'https://movie.douban.com/subject/1292052/'
    
    try:
        response = requests.get(test_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("查找电影信息元素...")
        
        # 查找标题
        title_element = soup.find('h1')
        if title_element:
            print(f"✓ 找到标题: {title_element.text.strip()}")
        else:
            print("✗ 未找到标题")
        
        # 查找评分
        rating_element = soup.find('strong', class_='ll rating_num')
        if rating_element:
            print(f"✓ 找到评分: {rating_element.text.strip()}")
        else:
            print("✗ 未找到评分")
        
        # 查找导演
        director_element = soup.find('a', rel='v:directedBy')
        if director_element:
            print(f"✓ 找到导演: {director_element.text.strip()}")
        else:
            print("✗ 未找到导演")
        
        # 查找演员
        actor_elements = soup.find_all('a', rel='v:starring')
        if actor_elements:
            print(f"✓ 找到 {len(actor_elements)} 个演员")
            for i, actor in enumerate(actor_elements[:3], 1):
                print(f"  演员{i}: {actor.text.strip()}")
        else:
            print("✗ 未找到演员")
        
        # 保存HTML到文件
        with open('douban_detail_debug.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"详情页HTML已保存到 douban_detail_debug.html")
        
        return True
        
    except Exception as e:
        print(f"调试详情页失败: {e}")
        return False

def main():
    """主函数"""
    print("豆瓣页面调试工具")
    print("=" * 50)
    
    # 调试电影列表
    list_ok = debug_movie_list()
    
    # 调试电影详情
    detail_ok = debug_movie_detail()
    
    print("\n" + "=" * 50)
    print("调试结果:")
    print(f"电影列表: {'✓' if list_ok else '✗'}")
    print(f"电影详情: {'✓' if detail_ok else '✗'}")
    
    if list_ok and detail_ok:
        print("\n✓ 页面结构正常，可以修复爬虫程序")
    else:
        print("\n✗ 页面结构有问题，需要调整解析逻辑")

if __name__ == "__main__":
    main() 