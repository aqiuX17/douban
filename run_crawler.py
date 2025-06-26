#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆瓣电影爬虫运行脚本
提供用户友好的界面来选择运行不同的程序
"""

import os
import sys
import subprocess

def check_dependencies():
    """检查依赖包是否已安装"""
    print("检查依赖包...")
    
    required_packages = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('lxml', 'lxml')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {package_name} 已安装")
        except ImportError:
            print(f"✗ {package_name} 未安装")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n缺少 {len(missing_packages)} 个依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        print("或者:")
        print("pip install requests beautifulsoup4 lxml")
        return False
    
    print("✓ 所有依赖包已安装")
    return True

def run_test():
    """运行测试程序"""
    print("运行测试程序...")
    try:
        result = subprocess.run([sys.executable, 'test_crawler.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        print(result.stdout)
        if result.stderr:
            print("错误信息:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"运行测试程序失败: {e}")
        return False

def run_crawler(version='success'):
    """运行爬虫程序"""
    if version == 'success':
        script = 'douban_movie_crawler_success.py'
        version_name = '成功版'
    elif version == 'final':
        script = 'douban_movie_crawler_final.py'
        version_name = '最终工作版'
    elif version == 'fixed':
        script = 'douban_movie_crawler_fixed.py'
        version_name = '修复版'
    elif version == 'simple':
        script = 'douban_movie_crawler_simple.py'
        version_name = '简化版'
    else:
        script = 'douban_movie_crawler.py'
        version_name = '完整版'
    
    print(f"运行{version_name}爬虫程序...")
    print("注意：爬取过程可能需要较长时间，请耐心等待")
    print("按 Ctrl+C 可以随时停止程序")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, script])
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"运行爬虫程序失败: {e}")

def show_menu():
    """显示菜单"""
    print("豆瓣电影爬虫程序")
    print("=" * 50)
    print("1. 运行测试程序")
    print("2. 运行成功版爬虫 (推荐)")
    print("3. 运行最终工作版爬虫")
    print("4. 运行修复版爬虫")
    print("5. 运行简化版爬虫")
    print("6. 运行完整版爬虫")
    print("7. 查看输出文件")
    print("8. 退出")
    print("=" * 50)

def show_output_files():
    """显示输出文件信息"""
    print("输出文件信息:")
    print("-" * 30)
    
    output_files = ['douban_movies.json', 'test_movie.json']
    
    for filename in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✓ {filename} ({size} 字节)")
            
            # 如果是JSON文件，显示基本信息
            if filename.endswith('.json'):
                try:
                    import json
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    print(f"  包含 {len(data)} 部电影信息")
                    
                    if data:
                        print("  前3部电影:")
                        for i, movie in enumerate(data[:3], 1):
                            title = movie.get('title', 'N/A')
                            rating = movie.get('rating', 'N/A')
                            print(f"    {i}. {title} - 评分: {rating}")
                except Exception as e:
                    print(f"  读取文件失败: {e}")
        else:
            print(f"✗ {filename} (文件不存在)")

def main():
    """主函数"""
    print("欢迎使用豆瓣电影爬虫！")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("请选择操作 (1-8): ").strip()
            
            if choice == '1':
                run_test()
            elif choice == '2':
                run_crawler('success')
            elif choice == '3':
                run_crawler('final')
            elif choice == '4':
                run_crawler('fixed')
            elif choice == '5':
                run_crawler('simple')
            elif choice == '6':
                run_crawler('full')
            elif choice == '7':
                show_output_files()
            elif choice == '8':
                print("感谢使用！")
                break
            else:
                print("无效选择，请输入 1-8")
                
        except KeyboardInterrupt:
            print("\n程序退出")
            break
        except Exception as e:
            print(f"发生错误: {e}")
        
        input("\n按回车键继续...")

if __name__ == "__main__":
    main() 