# Cron Job 设置指南

## 📅 定时任务配置

### 基本cron表达式

```
# 格式: 分 时 日 月 周 命令
# *    - 任何值
# ,    - 值列表分隔符
# -    - 范围
# /    - 步长值

# 每天上午9点运行
0 9 * * * /path/to/command

# 每天上午9点和下午5点运行
0 9,17 * * * /path/to/command

# 每30分钟运行一次
*/30 * * * * /path/to/command

# 每周一上午9点运行
0 9 * * 1 /path/to/command

# 每月1号上午9点运行
0 9 1 * * /path/to/command
```

### 设置GitHub Trending Scraper的cron job

#### 方法1: 使用crontab命令

```bash
# 编辑当前用户的crontab
crontab -e

# 添加以下行（根据你的需求选择时间）
# 每天上午9点运行
0 9 * * * cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py >> /tmp/github_trending.log 2>&1

# 每天上午9点和下午9点运行
0 9,21 * * * cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py >> /tmp/github_trending.log 2>&1

# 每6小时运行一次（0点、6点、12点、18点）
0 */6 * * * cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py >> /tmp/github_trending.log 2>&1
```

#### 方法2: 使用系统cron文件

```bash
# 创建系统cron文件
sudo nano /etc/cron.d/github_trending

# 添加以下内容
# 每天上午9点运行，以指定用户身份
0 9 * * * username cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py >> /var/log/github_trending.log 2>&1
```

#### 方法3: 使用脚本文件

创建脚本文件 `/usr/local/bin/run_github_trending.sh`:

```bash
#!/bin/bash
# GitHub Trending Scraper 运行脚本

cd /path/to/your/workspace
source .env 2>/dev/null || true
/usr/bin/python3 github_trending_scraper_with_telegram.py >> /var/log/github_trending.log 2>&1

# 发送运行状态通知（可选）
if [ $? -eq 0 ]; then
    echo "✅ GitHub Trending Scraper 运行成功 - $(date)" >> /var/log/github_trending_status.log
else
    echo "❌ GitHub Trending Scraper 运行失败 - $(date)" >> /var/log/github_trending_status.log
fi
```

设置权限并添加到crontab:

```bash
chmod +x /usr/local/bin/run_github_trending.sh

# 添加到crontab
0 9 * * * /usr/local/bin/run_github_trending.sh
```

## 🔧 环境变量处理

### 在cron中使用.env文件

cron job的环境与用户shell环境不同，需要特别注意环境变量。

#### 方案1: 在脚本中加载.env

脚本已经使用 `python-dotenv` 自动加载 `.env` 文件，确保cron job的工作目录包含 `.env` 文件。

#### 方案2: 在cron命令中设置环境变量

```bash
# 直接在cron命令中设置环境变量
0 9 * * * TELEGRAM_BOT_TOKEN="your_token" TELEGRAM_CHAT_ID="your_chat_id" cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py
```

#### 方案3: 使用env文件

创建环境变量文件 `/etc/github_trending.env`:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GIT_AUTO_PUSH=true
```

在cron中使用:

```bash
0 9 * * * . /etc/github_trending.env && cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py
```

## 📊 日志管理

### 日志文件配置

```bash
# 创建日志目录
sudo mkdir -p /var/log/github_trending
sudo chown $USER:$USER /var/log/github_trending

# 带时间戳的日志
0 9 * * * cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py >> /var/log/github_trending/$(date +\%Y-\%m-\%d).log 2>&1

# 轮转日志（使用logrotate）
sudo nano /etc/logrotate.d/github_trending
```

logrotate配置示例:

```bash
/var/log/github_trending/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
```

### 监控日志

```bash
# 查看最新日志
tail -f /var/log/github_trending/latest.log

