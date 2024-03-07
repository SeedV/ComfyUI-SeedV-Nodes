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
            },
            "optional": {
                "a": ("INT,FLOAT,STRING",),
                "b": ("INT,FLOAT,STRING",),
                "c": ("INT,FLOAT,STRING",),
                "d": ("INT,FLOAT,STRING",),
                "e": ("INT,FLOAT,STRING",),
            },
        }

    """
        The node will always be re executed if any of the inputs change but this 
        method can be used to force the node to execute again even when the 
        inputs don't change.
        You can make this node return a number or a string. This value will be
        compared to the one returned the last time the node was executed, if it 
        is different the node will be executed again.
        This method is used in the core repo for the LoadImage node where they 
        return the image hash as a string, if the image hash changes between 
        executions the LoadImage node is executed again.
    """
    @classmethod
    def IS_CHANGED(self):
        return float("nan")

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


NODE_CLASS_MAPPINGS = {
    "Script": Script,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Script": "Script",
}
