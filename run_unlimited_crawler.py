#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影无上限爬虫启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from douban_movie_crawler_unlimited import DoubanMovieCrawlerUnlimited

def main():
    """主函数"""
    print("豆瓣电影无上限爬虫启动器")
    print("=" * 50)
    
    crawler = DoubanMovieCrawlerUnlimited()
    
    # 加载已爬取的URL
    crawler.load_crawled_urls()
    
    print(f"当前已爬取 {len(crawler.crawled_urls)} 部电影")
    
    # 选择爬取模式
    print("\n请选择爬取模式：")
    print("1. 爬取Top250电影")
    print("2. 爬取指定标签电影")
    print("3. 爬取所有电影（无上限）")
    print("4. 自定义爬取")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == '1':
        movies = crawler.crawl_from_top250()
    elif choice == '2':
        tag = input("请输入标签名称 (默认'热门'): ").strip() or "热门"
        max_pages = int(input("请输入最大页数 (默认30): ") or "30")
        movies = crawler.crawl_from_tag(tag, max_pages)
    elif choice == '3':
        max_tags = input("请输入最大标签数量 (直接回车爬取所有40+标签): ").strip()
        max_tags = int(max_tags) if max_tags else None
        movies = crawler.crawl_all_movies(max_tags)
    elif choice == '4':
        print("\n自定义爬取选项：")
        print("1. 从Top250爬取")
        print("2. 从标签爬取")
        sub_choice = input("请选择 (1-2): ").strip()
        
        if sub_choice == '1':
            movies = crawler.crawl_from_top250()
        elif sub_choice == '2':
            tag = input("请输入标签名称: ").strip()
            max_pages = int(input("请输入最大页数: ") or "30")
            movies = crawler.crawl_from_tag(tag, max_pages)
        else:
            print("无效选择")
            return
    else:
        print("无效选择")
        return
    
    if movies:
        # 去重
        unique_movies = []
        seen_urls = set()
        for movie in movies:
            if movie.get('douban_url') not in seen_urls:
                unique_movies.append(movie)
                seen_urls.add(movie.get('douban_url'))
        
        # 保存结果
        crawler.save_to_json(unique_movies)
        crawler.save_crawled_urls()
        
        print("\n" + "=" * 60)
        print("爬取完成！统计信息：")
        print(f"总爬取电影数量: {len(movies)}")
        print(f"去重后电影数量: {len(unique_movies)}")
        
        ratings = [float(m.get('rating', 0)) for m in unique_movies if m.get('rating') and m.get('rating') != '0']
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            print(f"平均评分: {avg_rating:.1f}")
            print(f"最高评分: {max(ratings):.1f}")
            print(f"最低评分: {min(ratings):.1f}")
        
        print(f"\n前20部电影信息预览：")
        for i, movie in enumerate(unique_movies[:20], 1):
            print(f"{i:2d}. {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")
    else:
        print("没有成功爬取到任何电影信息")

if __name__ == "__main__":
    main() 