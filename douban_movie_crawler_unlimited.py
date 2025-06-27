#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影爬虫 - 无上限版本
专门用于爬取大量电影信息，无数量限制
"""

import requests
import json
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime
import os

class DoubanMovieCrawlerUnlimited:
    def __init__(self):
        self.base_url = "https://movie.douban.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        # 已爬取的电影URL集合，避免重复
        self.crawled_urls = set()
        
        # 热门标签列表
        self.popular_tags = [
            '热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', 
            '华语', '欧美', '韩国', '日本', '动作', '喜剧', '爱情', 
            '科幻', '悬疑', '恐怖', '动画', '纪录片', '短片', '情色',
            '音乐', '歌舞', '家庭', '儿童', '传记', '历史', '战争',
            '西部', '奇幻', '冒险', '灾难', '武侠', '古装', '运动',
            '黑色电影', '犯罪', '剧情', '惊悚', '同性', '女性', '青春'
        ]
        
    def get_movie_list_from_tag(self, tag, start=0):
        """通过标签获取电影列表"""
        tag_url = f"https://movie.douban.com/j/search_subjects?type=movie&tag={tag}&sort=recommend&page_limit=20&page_start={start}"
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(tag_url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取标签 '{tag}' 电影失败: {e}")
            return None
    
    def get_movie_list_from_top250(self, start=0):
        """从Top250获取电影列表"""
        url = f"{self.base_url}/top250?start={start}&filter="
        try:
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"获取Top250电影列表失败: {e}")
            return None
    
    def parse_top250_movies(self, html):
        """解析Top250电影列表"""
        soup = BeautifulSoup(html, 'html.parser')
        movie_links = []
        
        movie_link_elements = soup.find_all('a', href=lambda x: x and '/subject/' in x)
        
        for link in movie_link_elements:
            url = link.get('href')
            title = link.get_text(strip=True)
            
            if url and title and len(title) > 1:
                movie_links.append({
                    'url': url,
                    'title': title
                })
        
        return movie_links
    
    def parse_tag_movies(self, tag_data):
        """解析标签搜索结果"""
        movie_links = []
        if tag_data and 'subjects' in tag_data:
            for movie in tag_data['subjects']:
                movie_links.append({
                    'url': movie.get('url', ''),
                    'title': movie.get('title', ''),
                    'rate': movie.get('rate', ''),
                    'cover': movie.get('cover', '')
                })
        return movie_links
    
    def get_movie_detail(self, movie_url):
        """获取电影详细信息"""
        # 检查是否已经爬取过
        if movie_url in self.crawled_urls:
            return None
            
        try:
            time.sleep(random.uniform(2, 4))
            
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
            for actor in actor_elements[:5]:
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
            movie_info['crawl_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 标记为已爬取
            self.crawled_urls.add(movie_url)
            
            return movie_info
            
        except Exception as e:
            print(f"获取电影详情失败 {movie_url}: {e}")
            return None
    
    def crawl_from_tag(self, tag, max_pages=50):
        """从指定标签爬取电影"""
        all_movies = []
        page = 0
        
        print(f"开始从标签 '{tag}' 爬取电影...")
        
        while page < max_pages:
            print(f"正在爬取第 {page + 1} 页...")
            
            tag_data = self.get_movie_list_from_tag(tag, page * 20)
            if not tag_data or not tag_data.get('subjects'):
                print(f"标签 '{tag}' 第 {page + 1} 页无数据，停止爬取")
                break
                
            movie_links = self.parse_tag_movies(tag_data)
            if not movie_links:
                print(f"标签 '{tag}' 第 {page + 1} 页解析失败")
                break
            
            page_movies = 0
            for movie_link in movie_links:
                print(f"正在爬取: {movie_link['title']}")
                movie_detail = self.get_movie_detail(movie_link['url'])
                
                if movie_detail:
                    all_movies.append(movie_detail)
                    page_movies += 1
                    print(f"✓ 成功爬取: {movie_detail['title']}")
                
                # 每爬取5部电影休息一下
                if page_movies % 5 == 0 and page_movies > 0:
                    print("休息5秒...")
                    time.sleep(5)
            
            page += 1
            
            # 每页爬取完成后休息
            print(f"第 {page} 页完成，休息10秒...")
            time.sleep(10)
        
        print(f"标签 '{tag}' 爬取完成，共 {len(all_movies)} 部电影")
        return all_movies
    
    def crawl_from_top250(self):
        """从Top250爬取电影"""
        all_movies = []
        start = 0
        
        print("开始从Top250爬取电影...")
        
        while start < 250:
            print(f"正在爬取第 {start + 1} 到 {min(start + 25, 250)} 部电影...")
            
            html = self.get_movie_list_from_top250(start)
            if not html:
                print("无法获取Top250电影列表，程序退出")
                break
                
            movie_links = self.parse_top250_movies(html)
            if not movie_links:
                print("无法解析Top250电影链接，程序退出")
                break
            
            for movie_link in movie_links:
                print(f"正在爬取: {movie_link['title']}")
                movie_detail = self.get_movie_detail(movie_link['url'])
                
                if movie_detail:
                    all_movies.append(movie_detail)
                    print(f"✓ 成功爬取: {movie_detail['title']}")
                
                # 每爬取5部电影休息一下
                if len(all_movies) % 5 == 0 and len(all_movies) > 0:
                    print("休息5秒...")
                    time.sleep(5)
            
            start += 25
            
            # 每页爬取完成后休息
            print("休息10秒...")
            time.sleep(10)
        
        print(f"Top250爬取完成，共 {len(all_movies)} 部电影")
        return all_movies
    
    def crawl_all_movies(self, max_tags=None):
        """爬取所有可能的电影"""
        all_movies = []
        
        # 先爬取Top250
        print("=" * 60)
        print("第一阶段：爬取Top250电影")
        print("=" * 60)
        top250_movies = self.crawl_from_top250()
        all_movies.extend(top250_movies)
        
        # 从热门标签爬取
        print("\n" + "=" * 60)
        print("第二阶段：从热门标签爬取电影")
        print("=" * 60)
        
        tags_to_crawl = self.popular_tags[:max_tags] if max_tags else self.popular_tags
        
        for i, tag in enumerate(tags_to_crawl, 1):
            print(f"\n进度: {i}/{len(tags_to_crawl)} - 标签: {tag}")
            tag_movies = self.crawl_from_tag(tag, max_pages=30)
            all_movies.extend(tag_movies)
            
            # 每爬取5个标签休息一下
            if i % 5 == 0:
                print(f"已爬取 {i} 个标签，休息30秒...")
                time.sleep(30)
        
        return all_movies
    
    def save_to_json(self, movies, filename='douban_movies_unlimited.json'):
        """保存电影信息到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(movies, f, ensure_ascii=False, indent=2)
            print(f"✓ 成功保存 {len(movies)} 部电影信息到 {filename}")
        except Exception as e:
            print(f"保存文件失败: {e}")
    
    def load_crawled_urls(self, filename='crawled_urls_unlimited.json'):
        """加载已爬取的URL列表"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.crawled_urls = set(json.load(f))
                print(f"加载了 {len(self.crawled_urls)} 个已爬取的URL")
            except Exception as e:
                print(f"加载已爬取URL失败: {e}")
    
    def save_crawled_urls(self, filename='crawled_urls_unlimited.json'):
        """保存已爬取的URL列表"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(list(self.crawled_urls), f, ensure_ascii=False, indent=2)
            print(f"保存了 {len(self.crawled_urls)} 个已爬取的URL")
        except Exception as e:
            print(f"保存已爬取URL失败: {e}")

