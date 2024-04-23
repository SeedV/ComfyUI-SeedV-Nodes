from .script import Script
from .shared_ckpt import CheckpointLoaderSimpleShared

NODE_CLASS_MAPPINGS = {
    "Script": Script,
    "CheckpointLoaderSimpleShared //SeedV": CheckpointLoaderSimpleShared,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Script": "Script",
    "CheckpointLoaderSimpleShared //SeedV": "Shared Checkpoint Loader (SeedV)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
