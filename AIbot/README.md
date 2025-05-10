# AIbot - 基于DeepSeek的微信AI自动回复机器人

这是一个连接到ComWeChatBotClient项目的AI自动回复机器人，它可以：

- 自动回复用户的私聊消息
- 支持选择性开启/关闭对特定用户的自动回复
- 使用DeepSeek API生成高质量回复
- 支持自定义提示词
- 支持会话上下文，保持对话连贯性

## 功能特点

- 🤖 基于DeepSeek API的智能回复
- 🔄 保持对话上下文，支持连贯对话
- 🔒 可选择性开启/关闭对特定用户的自动回复
- 🎯 支持自定义提示词，个性化回复风格
- 📝 完整的命令系统，方便管理
- 🔐 管理员控制功能，可远程管理

## 环境要求

- Python 3.7+
- 微信版本 3.7.0.30
- ComWeChatBotClient项目环境

## 安装步骤

1. 确保已经设置好ComWeChatBotClient环境
2. 安装依赖包：

```bash
pip install httpx loguru
```

3. 设置DeepSeek API密钥：

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="你的DeepSeek API密钥"

# 或者在.env文件中设置
# DEEPSEEK_API_KEY=你的DeepSeek API密钥
```

4. 设置管理员微信ID（可选）：

```bash
# Windows PowerShell
$env:ADMIN_WXID="管理员的微信ID"
```

## 使用方法

1. 运行ComWeChatBotClient服务端，确保开启HTTP API和事件功能：

在`.env`文件中配置：
```
enable_http_api=true
event_enabled=true
event_buffer_size=100
```

2. 启动AIbot：

```bash
cd AIbot
python run.py
```

## 用户命令

机器人支持以下命令：

- `/help` - 显示帮助信息
- `/on` - 开启AI自动回复
- `/off` - 关闭AI自动回复
- `/status` - 查看当前状态
- `/clear` - 清除聊天历史
- `/prompt <文本>` - 设置个性化提示词

## 管理员命令

如果你设置了管理员微信ID，以下命令可用：

- `/admin list` - 列出所有启用自动回复的用户
- `/admin enable <wxid>` - 为指定用户开启自动回复
- `/admin disable <wxid>` - 为指定用户关闭自动回复

## 配置选项

可以通过环境变量或者在`config.py`中设置以下配置：

- `DEEPSEEK_API_KEY` - DeepSeek API密钥
- `ONEBOT_API_URL` - OneBot API地址
- `ONEBOT_ACCESS_TOKEN` - OneBot访问令牌
- `ADMIN_WXID` - 管理员微信ID

## 目录结构

```
AIbot/
├── config.py          # 配置文件
├── bot.py             # 机器人主程序
├── command_handler.py # 命令处理器
├── deepseek_client.py # DeepSeek API客户端
├── message_handler.py # 消息处理器
├── session_manager.py # 会话管理器
├── user_manager.py    # 用户管理器
├── run.py             # 启动脚本
├── data/              # 数据目录
└── logs/              # 日志目录
```

## 注意事项

- 确保DeepSeek API密钥有效
- 使用管理命令需要设置管理员微信ID
- 机器人只响应私聊消息，不响应群聊消息

## 许可证

本项目使用AGPLv3许可证 