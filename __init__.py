from .script import Script
from .shared_ckpt import CheckpointLoaderSimpleShared, LoraLoader, ControlNetLoaderAdvancedShared

NODE_CLASS_MAPPINGS = {
    "Script": Script,
    "CheckpointLoaderSimpleShared //SeedV": CheckpointLoaderSimpleShared,
    "LoraLoader //SeedV": LoraLoader,
    "ControlNetLoaderAdvancedShared": ControlNetLoaderAdvancedShared,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Script": "Script",
    "CheckpointLoaderSimpleShared //SeedV": "Shared Checkpoint Loader (SeedV)",
    "LoraLoader //SeedV": "Load LoRA (SeedV)",
    "ControlNetLoaderAdvancedShared": "Shared Load Advanced ControlNet Model (SeedV)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
