import nodes
import folder_paths
import comfy.sd
import comfy.utils


class CheckpointLoaderSimpleShared(nodes.CheckpointLoaderSimple):
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_name": ("STRING", {"default": ""}),
                "key_opt": ("STRING", {"multiline": False, "placeholder": "If empty, use 'ckpt_name' as the key."}),
            },
            "optional": {
                "mode": (['Auto', 'Override Cache', 'Read Only'],),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "cache key")
    FUNCTION = "doit"

    CATEGORY = "SeedV"

    def doit(self, ckpt_name, key_opt, mode='Auto'):
        if mode == 'Read Only':
            if key_opt.strip() == '':
                raise Exception("[CheckpointLoaderSimpleShared] key_opt cannot be omit if mode is 'Read Only'")
            key = key_opt.strip()
        elif key_opt.strip() == '':
            key = ckpt_name
        else:
            key = key_opt.strip()
        import importlib
        module = importlib.import_module(
            "custom_nodes.ComfyUI-Inspire-Pack.inspire.backend_support")
        cache = module.cache
        update_cache = module.update_cache
        if key not in cache or mode == 'Override Cache':
            res = self.load_checkpoint(ckpt_name)
            update_cache(key, "ckpt", (False, res))
            cache_kind = 'ckpt'
            print(f"[Inspire Pack] CheckpointLoaderSimpleShared: Ckpt '{ckpt_name}' is cached to '{key}'.")
        else:
            cache_kind, (_, res) = cache[key]
            print(f"[Inspire Pack] CheckpointLoaderSimpleShared: Cached ckpt '{key}' is loaded. (Loading skip)")

        if cache_kind == 'ckpt':
            model, clip, vae = res
        elif cache_kind == 'unclip_ckpt':
            model, clip, vae, _ = res
        else:
            raise Exception(f"[CheckpointLoaderSimpleShared] Unexpected cache_kind '{cache_kind}'")

        return model, clip, vae, key

    @staticmethod
    def IS_CHANGED(ckpt_name, key_opt, mode='Auto'):
        if mode == 'Read Only':
            if key_opt.strip() == '':
                raise Exception("[CheckpointLoaderSimpleShared] key_opt cannot be omit if mode is 'Read Only'")
            key = key_opt.strip()
        elif key_opt.strip() == '':
            key = ckpt_name
        else:
            key = key_opt.strip()
        import importlib
        cache_weak_hash = importlib.import_module(
            "custom_nodes.ComfyUI-Inspire-Pack.inspire.backend_support").cache_weak_hash
        if mode == 'Read Only':
            return (None, cache_weak_hash(key))
        elif mode == 'Override Cache':
            return (ckpt_name, key)

        return (None, cache_weak_hash(key))


class LoraLoader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model": ("MODEL",),
                             "clip": ("CLIP",),
                             "lora_name": ("STRING", {"default": ""}),
                             "strength_model": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                             "strength_clip": ("FLOAT", {"default": 1.0, "min": -20.0, "max": 20.0, "step": 0.01}),
                             }}

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_lora"

    CATEGORY = "SeedV"

    def load_lora(self, model, clip, lora_name, strength_model, strength_clip):
        if strength_model == 0 and strength_clip == 0 or not lora_name:
            return (model, clip)
        lora_path = folder_paths.get_full_path("loras", lora_name)
        assert lora_path, f"lora '{lora_name}' not found"

        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip if strength_clip else None, lora,
                                                              strength_model, strength_clip)
        if strength_clip == 0:
            clip_lora = clip

        return (model_lora, clip_lora)


controlnet_cache = {}


class ControlNetLoaderAdvancedShared:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "control_net_name": (folder_paths.get_filename_list("controlnet"),),
            },
        }

    RETURN_TYPES = ("CONTROL_NET",)
    FUNCTION = "load_controlnet"

    CATEGORY = "SeedV"

    def load_controlnet(self, control_net_name):
        if control_net_name in controlnet_cache:
            return controlnet_cache[control_net_name]

        import importlib
        load_controlnet = importlib.import_module(
            "custom_nodes.ComfyUI-Advanced-ControlNet.adv_control.control").load_controlnet
        controlnet_path = folder_paths.get_full_path("controlnet", control_net_name)
        controlnet = load_controlnet(controlnet_path)
        controlnet_cache[control_net_name] = (controlnet,)
        return (controlnet,)
