class HandleImage:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "script": ("STRING", {
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "filter"
    CATEGORY = "SeedV"

    def filter(self, image, script):
        loc = {"image": image}
        exec(script, globals(), loc)
        result = loc.get("result")
        return (result,)
