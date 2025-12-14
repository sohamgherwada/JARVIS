"""
JARVIS Text-to-Speech using pyttsx3
"""
import sys
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from config import VOICE_SAMPLE_PATH, TEMP_DIR


class VoiceCloningTTS:
    """Text-to-Speech for JARVIS using pyttsx3"""
    
    def __init__(self):
        self.engine = None
        self._init_tts()
        
    def _init_tts(self):
        """Initialize TTS engine"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # Find David voice (male, natural)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'david' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            
            self.engine.setProperty('rate', 170)
            print("✓ TTS initialized")
        except Exception as e:
            print(f"⚠️ TTS failed: {e}")
            self.engine = None
    
    def speak(self, text: str):
        """Speak text"""
        if not text.strip():
            return
        
        print(f"🔊 Speaking...")
        
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print(f"   [JARVIS]: {text}")
    
    def speak_streaming(self, text_generator):
        """Stream speech as text chunks arrive."""
        buffer = ""
        sentence_enders = ".!?"
        
        for chunk in text_generator:
            buffer += chunk
            
            for i, char in enumerate(buffer):
                if char in sentence_enders:
                    sentence = buffer[:i+1].strip()
                    buffer = buffer[i+1:]
                    if sentence:
                        self.speak(sentence)
                    break
        
        if buffer.strip():
            self.speak(buffer.strip())
            
    def record_voice_sample(self, duration: int = 15):
        """Record voice sample."""
        print(f"\n🎤 Recording {duration} seconds...")
        input("Press ENTER when ready...")
        
        recording = sd.rec(int(duration * 16000), samplerate=16000, channels=1, dtype='int16')
        sd.wait()
        
        VOICE_SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(VOICE_SAMPLE_PATH), recording, 16000)
        print(f"✓ Saved to: {VOICE_SAMPLE_PATH}")


if __name__ == "__main__":
    tts = VoiceCloningTTS()
    tts.speak("Hello! I am JARVIS. Can you hear me?")
