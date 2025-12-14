"""
JARVIS Chat Interface (Text Only)
Direct access to the Brain and Orchestra.
"""
import sys
import os
from config import PROMPT_FRIEND, PROMPT_AI
import re
import time
import queue
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.llm_stream import StreamingLLM
from core.brain import Brain
from core.actions import ActionEngine

from core.coordination import set_orchestra_status

def main():
    print("\n" + "="*50)
    print("  🎻 JARVIS Knowledge Orchestra - Conductor")
    print("  (Text Mode Active)")
    print("="*50 + "\n")
    
    llm = StreamingLLM()
    brain = Brain()
    actions = ActionEngine()
    
    # Simple history
    history = []
    
    print("Type 'exit' to quit. Type 'test idea: [idea]' to run simulation.")
    
    while True:
        try:
            print("\n__________________________________________________")
            set_orchestra_status("RUNNING") # Resume background work while waiting
            user_text = input("USER > ").strip()
            set_orchestra_status("PAUSED")  # Pause to focus on user
            
            if not user_text: continue
            if user_text.lower() in ["exit", "quit"]: break
            
            # Special Modes
            # Special Modes
            if user_text.lower().startswith("/friendmode"):
                cmd_parts = user_text.lower().split()
                mode = cmd_parts[1] if len(cmd_parts) > 1 else "toggle"
                
                if mode in ["on", "active"]:
                    print("\n🤜🤛 FRIEND MODE ACTIVATED. Let's chill.")
                    llm.set_mode(PROMPT_FRIEND)
                elif mode in ["off", "inactive"]:
                    print("\n👔 FRIEND MODE DEACTIVATED. Returning to AI Assistant mode.")
                    llm.set_mode(PROMPT_AI)
                else:
                    print("Usage: /friendmode [on|off]")
                continue

            if user_text.lower().startswith("predict"):
                query = user_text[7:].strip()
                print(f"\n🔮 Oracle Activated: {query}")
                result = actions.predict_outcome(query)
                
                # Streaming Output for Effect
                print("\nJARVIS (Oracle) > ", end="", flush=True)
                words = result.split(' ')
                for word in words:
                    print(word, end=" ", flush=True)
                    time.sleep(0.05)
                print("\n")
                continue
                
            if user_text.lower().startswith("test idea:"):
                idea = user_text.split(":", 1)[1].strip()
                print(f"\n🧪 Testing Idea: {idea}")
                print("   (Orchestra would dispatch Researcher Agents here...)")
                # TODO: Dispatch to orchestra
                # For now, just research standard
                user_text = f"Research the feasibility of this idea: {idea}"
            
            # 1. RECALL (The Brain)
            recalled_items = brain.recall(user_text, top_k=5)
            context_prefix = ""
            
            if recalled_items:
                print(f"   💡 Brain Activated: Found {len(recalled_items)} relevant citations.")
                
                # Check for Expert Persona
                topics = [r['source'].replace('verified:', '').replace('web:', '') for r in recalled_items if 'verified:' in r['source']]
                if topics:
                    dominant_topic = max(set(topics), key=topics.count)
                    print(f"   🎓 Expert Mode: {dominant_topic}")
                    context_prefix += f"[SYSTEM: You are an expert in {dominant_topic}.]\n"
                
                context_prefix += "[VERIFIED KNOWLEDGE BASE]:\n"
                for item in recalled_items:
                    context_prefix += f"- {item['text']} (Source: {item['source']})\n"
                context_prefix += "\n"
                
            full_input = context_prefix + "USER: " + user_text

            # 2. GENERATE (The Mind)
            print("\nJARVIS > ", end="", flush=True)
            
            full_response = ""
            full_response = ""
            for chunk in llm.chat_stream(full_input):
                # Clean up weird spacing
                clean_chunk = chunk.replace('\r', '').replace('\t', ' ')
                
                # WORD-BY-WORD TYPEWRITER EFFECT
                # We split by space but keep the spacing for natural flow
                words = clean_chunk.split(' ')
                for i, word in enumerate(words):
                    print(word, end="", flush=True)
                    if i < len(words) - 1:
                        print(" ", end="", flush=True)
                    time.sleep(0.02) # Fast typing speed
                    
                full_response += chunk
            print("\n")
            
            # 3. ACTION (The Hands)
            # Execute [DOC], [SEARCH], etc.
            commands = re.findall(r"\[(DOC|SEARCH|LEARN):\s*(.*?)\]", full_response, re.IGNORECASE | re.DOTALL)
            for cmd, param in commands:
                print(f"   ⚡ Executing {cmd}...")
                if cmd.upper() == "SEARCH":
                    res = actions.web_search(param)
                    print(f"      (Result: {len(res)} chars found)")
                elif cmd.upper() == "DOC":
                    actions.execute(f"DOC:{param}")
                elif cmd.upper() == "LEARN":
                    # Instant learn
                    actions.execute(f"SEARCH:{param}") 
                    # Real orchestration handles this in background
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
