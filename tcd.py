import torch
from comfy.k_diffusion.sampling import default_noise_sampler
from comfy.ldm.modules.diffusionmodules.util import make_beta_schedule
from comfy.model_sampling import EPS
from comfy.samplers import KSAMPLER, calculate_sigmas
from comfy_extras.nodes_model_advanced import ModelSamplingDiscreteDistilled
from tqdm.auto import trange


class ModelSamplingDiscreteDistilledTCD(ModelSamplingDiscreteDistilled, EPS):
    def __init__(self, model_config=None):
        super().__init__(model_config)
        sampling_settings = model_config.sampling_settings if model_config is not None else {}

        beta_schedule = sampling_settings.get("beta_schedule", "linear")
        linear_start = sampling_settings.get("linear_start", 0.00085)
        linear_end = sampling_settings.get("linear_end", 0.012)

        betas = make_beta_schedule(
            beta_schedule, n_timestep=1000, linear_start=linear_start, linear_end=linear_end, cosine_s=8e-3
        )
        alphas = 1.0 - betas
        alphas_cumprod = torch.cumprod(alphas, dim=0, dtype=torch.float32)
        self.register_buffer("alphas_cumprod", alphas_cumprod.clone().detach())

SCHEDULER_NAMES = ["simple", "sgm_uniform", "karras", "exponential", "normal", "ddim_uniform", "beta"]

class TCDModelSamplingDiscrete:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "steps": ("INT", {"default": 4, "min": 1, "max": 50}),
                "scheduler": (SCHEDULER_NAMES,),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "eta": ("FLOAT", {"default": 0.3, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("MODEL", "SAMPLER", "SIGMAS")
    FUNCTION = "patch"
    CATEGORY = "SeedV"

    def patch(self, model, steps=4, scheduler="simple", denoise=1.0, eta=0.3):
        m = model.clone()
        ms = ModelSamplingDiscreteDistilledTCD(model.model.model_config)

        total_steps = steps
        if denoise <= 0.0:
            sigmas = torch.FloatTensor([])
        elif denoise <= 1.0:
            total_steps = int(steps / denoise)
            sigmas = calculate_sigmas(ms, scheduler, total_steps).cpu()
            sigmas = sigmas[-(steps + 1) :]
        m.add_object_patch("model_sampling", ms)

        timesteps_s = torch.floor((1 - eta) * ms.timestep(sigmas)).to(dtype=torch.long).detach()
        timesteps_s[-1] = 0
        alpha_prod_s = ms.alphas_cumprod[timesteps_s]
        sampler = KSAMPLER(sample_tcd, extra_options={"eta": eta, "alpha_prod_s": alpha_prod_s}, inpaint_options={})
        return (m, sampler, sigmas)

@torch.no_grad()
def sample_tcd(model, x, sigmas, extra_args=None, callback=None, disable=None, noise_sampler=None, eta=0.3, alpha_prod_s: torch.Tensor = None):
    # TCD sampling using modified DDPM.
    extra_args = {} if extra_args is None else extra_args
    noise_sampler = default_noise_sampler(x) if noise_sampler is None else noise_sampler
    s_in = x.new_ones([x.shape[0]])
    
    for i in trange(len(sigmas) - 1, disable=disable):
        denoised = model(x, sigmas[i] * s_in, **extra_args)
        if callback is not None:
            callback({'x': x, 'i': i, 'sigma': sigmas[i], 'sigma_hat': sigmas[i], 'denoised': denoised})

        sigma_from, sigma_to = sigmas[i], sigmas[i+1]

        # TCD offset, based on gamma, and conversion between sigma and timestep
        t = model.inner_model.inner_model.model_sampling.timestep(sigma_from)
        t_s = (1 - eta) * t
        sigma_to_s = model.inner_model.inner_model.model_sampling.sigma(t_s)

        noise_est = (x - denoised) / sigma_from
        x /= torch.sqrt(1.0 + sigma_from ** 2.0)

        alpha_cumprod = 1 / ((sigma_from * sigma_from) + 1)  # _t
        alpha_cumprod_prev = 1 / ((sigma_to * sigma_to) + 1) # _t_prev
        alpha = (alpha_cumprod / alpha_cumprod_prev)

        # epsilon noise prediction from comfy DDPM implementation
        x = (1.0 / alpha).sqrt() * (x - (1 - alpha) * noise_est / (1 - alpha_cumprod).sqrt())

        first_step = sigma_to == 0
        last_step = i == len(sigmas) - 2

        if not first_step:
            if eta > 0 and not last_step:
                noise = noise_sampler(sigma_from, sigma_to)     
                variance = ((1 - alpha_cumprod_prev) / (1 - alpha_cumprod)) * (1 - alpha_cumprod / alpha_cumprod_prev)
                x += variance.sqrt() * noise # scale noise by std deviation

            x *= torch.sqrt(1.0 + sigma_to ** 2.0)
    return x