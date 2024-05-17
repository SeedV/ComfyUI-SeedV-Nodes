from .script import Script
from .shared_ckpt import CheckpointLoaderSimpleShared, LoraLoader

NODE_CLASS_MAPPINGS = {
    "Script": Script,
    "CheckpointLoaderSimpleShared //SeedV": CheckpointLoaderSimpleShared,
    "LoraLoader //SeedV": LoraLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Script": "Script",
    "CheckpointLoaderSimpleShared //SeedV": "Shared Checkpoint Loader (SeedV)",
    "LoraLoader //SeedV": "Load LoRA (SeedV)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
