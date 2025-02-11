import logging
import aiohttp
import asyncio
from .script import any  # 确保 `any` 是正确的导入路径

class ModelUnloader:
    def __init__(self) -> None:
        self.free_api = "http://127.0.0.1:8188/free"
        self.headers = {"Content-Type": "application/json"}  # 赋值给实例
        self.mode = {"unload_models": True, "free_memory": True}  # 直接存 JSON 结构

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "input_image": (any, {}),
                "input_text": (any, {})
            },
        }

    RETURN_TYPES = ("IMAGE", "String")
    FUNCTION = "execute"
    CATEGORY = "SeedV"

    def execute(self, input_image=None, input_text=None):
        self._unload_models_and_free_memory()
        return (input_image, input_text)

    def _unload_models_and_free_memory(self):
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._send_post_request())
        except RuntimeError:
            asyncio.run(self._send_post_request())

    async def _send_post_request(self):
        # 发送异步 POST 请求来卸载模型并释放内存
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.free_api, headers=self.headers, json=self.mode) as response:
                    response.raise_for_status()
                    response_text = await response.text()
                    logging.info(f"Models unloaded and memory freed successfully!")
        except asyncio.TimeoutError:
            logging.error("Request timed out while freeing memory.")
        except aiohttp.ClientError as e:
            logging.error(f"HTTP request failed: {e}")
