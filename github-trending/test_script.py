#!/usr/bin/env python3
"""
测试脚本 - 验证核心功能
"""

import os
import sys
import subprocess

def test_dotenv():
    """测试python-dotenv"""
    print("🔍 测试 python-dotenv...")
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 已安装")
        
        # 创建测试.env文件
        test_env_content = """# 测试环境变量
TEST_VAR=test_value
ANOTHER_VAR=123
"""
        
        with open(".test.env", "w") as f:
            f.write(test_env_content)
        
        # 加载测试文件
        load_dotenv(".test.env")
        
        if os.getenv("TEST_VAR") == "test_value":
            print("✅ .env 文件加载成功")
        else:
            print("❌ .env 文件加载失败")
        
        # 清理
        os.remove(".test.env")
        return True
        
    except ImportError:
        print("❌ python-dotenv 未安装")
        print("   运行: pip install python-dotenv")
        return False

def test_git():
    """测试Git命令"""
    print("\n🔍 测试 Git 命令...")
    
    commands = [
        ["git", "--version"],
        ["git", "status"],
    ]
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {' '.join(cmd)} - 成功")
            else:
                print(f"⚠️  {' '.join(cmd)} - 返回非零状态码")
                print(f"   错误: {result.stderr[:100]}")
        except FileNotFoundError:
            print(f"❌ {' '.join(cmd)} - Git未安装")
            return False
        except Exception as e:
            print(f"❌ {' '.join(cmd)} - 异常: {e}")
            return False
    
    return True

def test_requirements():
    """测试Python依赖"""
    print("\n🔍 测试 Python 依赖...")
    
    requirements = [
        ("requests", "网络请求"),
        ("bs4", "BeautifulSoup4"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_ok = True
    
    for module, description in requirements:
        try:
            if module == "bs4":
                import bs4
            elif module == "dotenv":
                from dotenv import load_dotenv
            else:
                __import__(module)
            print(f"✅ {module} ({description}) - 已安装")
        except ImportError as e:
            print(f"❌ {module} ({description}) - 未安装: {e}")
            all_ok = False
    
    return all_ok

def test_main_script():
    """测试主脚本导入"""
    print("\n🔍 测试主脚本导入...")
    
    try:
        # 模拟导入主脚本（不实际运行）
        import requests
        from bs4 import BeautifulSoup
        from dotenv import load_dotenv
        import json
        from datetime import datetime
        import subprocess
        
        print("✅ 所有必需模块可导入")
        
        # 检查主脚本文件
        if os.path.exists("github_trending_scraper_with_telegram.py"):
            print("✅ 主脚本文件存在")
            
            # 检查文件大小
            file_size = os.path.getsize("github_trending_scraper_with_telegram.py")
            print(f"   文件大小: {file_size} 字节")
            
            # 检查文件内容
            with open("github_trending_scraper_with_telegram.py", "r", encoding="utf-8") as f:
                content = f.read(500)
                if "load_dotenv" in content and "git_auto_push" in content:
                    print("✅ 脚本包含所需功能")
                else:
                    print("⚠️  脚本可能不完整")
        else:
            print("❌ 主脚本文件不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 导入测试失败: {e}")
        return False

def create_test_env():
    """创建测试环境"""
    print("\n🔧 创建测试环境...")
    
    # 检查.env文件
    if os.path.exists(".env"):
        print("✅ .env 文件已存在")
        
        # 读取现有配置
        with open(".env", "r") as f:
            content = f.read()
            
        # 检查必要配置
        required = ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"]
        missing = []
        
        for req in required:
            if req not in content:
                missing.append(req)
        
        if missing:
            print(f"⚠️  .env 文件缺少配置: {', '.join(missing)}")
            print("   请编辑 .env 文件添加配置")
        else:
            print("✅ .env 文件包含必要配置")
    else:
        print("❌ .env 文件不存在")
        print("   运行: cp .env.example .env")
        print("   然后编辑 .env 文件")

def main():
    """主测试函数"""
    print("=" * 50)
    print("GitHub Trending Scraper 功能测试")
    print("=" * 50)
    
    tests = [
        ("Python依赖", test_requirements),
        ("python-dotenv", test_dotenv),
        ("Git命令", test_git),
        ("主脚本", test_main_script),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))
    
    # 创建测试环境
    create_test_env()
    
    # 显示测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！")
        print("现在可以运行主脚本:")
        print("python3 github_trending_scraper_with_telegram.py")
    else:
        print("⚠️  部分测试失败，请检查上述错误")
        print("可能需要:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 初始化Git: git init")
        print("3. 创建.env文件: cp .env.example .env")
    
    print("=" * 50)

if __name__ == "__main__":
    main()