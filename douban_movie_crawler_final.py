#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影爬虫 - 最终工作版本
基于成功测试结果的爬虫程序
"""

import requests
import json
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime

class DoubanMovieCrawlerFinal:
    def __init__(self):
        self.base_url = "https://movie.douban.com"
        # 使用与成功测试相同的请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
    def get_movie_list(self, start=0):
        """获取电影列表页面"""
        url = f"{self.base_url}/top250?start={start}&filter="
        try:
            # 添加随机延迟
            time.sleep(random.uniform(2, 4))
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"获取电影列表失败: {e}")
            return None
    
    def parse_movie_list(self, html):
        """解析电影列表页面，提取电影链接"""
        soup = BeautifulSoup(html, 'html.parser')
        movie_links = []
        
        # 查找所有电影链接
        movie_link_elements = soup.find_all('a', href=lambda x: x and '/subject/' in x)
        
        print(f"找到 {len(movie_link_elements)} 个电影链接")
        
        # 去重并提取有效链接
        seen_urls = set()
        for link in movie_link_elements:
            url = link.get('href')
            if url and url not in seen_urls:
                seen_urls.add(url)
                
                # 获取电影标题
                title = link.get_text(strip=True)
                if title and len(title) > 1:  # 只保留有意义的标题
                    movie_links.append({
                        'url': url,
                        'title': title
                    })
                    print(f"解析到电影: {title}")
        
        print(f"成功解析 {len(movie_links)} 个有效电影链接")
        return movie_links
    
    def get_movie_detail(self, movie_url):
        """获取电影详细信息"""
        try:
            # 添加随机延迟
            time.sleep(random.uniform(3, 5))
            
            response = requests.get(movie_url, headers=self.headers, timeout=20)
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
            print(f"\n正在爬取第 {len(all_movies) + 1} 到 {min(len(all_movies) + 25, count)} 部电影...")
            
            # 获取电影列表
            html = self.get_movie_list(start)
            if not html:
                print("无法获取电影列表，程序退出")
                break
                
            # 解析电影链接
            movie_links = self.parse_movie_list(html)
            if not movie_links:
                print("无法解析电影链接，程序退出")
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
                
                # 每爬取5部电影后稍作休息
                if len(all_movies) % 5 == 0 and len(all_movies) > 0:
                    print("休息10秒...")
                    time.sleep(10)
            
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
    print("豆瓣电影爬虫 - 最终工作版本")
    print("=" * 50)
    print("注意：本程序包含反爬虫措施，爬取速度较慢是正常的")
    print("=" * 50)
    
    # 创建爬虫实例
    crawler = DoubanMovieCrawlerFinal()
    
    # 爬取50部电影
    movies = crawler.crawl_movies(count=50)
    
    if movies:
        # 保存到JSON文件
        crawler.save_to_json(movies)
        
        # 打印统计信息
        print("\n" + "=" * 50)
        print("爬取完成！统计信息：")
        print(f"成功爬取电影数量: {len(movies)}")
        
        # 计算平均评分
        ratings = [float(m.get('rating', 0)) for m in movies if m.get('rating') and m.get('rating') != '0']
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            print(f"平均评分: {avg_rating:.1f}")
        
        # 显示前5部电影的基本信息
        print("\n前5部电影信息预览：")
        for i, movie in enumerate(movies[:5], 1):
            print(f"{i}. {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")
    else:
        print("没有成功爬取到任何电影信息")

if __name__ == "__main__":
    main() 