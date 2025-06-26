@echo off
chcp 65001 >nul
echo 豆瓣电影爬虫启动器
echo ====================
echo.

REM 检查Python是否安装
echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.7+
    echo.
    echo 请访问 https://www.python.org/downloads/ 下载并安装Python
    pause
    exit /b 1
)

echo ✓ Python已安装
python --version

echo.
echo 正在检查pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到pip，请检查Python安装
    pause
    exit /b 1
)

echo ✓ pip可用
pip --version

echo.
echo 正在检查依赖包...

REM 检查每个依赖包
set missing_packages=0

echo 检查 requests...
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ✗ requests 未安装
    set /a missing_packages+=1
) else (
    echo ✓ requests 已安装
)

echo 检查 beautifulsoup4...
python -c "import bs4" >nul 2>&1
if errorlevel 1 (
    echo ✗ beautifulsoup4 未安装
    set /a missing_packages+=1
) else (
    echo ✓ beautifulsoup4 已安装
)

echo 检查 lxml...
python -c "import lxml" >nul 2>&1
if errorlevel 1 (
    echo ✗ lxml 未安装
    set /a missing_packages+=1
) else (
    echo ✓ lxml 已安装
)

echo.
if %missing_packages% gtr 0 (
    echo 发现 %missing_packages% 个依赖包未安装，正在安装...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo 自动安装失败，请手动运行以下命令：
        echo pip install requests beautifulsoup4 lxml
        echo.
        pause
        exit /b 1
    )
    echo.
    echo ✓ 依赖包安装完成！
) else (
    echo ✓ 所有依赖包已安装！
)

echo.
echo 启动豆瓣电影爬虫程序...
echo.

REM 运行主程序
python run_crawler.py

echo.
echo 程序已退出
pause 