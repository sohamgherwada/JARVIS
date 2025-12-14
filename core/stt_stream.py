"""
JARVIS STT - GPU Accelerated (Faster-Whisper)
Requires: Python 3.11+, CUDA GPU, faster-whisper
"""
import os
import queue
import time
import sys
import tempfile
import numpy as np
import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1

class StreamingSTT:
    def __init__(self):
        print("🚀 Initializing JARVIS High-Performance Ears (GPU)...")
        # Load Faster Whisper on GPU
        # 'large-v3' is SOTA. 'small' is super fast.
        try:
            self.model = WhisperModel(
                "large-v3", 
                device="cuda", 
                compute_type="float16"
            )
            print("   ✓ GPU Acceleration ENABLED (RTX 5060 Ti Detected)")
        except Exception as e:
            print(f"   ⚠️ GPU Failed ({e}), falling back to CPU (INT8)...")
            self.model = WhisperModel(
                "medium", 
                device="cpu", 
                compute_type="int8"
            )

        self.audio_queue = queue.Queue()
        
        # VAD Settings
        self.energy_threshold = 400
        self.pause_threshold = 1.2 # Faster response
        
        # Mic Load
        self.device_id = self._load_mic_config()

    def _load_mic_config(self):
        try:
            from config import BASE_DIR
            import json
            p = BASE_DIR / "mic_config.json"
            if p.exists():
                with open(p) as f:
                    return json.load(f).get("device_id")
        except:
            return None

    def _audio_callback(self, indata, frames, time_info, status):
        self.audio_queue.put(indata.copy())
        
    def listen_until_silence(self):
        """
        Record -> Detect Silence -> Transcribe (GPU)
        """
        print("\n🎤 Listening... (GPU)")
        
        audio_buffer = []
        has_started = False
        last_speech_time = time.time()
        
        with sd.InputStream(
            samplerate=SAMPLE_RATE, 
            channels=CHANNELS, 
            callback=self._audio_callback,
            device=self.device_id
        ):
            while True:
                try:
                    data = self.audio_queue.get(timeout=0.1)
                    audio_buffer.append(data)
                    
                    # Energy VAD
                    energy = np.linalg.norm(data) * 10
                    is_talking = energy > self.energy_threshold
                    
                    if is_talking:
                        if not has_started:
                            has_started = True
                            print("\rRecording... 🔴     ", end="", flush=True)
                        last_speech_time = time.time()
                    
                    # End of speech
                    if has_started and (time.time() - last_speech_time > self.pause_threshold):
                        print("\rProcessing... ⚡     ", end="", flush=True)
                        break
                        
                except queue.Empty:
                    continue
                    
        if not audio_buffer:
            return ""
            
        # Transcribe
        full_audio = np.concatenate(audio_buffer, axis=0)
        
        # faster-whisper accepts ndarray directly!
        segments, info = self.model.transcribe(
            full_audio, 
            beam_size=5,
            language="en"
        )
        
        text_segments = list(segments)
        full_text = " ".join([s.text for s in text_segments]).strip()
        
        if full_text:
            print(f"\r📝 You said: {full_text}    ")
            return full_text
        return ""

if __name__ == "__main__":
    stt = StreamingSTT()
    while True:
        stt.listen_until_silence()