# 查看错误
grep -i error /var/log/github_trending/*.log

# 统计运行情况
grep -c "脚本执行完成" /var/log/github_trending/*.log
```

## 🐛 故障排除

### 常见问题

#### 问题1: cron job没有运行
```bash
# 检查cron服务状态
sudo systemctl status cron

# 检查cron日志
sudo grep CRON /var/log/syslog

# 测试cron命令
cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py
```

#### 问题2: 环境变量未加载
```bash
# 在cron命令中打印环境
0 9 * * * env > /tmp/cron_env.log && cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py

# 检查.env文件路径
0 9 * * * pwd > /tmp/cron_pwd.log && ls -la .env >> /tmp/cron_pwd.log && cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py
```

#### 问题3: Python路径问题
```bash
# 使用绝对路径
which python3
# 输出: /usr/bin/python3

# 在cron中使用绝对路径
0 9 * * * cd /path/to/your/workspace && /usr/bin/python3 github_trending_scraper_with_telegram.py
```

#### 问题4: Git操作失败
```bash
# 检查Git配置
git config --list

# 确保有写权限
ls -la .git

# 测试Git命令
git status
git add .
git commit -m "test"
```

### 调试脚本

创建调试版本脚本 `debug_github_trending.py`:

```python
#!/usr/bin/env python3
import sys
import os

print("Python路径:", sys.executable)
print("工作目录:", os.getcwd())
print("环境变量:")
for key in ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "PATH"]:
    print(f"  {key}: {os.getenv(key, '未设置')}")

# 导入检查
try:
    import requests
    print("✅ requests 已安装")
except ImportError as e:
    print(f"❌ requests 导入失败: {e}")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv 已安装")
except ImportError as e:
    print(f"❌ python-dotenv 导入失败: {e}")
```

## 🔄 自动化部署脚本

创建部署脚本 `deploy_cron.sh`:

```bash
#!/bin/bash
# GitHub Trending Scraper cron job部署脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="0 9 * * * cd $SCRIPT_DIR && /usr/bin/python3 github_trending_scraper_with_telegram.py >> $SCRIPT_DIR/cron.log 2>&1"

echo "🔧 部署GitHub Trending Scraper cron job"
echo "========================================"

# 检查当前cron jobs
echo -e "\n📋 当前cron jobs:"
crontab -l | grep -v "^#" | grep -v "^$" || echo "  无"

# 移除旧的cron job
echo -e "\n🗑️  移除旧的cron job..."
(crontab -l | grep -v "github_trending_scraper_with_telegram.py" | grep -v "^#" | grep -v "^$") | crontab -

# 添加新的cron job
echo -e "\n➕ 添加新的cron job..."
(crontab -l; echo "$CRON_JOB") | crontab -

echo -e "\n✅ 部署完成！"
echo "Cron job: $CRON_JOB"
echo ""
echo "📊 验证部署:"
crontab -l | grep "github_trending_scraper_with_telegram.py"
```

## 📱 通知集成

### 失败通知

修改脚本以在失败时发送Telegram通知:

```python
# 在脚本开头添加
import traceback

try:
    # 主逻辑
    main()
except Exception as e:
    error_msg = f"❌ GitHub Trending Scraper 运行失败\n\n错误: {str(e)}\n\n跟踪: {traceback.format_exc()[:1000]}"
    # 发送错误通知到Telegram
    send_telegram_message(bot_token, chat_id, error_msg)
    raise
```

### 运行状态报告

创建状态报告脚本:

```bash
#!/bin/bash
# 发送每日运行状态报告

LOG_FILE="/var/log/github_trending/latest.log"
STATUS=""

if grep -q "脚本执行完成" "$LOG_FILE"; then
    REPOS=$(grep -o "总计: [0-9]* 个仓库" "$LOG_FILE" | tail -1)
    STATUS="✅ 运行成功 - $REPOS"
else
    STATUS="❌ 运行失败"
    ERROR=$(grep -i "error\|失败\|exception" "$LOG_FILE" | tail -3)
    STATUS="$STATUS\n错误: $ERROR"
fi

# 发送到Telegram
python3 -c "
import requests
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

if bot_token and chat_id:
    import sys
    status = sys.argv[1]
    requests.post(f'https://api.telegram.org/bot{bot_token}/sendMessage', 
                  json={'chat_id': chat_id, 'text': status, 'parse_mode': 'Markdown'})
" "$STATUS"
```

## 🎯 最佳实践

1. **使用绝对路径**: 在cron中使用所有命令的绝对路径
2. **设置工作目录**: 使用 `cd` 命令确保在正确的目录中运行
3. **记录日志**: 重定向输出到日志文件以便调试
4. **测试配置**: 先手动测试，再添加到cron
5. **监控运行**: 定期检查日志和运行状态
6. **错误处理**: 脚本应包含完善的错误处理
7. **安全考虑**: 不要将敏感信息硬编码在脚本中
8. **版本控制**: 使用Git管理脚本和配置