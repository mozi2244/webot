"""
会话管理器，用于管理用户的对话历史
"""
import time
from collections import defaultdict, deque
from typing import Dict, List, Optional


class SessionManager:
    """会话管理器，负责管理每个用户的对话历史和会话超时。"""
    
    def __init__(self, max_history: int = 10, session_timeout: int = 1800):
        """
        初始化会话管理器
        参数：
            max_history: 每个用户保存的最大消息数
            session_timeout: 会话超时时间（秒）
        """
        self.max_history = max_history
        self.session_timeout = session_timeout
        self.sessions: Dict[str, Dict] = defaultdict(dict)
    
    def add_message(self, wxid: str, role: str, content: str) -> None:
        """
        添加消息到用户会话历史
        参数：
            wxid: 用户ID
            role: 消息角色（user/assistant）
            content: 消息内容
        """
        if wxid not in self.sessions:
            self.sessions[wxid] = {
                "messages": deque(maxlen=self.max_history),
                "last_time": time.time()
            }
        
        self.sessions[wxid]["messages"].append({"role": role, "content": content})
        self.sessions[wxid]["last_time"] = time.time()
    
    def get_history(self, wxid: str, max_count: Optional[int] = None) -> List[Dict[str, str]]:
        """
        获取用户的会话历史
        参数：
            wxid: 用户ID
            max_count: 最大返回消息数，None为全部
        返回：消息历史列表
        """
        if wxid not in self.sessions:
            return []
        
        # 检查会话是否超时
        if time.time() - self.sessions[wxid]["last_time"] > self.session_timeout:
            self.clear_history(wxid)
            return []
        
        messages = list(self.sessions[wxid]["messages"])
        if max_count is not None and max_count > 0:
            messages = messages[-max_count:]
        
        return messages
    
    def clear_history(self, wxid: str) -> None:
        """
        清除指定用户的会话历史
        参数：wxid: 用户ID
        """
        if wxid in self.sessions:
            del self.sessions[wxid]
    
    def clear_expired_sessions(self) -> int:
        """
        清理所有过期会话
        返回：清理的会话数量
        """
        current_time = time.time()
        expired_wxids = [
            wxid for wxid, session in self.sessions.items()
            if current_time - session["last_time"] > self.session_timeout
        ]
        
        for wxid in expired_wxids:
            self.clear_history(wxid)
        
        return len(expired_wxids)


# 创建全局会话管理器实例
session_manager = SessionManager() 