@echo off
chcp 65001 >nul
echo 豆瓣电影爬虫 - 环境诊断工具
echo ============================
echo.

REM 运行诊断程序
python check_environment.py

echo.
pause 