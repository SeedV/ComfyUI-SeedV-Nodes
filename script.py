import random


class AnyType(str):
    """A special class that is always equal in not equal comparisons."""

    def __eq__(self, __value: object) -> bool:
        return True

    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class Script:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "script": ("STRING", {
                    "multiline": True,
                }),
            },
            "optional": {
                "a": (any, {}),
                "b": (any, {}),
                "c": (any, {}),
                "d": (any, {}),
                "e": (any, {}),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING",)
    FUNCTION = "execute"
    CATEGORY = "SeedV"

    def execute(self, script, a=None, b=None, c=None, d=None, e=None):
        loc = {"a": a, "b": b, "c": c, "d": d, "e": e}
        exec(script, {"__builtins__": {"random": random}}, loc)

        result = loc["result"]
        try:
            result_int = int(result)
        except ValueError:
            result_int = 0
        try:
            result_float = float(result)
        except ValueError:
            result_float = 0

        return {"result": (result_int, result_float, str(result))}

    @classmethod
    def IS_CHANGED(cls):
        """返回 Nan, 确保脚本中使用随机数的情况下，每次都会重新执行脚本。"""
        return float("NaN")
