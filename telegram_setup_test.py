#!/usr/bin/env python3
"""
Telegram Bot 设置测试脚本
测试你的 Bot Token 和 Chat ID 是否正确配置
"""

import os
import requests
import sys


def test_bot_token(bot_token):
    """测试 Bot Token 是否有效"""
    print("🔍 测试 Bot Token...")
    
    api_url = f"https://api.telegram.org/bot{bot_token}/getMe"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            bot_info = result["result"]
            print(f"✅ Bot Token 有效！")
            print(f"   Bot 名称: {bot_info.get('first_name', 'N/A')}")
            print(f"   Bot 用户名: @{bot_info.get('username', 'N/A')}")
            print(f"   Bot ID: {bot_info.get('id', 'N/A')}")
            return True, bot_info
        else:
            print(f"❌ Bot Token 无效: {result.get('description', 'Unknown error')}")
            return False, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接失败: {e}")
        return False, None


def test_chat_id(bot_token, chat_id):
    """测试 Chat ID 是否有效"""
    print(f"\n🔍 测试 Chat ID ({chat_id})...")
    
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": "✅ Telegram Bot 设置测试成功！\n你的配置正确，可以接收通知了。",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            print(f"✅ Chat ID 有效！测试消息已发送。")
            print(f"   消息 ID: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ Chat ID 无效: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 发送测试消息失败: {e}")
        return False


def get_environment_variables():
    """获取环境变量"""
    print("📋 检查环境变量...")
    
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if bot_token:
        print(f"✅ 找到 TELEGRAM_BOT_TOKEN: {bot_token[:10]}...{bot_token[-10:]}")
    else:
        print("❌ 未找到 TELEGRAM_BOT_TOKEN")
    
    if chat_id:
        print(f"✅ 找到 TELEGRAM_CHAT_ID: {chat_id}")
    else:
        print("❌ 未找到 TELEGRAM_CHAT_ID")
    
    return bot_token, chat_id


def main():
    """主函数"""
    print("=" * 50)
    print("Telegram Bot 设置测试")
    print("=" * 50)
    
    # 获取环境变量
    bot_token, chat_id = get_environment_variables()
    
    if not bot_token:
        print("\n❌ 请先设置 TELEGRAM_BOT_TOKEN 环境变量")
        print("运行: export TELEGRAM_BOT_TOKEN='你的BotToken'")
        return
    
    # 测试 Bot Token
    token_valid, bot_info = test_bot_token(bot_token)
    if not token_valid:
        return
    
    if not chat_id:
        print("\n⚠️  未设置 TELEGRAM_CHAT_ID")
        print("请按照以下步骤获取你的 Chat ID:")
        print("1. 在 Telegram 中搜索 @userinfobot")
        print("2. 发送 /start 命令")
        print("3. 复制显示的 Chat ID")
        print("4. 运行: export TELEGRAM_CHAT_ID='你的ChatID'")
        return
    
    # 测试 Chat ID
    test_chat_id(bot_token, chat_id)
    
    print("\n" + "=" * 50)
    print("✅ 设置完成！")
    print("=" * 50)
    print("\n现在你可以运行主脚本了:")
    print("python3 github_trending_scraper_with_telegram.py")


if __name__ == "__main__":
    main()