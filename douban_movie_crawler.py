#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影爬虫
爬取电影信息包括：标题、评分、导演、演员、简介、封面等
输出为JSON格式
"""

import requests
import json
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from datetime import datetime

class DoubanMovieCrawler:
    def __init__(self):
        self.base_url = "https://movie.douban.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def get_movie_list(self, start=0, count=50):
        """获取电影列表页面"""
        url = f"{self.base_url}/top250?start={start}&filter="
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"获取电影列表失败: {e}")
            return None
    
    def parse_movie_list(self, html):
        """解析电影列表页面，提取电影链接"""
        soup = BeautifulSoup(html, 'html.parser')
        movie_links = []
        
        # 查找电影条目
        movie_items = soup.find_all('div', class_='item')
        
        for item in movie_items:
            try:
                # 获取电影链接
                link_element = item.find('div', class_='hd').find('a')
                movie_url = link_element.get('href')
                movie_title = link_element.find('span', class_='title').text.strip()
                
                movie_links.append({
                    'url': movie_url,
                    'title': movie_title
                })
            except Exception as e:
                print(f"解析电影链接失败: {e}")
                continue
                
        return movie_links
    
    def get_movie_detail(self, movie_url):
        """获取电影详细信息"""
        try:
            # 添加随机延迟，避免被反爬
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(movie_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取电影信息
            movie_info = {}
            
            # 电影标题
            title_element = soup.find('h1')
            if title_element:
                movie_info['title'] = title_element.text.strip()
            
            # 年份
            year_element = soup.find('span', class_='year')
            if year_element:
                movie_info['year'] = year_element.text.strip('()')
            
            # 评分
            rating_element = soup.find('strong', class_='ll rating_num')
            if rating_element:
                movie_info['rating'] = rating_element.text.strip()
            
            # 评价人数
            votes_element = soup.find('a', class_='rating_people')
            if votes_element:
                movie_info['votes'] = votes_element.text.strip()
            
            # 导演
            director_element = soup.find('a', rel='v:directedBy')
            if director_element:
                movie_info['director'] = director_element.text.strip()
            
            # 演员列表
            actors = []
            actor_elements = soup.find_all('a', rel='v:starring')
            for actor in actor_elements[:5]:  # 只取前5个演员
                actors.append(actor.text.strip())
            movie_info['actors'] = actors
            
            # 类型
            genres = []
            genre_elements = soup.find_all('span', property='v:genre')
            for genre in genre_elements:
                genres.append(genre.text.strip())
            movie_info['genres'] = genres
            
            # 上映日期
            release_date_element = soup.find('span', property='v:initialReleaseDate')
            if release_date_element:
                movie_info['release_date'] = release_date_element.text.strip()
            
            # 片长
            runtime_element = soup.find('span', property='v:runtime')
            if runtime_element:
                movie_info['runtime'] = runtime_element.text.strip()
            
            # 简介
            summary_element = soup.find('span', property='v:summary')
            if summary_element:
                movie_info['summary'] = summary_element.text.strip()
            
            # 封面图片
            poster_element = soup.find('img', rel='v:image')
            if poster_element:
                movie_info['poster_url'] = poster_element.get('src')
            
            # 豆瓣链接
            movie_info['douban_url'] = movie_url
            
            # 爬取时间
            movie_info['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return movie_info
            
        except Exception as e:
            print(f"获取电影详情失败 {movie_url}: {e}")
            return None
    
    def crawl_movies(self, count=50):
        """爬取指定数量的电影"""
        all_movies = []
        start = 0
        
        while len(all_movies) < count:
            print(f"正在爬取第 {len(all_movies) + 1} 到 {min(len(all_movies) + 25, count)} 部电影...")
            
            # 获取电影列表
            html = self.get_movie_list(start, 25)
            if not html:
                break
                
            # 解析电影链接
            movie_links = self.parse_movie_list(html)
            if not movie_links:
                break
            
            # 获取每部电影的详细信息
            for movie_link in movie_links:
                if len(all_movies) >= count:
                    break
                    
                print(f"正在爬取: {movie_link['title']}")
                movie_detail = self.get_movie_detail(movie_link['url'])
                
                if movie_detail:
                    all_movies.append(movie_detail)
                    print(f"✓ 成功爬取: {movie_detail['title']}")
                else:
                    print(f"✗ 爬取失败: {movie_link['title']}")
            
            start += 25
            
            # 如果已经爬取足够数量，退出循环
            if len(all_movies) >= count:
                break
        
        return all_movies
    
    def save_to_json(self, movies, filename='douban_movies.json'):
        """保存电影信息到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(movies, f, ensure_ascii=False, indent=2)
            print(f"✓ 成功保存 {len(movies)} 部电影信息到 {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")

def main():
    """主函数"""
    print("豆瓣电影爬虫启动...")
    print("=" * 50)
    
    # 创建爬虫实例
    crawler = DoubanMovieCrawler()
    
    # 爬取50部电影
    movies = crawler.crawl_movies(count=50)
    
    if movies:
        # 保存到JSON文件
        crawler.save_to_json(movies)
        
        # 打印统计信息
        print("\n" + "=" * 50)
        print("爬取完成！统计信息：")
        print(f"成功爬取电影数量: {len(movies)}")
        print(f"平均评分: {sum(float(m.get('rating', 0)) for m in movies if m.get('rating')) / len([m for m in movies if m.get('rating')]):.1f}")
        
        # 显示前5部电影的基本信息
        print("\n前5部电影信息预览：")
        for i, movie in enumerate(movies[:5], 1):
            print(f"{i}. {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")
    else:
        print("没有成功爬取到任何电影信息")

if __name__ == "__main__":
    main() 