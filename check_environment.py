#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境诊断脚本
用于检查Python环境和依赖包状态
"""

import sys
import subprocess
import os

def check_python_version():
    """检查Python版本"""
    print("=" * 50)
    print("Python环境检查")
    print("=" * 50)
    
    version = sys.version_info
    print(f"Python版本: {version.major}.{version.minor}.{version.micro}")
    print(f"Python路径: {sys.executable}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✓ Python版本符合要求 (3.7+)")
        return True
    else:
        print("✗ Python版本过低，需要3.7+")
        return False

def check_pip():
    """检查pip"""
    print("\n" + "=" * 50)
    print("pip检查")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ pip可用: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ pip不可用: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ 检查pip失败: {e}")
        return False

def check_package(package_name, import_name=None):
    """检查单个包"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ {package_name} 已安装")
        return True
    except ImportError:
        print(f"✗ {package_name} 未安装")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n" + "=" * 50)
    print("依赖包检查")
    print("=" * 50)
    
    packages = [
        ('requests', 'requests'),
        ('beautifulsoup4', 'bs4'),
        ('lxml', 'lxml')
    ]
    
    missing = []
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing.append(package_name)
    
    return missing

def install_packages(packages):
    """安装包"""
    print("\n" + "=" * 50)
    print("安装依赖包")
    print("=" * 50)
    
    for package in packages:
        print(f"正在安装 {package}...")
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"✓ {package} 安装成功")
            else:
                print(f"✗ {package} 安装失败: {result.stderr}")
        except Exception as e:
            print(f"✗ {package} 安装异常: {e}")

def check_pip_list():
    """显示已安装的包"""
    print("\n" + "=" * 50)
    print("已安装的包")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # 过滤显示相关包
            lines = result.stdout.split('\n')
            for line in lines:
                if any(pkg in line.lower() for pkg in ['requests', 'beautifulsoup4', 'lxml', 'bs4']):
                    print(line)
        else:
            print("无法获取包列表")
    except Exception as e:
        print(f"获取包列表失败: {e}")

def main():
    """主函数"""
    print("豆瓣电影爬虫 - 环境诊断工具")
    
    # 检查Python版本
    python_ok = check_python_version()
    
    # 检查pip
    pip_ok = check_pip()
    
    # 检查依赖包
    missing_packages = check_dependencies()
    
    # 显示已安装的包
    check_pip_list()
    
    print("\n" + "=" * 50)
    print("诊断结果")
    print("=" * 50)
    
    if not python_ok:
        print("✗ Python环境有问题")
        print("建议：重新安装Python 3.7+")
        return
    
    if not pip_ok:
        print("✗ pip有问题")
        print("建议：重新安装Python或修复pip")
        return
    
    if missing_packages:
        print(f"✗ 缺少 {len(missing_packages)} 个依赖包: {', '.join(missing_packages)}")
        
        choice = input("\n是否自动安装缺失的包？(y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            install_packages(missing_packages)
            
            # 重新检查
            print("\n重新检查依赖包...")
            missing_packages = check_dependencies()
            
            if not missing_packages:
                print("✓ 所有依赖包安装成功！")
            else:
                print(f"✗ 仍有 {len(missing_packages)} 个包未安装")
        else:
            print("请手动安装依赖包:")
            print("pip install requests beautifulsoup4 lxml")
    else:
        print("✓ 环境检查通过，可以运行爬虫程序！")
    
    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)

if __name__ == "__main__":
    main() 