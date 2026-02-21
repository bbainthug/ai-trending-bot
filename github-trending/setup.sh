#!/bin/bash

# GitHub Trending Scraper 安装脚本

echo "🔧 GitHub Trending Scraper 安装脚本"
echo "====================================="

# 检查Python版本
echo -e "\n🐍 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 安装依赖
echo -e "\n📦 安装Python依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败，尝试使用 --break-system-packages..."
    pip3 install -r requirements.txt --break-system-packages
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动安装"
        exit 1
    fi
fi

# 创建.env文件（如果不存在）
if [ ! -f .env ]; then
    echo -e "\n📝 创建 .env 配置文件..."
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑该文件配置你的设置"
else
    echo -e "\n✅ .env 文件已存在"
fi

# 检查Git仓库
echo -e "\n🔍 检查Git仓库状态..."
if [ -d .git ]; then
    echo "✅ Git仓库已初始化"
    
    # 检查远程仓库
    git remote -v | grep -q "origin"
    if [ $? -eq 0 ]; then
        echo "✅ 远程仓库已配置"
    else
        echo "⚠️  未配置远程仓库，自动推送将无法工作"
        echo "   运行: git remote add origin <你的仓库URL>"
    fi
else
    echo "⚠️  当前目录不是Git仓库，自动推送将无法工作"
    echo "   如需自动推送，请运行:"
    echo "   git init"
    echo "   git remote add origin <你的仓库URL>"
fi

# 测试脚本
echo -e "\n🧪 测试脚本..."
python3 -c "import requests; import bs4; from dotenv import load_dotenv; print('✅ 所有依赖已正确安装')"

# 显示使用说明
echo -e "\n🎯 使用说明:"
echo "1. 编辑 .env 文件，配置你的 Telegram Bot Token 和 Chat ID"
echo "2. 运行脚本: python3 github_trending_scraper_with_telegram.py"
echo "3. 设置定时任务 (cron):"
echo "   crontab -e"
echo "   添加: 0 9 * * * cd $(pwd) && python3 github_trending_scraper_with_telegram.py"
echo ""
echo "📁 文件说明:"
echo "  .env.example      - 配置文件模板"
echo "  .env             - 你的配置文件（不要提交到Git）"
echo "  requirements.txt - Python依赖"
echo "  setup.sh         - 安装脚本"
echo "  TELEGRAM_SETUP_GUIDE.md - Telegram设置指南"

echo -e "\n✅ 安装完成！"