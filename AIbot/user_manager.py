"""
用户管理器，用于管理用户的自动回复设置
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
import asyncio
import httpx

from .config import USER_CONFIG_FILE, DEFAULT_ENABLED_USERS, BOT_NAME, BOT_DESCRIPTION, LOG_LEVEL, DEFAULT_PROMPT, MAX_TOKENS, TEMPERATURE, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# 新增：读取OneBot API地址
ONEBOT_API_URL = os.environ.get("ONEBOT_API_URL", "http://127.0.0.1:8000")
ONEBOT_ACCESS_TOKEN = os.environ.get("ONEBOT_ACCESS_TOKEN", "")

class UserManager:
    """用户管理器，管理用户自动回复设置"""

    def __init__(self):
        self.enabled_users: Set[str] = set()
        self.user_config: Dict[str, Dict] = {}
        # 只加载配置，不再做微信号映射
        asyncio.get_event_loop().run_until_complete(self.load_config_async())

    async def load_config_async(self) -> None:
        """异步加载用户配置，不再做微信号映射"""
        if os.path.exists(USER_CONFIG_FILE):
            try:
                with open(USER_CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.user_config = config.get("user_config", {})
                    self.enabled_users = set(config.get("enabled_users", []))
            except Exception as e:
                print(f"加载用户配置出错: {e}")
                self.user_config = {}
                self.enabled_users = set()
        else:
            # 创建默认配置，并根据.env自动添加初始用户
            if DEFAULT_ENABLED_USERS:
                wxids = [wxid.strip() for wxid in DEFAULT_ENABLED_USERS.split(',') if wxid.strip()]
                self.enabled_users = set(wxids)
                for wxid in wxids:
                    if wxid not in self.user_config:
                        self.user_config[wxid] = {"custom_prompt": None}
            self.save_config()

    def save_config(self) -> None:
        """保存用户配置"""
        config = {
            "user_config": self.user_config,
            "enabled_users": list(self.enabled_users)
        }
        os.makedirs(os.path.dirname(USER_CONFIG_FILE), exist_ok=True)
        with open(USER_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def enable_auto_reply(self, wxid: str) -> bool:
        """开启用户的自动回复"""
        self.enabled_users.add(wxid)
        if wxid not in self.user_config:
            self.user_config[wxid] = {"custom_prompt": None}
        self.save_config()
        return True

    def disable_auto_reply(self, wxid: str) -> bool:
        """关闭用户的自动回复"""
        if wxid in self.enabled_users:
            self.enabled_users.remove(wxid)
            self.save_config()
            return True
        return False

    def is_auto_reply_enabled(self, wxid: str) -> bool:
        """检查用户是否开启了自动回复"""
        return wxid in self.enabled_users
    
    def get_all_enabled_users(self) -> List[str]:
        """获取所有开启自动回复的用户列表"""
        return list(self.enabled_users)
    
    def set_custom_prompt(self, wxid: str, prompt: str) -> None:
        """设置用户自定义的提示词"""
        if wxid not in self.user_config:
            self.user_config[wxid] = {}
        self.user_config[wxid]["custom_prompt"] = prompt
        self.save_config()
    
    def get_custom_prompt(self, wxid: str) -> Optional[str]:
        """获取用户自定义的提示词"""
        if wxid in self.user_config and "custom_prompt" in self.user_config[wxid]:
            return self.user_config[wxid]["custom_prompt"]
        return None


# 创建全局用户管理器实例
user_manager = UserManager() 