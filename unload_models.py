import logging
import aiohttp
import asyncio
from comfy.cli_args import args
from .script import any

class ModelUnloader:
    def __init__(self) -> None:
        self.port = args.port
        self.free_api = "http://127.0.0.1:" + str(self.port) + "/free"
        self.headers = {"Content-Type": "application/json"}  # 赋值给实例
        self.mode = {"unload_models": True, "free_memory": True}  # 直接存 JSON 结构
        self.timeout = aiohttp.ClientTimeout(total=20) 
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
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.post(self.free_api, headers=self.headers, json=self.mode) as response:
                    response.raise_for_status()
                    response_text = await response.text()
                    logging.info(f"Models unloaded and memory freed successfully!")
        except Exception as e:
            logging.error(f"An error occurred: {e}")