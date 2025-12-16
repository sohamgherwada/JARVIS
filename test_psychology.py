
import sys
import os

# Fix path to allow imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.llm_stream import StreamingLLM

def test_jarvis():
    llm = StreamingLLM()
    
    print("\n--- TEST 1: INTELLECTUAL (Teacher Mode) ---")
    prompt1 = "I want to learn about Quantum Entanglement. How does it work?"
    print(f"User: {prompt1}")
    print("JARVIS: ", end="", flush=True)
    for chunk in llm.chat_stream(prompt1):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Clear history for clean test
    llm.clear_history() 

    print("\n--- TEST 2: EMOTIONAL (Companion Mode) ---")
    prompt2 = "I'm having a panic attack about my deadlines. I can't breathe."
    print(f"User: {prompt2}")
    print("JARVIS: ", end="", flush=True)
    for chunk in llm.chat_stream(prompt2):
        print(chunk, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    test_jarvis()
