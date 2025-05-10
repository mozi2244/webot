#!/usr/bin/env python
"""
AI机器人启动脚本
"""
import os
import sys
from pathlib import Path
import httpx
import json
import asyncio

# 将项目根目录添加到路径
WECHATBOT_PATH = str(Path(__file__).parent.parent.absolute())
if WECHATBOT_PATH not in sys.path:
    sys.path.insert(0, WECHATBOT_PATH)

from AIbot.bot import main

if __name__ == "__main__":
    # 确保logs目录存在
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # 确保data目录存在
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    # 新增：启动时获取好友列表并保存
    async def fetch_and_save_friends():
        api_url = os.environ.get("ONEBOT_API_URL", "http://127.0.0.1:8000")
        access_token = os.environ.get("ONEBOT_ACCESS_TOKEN", "")
        headers = {"Content-Type": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        data = {"action": "get_friend_list", "params": {}}
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(f"{api_url}/", headers=headers, json=data)
                if resp.status_code == 200:
                    result = resp.json()
                    if result.get("status") == "ok" and "data" in result:
                        friends = result["data"]
                        with open(data_dir / "friends.json", "w", encoding="utf-8") as f:
                            json.dump(friends, f, ensure_ascii=False, indent=2)
                        print(f"已保存好友列表到 {data_dir / 'friends.json'}")
                    else:
                        print(f"获取好友列表失败: {result}")
                else:
                    print(f"请求好友列表失败，状态码: {resp.status_code}")
        except Exception as e:
            print(f"获取好友列表异常: {e}")
    asyncio.run(fetch_and_save_friends())

    # 执行主程序
    main() 