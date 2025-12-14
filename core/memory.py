"""
JARVIS Memory System
Simple JSON database to remember facts about the user.
"""
import json
from pathlib import Path
from datetime import datetime
from config import BASE_DIR

MEMORY_FILE = BASE_DIR / "memory.json"

class Memory:
    def __init__(self):
        self._load()
    
    def _load(self):
        """Load memory from file"""
        if MEMORY_FILE.exists():
            try:
                with open(MEMORY_FILE, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = {"facts": []}
        else:
            self.data = {"facts": []}
            
    def _save(self):
        """Save memory to file"""
        with open(MEMORY_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
            
    def add(self, fact: str):
        """Add a new fact about the user"""
        entry = {
            "fact": fact,
            "timestamp": datetime.now().isoformat()
        }
        self.data["facts"].append(entry)
        self._save()
        print(f"📝 [Memory] Saved: {fact}")
        
    def get_context(self) -> str:
        """Get all facts formatted as a string context"""
        if not self.data["facts"]:
            return "No prior knowledge about Soham."
        
        # Get last 15 facts (keep it relevant)
        recent_facts = self.data["facts"][-15:]
        context_str = "\n".join([f"- {item['fact']}" for item in recent_facts])
        return context_str
        
    def extract_and_save(self, user_text: str, llm_response: str):
        """
        Naive extraction: In a real system, we'd ask the LLM 'Did the user say something important?'
        For now, let's look for keywords or just assume specific commands.
        
        Advanced: We can run a background LLM call to extract facts.
        """
        # TODO: Implement LLM-based extraction
        pass

# Test
if __name__ == "__main__":
    mem = Memory()
    mem.add("Cares about efficiency.")
    print(mem.get_context())
