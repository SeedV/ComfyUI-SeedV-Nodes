from .script import any

class Switch_Any:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "on_true": (any, {"forceInput": True}),
                "on_false": (any, {"forceInput": True}),
                "boolean": (any, {"forceInput": True})
            }
        }

    RETURN_TYPES = (any,)
    FUNCTION = "execute"

    CATEGORY = "SeedV"

    def execute(self, on_true, on_false, boolean=True):
        if boolean:
            return (on_true, )
        else:
            return (on_false, )