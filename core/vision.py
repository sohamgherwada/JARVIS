"""
JARVIS Vision
Allows JARVIS to see the screen using Ollama Vision models.
"""
import mss
import base64
import ollama
from io import BytesIO
from PIL import Image

class Vision:
    def __init__(self):
        self.model = "llava" # Standard vision model
        
    def analyze_image_from_url(self, url, prompt="Describe this educational image in detail."):
        """Download image and analyze it with VLM"""
        import requests
        print(f"👀 Visually analyzing: {url[:50]}...")
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 200: return None
            
            img_bytes = res.content
            
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [img_bytes]
                }]
            )
            description = response['message']['content']
            print(f"   👁️ Vision: {description[:100]}...")
            return description
        except Exception as e:
            print(f"❌ Vision URL Error: {e} (Try: ollama pull llava)")
            return None
        
    def see_screen(self, prompt="Describe what is on the screen."):
        """Capture screen and analyze it"""
        print("👀 JARVIS is looking at your screen...")
        
        with mss.mss() as sct:
            # Capture primary monitor
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Resize for speed (optional)
            img.thumbnail((1024, 1024))
            
            # Convert to bytes
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [img_bytes]
                }]
            )
            description = response['message']['content']
            print(f"👀 Vision Result: {description[:100]}...")
            return description
            
        except Exception as e:
            print(f"❌ Vision Error: {e}")
            return "I tried to look, but my vision system (Ollama) failed. Do you have 'llama3.2-vision' installed?"

if __name__ == "__main__":
    v = Vision()
    v.see_screen()
