"""
消息处理模块
"""
import asyncio
import json
import re
from typing import Dict, List, Optional, Union

from .command_handler import command_handler
from .deepseek_client import deepseek_client
from .session_manager import session_manager
from .user_manager import user_manager


class MessageHandler:
    """消息处理器"""
    
    def __init__(self):
        """初始化消息处理器"""
        self.is_processing = {}  # 用于跟踪正在处理的消息，避免重复处理
    
    async def handle_message(self, message: dict) -> Optional[dict]:
        """
        处理接收到的消息
        
        Args:
            message: 消息数据字典
            
        Returns:
            回复消息数据或None
        """
        # 增加调试日志，打印收到的消息内容
        print(f"[调试] handle_message收到消息: {message}")
        # 提取消息类型和内容
        try:
            msg_type = message.get("type")
            detail_type = message.get("detail_type")
            print(f"[调试] 消息类型: {msg_type}, detail_type: {detail_type}")
            if msg_type != "message" or detail_type != "private":
                print("[调试] 非私聊消息，忽略")
                return None  # 只处理私聊消息
            
            wxid = message.get("user_id", "")
            print(f"[调试] 用户wxid: {wxid}")
            if not wxid:
                print("[调试] 未获取到用户wxid")
                return None
            
            # 避免重复处理同一条消息
            msg_id = message.get("message_id", "")
            if msg_id and self.is_processing.get(msg_id):
                print(f"[调试] 消息ID {msg_id} 正在处理中，跳过")
                return None
            
            if msg_id:
                self.is_processing[msg_id] = True
            
            content = self._extract_text_content(message)
            print(f"[调试] 提取到的文本内容: {content}")
            if not content:
                print("[调试] 未提取到文本内容")
                return None
            
            # 处理命令
            command_result = await command_handler.handle_command(wxid, content)
            print(f"[调试] 命令处理结果: {command_result}")
            if command_result is not None:
                # 是命令，直接返回命令处理结果
                self._clear_processing_state(msg_id)
                return {"user_id": wxid, "detail_type": "private", "message": [{"type": "text", "data": {"text": command_result}}]}
            
            # 检查是否启用了自动回复
            if not user_manager.is_auto_reply_enabled(wxid):
                print(f"[调试] 用户 {wxid} 未开启自动回复")
                self._clear_processing_state(msg_id)
                return None
            
            # 处理普通消息
            return await self._process_ai_message(wxid, content, msg_id)
            
        except Exception as e:
            print(f"处理消息时出错: {e}")
            self._clear_processing_state(msg_id if 'msg_id' in locals() else None)
            return None
    
    def _extract_text_content(self, message: dict) -> Optional[str]:
        """提取消息中的文本内容"""
        if "message" not in message:
            print("[调试] 消息中无'message'字段")
            return None
            
        # 从消息段中提取文本
        text_segments = []
        for segment in message["message"]:
            print(f"[调试] 消息段: {segment}")
            if segment.get("type") == "text" and "data" in segment and "text" in segment["data"]:
                text_segments.append(segment["data"]["text"])
        print(f"[调试] 提取到的所有文本段: {text_segments}")
        return "".join(text_segments) if text_segments else None
    
    async def _process_ai_message(self, wxid: str, content: str, msg_id: Optional[str]) -> Optional[dict]:
        """处理需要AI回复的消息"""
        try:
            # 记录用户消息到会话
            session_manager.add_message(wxid, "user", content)
            
            # 获取历史消息
            history = session_manager.get_history(wxid)
            
            # 获取用户自定义提示词
            custom_prompt = user_manager.get_custom_prompt(wxid)
            
            # 生成回复
            reply = await deepseek_client.generate_response(custom_prompt, history)
            
            if reply:
                # 记录AI回复到会话
                session_manager.add_message(wxid, "assistant", reply)
                
                # 构建回复消息
                return {
                    "user_id": wxid,
                    "detail_type": "private",
                    "message": [{"type": "text", "data": {"text": reply}}]
                }
            
            return None
        finally:
            self._clear_processing_state(msg_id)
    
    def _clear_processing_state(self, msg_id: Optional[str]) -> None:
        """清除消息处理状态"""
        if msg_id and msg_id in self.is_processing:
            del self.is_processing[msg_id]


# 创建全局消息处理器实例
message_handler = MessageHandler() 