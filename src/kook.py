import aiohttp
import asyncio
import json
import websockets
import logging
import zlib

from logger import logger
import event
import traceback


class Endpoints:

    # 服务器相关
    GUILD_LIST = "/guild/list"  # 获取服务器列表
    GUILD_VIEW = "/guild/view"  # 获取服务器信息

    # 频道相关
    CHANNEL_LIST = "/channel/list"  # 获取频道列表
    CHANNEL_VIEW = "/channel/view"  # 获取频道信息
    CHANNEL_ROLE_INDEX = "/channel-role/index"  # 获取频道角色权限详情

    # 频道消息相关
    MESSAGE_LIST = "/message/list"  # 获取消息列表
    MESSAGE_VIEW = "/message/view"  # 获取消息信息
    MESSAGE_CREATE = "/message/create"  # 发送消息
    MESSAGE_UPDATE = "/message/update"  # 更新消息
    MESSAGE_DELETE = "/message/delete"  # 删除消息

    # 用户相关
    USER_ME = "/user/me"  # 获取当前用户信息
    USER_VIEW = "/user/view"  # 获取指定用户信息
    USER_OFFLINE = "/user/offline"  # 下线用户

    # GATEWAY
    GATEWAY_INDEX = "/gateway/index"  # 获取网关地址


class Events:
    KMARKDOWN_MESSAGE = 9
    UPDATED_MESSAGE = "updated_message"
    DELETED_MESSAGE = "deleted_message"


class Client:
    def __init__(self, token: str):
        logger.info("KookClient initializing...")
        self._base_url = "https://www.kookapp.cn/api/v3"
        self._authorization = f"Bot {token}"
        self._headers = {"Authorization": self._authorization}
        self.bus = event.Bus()

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        headers: dict = {},
        data: str = None,
    ):
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=f"{self._base_url}{endpoint}",
                headers={**self._headers, **headers},
                data=data,
            ) as response:
                return await response.json()

    async def connect(self):
        res = await self._make_request(method="GET", endpoint=Endpoints.GATEWAY_INDEX)
        url = res["data"]["url"]
        async with websockets.connect(url) as websocket:
            logger.info("Connected to gateway.")
            try:
                while True:
                    zippedData = await websocket.recv()
                    data = json.loads(zlib.decompress(zippedData).decode())
                    d = data.get("d")
                    extra = d.get("extra") if d else None
                    type = extra.get("type") if extra else None
                    if data["s"] == 0:
                        self.bus.publish(self, type, d)
            except asyncio.CancelledError:
                logger.info("Connection closed.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                logger.error(traceback.format_exc())

    async def get_me_id(self):
        res = await self._make_request(method="GET", endpoint=Endpoints.USER_ME)
        return res["data"]["id"]

    async def send_message(self, target_id: str, content: str, type: int = 1):
        res = await self._make_request(
            method="POST",
            endpoint=Endpoints.MESSAGE_CREATE,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "target_id": target_id,
                    "content": content,
                    "type": type,
                }
            ),
        )
        return res
