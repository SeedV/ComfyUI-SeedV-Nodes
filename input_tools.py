import base64
import io
import torchaudio
import hashlib

def process_audio_base64(audio_base64):
    audio_bytes = base64.b64decode(audio_base64)
    audio_io = io.BytesIO(audio_bytes)
    audio_bytes, sample_rate = torchaudio.load(audio_io)
    return audio_bytes, sample_rate

class LoadAudioBase64:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"audio": ("STRING", {"multiline": False})}}

    RETURN_TYPES = ("AUDIO",)
    CATEGORY = "_external_tooling"
    FUNCTION = "load_audio"

    def load_audio(self, audio_base64_str):
        audio_bytes, sample_rate = process_audio_base64(audio_base64_str)
        audio = {"waveform": audio_bytes, "sample_rate": sample_rate}
        return audio
    
    @classmethod
    def IS_CHANGED(s, audio_base64_str):
        m = hashlib.sha256()
        m.update(audio_base64_str)
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, audio):
        try:
            process_audio_base64(audio)
            return True
        except Exception as e:
            return False

