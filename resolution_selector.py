import math
from enum import Enum
from comfy_api.latest import io


class AspectRatioSeedV(str, Enum):
    SQUARE = "1:1"
    PHOTO_V = "2:3"
    PHOTO_H = "3:2"
    STANDARD_V = "3:4"
    STANDARD_H = "4:3"
    WIDESCREEN_V = "9:16"
    WIDESCREEN_H = "16:9"
    ULTRAWIDE_H = "21:9"


ASPECT_RATIOS: dict[AspectRatioSeedV, tuple[int, int]] = {
    AspectRatioSeedV.SQUARE: (1, 1),
    AspectRatioSeedV.PHOTO_V: (2, 3),
    AspectRatioSeedV.PHOTO_H: (3, 2),
    AspectRatioSeedV.STANDARD_V: (3, 4),
    AspectRatioSeedV.STANDARD_H: (4, 3),
    AspectRatioSeedV.WIDESCREEN_V: (9, 16),
    AspectRatioSeedV.WIDESCREEN_H: (16, 9),
    AspectRatioSeedV.ULTRAWIDE_H: (21, 9),
}


class ResolutionSelector(io.ComfyNode):
    """Calculate width and height from aspect ratio and megapixel target."""

    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="ResolutionSelector(SeedV)",
            display_name="Resolution Selector (SeedV)",
            category="SeedV",
            description="Calculate width and height from aspect ratio and megapixel target. Useful for setting up Empty Latent Image dimensions.",
            inputs=[
                io.Combo.Input(
                    "aspect_ratio",
                    options=AspectRatioSeedV,
                    default=AspectRatioSeedV.SQUARE,
                    tooltip="The aspect ratio for the output dimensions.",
                ),
                io.Float.Input(
                    "megapixels",
                    default=1.0,
                    min=0.1,
                    max=16.0,
                    step=0.1,
                    tooltip="Target total megapixels. 1.0 MP ≈ 1024x1024 for square.",
                ),
                io.Int.Input(
                    id="multiple",
                    default=8,
                    min=8,
                    max=128,
                    step=4,
                    tooltip="Nearest multiple of the result to set the selected resolution to.",
                    advanced=True,
                ),
            ],
            outputs=[
                io.Int.Output(
                    "width", tooltip="Calculated width in pixels multiplied by the selected multiple."
                ),
                io.Int.Output(
                    "height", tooltip="Calculated height in pixels multiplied by the selected multiple."
                ),
            ],
        )

    @classmethod
    def execute(cls, aspect_ratio: str, megapixels: float, multiple: int) -> io.NodeOutput:
        w_ratio, h_ratio = ASPECT_RATIOS[aspect_ratio]
        total_pixels = megapixels * 1024 * 1024
        scale = math.sqrt(total_pixels / (w_ratio * h_ratio))
        width = round(w_ratio * scale / multiple) * multiple
        height = round(h_ratio * scale / multiple) * multiple
        return io.NodeOutput(width, height)
