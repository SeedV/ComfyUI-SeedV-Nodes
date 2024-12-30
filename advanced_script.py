import json
import random
import time

from .script import any, builtin_symbols


class AdvancedScript:
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
                "functions": ("STRING", {
                    "multiline": True,
                    "defaultInput": True,
                }),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", "STRING", "INT", "FLOAT", "STRING")
    FUNCTION = "execute"
    CATEGORY = "SeedV"

    def execute(self, script, a=None, b=None, c=None, d=None, e=None,
                functions=None):
        full_script = script if not functions else f"{functions}\n{script}"
        loc = {"a": a, "b": b, "c": c, "d": d, "e": e}
        exec(full_script, {"__builtins__": builtin_symbols}, loc)

        result1 = loc.get("result1", 0)
        try:
            result1_int = int(result1)
        except ValueError:
            result1_int = 0
        try:
            result1_float = float(result1)
        except ValueError:
            result1_float = 0

        result2 = loc.get("result2", 0)
        try:
            result2_int = int(result2)
        except ValueError:
            result2_int = 0
        try:
            result2_float = float(result2)
        except ValueError:
            result2_float = 0

        return (result1_int, result1_float, str(result1),
                result2_int, result2_float, str(result2))

    @classmethod
    def IS_CHANGED(cls, script, a=None, b=None, c=None, d=None, e=None,
                   functions=None):
        # Ensure the script is re-executed each time when using random numbers
        # in the script.
        return time.time()
