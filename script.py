import random


class Script:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "script": ("STRING", {
                    "multiline": True,
                    "dynamicPrompts": False,
                }),
                "seed": ("INT", {
                    "default": 0, "min": 0, "max": 0xffffffffffffffff
                }),
            },
            "optional": {
                "a": ("INT,FLOAT,STRING",),
                "b": ("INT,FLOAT,STRING",),
                "c": ("INT,FLOAT,STRING",),
                "d": ("INT,FLOAT,STRING",),
                "e": ("INT,FLOAT,STRING",),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING",)
    FUNCTION = "execute"
    CATEGORY = "SeedV"

    def execute(self, script, seed, a=None, b=None, c=None, d=None, e=None):
        random.seed(seed)
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


NODE_CLASS_MAPPINGS = {
    "Script": Script,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Script": "Script",
}