def main():
    """主函数"""
    print("豆瓣电影爬虫 - 无上限版本")
    print("=" * 60)
    print("本程序将爬取大量电影信息，包括：")
    print("1. Top250电影")
    print("2. 40+个热门标签的电影")
    print("3. 预计可爬取数千部电影")
    print("=" * 60)
    
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
        
        # 统计年份分布
        years = [m.get('year') for m in unique_movies if m.get('year')]
        if years:
            year_counts = {}
            for year in years:
                year_counts[year] = year_counts.get(year, 0) + 1
            print(f"\n年份分布 (前10):")
            sorted_years = sorted(year_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for year, count in sorted_years:
                print(f"  {year}: {count}部")
        
        # 统计类型分布
        all_genres = []
        for movie in unique_movies:
            if movie.get('genres'):
                all_genres.extend(movie['genres'])
        
        if all_genres:
            genre_counts = {}
            for genre in all_genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            print(f"\n类型分布 (前10):")
            sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            for genre, count in sorted_genres:
                print(f"  {genre}: {count}部")
        
        print(f"\n前20部电影信息预览：")
        for i, movie in enumerate(unique_movies[:20], 1):
            print(f"{i:2d}. {movie.get('title', 'N/A')} ({movie.get('year', 'N/A')}) - 评分: {movie.get('rating', 'N/A')}")
    else:
        print("没有成功爬取到任何电影信息")

if __name__ == "__main__":
    main() 