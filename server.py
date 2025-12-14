"""
JARVIS API Server
Exposes JARVIS capabilities via REST API.
Run with: uvicorn server:app --reload
"""
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Add path to find core modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.brain import Brain
from core.actions import ActionEngine
from config import PROMPT_AI, PROMPT_FRIEND
import ollama

app = FastAPI(title="JARVIS API", version="1.0")

# Initialize Cores
brain = Brain()
actions = ActionEngine()

class ChatRequest(BaseModel):
    message: str
    persona: str = "ai"  # "ai" or "friend"

class ChatResponse(BaseModel):
    response: str
    actions_triggered: list = []

@app.get("/")
def health_check():
    return {"status": "online", "system": "JARVIS"}

@app.get("/ask")
def simple_ask(q: str):
    """
    Simple GET endpoint.
    Usage: /ask?q=What is the weather?
    Returns: Just the text answer.
    """
    # Use AI mode by default for simple queries
    memories = brain.recall(q)
    context_str = ""
    if memories:
        context_str = "\n[RECALLED MEMORY]:\n" + "\n".join([f"- {m['text']}" for m in memories])
        
    final_prompt = PROMPT_AI.replace("{memory_context}", context_str)
    
    res = ollama.chat(
        model="mixtral", # Reverting to installed model
        messages=[
            {"role": "system", "content": final_prompt},
            {"role": "user", "content": q}
        ]
    )
    return res['message']['content']

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Send a message to JARVIS.
    """
    # 1. Select Persona
    system_prompt = PROMPT_FRIEND if req.persona == "friend" else PROMPT_AI
    
    # 2. Recall Memory
    memories = brain.recall(req.message)
    context_str = ""
    if memories:
        context_str = "\n[RECALLED MEMORY]:\n" + "\n".join([f"- {m['text']}" for m in memories])
        
    # 3. Inject Context
    final_prompt = system_prompt.replace("{memory_context}", context_str)
    
    # 4. Generate Response (Non-streaming for API simplicity)
    try:
        res = ollama.chat(
            model="mixtral", 
            messages=[
                {"role": "system", "content": final_prompt},
                {"role": "user", "content": req.message}
            ]
        )
        reply = res['message']['content']
        
        # 5. Execute embedded commands if any (Basic auto-execution)
        # Note: In a real API, maybe we simply return them, but user asked to "call upon" JARVIS.
        # Let's execute non-intrusive ones or just return text.
        # For a "Goated" API, let's actually run the predictive stuff if requested.
        
        if req.message.lower().startswith("predict "):
            reply = actions.predict_outcome(req.message[8:])
            
        return {"response": reply, "actions_triggered": []}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/action")
def execute_action(command: str):
    """
    Force execute an action string like 'OPEN: spotify'
    """
    return {"result": actions.execute(command)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
