#!/usr/bin/env python3
"""
GitHub Trending Scraper with Telegram Notification and Git Auto-Push
从GitHub Trending页面提取AI/LLM/Agent相关仓库信息
输出格式：Markdown表格并通过Telegram Bot发送通知
自动提交和推送到Git仓库
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os
import sys
import subprocess
import json
from pathlib import Path

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("⚠️  python-dotenv 未安装，将使用系统环境变量")
    print("   安装: pip install python-dotenv")


def load_environment():
    """从.env文件或环境变量加载配置"""
    config = {
        "bot_token": None,
        "chat_id": None,
        "git_auto_push": True,
        "git_commit_message": "自动更新每日 GitHub 趋势数据",
        "exclude_repos": ["openclaw/openclaw"],
        "max_repos_in_telegram": 5,
        "save_filename": "github_trending_ai.md"
    }
    
    # 尝试从.env文件加载
    if DOTENV_AVAILABLE:
        env_loaded = load_dotenv()
        if env_loaded:
            print("✅ 从 .env 文件加载配置")
        else:
            print("⚠️  未找到 .env 文件，使用系统环境变量")
    
    # 加载配置
    config["bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN")
    config["chat_id"] = os.getenv("TELEGRAM_CHAT_ID")
    
    # Git 配置
    git_auto_push = os.getenv("GIT_AUTO_PUSH", "true").lower()
    config["git_auto_push"] = git_auto_push in ("true", "1", "yes", "y")
    
    config["git_commit_message"] = os.getenv("GIT_COMMIT_MESSAGE", config["git_commit_message"])
    
    # 排除的仓库
    exclude_repos_str = os.getenv("EXCLUDE_REPOS", "")
    if exclude_repos_str:
        config["exclude_repos"] = [repo.strip() for repo in exclude_repos_str.split(",") if repo.strip()]
    
    # 其他配置
    max_repos = os.getenv("MAX_REPOS_IN_TELEGRAM")
    if max_repos and max_repos.isdigit():
        config["max_repos_in_telegram"] = int(max_repos)
    
    config["save_filename"] = os.getenv("SAVE_FILENAME", config["save_filename"])
    
    return config


def scrape_github_trending():
    """抓取GitHub Trending页面"""
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取页面失败: {e}")
        return None


def parse_repositories(html_content):
    """解析HTML内容，提取仓库信息"""
    soup = BeautifulSoup(html_content, "html.parser")
    repo_elements = soup.find_all("article", class_="Box-row")
    
    repositories = []
    
    for repo in repo_elements:
        info = extract_repository_info(repo)
        if info:
            repositories.append(info)
    
    return repositories


def extract_repository_info(repo_element):
    """从仓库元素中提取详细信息"""
    try:
        # 提取名称和URL
        h2 = repo_element.find("h2", class_="h3")
        if not h2:
            return None
        
        a = h2.find("a")
        if not a:
            return None
        
        name = a.get_text(strip=True).replace(" ", "")
        url = "https://github.com" + a["href"]
        
        # 验证URL
        if not re.match(r'^https://github\.com/[^/]+/[^/]+$', url):
            return None
        
        # 提取描述
        description = "N/A"
        p = repo_element.find("p", class_="col-9")
        if p:
            description = p.get_text(strip=True)
        
        # 提取星数
        stars = "0"
        star_link = repo_element.find("a", href=lambda x: x and "/stargazers" in x)
        if star_link:
            stars_text = star_link.get_text(strip=True)
            stars = stars_text.replace(",", "")
            if not stars.isdigit():
                stars = "0"
        
        return {
            "name": name,
            "url": url,
            "description": description,
            "stars": stars
        }
    except Exception as e:
        print(f"⚠️ 提取仓库信息时出错: {e}")
        return None


def filter_ai_repositories(repositories):
    """过滤AI/LLM/Agent相关仓库"""
    ai_keywords = [
        "ai", "llm", "agent", "machine learning", "deep learning",
        "neural network", "transformer", "gpt", "chatgpt", "openai",
        "anthropic", "claude", "gemini", "vector", "embedding", "rag",
        "language model", "large language model", "ai agent"
    ]
    
    filtered = []
    
    for repo in repositories:
        desc_lower = repo["description"].lower()
        name_lower = repo["name"].lower()
        
        for keyword in ai_keywords:
            if keyword in desc_lower or keyword in name_lower:
                filtered.append(repo)
                break
    
    return filtered


def exclude_repositories(repositories, exclude_names):
    """排除特定仓库"""
    if not exclude_names:
        return repositories
    
    filtered = []
    
    for repo in repositories:
        exclude = False
        for exclude_name in exclude_names:
            if exclude_name.lower() in repo["name"].lower():
                exclude = True
                break
        
        if not exclude:
            filtered.append(repo)
    
    return filtered


def create_markdown_table(repositories):
    """生成Markdown表格"""
    if not repositories:
        return "# GitHub Trending\n\n未找到相关仓库。"
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 表格标题
    markdown = f"# GitHub Trending (AI/LLM/Agent相关) - {current_date}\n\n"
    markdown += "| 仓库名称 | URL | 描述（功能） | 星数 |\n"
    markdown += "|----------|-----|--------------|------|\n"
    
    # 表格内容
    for repo in repositories:
        name = repo["name"].replace("|", "\\|")
        url = repo["url"]
        desc = repo["description"].replace("|", "\\|").replace("\n", " ")
        stars = repo["stars"]
        
        markdown += f"| {name} | [{url}]({url}) | {desc} | {stars} |\n"
    
    # 统计信息
    markdown += f"\n**总计: {len(repositories)} 个仓库**\n"
    markdown += f"**更新时间: {current_date}**\n"
    
    return markdown


def create_telegram_message(repositories, max_repos=5):
    """创建适合Telegram的消息（限制在4096字符内）"""
    if not repositories:
        return "GitHub Trending: 今天没有找到AI/LLM/Agent相关仓库。"
    
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 创建消息头
    message = f"🚀 *GitHub Trending (AI/LLM/Agent相关) - {current_date}*\n\n"
    
    # 添加前几个仓库（避免消息过长）
    max_repos = min(max_repos, len(repositories))
    for i, repo in enumerate(repositories[:max_repos], 1):
        # 缩短描述以避免消息过长
        short_desc = repo["description"][:80] + "..." if len(repo["description"]) > 80 else repo["description"]
        message += f"{i}. *{repo['name']}*\n"
        message += f"   ⭐ {repo['stars']} | {short_desc}\n"
        message += f"   🔗 {repo['url']}\n\n"
    
    if len(repositories) > max_repos:
        message += f"... 还有 {len(repositories) - max_repos} 个仓库\n\n"
    
    message += f"📊 总计: {len(repositories)} 个仓库"
    
    # 检查消息长度（Telegram限制4096字符）
    if len(message) > 4000:
        # 如果太长，进一步缩短
        message = message[:3900] + "\n\n...（消息过长，已截断）"
    
    return message


def send_telegram_message(bot_token, chat_id, message):
    """通过Telegram Bot发送消息"""
    if not bot_token or not chat_id:
        print("⚠️  Telegram配置不完整，跳过发送消息")
        return False
    
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            print(f"✅ Telegram消息发送成功！消息ID: {result['result']['message_id']}")
            return True
        else:
            print(f"❌ Telegram API返回错误: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 发送Telegram消息超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 发送Telegram消息失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 处理Telegram响应时出错: {e}")
        return False


def save_markdown(content, filename="github_trending_ai.md"):
    """保存Markdown文件"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 数据已保存到 {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        return False


