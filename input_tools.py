import base64
import io
import torchaudio
import hashlib
import folder_paths
import os

def process_audio_base64(audio_base64):
    audio_bytes = base64.b64decode(audio_base64)
    audio_io = io.BytesIO(audio_bytes)
    audio_bytes, sample_rate = torchaudio.load(audio_io)
    return audio_bytes, sample_rate

class LoadAudioOrBase64:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = folder_paths.filter_files_content_types(os.listdir(input_dir), ["audio", "video"])
        return {
                "required": 
                    {
                        "audio": (sorted(files), ),
                        "audio_base64": ("STRING", {"multiline": False})
                    },
                }

    RETURN_TYPES = ("AUDIO",)
    CATEGORY = "SeedV"
    FUNCTION = "load_audio"

    def load_audio(self, audio, audio_base64):
        if audio_base64:
            audio_bytes, sample_rate = process_audio_base64(audio_base64)
        else:
            audio_path = folder_paths.get_annotated_filepath(audio)
            audio_bytes, sample_rate = torchaudio.load(audio_path)
        audio = {"waveform": audio_bytes.unsqueeze(0), "sample_rate": sample_rate}
        return (audio,)
    
    @classmethod
    def IS_CHANGED(s, audio, audio_base64):
        if not audio_base64:
            audio_path = folder_paths.get_annotated_filepath(audio)
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
        else:
            audio_bytes = base64.b64decode(audio_base64)
        m = hashlib.sha256()
        m.update(audio_bytes)
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, audio, audio_base64):
        if not audio_base64 and not folder_paths.exists_annotated_file(audio):
            return "Invalid audio input"
        return True
    
class LoadAudioBase64:
    @classmethod
    def INPUT_TYPES(s):
        return {
                "required": 
                    {
                        "audio_base64": ("STRING", {"multiline": False})
                    },
                }

    RETURN_TYPES = ("AUDIO",)
    CATEGORY = "SeedV"
    FUNCTION = "load_audio"

    def load_audio(self, audio_base64):
        audio_bytes, sample_rate = process_audio_base64(audio_base64)
        audio = {"waveform": audio_bytes.unsqueeze(0), "sample_rate": sample_rate}
        return (audio,)
    
    @classmethod
    def IS_CHANGED(s, audio_base64):
        audio_bytes = base64.b64decode(audio_base64)
        m = hashlib.sha256()
        m.update(audio_bytes)
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, audio_base64):
        return True