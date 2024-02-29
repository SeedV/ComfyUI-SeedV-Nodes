class Script:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "script": ("STRING", {
                    "multiline": True,
                    "dynamicPrompts": False,
                }),
            },
            "optional": {
                "a": ("INT,FLOAT,STRING",),
                "b": ("INT,FLOAT,STRING",),
                "c": ("INT,FLOAT,STRING",),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING",)
    FUNCTION = "execute"
    CATEGORY = "SeedV"

    def execute(self, script, a=None, b=None, c=None):
        loc = {"a": a, "b": b, "c": c}
        exec(script, {"__builtins__": None}, loc)

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
