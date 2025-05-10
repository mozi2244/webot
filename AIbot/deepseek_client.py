"""
DeepSeek API客户端
"""
import json
import time
from typing import Dict, List, Optional, Union

import httpx

from .config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEFAULT_PROMPT, MAX_TOKENS, TEMPERATURE


class DeepSeekClient:
    """DeepSeek API客户端"""
    
    def __init__(self, api_key: str = DEEPSEEK_API_KEY, base_url: str = DEEPSEEK_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.default_prompt = DEFAULT_PROMPT
        self.model = "deepseek-chat"  # 使用deepseek-chat模型
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def generate_response(
        self,
        prompt: str,
        messages: List[Dict[str, str]],
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS
    ) -> Optional[str]:
        """生成回复"""
        if not self.api_key:
            print("错误: DeepSeek API密钥未设置")
            return "很抱歉，AI服务暂时不可用，请联系管理员设置API密钥。"

        # 添加系统提示词
        system_message = {"role": "system", "content": prompt or self.default_prompt}
        all_messages = [system_message] + messages
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": all_messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        return result["choices"][0]["message"]["content"]
                    else:
                        print(f"DeepSeek API返回了无效的响应: {result}")
                        return "AI生成回复失败，请稍后再试。"
                else:
                    print(f"DeepSeek API调用失败，状态码: {response.status_code}，响应: {response.text}")
                    return f"AI服务出现问题({response.status_code})，请稍后再试。"
                    
        except Exception as e:
            print(f"调用DeepSeek API时出错: {e}")
            return "很抱歉，调用AI服务时出现了错误，请稍后再试。"

# 创建全局DeepSeek客户端实例
deepseek_client = DeepSeekClient() 