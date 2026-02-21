#!/usr/bin/env python3
"""
GitHub Trending Scraper
从GitHub Trending页面提取AI/LLM/Agent相关仓库信息
输出格式：Markdown表格
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


def scrape_github_trending():
    """抓取GitHub Trending页面"""
    url = "https://github.com/trending"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"获取页面失败: {e}")
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
    except:
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
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
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


def save_markdown(content, filename="github_trending_ai.md"):
    """保存Markdown文件"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False


def main():
    """主函数"""
    print("正在抓取GitHub Trending页面...")
    
    # 抓取页面
    response = scrape_github_trending()
    if not response:
        return
    
    # 解析仓库
    all_repos = parse_repositories(response.content)
    print(f"找到 {len(all_repos)} 个仓库")
    
    # 过滤AI相关
    ai_repos = filter_ai_repositories(all_repos)
    print(f"找到 {len(ai_repos)} 个AI/LLM/Agent相关仓库")
    
    # 排除特定仓库
    ai_repos = exclude_repositories(ai_repos, ["openclaw/openclaw"])
    print(f"排除后剩余 {len(ai_repos)} 个仓库")
    
    if not ai_repos:
        print("没有符合条件的仓库")
        return
    
    # 生成Markdown
    markdown = create_markdown_table(ai_repos)
    
    # 保存文件
    if save_markdown(markdown):
        print(f"✅ 数据已保存到 github_trending_ai.md")
        
        # 显示简要信息
        print("\n仓库列表:")
        for i, repo in enumerate(ai_repos[:5], 1):
            print(f"{i}. {repo['name']} - ★{repo['stars']}")
        
        if len(ai_repos) > 5:
            print(f"... 还有 {len(ai_repos) - 5} 个仓库")
    else:
        print("❌ 保存失败")


if __name__ == "__main__":
    main()