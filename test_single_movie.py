#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单个电影爬取
"""

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

def test_single_movie():
    """测试爬取单个电影"""
    print("测试爬取单个电影...")
    
    # 测试电影URL
    test_url = 'https://movie.douban.com/subject/1292052/'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        print(f"正在请求: {test_url}")
        response = requests.get(test_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容长度: {len(response.text)}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取电影信息
        movie_info = {}
        
        # 电影标题
        title_element = soup.find('h1')
        if title_element:
            movie_info['title'] = title_element.text.strip()
            print(f"✓ 标题: {movie_info['title']}")
        
        # 年份
        year_element = soup.find('span', class_='year')
        if year_element:
            movie_info['year'] = year_element.text.strip('()')
            print(f"✓ 年份: {movie_info['year']}")
        
        # 评分
        rating_element = soup.find('strong', class_='ll rating_num')
        if rating_element:
            movie_info['rating'] = rating_element.text.strip()
            print(f"✓ 评分: {movie_info['rating']}")
        
        # 导演
        director_element = soup.find('a', rel='v:directedBy')
        if director_element:
            movie_info['director'] = director_element.text.strip()
            print(f"✓ 导演: {movie_info['director']}")
        
        # 演员列表
        actors = []
        actor_elements = soup.find_all('a', rel='v:starring')
        for actor in actor_elements[:5]:
            actors.append(actor.text.strip())
        movie_info['actors'] = actors
        print(f"✓ 演员: {', '.join(actors)}")
        
        # 类型
        genres = []
        genre_elements = soup.find_all('span', property='v:genre')
        for genre in genre_elements:
            genres.append(genre.text.strip())
        movie_info['genres'] = genres
        print(f"✓ 类型: {', '.join(genres)}")
        
        # 简介
        summary_element = soup.find('span', property='v:summary')
        if summary_element:
            movie_info['summary'] = summary_element.text.strip()
            print(f"✓ 简介: {movie_info['summary'][:50]}...")
        
        # 豆瓣链接
        movie_info['douban_url'] = test_url
        movie_info['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 保存到JSON文件
        with open('test_movie.json', 'w', encoding='utf-8') as f:
            json.dump([movie_info], f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 成功爬取电影信息，已保存到 test_movie.json")
        return True
        
    except Exception as e:
        print(f"✗ 爬取失败: {e}")
        return False

def main():
    """主函数"""
    print("单个电影爬取测试")
    print("=" * 50)
    
    success = test_single_movie()
    
    if success:
        print("\n✓ 测试成功！可以运行完整爬虫程序")
    else:
        print("\n✗ 测试失败，需要进一步调试")

if __name__ == "__main__":
    main() 