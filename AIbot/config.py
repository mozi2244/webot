"""
配置文件，定义AIbot相关的环境变量和默认参数
"""
from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path

# DeepSeek API配置
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# 机器人配置
BOT_NAME = os.environ.get("BOT_NAME", "AIbot")
BOT_DESCRIPTION = os.environ.get("BOT_DESCRIPTION", "基于DeepSeek的AI自动回复机器人")

# 存储配置
DATA_DIR = Path(__file__).parent / "data"
USER_CONFIG_FILE = DATA_DIR / "user_config.json"

# 确保数据目录存在
DATA_DIR.mkdir(exist_ok=True)

# 日志配置
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# 机器人默认设置
DEFAULT_PROMPT = os.environ.get("DEFAULT_PROMPT", """你是一个友好的聊天助手，请用简洁友好的语气回复用户的消息。\n如果用户问题涉及敏感内容，请礼貌拒绝。\n回复尽量简短，不超过100字。""")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 1000))
TEMPERATURE = float(os.environ.get("TEMPERATURE", 0.7))

# 新增：支持本地.env配置初始自动回复好友
DEFAULT_ENABLED_USERS = os.environ.get("DEFAULT_ENABLED_USERS", "")  # 逗号分隔的wxid字符串 