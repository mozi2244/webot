![ComWeChatBotClient](https://socialify.git.ci/JustUndertaker/ComWeChatBotClient/image?description=1&font=Inter&name=1&pattern=Circuit%20Board&theme=Auto)
<p align="center">
    <a href="https://onebot.dev/"><img src="https://img.shields.io/badge/OneBot-12-black?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHAAAABwCAMAAADxPgR5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAAxQTFRF////29vbr6+vAAAAk1hCcwAAAAR0Uk5T////AEAqqfQAAAKcSURBVHja7NrbctswDATQXfD//zlpO7FlmwAWIOnOtNaTM5JwDMa8E+PNFz7g3waJ24fviyDPgfhz8fHP39cBcBL9KoJbQUxjA2iYqHL3FAnvzhL4GtVNUcoSZe6eSHizBcK5LL7dBr2AUZlev1ARRHCljzRALIEog6H3U6bCIyqIZdAT0eBuJYaGiJaHSjmkYIZd+qSGWAQnIaz2OArVnX6vrItQvbhZJtVGB5qX9wKqCMkb9W7aexfCO/rwQRBzsDIsYx4AOz0nhAtWu7bqkEQBO0Pr+Ftjt5fFCUEbm0Sbgdu8WSgJ5NgH2iu46R/o1UcBXJsFusWF/QUaz3RwJMEgngfaGGdSxJkE/Yg4lOBryBiMwvAhZrVMUUvwqU7F05b5WLaUIN4M4hRocQQRnEedgsn7TZB3UCpRrIJwQfqvGwsg18EnI2uSVNC8t+0QmMXogvbPg/xk+Mnw/6kW/rraUlvqgmFreAA09xW5t0AFlHrQZ3CsgvZm0FbHNKyBmheBKIF2cCA8A600aHPmFtRB1XvMsJAiza7LpPog0UJwccKdzw8rdf8MyN2ePYF896LC5hTzdZqxb6VNXInaupARLDNBWgI8spq4T0Qb5H4vWfPmHo8OyB1ito+AysNNz0oglj1U955sjUN9d41LnrX2D/u7eRwxyOaOpfyevCWbTgDEoilsOnu7zsKhjRCsnD/QzhdkYBLXjiK4f3UWmcx2M7PO21CKVTH84638NTplt6JIQH0ZwCNuiWAfvuLhdrcOYPVO9eW3A67l7hZtgaY9GZo9AFc6cryjoeFBIWeU+npnk/nLE0OxCHL1eQsc1IciehjpJv5mqCsjeopaH6r15/MrxNnVhu7tmcslay2gO2Z1QfcfX0JMACG41/u0RrI9QAAAABJRU5ErkJggg==" alt="onebot12"></a>
    <a href="https://github.com/JustUndertaker/ComWeChatBotClient/blob/main/LICENSE"><img src="https://img.shields.io/github/license/JustUndertaker/ComWeChatBotClient" alt="License"></a>
    <a href="https://github.com/JustUndertaker/ComWeChatBotClient/releases"><img src="https://img.shields.io/github/v/release/JustUndertaker/ComWeChatBotClient?color=blueviolet&include_prereleases" alt="release"></a>
</p>

# ComWeChatBotClient

## 项目简介 | Project Introduction

ComWeChatBotClient 是基于 PC 微信的自动化机器人客户端，支持 [OneBot 12](https://onebot.dev/) 协议，集成 AI 智能回复（DeepSeek），可实现微信消息的自动处理、智能对话、远程管理等功能。

ComWeChatBotClient is an automation bot client for PC WeChat, supporting the [OneBot 12](https://onebot.dev/) protocol. It integrates AI-powered auto-reply (DeepSeek) and enables automatic message handling, intelligent conversation, and remote management for WeChat.

## 主要功能 | Main Features

- 支持 OneBot 12 协议（HTTP、Webhook、正/反向 WebSocket）
- 微信私聊消息自动回复，集成 DeepSeek AI
- 支持自定义提示词、上下文对话
- 管理员远程控制与多用户管理
- 丰富的命令系统，支持个性化配置
- 日志、数据、文件缓存管理

- Supports OneBot 12 protocol (HTTP, Webhook, Forward/Reverse WebSocket)
- Auto-reply for WeChat private messages with DeepSeek AI
- Custom prompt and context-aware conversation
- Remote admin control and multi-user management
- Rich command system and personalized configuration
- Logging, data, and file cache management

## 目录结构 | Directory Structure

```
├── AIbot/                # AI 智能回复模块（AI Auto-reply Module）
├── wechatbot_client/     # 微信客户端核心（WeChat Client Core）
├── data/                 # 数据存储（Data Storage）
├── file_cache/           # 文件缓存（File Cache）
├── log/                  # 日志文件（Logs）
├── docs/                 # 项目文档（Documentation）
├── main.py               # 启动入口（Entry Point）
├── requirements.txt      # Python依赖（Python Requirements）
├── package.json          # Node依赖（Node Requirements）
└── README.md             # 项目说明（Project Readme）
```

## 安装与使用 | Installation & Usage

1. **环境准备 | Environment**
   - Windows 10/11，Python 3.7+
   - 安装依赖 Install dependencies:
     ```powershell
     pip install -r requirements.txt
     pip install httpx loguru
     ```
2. **配置微信与API | Configure WeChat & API**
   - 下载并安装支持的微信版本（3.7.0.30）
   - 配置 `.env` 文件或环境变量，设置 DeepSeek API 密钥、OneBot API 地址等
3. **启动服务 | Start Service**
   - 启动微信客户端和 ComWeChatBotClient 服务端
   - 启动 AIbot：
     ```powershell
     cd AIbot
     python run.py
     ```

## 配置说明 | Configuration

- `DEEPSEEK_API_KEY`：DeepSeek API 密钥（必填 Required）
- `ONEBOT_API_URL`：OneBot API 地址（如 http://127.0.0.1:8000）
- `ONEBOT_ACCESS_TOKEN`：OneBot 访问令牌（可选 Optional）
- `ADMIN_WXID`：管理员微信ID（可选 Optional）
- 其他参数详见 `AIbot/config.py` 和 `.env` 文件

## 常见问题 | FAQ

- **Q: 支持哪些微信版本？**
  - A: 仅支持 3.7.0.30，下载链接见上文。
- **Q: 如何自定义AI回复风格？**
  - A: 通过 `/prompt <内容>` 命令或配置自定义提示词。
- **Q: 如何添加/移除自动回复用户？**
  - A: 普通用户可用 `/on` `/off`，管理员可用 `/admin enable <wxid>` `/admin disable <wxid>`。
- **Q: 日志和数据存储在哪里？**
  - A: 日志在 `log/`，用户数据在 `data/`。

## 开源协议 | License

本项目采用 [AGPLv3](https://github.com/JustUndertaker/ComWeChatBotClient/blob/main/LICENSE) 协议开源，禁止商业用途。

This project is licensed under [AGPLv3](https://github.com/JustUndertaker/ComWeChatBotClient/blob/main/LICENSE), commercial use is NOT allowed.
