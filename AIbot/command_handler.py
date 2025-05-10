"""
命令处理器，用于处理用户命令和管理员命令
"""
import re
from typing import Dict, Optional, Tuple

from .user_manager import user_manager
from .session_manager import session_manager


class CommandHandler:
    """命令处理器，负责解析和执行用户/管理员命令"""
    
    def __init__(self, admin_wxid: Optional[str] = None):
        """
        初始化命令处理器
        参数：
            admin_wxid: 管理员微信ID
        """
        self.admin_wxid = admin_wxid
        self.commands = {
            r"^/help\s*$": self.help_command,
            r"^/on\s*$": self.enable_auto_reply,
            r"^/off\s*$": self.disable_auto_reply,
            r"^/status\s*$": self.status_command,
            r"^/clear\s*$": self.clear_history,
            r"^/prompt (.+)$": self.set_prompt,
            # 以下是管理员命令
            r"^/admin list$": self.list_enabled_users,
            r"^/admin enable (.+)$": self.admin_enable_user,
            r"^/admin disable (.+)$": self.admin_disable_user,
        }
    
    def is_command(self, text: str) -> bool:
        """
        判断文本是否为命令（以/开头）
        参数：text: 文本内容
        返回：是否为命令
        """
        return text.startswith("/")
    
    async def handle_command(self, wxid: str, text: str) -> Optional[str]:
        """
        处理命令文本，分发到对应命令处理函数
        参数：
            wxid: 用户微信ID
            text: 命令文本
        返回：命令处理结果字符串或None
        """
        print(f"[调试] handle_command收到: '{text}'")
        if not self.is_command(text):
            return None
        
        for pattern, handler in self.commands.items():
            match = re.match(pattern, text.strip())
            if match:
                args = match.groups()
                return await handler(wxid, *args)
        
        return "未知命令，发送 /help 查看帮助"
    
    async def help_command(self, wxid: str) -> str:
        """
        帮助命令，返回命令帮助信息
        """
        help_text = """AI机器人命令帮助：
/on - 开启AI自动回复
/off - 关闭AI自动回复
/status - 查看当前状态
/clear - 清除聊天历史
/prompt <文本> - 设置个性化提示词

发送任何不以/开头的消息将直接与AI对话"""

        if wxid == self.admin_wxid:
            help_text += """

管理员命令：
/admin list - 列出所有启用自动回复的用户
/admin enable <wxid> - 为指定用户开启自动回复
/admin disable <wxid> - 为指定用户关闭自动回复"""
        
        return help_text
    
    async def enable_auto_reply(self, wxid: str) -> str:
        """
        开启AI自动回复
        """
        user_manager.enable_auto_reply(wxid)
        return "已开启AI自动回复功能"
    
    async def disable_auto_reply(self, wxid: str) -> str:
        """
        关闭AI自动回复
        """
        user_manager.disable_auto_reply(wxid)
        return "已关闭AI自动回复功能"
    
    async def status_command(self, wxid: str) -> str:
        """
        查询当前AI自动回复状态和个性化提示词
        """
        enabled = user_manager.is_auto_reply_enabled(wxid)
        status = "已开启" if enabled else "已关闭"
        custom_prompt = user_manager.get_custom_prompt(wxid)
        prompt_info = f"\n当前提示词: {custom_prompt}" if custom_prompt else ""
        return f"AI自动回复功能: {status}{prompt_info}"
    
    async def clear_history(self, wxid: str) -> str:
        """
        清除当前用户的聊天历史
        """
        session_manager.clear_history(wxid)
        return "已清除聊天历史记录"
    
    async def set_prompt(self, wxid: str, prompt: str) -> str:
        """
        设置个性化提示词
        """
        user_manager.set_custom_prompt(wxid, prompt)
        return f"已设置个性化提示词:\n{prompt}"
    
    async def list_enabled_users(self, wxid: str) -> str:
        """
        管理员命令：列出所有已启用自动回复的用户
        """
        if wxid != self.admin_wxid:
            return "权限不足，此命令仅管理员可用"
        
        users = user_manager.get_all_enabled_users()
        if not users:
            return "当前没有用户启用AI自动回复"
        
        return "已启用AI自动回复的用户：\n" + "\n".join(users)
    
    async def admin_enable_user(self, wxid: str, target_wxid: str) -> str:
        """
        管理员命令：为指定用户开启自动回复
        """
        if wxid != self.admin_wxid:
            return "权限不足，此命令仅管理员可用"
        
        user_manager.enable_auto_reply(target_wxid)
        return f"已为用户 {target_wxid} 开启AI自动回复"
    
    async def admin_disable_user(self, wxid: str, target_wxid: str) -> str:
        """
        管理员命令：为指定用户关闭自动回复
        """
        if wxid != self.admin_wxid:
            return "权限不足，此命令仅管理员可用"
        
        success = user_manager.disable_auto_reply(target_wxid)
        if success:
            return f"已为用户 {target_wxid} 关闭AI自动回复"
        else:
            return f"用户 {target_wxid} 未开启AI自动回复"


# 创建全局命令处理器实例
command_handler = CommandHandler() 