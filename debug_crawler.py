#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬虫调试工具
详细调试爬虫程序的问题
"""

import requests
from bs4 import BeautifulSoup
import time

def debug_crawler_issue():
    """调试爬虫问题"""
    print("调试爬虫问题...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    url = 'https://movie.douban.com/top250'
    
    try:
        print(f"正在请求: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容长度: {len(response.text)}")
        
        # 保存原始HTML
        with open('debug_raw.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("原始HTML已保存到 debug_raw.html")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 检查页面标题
        title = soup.find('title')
        if title:
            print(f"页面标题: {title.text.strip()}")
        
        # 查找所有div元素
        all_divs = soup.find_all('div')
        print(f"页面中共有 {len(all_divs)} 个div元素")
        
        # 查找class='item'的div
        items = soup.find_all('div', class_='item')
        print(f"找到 {len(items)} 个 class='item' 的div")
        
        # 查找所有class属性包含'item'的div
        items_with_item = soup.find_all('div', class_=lambda x: x and 'item' in x)
        print(f"找到 {len(items_with_item)} 个class包含'item'的div")
        
        # 查找所有包含电影链接的a标签
        movie_links = soup.find_all('a', href=lambda x: x and '/subject/' in x)
        print(f"找到 {len(movie_links)} 个电影链接")
        
        # 显示前几个电影链接
        for i, link in enumerate(movie_links[:5], 1):
            print(f"电影链接{i}: {link.get('href')}")
        
        # 查找所有span元素
        all_spans = soup.find_all('span')
        print(f"页面中共有 {len(all_spans)} 个span元素")
        
        # 查找class='title'的span
        title_spans = soup.find_all('span', class_='title')
        print(f"找到 {len(title_spans)} 个 class='title' 的span")
        
        # 显示前几个标题
        for i, span in enumerate(title_spans[:5], 1):
            print(f"标题{i}: {span.text.strip()}")
        
        # 查找所有class属性包含'title'的span
        title_spans_any = soup.find_all('span', class_=lambda x: x and 'title' in x)
        print(f"找到 {len(title_spans_any)} 个class包含'title'的span")
        
        # 检查是否有反爬虫检测
        if '验证码' in response.text or 'captcha' in response.text.lower():
            print("⚠️ 检测到验证码页面，可能被反爬虫机制拦截")
        
        if 'robot' in response.text.lower() or 'bot' in response.text.lower():
            print("⚠️ 检测到机器人检测页面")
        
        # 检查页面是否正常
        if len(items) == 0 and len(movie_links) == 0:
            print("❌ 页面结构异常，可能被反爬虫机制拦截")
            return False
        else:
            print("✅ 页面结构正常")
            return True
            
    except Exception as e:
        print(f"调试失败: {e}")
        return False

def test_simple_parsing():
    """测试简单的解析方法"""
    print("\n测试简单解析方法...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get('https://movie.douban.com/top250', headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 方法1: 直接查找所有电影链接
        movie_links = soup.find_all('a', href=lambda x: x and '/subject/' in x)
        print(f"方法1 - 直接查找电影链接: 找到 {len(movie_links)} 个")
        
        # 方法2: 查找包含评分的元素
        ratings = soup.find_all('span', class_='rating_num')
        print(f"方法2 - 查找评分: 找到 {len(ratings)} 个")
        
        # 方法3: 查找包含标题的元素
        titles = soup.find_all('span', class_='title')
        print(f"方法3 - 查找标题: 找到 {len(titles)} 个")
        
        # 方法4: 查找所有可能的电影容器
        containers = soup.find_all('div', class_=lambda x: x and ('item' in x or 'movie' in x))
        print(f"方法4 - 查找电影容器: 找到 {len(containers)} 个")
        
        # 显示前3个电影的信息
        print("\n前3个电影信息:")
        for i in range(min(3, len(movie_links))):
            link = movie_links[i]
            href = link.get('href', '')
            text = link.get_text(strip=True)
            print(f"  {i+1}. {text} - {href}")
        
        return len(movie_links) > 0
        
    except Exception as e:
        print(f"简单解析测试失败: {e}")
        return False

def main():
    """主函数"""
    print("爬虫调试工具")
    print("=" * 50)
    
    # 调试爬虫问题
    issue_ok = debug_crawler_issue()
    
    # 测试简单解析
    simple_ok = test_simple_parsing()
    
    print("\n" + "=" * 50)
    print("调试结果:")
    print(f"页面结构: {'✓' if issue_ok else '✗'}")
    print(f"简单解析: {'✓' if simple_ok else '✗'}")
    
    if issue_ok and simple_ok:
        print("\n✓ 页面正常，可以修复爬虫程序")
    else:
        print("\n✗ 页面有问题，可能需要调整请求方式")

if __name__ == "__main__":
    main() 