"""
JARVIS LLM Integration using Ollama
Streaming responses for low latency
"""
import json
import requests
from typing import Generator

from config import OLLAMA_URL, OLLAMA_MODEL, SYSTEM_PROMPT


class StreamingLLM:
    """Connect to Ollama with streaming responses"""
    
    def __init__(self):
        self.conversation_history = []
        # Base prompt will be formatted later
        self.base_system_prompt = SYSTEM_PROMPT
        self.system_prompt = self.base_system_prompt.replace("{memory_context}", "")
        
    def update_system_prompt(self, memory_context: str):
        """Update prompt with latest memory"""
        self.system_prompt = self.base_system_prompt.replace("{memory_context}", memory_context)

    def set_mode(self, new_prompt_template: str):
        """Switch between Friend/AI modes"""
        self.base_system_prompt = new_prompt_template
        # Refresh current prompt (clearing memory placeholder for now, or keeping it empty)
        self.system_prompt = self.base_system_prompt.replace("{memory_context}", "")
        print("   🔄 System Persona Switched.")
        
    def _check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def chat(self, user_message: str) -> str:
        """
        Send message and get complete response.
        Good for simple use cases.
        """
        response_text = ""
        for chunk in self.chat_stream(user_message):
            response_text += chunk
        return response_text
    
    def chat_stream(self, user_message: str) -> Generator[str, None, None]:
        """
        Send message and stream response token by token.
        Perfect for low-latency TTS integration.
        """
        if not self._check_ollama():
            yield "I can't connect to Ollama. Make sure it's running with: ollama serve"
            return
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Build messages for API
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
        
        # Stream from Ollama
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": OLLAMA_MODEL,
                    "messages": messages,
                    "stream": True
                },
                stream=True,
                timeout=60
            )
            
            full_response = ""
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        chunk = data["message"]["content"]
                        full_response += chunk
                        yield chunk
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant", 
                "content": full_response
            })
            
        except requests.exceptions.Timeout:
            yield "Sorry, I took too long to think. Can you try again?"
        except Exception as e:
            yield f"Hmm, something went wrong: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("Conversation history cleared.")


# Quick test
if __name__ == "__main__":
    llm = StreamingLLM()
    
    print("Testing streaming LLM...")
    print("JARVIS: ", end="", flush=True)
    
    for chunk in llm.chat_stream("Hey Jarvis, I'm feeling a bit overwhelmed today"):
        print(chunk, end="", flush=True)
    
    print()
