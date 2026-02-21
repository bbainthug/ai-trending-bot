#!/bin/bash

# Telegram Bot 环境变量设置脚本
# 使用方法: source setup_env.sh

echo "🔧 Telegram Bot 环境变量设置"
echo "============================="

# 检查当前设置
echo -e "\n📋 当前环境变量:"
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    echo "✅ TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:0:10}...${TELEGRAM_BOT_TOKEN: -10}"
else
    echo "❌ TELEGRAM_BOT_TOKEN: 未设置"
fi

if [ -n "$TELEGRAM_CHAT_ID" ]; then
    echo "✅ TELEGRAM_CHAT_ID: $TELEGRAM_CHAT_ID"
else
    echo "❌ TELEGRAM_CHAT_ID: 未设置"
fi

echo -e "\n📝 请输入你的设置:"

# 设置 Bot Token
read -p "1. 输入 Telegram Bot Token: " BOT_TOKEN
if [ -n "$BOT_TOKEN" ]; then
    export TELEGRAM_BOT_TOKEN="$BOT_TOKEN"
    echo "✅ TELEGRAM_BOT_TOKEN 已设置"
fi

# 设置 Chat ID
read -p "2. 输入 Telegram Chat ID: " CHAT_ID
if [ -n "$CHAT_ID" ]; then
    export TELEGRAM_CHAT_ID="$CHAT_ID"
    echo "✅ TELEGRAM_CHAT_ID 已设置"
fi

echo -e "\n🎯 永久设置（可选）"
read -p "是否永久保存到 ~/.bashrc? (y/n): " SAVE_PERMANENTLY

if [[ "$SAVE_PERMANENTLY" == "y" || "$SAVE_PERMANENTLY" == "Y" ]]; then
    # 移除旧的设置
    sed -i '/export TELEGRAM_BOT_TOKEN=/d' ~/.bashrc
    sed -i '/export TELEGRAM_CHAT_ID=/d' ~/.bashrc
    
    # 添加新的设置
    if [ -n "$BOT_TOKEN" ]; then
        echo "export TELEGRAM_BOT_TOKEN=\"$BOT_TOKEN\"" >> ~/.bashrc
    fi
    if [ -n "$CHAT_ID" ]; then
        echo "export TELEGRAM_CHAT_ID=\"$CHAT_ID\"" >> ~/.bashrc
    fi
    
    echo "✅ 已保存到 ~/.bashrc"
    echo "   重启终端或运行 'source ~/.bashrc' 生效"
fi

echo -e "\n🚀 测试配置:"
echo "运行: python3 telegram_setup_test.py"
echo "运行: python3 github_trending_scraper_with_telegram.py"