@echo off
chcp 65001 >nul
echo 豆瓣电影爬虫 - 依赖修复工具
echo ============================
echo.

echo 正在修复依赖包问题...
echo.

REM 尝试多种安装方法
echo 方法1: 使用pip安装
pip install requests beautifulsoup4 lxml
if errorlevel 1 (
    echo.
    echo 方法1失败，尝试方法2...
    echo.
    python -m pip install requests beautifulsoup4 lxml
    if errorlevel 1 (
        echo.
        echo 方法2失败，尝试方法3...
        echo.
        pip3 install requests beautifulsoup4 lxml
        if errorlevel 1 (
            echo.
            echo 所有方法都失败了，请手动安装：
            echo 1. 打开命令提示符
            echo 2. 运行: pip install requests beautifulsoup4 lxml
            echo 3. 如果失败，尝试: python -m pip install requests beautifulsoup4 lxml
            echo.
            pause
            exit /b 1
        )
    )
)

echo.
echo 依赖包安装完成！
echo.

REM 验证安装
echo 验证安装结果...
python -c "import requests, bs4, lxml; print('✓ 所有依赖包安装成功！')" 2>nul
if errorlevel 1 (
    echo ✗ 依赖包验证失败
    echo 请运行 diagnose.bat 进行详细诊断
) else (
    echo ✓ 依赖包验证成功
    echo 现在可以运行 start.bat 启动程序了
)

echo.
pause 