def test_telegram_bot(bot_token, chat_id):
    """测试Telegram Bot连接"""
    if not bot_token or not chat_id:
        return False
    
    print("🔍 测试Telegram Bot连接...")
    
    api_url = f"https://api.telegram.org/bot{bot_token}/getMe"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            bot_info = result["result"]
            print(f"✅ Bot连接成功！")
            print(f"   Bot名称: {bot_info.get('first_name', 'N/A')}")
            print(f"   Bot用户名: @{bot_info.get('username', 'N/A')}")
            return True
        else:
            print(f"❌ Bot测试失败: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 测试Bot连接失败: {e}")
        return False


def git_auto_push(commit_message="自动更新每日 GitHub 趋势数据"):
    """自动执行Git添加、提交和推送操作"""
    print("\n🔧 开始自动Git操作...")
    
    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", commit_message],
        ["git", "push"]
    ]
    
    results = []
    
    for i, cmd in enumerate(commands):
        cmd_name = " ".join(cmd)
        print(f"  执行: {cmd_name}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # 60秒超时
            )
            
            if result.returncode == 0:
                print(f"  ✅ 成功: {cmd_name}")
                results.append(True)
            else:
                print(f"  ⚠️  警告: {cmd_name} 返回非零状态码")
                print(f"     错误: {result.stderr[:200]}")
                results.append(False)
                
                # 如果是git add失败，可能是没有更改
                if i == 0 and "nothing to commit" in result.stdout.lower():
                    print("  ℹ️  没有需要提交的更改")
                    return False
                    
        except subprocess.TimeoutExpired:
            print(f"  ❌ 超时: {cmd_name} 执行超时")
            results.append(False)
        except FileNotFoundError:
            print(f"  ❌ 错误: Git未安装或不在PATH中")
            results.append(False)
        except Exception as e:
            print(f"  ❌ 异常: {cmd_name} 执行出错: {e}")
            results.append(False)
    
    # 检查所有命令是否成功
    if all(results):
        print("✅ Git自动推送完成！")
        return True
    else:
        print("⚠️  Git操作部分失败，请手动检查")
        return False


