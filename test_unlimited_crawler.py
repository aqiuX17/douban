#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试无上限爬虫的基本功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from douban_movie_crawler_unlimited import DoubanMovieCrawlerUnlimited

def test_basic_functionality():
    """测试基本功能"""
    print("测试豆瓣电影无上限爬虫基本功能")
    print("=" * 50)
    
    crawler = DoubanMovieCrawlerUnlimited()
    
    # 测试1: 获取Top250电影列表
    print("\n1. 测试获取Top250电影列表...")
    html = crawler.get_movie_list_from_top250(0)
    if html:
        movie_links = crawler.parse_top250_movies(html)
        print(f"✓ 成功获取 {len(movie_links)} 部Top250电影链接")
        if movie_links:
            print(f"   示例: {movie_links[0]['title']}")
    else:
        print("✗ 获取Top250电影列表失败")
        return False
    
    # 测试2: 获取标签电影列表
    print("\n2. 测试获取标签电影列表...")
    tag_data = crawler.get_movie_list_from_tag('热门', 0)
    if tag_data:
        movie_links = crawler.parse_tag_movies(tag_data)
        print(f"✓ 成功获取 {len(movie_links)} 部热门标签电影")
        if movie_links:
            print(f"   示例: {movie_links[0]['title']}")
    else:
        print("✗ 获取标签电影列表失败")
        return False
    
    # 测试3: 爬取单部电影详情
    print("\n3. 测试爬取单部电影详情...")
    if movie_links:
        test_url = movie_links[0]['url']
        print(f"   测试电影: {movie_links[0]['title']}")
        movie_detail = crawler.get_movie_detail(test_url)
        if movie_detail:
            print(f"✓ 成功爬取电影详情")
            print(f"   标题: {movie_detail.get('title', 'N/A')}")
            print(f"   年份: {movie_detail.get('year', 'N/A')}")
            print(f"   评分: {movie_detail.get('rating', 'N/A')}")
            print(f"   导演: {movie_detail.get('director', 'N/A')}")
        else:
            print("✗ 爬取电影详情失败")
            return False
    
    # 测试4: 测试爬取少量电影
    print("\n4. 测试爬取少量电影...")
    test_movies = crawler.crawl_from_tag('热门', max_pages=1)
    if test_movies:
        print(f"✓ 成功爬取 {len(test_movies)} 部测试电影")
        
        # 保存测试结果
        crawler.save_to_json(test_movies, 'test_unlimited_movies.json')
        print("✓ 测试结果已保存到 test_unlimited_movies.json")
        
        # 显示统计信息
        ratings = [float(m.get('rating', 0)) for m in test_movies if m.get('rating') and m.get('rating') != '0']
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            print(f"   平均评分: {avg_rating:.1f}")
        
        print("\n前5部测试电影:")
        for i, movie in enumerate(test_movies[:5], 1):
            print(f"   {i}. {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")
    else:
        print("✗ 测试爬取失败")
        return False
    
    print("\n" + "=" * 50)
    print("✓ 所有测试通过！程序可以正常使用")
    print("=" * 50)
    return True

def test_save_and_load():
    """测试保存和加载功能"""
    print("\n测试保存和加载功能...")
    
    crawler = DoubanMovieCrawlerUnlimited()
    
    # 添加一些测试URL
    test_urls = [
        "https://movie.douban.com/subject/1292052/",
        "https://movie.douban.com/subject/1291546/",
        "https://movie.douban.com/subject/1292720/"
    ]
    
    crawler.crawled_urls.update(test_urls)
    
    # 保存URL列表
    crawler.save_crawled_urls('test_crawled_urls.json')
    print("✓ 已保存测试URL列表")
    
    # 创建新的爬虫实例并加载URL列表
    new_crawler = DoubanMovieCrawlerUnlimited()
    new_crawler.load_crawled_urls('test_crawled_urls.json')
    
    if len(new_crawler.crawled_urls) == len(test_urls):
        print("✓ URL列表加载成功")
        return True
    else:
        print("✗ URL列表加载失败")
        return False

def main():
    """主测试函数"""
    print("豆瓣电影无上限爬虫测试程序")
    print("=" * 60)
    
    # 测试基本功能
    if not test_basic_functionality():
        print("\n✗ 基本功能测试失败，程序可能存在问题")
        return
    
    # 测试保存和加载功能
    if not test_save_and_load():
        print("\n✗ 保存和加载功能测试失败")
        return
    
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！程序可以正常使用")
    print("=" * 60)
    print("\n现在可以运行以下命令开始爬取：")
    print("1. python run_unlimited_crawler.py")
    print("2. 或者双击 run_unlimited.bat")
    print("\n建议先选择模式2（标签模式）进行小规模测试")

if __name__ == "__main__":
    main() 