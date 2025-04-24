from .advanced_script import AdvancedScript
from .script import Script
from .shared_ckpt import CheckpointLoaderSimpleShared, LoraLoader, ControlNetLoaderAdvancedShared
from .unload_models import ModelUnloader
from .tcd import TCDModelSamplingDiscrete
from .switch_any import Switch_Any
from .nunchakuLoraAdapter import nunchakuLoraAdapter

NODE_CLASS_MAPPINGS = {
    "AdvancedScript": AdvancedScript,
    "Script": Script,
    "CheckpointLoaderSimpleShared //SeedV": CheckpointLoaderSimpleShared,
    "LoraLoader //SeedV": LoraLoader,
    "ControlNetLoaderAdvancedShared": ControlNetLoaderAdvancedShared,
    "ALL_Model_UnLoader(SEEDV)": ModelUnloader,
    "Switch_Any(SEEDV)": Switch_Any,
    "TCD_Sampler(SEEDV)": TCDModelSamplingDiscrete,
    "nunchakuLoraAdapter(SEEDV)": nunchakuLoraAdapter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AdvancedScript": "Advanced Script (SeedV)",
    "Script": "Script (SeedV)",
    "CheckpointLoaderSimpleShared //SeedV": "Shared Checkpoint Loader (SeedV)",
    "LoraLoader //SeedV": "Load LoRA (SeedV)",
    "ControlNetLoaderAdvancedShared": "Shared Load Advanced ControlNet Model (SeedV)",
    "ALL_Model_UnLoader(SEEDV)": "ALL_Model_UnLoader(SEEDV)",
    "Switch_Any(SEEDV)": "Switch_Any(SEEDV UnSafe)",
    "TCD_Sampler(SEEDV)": "TCD_Sampler(SEEDV)",
    "nunchakuLoraAdapter(SEEDV)": "nunchakuLoraAdapter(SEEDV)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']