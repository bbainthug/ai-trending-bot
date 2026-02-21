#!/usr/bin/env python3
"""
GitHub Trending Scraper
提取GitHub Trending页面的仓库信息并保存为Markdown表格
"""

import requests
from bs4 import BeautifulSoup
import re


def scrape_github_trending():
    """
    从GitHub Trending页面提取仓库信息
    
    Returns:
        list: 包含仓库信息的字典列表
    """
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取页面失败: {e}")
        return []
    
    soup = BeautifulSoup(response.content, "html.parser")
    repo_elements = soup.find_all("article", class_="Box-row")
    
    if not repo_elements:
        print("⚠️ 未找到仓库元素，页面结构可能已更改")
        return []
    
    trending_repos = []
    
    for repo in repo_elements:
        repo_info = extract_repo_info(repo)
        if repo_info:
            trending_repos.append(repo_info)
    
    return trending_repos


def extract_repo_info(repo_element):
    """
    从单个仓库元素中提取信息
    
    Args:
        repo_element: BeautifulSoup仓库元素
        
    Returns:
        dict: 包含仓库信息的字典，如果提取失败则返回None
    """
    try:
        # 提取仓库名称和URL
        h2_tag = repo_element.find("h2", class_="h3")
        if not h2_tag:
            return None
            
        a_tag = h2_tag.find("a")
        if not a_tag:
            return None
            
        repo_name = a_tag.get_text(strip=True).replace(" ", "")
        repo_url = "https://github.com" + a_tag["href"]
        
        # 验证URL格式
        if not re.match(r'^https://github\.com/[^/]+/[^/]+$', repo_url):
            return None
        
        # 提取描述
        description = "N/A"
        p_tag = repo_element.find("p", class_="col-9")
        if p_tag:
            description = p_tag.get_text(strip=True)
        
        # 提取星数
        stars = "0"
        star_link = repo_element.find("a", href=lambda x: x and "/stargazers" in x)
        if star_link:
            stars_text = star_link.get_text(strip=True)
            # 移除逗号并验证是否为数字
            stars = stars_text.replace(",", "")
            if not stars.isdigit():
                stars = "0"
        
        # 提取编程语言（可选）
        language = "N/A"
        lang_span = repo_element.find("span", itemprop="programmingLanguage")
        if lang_span:
            language = lang_span.get_text(strip=True)
        
        return {
            "name": repo_name,
            "url": repo_url,
            "description": description,
            "stars": stars,
            "language": language
        }
        
    except Exception as e:
        print(f"⚠️ 提取仓库信息时出错: {e}")
        return None


def filter_ai_repos(repos):
    """
    过滤AI/LLM/Agent相关的仓库
    
    Args:
        repos: 仓库列表
        
    Returns:
        list: 过滤后的仓库列表
    """
    if not repos:
        return []
    
    ai_keywords = ["ai", "llm", "agent", "artificial intelligence", 
                   "machine learning", "deep learning", "neural network",
                   "transformer", "gpt", "chatgpt", "openai", "anthropic",
                   "claude", "gemini", "vector", "embedding", "rag"]
    
    filtered_repos = []
    
    for repo in repos:
        description_lower = repo["description"].lower()
        name_lower = repo["name"].lower()
        
        # 检查描述或名称中是否包含关键词
        for keyword in ai_keywords:
            if keyword in description_lower or keyword in name_lower:
                filtered_repos.append(repo)
                break
    
    return filtered_repos


def create_markdown_table(repos):
    """
    创建Markdown表格
    
    Args:
        repos: 仓库列表
        
    Returns:
        str: Markdown格式的表格
    """
    if not repos:
        return "# GitHub Trending (AI/LLM/Agent相关)\n\n未找到相关仓库。"
    
    # 表格标题
    markdown = "# GitHub Trending (AI/LLM/Agent相关)\n\n"
    markdown += "| 仓库名称 | URL | 描述（功能） | 星数 |\n"
    markdown += "|----------|-----|--------------|------|\n"
    
    # 表格内容
    for repo in repos:
        # 转义Markdown特殊字符
        name = repo["name"].replace("|", "\\|")
        url = repo["url"]
        description = repo["description"].replace("|", "\\|").replace("\n", " ")
        stars = repo["stars"]
        
        markdown += f"| {name} | [{url}]({url}) | {description} | {stars} |\n"
    
    # 添加统计信息
    markdown += f"\n**总计: {len(repos)} 个仓库**\n"
    
    return markdown


def save_to_file(content, filename="trending_today.md"):
    """
    保存内容到文件
    
    Args:
        content: 要保存的内容
        filename: 文件名
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 数据已保存到 {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存文件失败: {e}")
        return False


def main():
    """主函数"""
    print("🚀 开始抓取GitHub Trending页面...")
    
    # 抓取所有仓库
    all_repos = scrape_github_trending()
    
    if not all_repos:
        print("❌ 未找到任何仓库")
        return
    
    print(f"📊 找到 {len(all_repos)} 个仓库")
    
    # 过滤AI相关仓库
    ai_repos = filter_ai_repos(all_repos)
    
    if not ai_repos:
        print("⚠️ 未找到AI/LLM/Agent相关的仓库")
        # 显示前5个仓库供参考
        print("\n前5个热门仓库:")
        for i, repo in enumerate(all_repos[:5], 1):
            print(f"{i}. {repo['name']} - {repo['description'][:50]}...")
        return
    
    print(f"🤖 找到 {len(ai_repos)} 个AI/LLM/Agent相关仓库")
    
    # 创建Markdown表格
    markdown_content = create_markdown_table(ai_repos)
    
    # 保存到文件
    if save_to_file(markdown_content):
        # 显示前几个仓库
        print("\n📋 前几个AI相关仓库:")
        for i, repo in enumerate(ai_repos[:3], 1):
            print(f"{i}. {repo['name']}")
            print(f"   描述: {repo['description'][:60]}...")
            print(f"   星数: {repo['stars']}")
            print(f"   URL: {repo['url']}")
            print()
        
        if len(ai_repos) > 3:
            print(f"... 还有 {len(ai_repos) - 3} 个仓库")
    else:
        print("❌ 保存失败")


if __name__ == "__main__":
    main()