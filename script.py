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
    FUNCTION = "exec"
    CATEGORY = "SeedV"

    def exec(self, script, a=None, b=None, c=None):
        loc = {"a": a, "b": b, "c": c}

        exec(script, {"__builtins__": None}, loc)
        return {"result": (
            int(loc["result"]), 
            float(loc["result"]), 
            str(loc["result"])
        )}


NODE_CLASS_MAPPINGS = {
    "Script": Script,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Script": "Script",
}
