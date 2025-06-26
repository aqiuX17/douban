# 豆瓣电影爬虫

这是一个用于爬取豆瓣电影信息的Python程序，可以获取电影的详细信息并输出为JSON格式。

## 功能特点

- 爬取豆瓣Top250电影信息
- 获取电影详细信息：标题、评分、导演、演员、简介、封面等
- 输出为JSON格式
- 包含反爬虫措施（随机延迟、User-Agent等）
- 错误处理和重试机制

## 爬取的电影信息

每部电影包含以下信息：
- `title`: 电影标题
- `year`: 上映年份
- `rating`: 豆瓣评分
- `votes`: 评价人数
- `director`: 导演
- `actors`: 演员列表（前5个）
- `genres`: 电影类型
- `release_date`: 上映日期
- `runtime`: 片长
- `summary`: 电影简介
- `poster_url`: 封面图片URL
- `douban_url`: 豆瓣链接
- `crawl_time`: 爬取时间

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 安装依赖包：
```bash
pip install requests beautifulsoup4 lxml
```

2. 运行爬虫程序：
```bash
python douban_movie_crawler.py
```

3. 程序会自动爬取50部电影信息并保存到 `douban_movies.json` 文件中

## 输出文件

程序运行完成后会生成 `douban_movies.json` 文件，包含所有爬取到的电影信息。

## 注意事项

- 程序包含随机延迟以避免被豆瓣反爬虫机制检测
- 建议在网络状况良好的环境下运行
- 爬取速度较慢是正常的，这是为了避免被反爬虫
- 如果遇到网络问题，程序会自动跳过并继续爬取下一部电影

## 示例输出

```json
[
  {
    "title": "肖申克的救赎",
    "year": "1994",
    "rating": "9.7",
    "votes": "2,123,456人评价",
    "director": "弗兰克·德拉邦特",
    "actors": ["蒂姆·罗宾斯", "摩根·弗里曼", "鲍勃·冈顿"],
    "genres": ["剧情", "犯罪"],
    "release_date": "1994-09-10(多伦多电影节)",
    "runtime": "142分钟",
    "summary": "一场谋杀案使银行家安迪（蒂姆·罗宾斯）蒙冤入狱...",
    "poster_url": "https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg",
    "douban_url": "https://movie.douban.com/subject/1292052/",
    "crawl_time": "2024-01-01 12:00:00"
  }
]
```

## 自定义配置

如果需要修改爬取数量，可以在 `main()` 函数中修改 `count` 参数：

```python
movies = crawler.crawl_movies(count=100)  # 爬取100部电影
```

## 免责声明

本程序仅用于学习和研究目的，请遵守豆瓣的使用条款和robots.txt协议。使用本程序产生的任何后果由使用者自行承担。 