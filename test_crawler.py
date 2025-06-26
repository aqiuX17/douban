#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆瓣电影爬虫
用于验证爬虫程序的基本功能
"""

import requests
from bs4 import BeautifulSoup
import json

def test_douban_connection():
    """测试豆瓣网站连接"""
    print("测试豆瓣网站连接...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get('https://movie.douban.com/top250', headers=headers, timeout=10)
        response.raise_for_status()
        print("✓ 豆瓣网站连接成功")
        return True
    except Exception as e:
        print(f"✗ 豆瓣网站连接失败: {e}")
        return False

def test_parse_movie_list():
    """测试解析电影列表"""
    print("\n测试解析电影列表...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get('https://movie.douban.com/top250', headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        movie_items = soup.find_all('div', class_='item')
        
        if movie_items:
            print(f"✓ 成功找到 {len(movie_items)} 部电影")
            
            # 显示前3部电影信息
            for i, item in enumerate(movie_items[:3], 1):
                try:
                    title_element = item.find('span', class_='title')
                    if title_element:
                        title = title_element.text.strip()
                        print(f"  {i}. {title}")
                except:
                    continue
            return True
        else:
            print("✗ 未找到电影条目")
            return False
            
    except Exception as e:
        print(f"✗ 解析电影列表失败: {e}")
        return False

def test_single_movie():
    """测试单个电影详情页面"""
    print("\n测试单个电影详情页面...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    # 测试肖申克的救赎页面
    test_url = 'https://movie.douban.com/subject/1292052/'
    
    try:
        response = requests.get(test_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取基本信息
        title_element = soup.find('h1')
        rating_element = soup.find('strong', class_='ll rating_num')
        
        if title_element and rating_element:
            title = title_element.text.strip()
            rating = rating_element.text.strip()
            print(f"✓ 成功获取电影信息: {title} - 评分: {rating}")
            return True
        else:
            print("✗ 无法获取电影基本信息")
            return False
            
    except Exception as e:
        print(f"✗ 获取电影详情失败: {e}")
        return False

def test_json_output():
    """测试JSON输出格式"""
    print("\n测试JSON输出格式...")
    
    # 创建测试数据
    test_movie = {
        "title": "肖申克的救赎",
        "year": "1994",
        "rating": "9.7",
        "director": "弗兰克·德拉邦特",
        "actors": ["蒂姆·罗宾斯", "摩根·弗里曼"],
        "genres": ["剧情", "犯罪"],
        "summary": "一场谋杀案使银行家安迪蒙冤入狱...",
        "douban_url": "https://movie.douban.com/subject/1292052/",
        "crawl_time": "2024-01-01 12:00:00"
    }
    
    try:
        # 保存测试数据
        with open('test_output.json', 'w', encoding='utf-8') as f:
            json.dump([test_movie], f, ensure_ascii=False, indent=2)
        
        # 读取并验证
        with open('test_output.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if data and len(data) > 0:
            print("✓ JSON输出格式测试成功")
            print(f"  电影标题: {data[0]['title']}")
            print(f"  评分: {data[0]['rating']}")
            return True
        else:
            print("✗ JSON输出格式测试失败")
            return False
            
    except Exception as e:
        print(f"✗ JSON输出测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("豆瓣电影爬虫测试程序")
    print("=" * 50)
    
    tests = [
        ("网站连接测试", test_douban_connection),
        ("电影列表解析测试", test_parse_movie_list),
        ("单个电影详情测试", test_single_movie),
        ("JSON输出格式测试", test_json_output)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✓ 所有测试通过！可以运行爬虫程序")
    else:
        print("✗ 部分测试失败，请检查网络连接或豆瓣网站状态")
    
    # 清理测试文件
    try:
        import os
        if os.path.exists('test_output.json'):
            os.remove('test_output.json')
    except:
        pass

if __name__ == "__main__":
    main() 