"""
JARVIS 3.0 - The Ultimate AI
Voice, Vision, Brain, and Control.
"""
import sys
import os
import re
import time
import random

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.stt_stream import StreamingSTT
from core.llm_stream import StreamingLLM
from core.memory import Memory
from core.actions import ActionEngine
from core.brain import Brain
from core.vision import Vision

WAKE_WORDS = ["jarvis", "hi jarvis", "hey jarvis", "yo jarvis"]
SLEEP_TIMEOUT = 30

def main():
    print("\n" + "="*50)
    print("  🤖 JARVIS 3.0 - (Voice/Vision/Control)")
    print("="*50 + "\n")
    
    # Initialize components
    stt = StreamingSTT()
    llm = StreamingLLM()
    memory = Memory()
    actions = ActionEngine()
    brain = Brain()
    vision = Vision()
    
    # Load memory
    llm.update_system_prompt(memory.get_context())
    
    is_awake = False
    last_interaction = time.time()
    visual_context = ""
    
    print("💤 Waiting for 'Jarvis'...")
    
    while True:
        try:
            # Listen
            user_text = stt.listen_until_silence()
            
            if not user_text:
                if is_awake and (time.time() - last_interaction > SLEEP_TIMEOUT):
                    print("\n💤 JARVIS going to sleep...")
                    is_awake = False
                    visual_context = "" # Clear vision context
                continue
            
            lower_text = user_text.lower()
            
            # WAKE WORD
            if not is_awake:
                detected = any(w in lower_text for w in WAKE_WORDS)
                if detected:
                    is_awake = True
                    print("\n👀 JARVIS Waking up!")
                    print("🧠 JARVIS: I'm here.")
                    last_interaction = time.time()
                else:
                    continue
            
            # --- AWAKE ---
            last_interaction = time.time()
            print(f"\n📝 You said: {user_text}")
            
            # 1. RECALL KNOWLEDGE
            recalled_items = brain.recall(user_text)
            
            final_input = user_text
            context_prefix = ""
            
            if recalled_items:
                print(f"💡 Brain Recalled: {len(recalled_items)} chunks")
                
                # Deduce Topic from sources
                topics = [r['source'].replace('verified:', '').replace('web:', '') for r in recalled_items if 'verified:' in r['source']]
                # Pick most common topic
                if topics:
                    dominant_topic = max(set(topics), key=topics.count)
                    print(f"🎓 Switching Persona: Academic Expert in {dominant_topic}")
                    context_prefix += f"[SYSTEM: You are now an ACADEMIC EXPERT in {dominant_topic}. Use the verified facts below to answer accurately. Be professional and deep.]\n"
                
                knowledge_text = "\n".join([f"- {r['text']} (Source: {r['source']})" for r in recalled_items])
                context_prefix += f"[VERIFIED KNOWLEDGE]:\n{knowledge_text}\n"
            
            if visual_context:
                context_prefix += f"[SCREEN VISUALS]: {visual_context}\n"
                
            if context_prefix:
                final_input = context_prefix + "\nUSER QUERY: " + user_text
            
            # 2. GENERATE RESPONSE
            print("\n🧠 JARVIS: ", end="", flush=True)
            full_response = ""
            for chunk in llm.chat_stream(final_input):
                print(chunk, end="", flush=True)
                full_response += chunk
            print("\n")
            
            # 3. EXECUTE ACTIONS
            commands = re.findall(r"\[(OPEN|CLOSE|SEARCH|SYSTEM|TYPE|LOOK|LEARN|DOC):\s*(.*?)\]", full_response, re.IGNORECASE | re.DOTALL)
            
            if commands:
                print("⚡ Action Detected:")
                
                for cmd, param in commands:
                    cmd = cmd.upper()
                    
                    if cmd == "LOOK":
                        # Vision
                        desc = vision.see_screen()
                        visual_context = desc # Save for next turn
                        print(f"   ✓ Vision System Active")
                        # Optional: Trigger follow-up response?
                        
                    elif cmd == "LEARN":
                        # Learning
                        print(f"   🧠 Learning about {param}...")
                        search_result = actions.web_search(param)
                        brain.learn(search_result, source="web")
                        print("   ✓ Knowledge absorbed.")
                        
                    else:
                        # Standard Actions
                        action_str = f"{cmd}:{param}"
                        result = actions.execute(action_str)
                        print(f"   ✓ {result}")
                        
                        # Use search result for learning too?
                        if cmd == "SEARCH":
                            # Auto-learn what we search
                            brain.learn(result, source="search")

        except KeyboardInterrupt:
            print("\n👋 Shutting down.")
            break
        except Exception as e:
            print(f"\n❌ Loop Error: {e}")
            continue

if __name__ == "__main__":
    main()
