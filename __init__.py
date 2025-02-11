from .advanced_script import AdvancedScript
from .script import Script
from .shared_ckpt import CheckpointLoaderSimpleShared, LoraLoader, ControlNetLoaderAdvancedShared
from .unload_models import ModelUnloader

NODE_CLASS_MAPPINGS = {
    "AdvancedScript": AdvancedScript,
    "Script": Script,
    "CheckpointLoaderSimpleShared //SeedV": CheckpointLoaderSimpleShared,
    "LoraLoader //SeedV": LoraLoader,
    "ControlNetLoaderAdvancedShared": ControlNetLoaderAdvancedShared,
    "ALL_Model_UnLoader(SEEDV)": ModelUnloader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedScript": "Advanced Script (SeedV)",
    "Script": "Script (SeedV)",
    "CheckpointLoaderSimpleShared //SeedV": "Shared Checkpoint Loader (SeedV)",
    "LoraLoader //SeedV": "Load LoRA (SeedV)",
    "ControlNetLoaderAdvancedShared": "Shared Load Advanced ControlNet Model (SeedV)",
    "ALL_Model_UnLoader(SEEDV)": "ALL_Model_UnLoader(SEEDV)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']