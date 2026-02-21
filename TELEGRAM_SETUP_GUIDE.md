# Telegram Bot 设置指南

## 📋 概述

本指南将帮助你设置 Telegram Bot，以便接收 GitHub Trending 通知。

## 🚀 快速开始

### 1. 创建 Telegram Bot

1. 在 Telegram 中搜索 **@BotFather**
2. 发送 `/newbot` 命令
3. 按照提示：
   - 输入 Bot 名称（例如：`GitHub Trending Bot`）
   - 输入 Bot 用户名（必须以 `bot` 结尾，例如：`github_trending_bot`）
4. 复制 Bot Father 提供的 **Bot Token**（格式如：`1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`）

### 2. 获取你的 Chat ID

#### 方法一：使用 @userinfobot（推荐）
1. 在 Telegram 中搜索 **@userinfobot**
2. 发送 `/start` 命令
3. 复制显示的 **Chat ID**（是一个数字，如：`123456789`）

#### 方法二：使用 @getidsbot
1. 在 Telegram 中搜索 **@getidsbot**
2. 发送任何消息
3. 复制显示的 **Your user ID**

#### 方法三：通过代码获取（如果你已经和 Bot 对话过）
1. 先和你的 Bot 对话（发送 `/start`）
2. 运行以下 Python 代码：
```python
import requests

BOT_TOKEN = "你的BotToken"

# 获取最近的消息
response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
data = response.json()

if data["ok"]:
    for update in data["result"]:
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            print(f"Chat ID: {chat_id}")
            break
```

### 3. 设置环境变量

#### Linux/macOS:
```bash
# 设置 Bot Token
export TELEGRAM_BOT_TOKEN="你的BotToken"

# 设置 Chat ID
export TELEGRAM_CHAT_ID="你的ChatID"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export TELEGRAM_BOT_TOKEN="你的BotToken"' >> ~/.bashrc
echo 'export TELEGRAM_CHAT_ID="你的ChatID"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows (PowerShell):
```powershell
# 设置 Bot Token
$env:TELEGRAM_BOT_TOKEN="你的BotToken"

# 设置 Chat ID
$env:TELEGRAM_CHAT_ID="你的ChatID"

# 永久设置（系统属性 -> 高级 -> 环境变量）
```

#### Windows (CMD):
```cmd
set TELEGRAM_BOT_TOKEN=你的BotToken
set TELEGRAM_CHAT_ID=你的ChatID
```

### 4. 测试配置

运行测试脚本：
```bash
python3 telegram_setup_test.py
```

如果一切正常，你会看到：
```
✅ Bot Token 有效！
✅ Chat ID 有效！测试消息已发送。
```

### 5. 运行主脚本

```bash
python3 github_trending_scraper_with_telegram.py
```

## 🔧 脚本功能

### 主脚本 (`github_trending_scraper_with_telegram.py`)

1. **抓取数据**：从 GitHub Trending 页面获取仓库信息
2. **过滤AI相关**：只保留 AI/LLM/Agent 相关仓库
3. **生成表格**：创建 Markdown 格式的表格
4. **保存文件**：保存到 `github_trending_ai.md`
5. **发送通知**：通过 Telegram Bot 发送通知

### 测试脚本 (`telegram_setup_test.py`)

1. 检查环境变量
2. 验证 Bot Token 有效性
3. 测试 Chat ID 是否正确
4. 发送测试消息

## 📱 Telegram 消息格式

脚本会发送格式化的消息：
```
🚀 GitHub Trending (AI/LLM/Agent相关) - 2026-02-19

1. alibaba/zvec
   ⭐ 5009 | A lightweight, lightning-fast, in-process vector database...
   🔗 https://github.com/alibaba/zvec

2. QwenLM/qwen-code
   ⭐ 18949 | An open-source AI agent that lives in your terminal.
   🔗 https://github.com/QwenLM/qwen-code

📊 总计: 8 个仓库
```

## ⚠️ 注意事项

1. **Bot Token 保密**：不要将 Bot Token 分享给他人或上传到公开仓库
2. **Chat ID 格式**：Chat ID 通常是数字，不是用户名
3. **消息长度限制**：Telegram 消息限制为 4096 字符，脚本会自动截断
4. **Markdown 支持**：脚本使用 Markdown 格式，确保消息可读性
5. **网络连接**：需要稳定的网络连接访问 Telegram API

## 🔄 自动化运行

### 使用 cron（Linux/macOS）

每天上午9点运行：
```bash
# 编辑 crontab
crontab -e

# 添加以下行（替换为你的路径）
0 9 * * * cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py
```

### 使用 Task Scheduler（Windows）

1. 打开 Task Scheduler
2. 创建基本任务
3. 设置每天运行
4. 程序：`python.exe`
5. 参数：`github_trending_scraper_with_telegram.py`
6. 起始于：脚本所在目录

## 🐛 故障排除

### 问题：Bot Token 无效
- 检查是否复制了完整的 Token
- 确保 Token 格式正确（包含冒号）
- 重新创建 Bot 获取新 Token

### 问题：Chat ID 无效
- 确认 Bot 已启动（发送 `/start`）
- 使用 @userinfobot 重新获取 Chat ID
- 确保使用的是数字 ID，不是用户名

### 问题：收不到消息
- 检查 Bot 是否被屏蔽
- 确认 Chat ID 是否正确
- 查看 Bot 的隐私设置（/setprivacy 命令）

### 问题：脚本运行但无输出
- 检查环境变量是否设置正确
- 运行测试脚本验证配置
- 查看 Python 错误信息

## 📞 支持

如果遇到问题：
1. 运行测试脚本查看详细错误
2. 检查环境变量设置
3. 确保网络可以访问 Telegram API
4. 查看脚本的打印输出

## 🔗 参考链接

- [Telegram Bot API 文档](https://core.telegram.org/bots/api)
- [Bot Father](https://t.me/botfather)
- [User Info Bot](https://t.me/userinfobot)
- [GitHub Trending](https://github.com/trending)