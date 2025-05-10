"""
AI机器人主程序
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import httpx
from loguru import logger

# 将项目根目录添加到路径
WECHATBOT_PATH = str(Path(__file__).parent.parent.absolute())
if WECHATBOT_PATH not in sys.path:
    sys.path.insert(0, WECHATBOT_PATH)

from AIbot.command_handler import command_handler
from AIbot.config import DEEPSEEK_API_KEY
from AIbot.message_handler import message_handler
from AIbot.session_manager import session_manager
from AIbot.user_manager import user_manager


class AIBot:
    """AI机器人类"""
    
    def __init__(
        self,
        api_url: str = "http://127.0.0.1:8000",
        access_token: Optional[str] = None,
        admin_wxid: Optional[str] = None
    ):
        """
        初始化AI机器人
        
        Args:
            api_url: OneBot API的地址
            access_token: 访问令牌
            admin_wxid: 管理员微信ID
        """
        self.api_url = api_url.rstrip("/")
        self.access_token = access_token
        self.running = False
        
        # 新增：调试输出API地址和Token（仅显示前后几位，防止泄露）
        logger.info(f"[调试] OneBot API地址: {self.api_url}")
        if self.access_token:
            logger.info(f"[调试] OneBot Access Token: {self.access_token[:3]}***{self.access_token[-3:]}")
        else:
            logger.info("[调试] 未设置OneBot Access Token")
        
        # 设置管理员
        if admin_wxid:
            command_handler.admin_wxid = admin_wxid
        
        # 设置日志
        logger.remove()
        logger.add(
            sys.stdout,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
        )
        logger.add(
            Path(__file__).parent / "logs" / "bot_{time}.log",
            rotation="1 day",
            retention="7 days",
            level="INFO"
        )
        
        # 检查API密钥
        if not DEEPSEEK_API_KEY:
            logger.warning("未设置DeepSeek API密钥，请设置环境变量DEEPSEEK_API_KEY")
    
    async def _call_api(self, action: str, params: Dict[str, Any] = None) -> Dict:
        """
        调用OneBot API
        
        Args:
            action: 动作名称
            params: 参数
            
        Returns:
            API返回结果
        """
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        # 修改：始终带上params字段
        data = {"action": action, "params": params if params is not None else {}}
        
        logger.debug(f"[调试] 调用API: {self.api_url}/, action: {action}, params: {params}, headers: {headers}")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/",
                    headers=headers,
                    json=data
                )
                logger.debug(f"[调试] API响应状态: {response.status_code}, 响应内容: {response.text}")
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"API调用失败: {response.status_code} {response.text}")
                    return {"status": "failed", "retcode": response.status_code, "response": response.text}
        except Exception as e:
            import traceback
            logger.error(f"API调用出错: {e}\n[调试] 异常堆栈: {traceback.format_exc()}")
            return {"status": "failed", "retcode": -1, "message": str(e)}
    
    async def _process_event(self, event: Dict) -> None:
        """
        处理事件
        
        Args:
            event: 事件数据
        """
        try:
            if event.get("type") == "message" and event.get("detail_type") == "private":
                # 处理私聊消息
                logger.info(f"收到私聊消息: {event.get('user_id')} -> {self._get_message_text(event)}")
                
                # 处理消息并获取回复
                reply = await message_handler.handle_message(event)
                logger.info(f"[调试] handle_message返回: {reply}")
                
                # 发送回复
                if reply:
                    logger.info(f"发送回复: {reply.get('user_id')} <- {self._get_message_text(reply)}")
                    result = await self._call_api("send_message", reply)
                    logger.info(f"[调试] send_message API返回: {result}")
        except Exception as e:
            logger.error(f"处理事件出错: {e}")
    
    def _get_message_text(self, event: Dict) -> str:
        """从事件中提取消息文本用于日志输出"""
        try:
            if "message" in event:
                text_parts = []
                for segment in event["message"]:
                    if segment.get("type") == "text" and "data" in segment and "text" in segment["data"]:
                        text_parts.append(segment["data"]["text"])
                return "".join(text_parts) if text_parts else "[非文本消息]"
            return "[无消息内容]"
        except Exception:
            return "[消息解析错误]"
    
    async def _fetch_events(self) -> List[Dict]:
        """获取最新事件"""
        result = await self._call_api("get_latest_events", {"timeout": 30})
        if result.get("status") == "ok" and "data" in result:
            # 兼容data为list或dict
            if isinstance(result["data"], list):
                return result["data"]
            elif isinstance(result["data"], dict) and "events" in result["data"]:
                return result["data"]["events"]
        return []
    
    async def run(self) -> None:
        """运行机器人"""
        self.running = True
        logger.info("AI机器人启动...")
        # 新增：输出当前环境变量相关信息
        logger.info(f"[调试] 当前ONEBOT_API_URL: {os.environ.get('ONEBOT_API_URL')}")
        logger.info(f"[调试] 当前ONEBOT_ACCESS_TOKEN: {os.environ.get('ONEBOT_ACCESS_TOKEN')}")
        logger.info(f"[调试] 当前ADMIN_WXID: {os.environ.get('ADMIN_WXID')}")
        
        # 检查自身在线状态
        status = await self._call_api("get_self_info")
        if status.get("status") != "ok":
            logger.error("无法连接到OneBot API，请检查配置")
            logger.error(f"[调试] OneBot API连接失败详细返回: {status}")
            logger.error("[调试] 请确认OneBot服务已启动，API地址和Token配置正确，且网络可达。")
            return
        
        logger.info(f"成功连接到OneBot API: {self.api_url}")
        logger.info(f"机器人信息: {status.get('data', {})}")
        
        # 定期清理过期会话
        asyncio.create_task(self._session_cleanup_task())
        
        # 主事件循环
        while self.running:
            try:
                events = await self._fetch_events()
                for event in events:
                    asyncio.create_task(self._process_event(event))
                await asyncio.sleep(1)  # 每秒轮询一次，降低请求频率
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"事件获取出错: {e}")
                await asyncio.sleep(5)
    
    async def _session_cleanup_task(self) -> None:
        """定期清理过期会话的任务"""
        while self.running:
            try:
                count = session_manager.clear_expired_sessions()
                if count > 0:
                    logger.info(f"已清理 {count} 个过期会话")
            except Exception as e:
                logger.error(f"会话清理出错: {e}")
            
            await asyncio.sleep(3600)  # 每小时清理一次
    
    def stop(self) -> None:
        """停止机器人"""
        self.running = False
        logger.info("AI机器人停止...")


async def run_bot():
    """运行机器人的入口函数"""
    # 从环境变量获取配置
    api_url = os.environ.get("ONEBOT_API_URL", "http://127.0.0.1:8000")
    access_token = os.environ.get("ONEBOT_ACCESS_TOKEN", "")
    admin_wxid = os.environ.get("ADMIN_WXID")
    
    bot = AIBot(api_url, access_token, admin_wxid)
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        bot.stop()
    except Exception as e:
        logger.exception(f"机器人运行出错: {e}")
    finally:
        logger.info("机器人已关闭")


def main():
    """主函数"""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.exception(f"程序出错: {e}")


if __name__ == "__main__":
    main() 