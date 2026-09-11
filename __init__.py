from .resolution_selector import ResolutionSelector
from .advanced_script import AdvancedScript
from .script import Script
from .shared_ckpt import CheckpointLoaderSimpleShared, LoraLoader, ControlNetLoaderAdvancedShared
from .unload_models import ModelUnloader
from .tcd import TCDModelSamplingDiscrete
from .switch_any import Switch_Any
from .nunchakuLoraAdapter import nunchakuLoraAdapter
from .handle_image import HandleImage

NODE_CLASS_MAPPINGS = {
    "ResolutionSelector(SeedV)": ResolutionSelector,
    "AdvancedScript": AdvancedScript,
    "Script": Script,
    "CheckpointLoaderSimpleShared //SeedV": CheckpointLoaderSimpleShared,
    "LoraLoader //SeedV": LoraLoader,
    "ControlNetLoaderAdvancedShared": ControlNetLoaderAdvancedShared,
    "ALL_Model_UnLoader(SEEDV)": ModelUnloader,
    "Switch_Any(SEEDV)": Switch_Any,
    "TCD_Sampler(SEEDV)": TCDModelSamplingDiscrete,
    "nunchakuLoraAdapter(SEEDV)": nunchakuLoraAdapter,
    "HandleImage(SEEDV)": HandleImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ResolutionSelector(SeedV)": "Resolution Selector (SeedV)",
    "AdvancedScript": "Advanced Script (SeedV)",
    "Script": "Script (SeedV)",
    "CheckpointLoaderSimpleShared //SeedV": "Shared Checkpoint Loader (SeedV)",
    "LoraLoader //SeedV": "Load LoRA (SeedV)",
    "ControlNetLoaderAdvancedShared": "Shared Load Advanced ControlNet Model (SeedV)",
    "ALL_Model_UnLoader(SEEDV)": "ALL_Model_UnLoader(SEEDV)",
    "Switch_Any(SEEDV)": "Switch_Any(SEEDV UnSafe)",
    "TCD_Sampler(SEEDV)": "TCD_Sampler(SEEDV)",
    "nunchakuLoraAdapter(SEEDV)": "nunchakuLoraAdapter(SEEDV)",
    "HandleImage(SEEDV)": "HandleImage",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']