def check_git_repository():
    """检查当前目录是否是Git仓库"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False


def save_data_json(repositories, filename="github_trending_data.json"):
    """保存原始数据为JSON文件（用于历史记录）"""
    if not repositories:
        return False
    
    try:
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_repos": len(repositories),
            "repositories": repositories
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 原始数据已保存到 {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存JSON数据失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("GitHub Trending Scraper with Telegram & Git Auto-Push")
    print("=" * 60)
    
    # 加载配置
    config = load_environment()
    
    # 检查Telegram配置
    if not config["bot_token"]:
        print("❌ 未配置 TELEGRAM_BOT_TOKEN")
        print("   请在 .env 文件中设置或使用环境变量")
        return
    
    # 测试Bot连接
    if config["chat_id"]:
        if not test_telegram_bot(config["bot_token"], config["chat_id"]):
            print("❌ Telegram Bot测试失败，请检查配置")
            return
    else:
        print("⚠️  未配置 TELEGRAM_CHAT_ID，跳过Telegram通知")
    
    print("\n🚀 正在抓取GitHub Trending页面...")
    
    # 抓取页面
    response = scrape_github_trending()
    if not response:
        return
    
    # 解析仓库
    all_repos = parse_repositories(response.content)
    print(f"📊 找到 {len(all_repos)} 个仓库")
    
    if not all_repos:
        print("❌ 未找到任何仓库，可能页面结构已更改")
        return
    
    # 过滤AI相关
    ai_repos = filter_ai_repositories(all_repos)
    print(f"🤖 找到 {len(ai_repos)} 个AI/LLM/Agent相关仓库")
    
    # 排除特定仓库
    if config["exclude_repos"]:
        ai_repos = exclude_repositories(ai_repos, config["exclude_repos"])
        print(f"🔍 排除 {len(config['exclude_repos'])} 个仓库后剩余 {len(ai_repos)} 个")
    
    if not ai_repos:
        print("没有符合条件的仓库")
        # 发送空结果通知
        if config["chat_id"]:
            message = "GitHub Trending: 今天没有找到AI/LLM/Agent相关仓库。"
            send_telegram_message(config["bot_token"], config["chat_id"], message)
        return
    
    # 生成Markdown
    markdown = create_markdown_table(ai_repos)
    
    # 保存文件
    if save_markdown(markdown, config["save_filename"]):
        # 保存原始数据为JSON
        save_data_json(ai_repos, "github_trending_data.json")
    else:
        print("❌ 保存文件失败")
    
    # 发送Telegram通知
    if config["chat_id"]:
        print("\n📱 正在发送Telegram通知...")
        telegram_message = create_telegram_message(ai_repos, config["max_repos_in_telegram"])
        send_telegram_message(config["bot_token"], config["chat_id"], telegram_message)
    
    # 显示简要信息
    print("\n📋 仓库列表:")
    for i, repo in enumerate(ai_repos[:5], 1):
        print(f"{i}. {repo['name']} - ★{repo['stars']}")
    
    if len(ai_repos) > 5:
        print(f"... 还有 {len(ai_repos) - 5} 个仓库")
    
    # 自动Git推送
    if config["git_auto_push"]:
        if check_git_repository():
            print("\n" + "=" * 40)
            print("🔄 执行自动Git推送")
            print("=" * 40)
            
            success = git_auto_push(config["git_commit_message"])
            if not success:
                print("⚠️  Git自动推送失败，请手动处理")
        else:
            print("\n⚠️  当前目录不是Git仓库，跳过自动推送")
            print("   如需自动推送，请先初始化Git仓库:")
            print("   git init")
            print("   git remote add origin <你的仓库URL>")
    else:
        print("\nℹ️  Git自动推送已禁用（GIT_AUTO_PUSH=false）")
    
    print("\n" + "=" * 60)
    print("✅ 脚本执行完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()