#!/usr/bin/env python3
"""
GitHub Trending Scraper 使用演示
展示如何使用 .env 文件和自动 Git 推送功能
"""

import os
import subprocess
from dotenv import load_dotenv, dotenv_values

def demo_dotenv_usage():
    """演示 .env 文件使用"""
    print("=" * 60)
    print(".env 文件使用演示")
    print("=" * 60)
    
    # 方法1: 使用 load_dotenv() 加载到环境变量
    print("\n1. 使用 load_dotenv() 加载配置:")
    print("-" * 40)
    
    # 保存原始环境变量
    original_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # 加载 .env 文件
    load_dotenv()
    
    # 读取配置
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    print(f"   TELEGRAM_BOT_TOKEN: {'已设置' if token else '未设置'}")
    print(f"   TELEGRAM_CHAT_ID: {'已设置' if chat_id else '未设置'}")
    
    # 方法2: 使用 dotenv_values() 获取字典
    print("\n2. 使用 dotenv_values() 获取配置字典:")
    print("-" * 40)
    
    config = dotenv_values()
    print(f"   配置项数量: {len(config)}")
    
    # 显示部分配置
    for key in ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "GIT_AUTO_PUSH"]:
        if key in config:
            value = config[key]
            masked = value[:10] + "..." + value[-10:] if len(value) > 20 else value
            print(f"   {key}: {masked}")
    
    # 恢复原始环境变量
    if original_token:
        os.environ["TELEGRAM_BOT_TOKEN"] = original_token

def demo_git_auto_push():
    """演示 Git 自动推送"""
    print("\n" + "=" * 60)
    print("Git 自动推送演示")
    print("=" * 60)
    
    # 检查是否是 Git 仓库
    print("\n1. 检查 Git 仓库状态:")
    print("-" * 40)
    
    try:
        result = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ 当前在 Git 仓库中")
            
            # 获取远程仓库信息
            remote_result = subprocess.run(["git", "remote", "-v"],
                                         capture_output=True, text=True)
            if remote_result.stdout:
                print("   📡 远程仓库配置:")
                for line in remote_result.stdout.strip().split('\n'):
                    print(f"      {line}")
            else:
                print("   ⚠️  未配置远程仓库")
        else:
            print("   ⚠️  当前不在 Git 仓库中")
    except Exception as e:
        print(f"   ❌ 检查 Git 仓库失败: {e}")
    
    # 演示 Git 命令
    print("\n2. Git 命令演示:")
    print("-" * 40)
    
    git_commands = [
        ["git", "status", "--short"],
        ["git", "log", "--oneline", "-3"],
    ]
    
    for cmd in git_commands:
        print(f"   执行: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    lines = output.split('\n')
                    for line in lines[:3]:  # 只显示前3行
                        print(f"      {line}")
                    if len(lines) > 3:
                        print(f"      ... 还有 {len(lines) - 3} 行")
                else:
                    print("      (无输出)")
            else:
                print(f"      ❌ 失败: {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            print("      ⏰ 超时")
        except Exception as e:
            print(f"      ❌ 异常: {e}")

def demo_cron_setup():
    """演示 Cron Job 设置"""
    print("\n" + "=" * 60)
    print("Cron Job 设置演示")
    print("=" * 60)
    
    print("\n1. 推荐的 Cron 表达式:")
    print("-" * 40)
    
    cron_examples = [
        ("每天上午9点", "0 9 * * *"),
        ("每天上午9点和下午9点", "0 9,21 * * *"),
        ("每6小时运行一次", "0 */6 * * *"),
        ("每周一上午9点", "0 9 * * 1"),
        ("每分钟运行（测试用）", "* * * * *"),
    ]
    
    for desc, expr in cron_examples:
        print(f"   {desc:20} {expr}")
    
    print("\n2. Cron 命令示例:")
    print("-" * 40)
    
    script_path = os.path.abspath("github_trending_scraper_with_telegram.py")
    
    cron_commands = [
        f"# 基本用法\n0 9 * * * cd {os.path.dirname(script_path)} && python3 {os.path.basename(script_path)}",
        f"# 带日志输出\n0 9 * * * cd {os.path.dirname(script_path)} && python3 {os.path.basename(script_path)} >> /tmp/github_trending.log 2>&1",
        f"# 使用完整路径\n0 9 * * * /usr/bin/python3 {script_path}",
    ]
    
    for i, cmd in enumerate(cron_commands, 1):
        print(f"   示例{i}:")
        print(f"   {cmd}")
        print()

def demo_script_workflow():
    """演示脚本工作流程"""
    print("\n" + "=" * 60)
    print("脚本工作流程演示")
    print("=" * 60)
    
    workflow = [
        ("1. 加载配置", "从 .env 文件加载 Telegram 和 Git 配置"),
        ("2. 抓取数据", "访问 GitHub Trending 页面并解析 HTML"),
        ("3. 过滤仓库", "筛选 AI/LLM/Agent 相关仓库"),
        ("4. 生成输出", "创建 Markdown 表格和 Telegram 消息"),
        ("5. 保存文件", "保存 Markdown 文件到本地"),
        ("6. 发送通知", "通过 Telegram Bot 发送通知"),
        ("7. Git 推送", "自动提交和推送到 Git 仓库"),
        ("8. 日志记录", "记录运行状态和错误信息"),
    ]
    
    for step, description in workflow:
        print(f"{step:15} {description}")

def main():
    """主演示函数"""
    print("🚀 GitHub Trending Scraper 功能演示")
    print("✨ 展示 .env 文件和自动 Git 推送功能")
    
    demos = [
        demo_dotenv_usage,
        demo_git_auto_push,
        demo_cron_setup,
        demo_script_workflow,
    ]
    
    for demo_func in demos:
        demo_func()
        input("\n按 Enter 继续...")
    
    print("\n" + "=" * 60)
    print("🎯 快速开始指南")
    print("=" * 60)
    
    quick_start = [
        "1. 安装依赖: pip install -r requirements.txt",
        "2. 复制配置文件: cp .env.example .env",
        "3. 编辑 .env 文件，设置你的 Telegram Bot Token 和 Chat ID",
        "4. 初始化 Git 仓库（如果需要自动推送）:",
        "   git init",
        "   git remote add origin <你的仓库URL>",
        "5. 测试运行: python3 github_trending_scraper_with_telegram.py",
        "6. 设置定时任务:",
        "   crontab -e",
        "   添加: 0 9 * * * cd /path/to/script && python3 github_trending_scraper_with_telegram.py",
    ]
    
    for step in quick_start:
        print(f"   {step}")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()