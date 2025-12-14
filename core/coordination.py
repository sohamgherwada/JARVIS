"""
JARVIS Coordinator
Manages state between Chatbot (User) and Orchestra (Background).
"""
import json
import os
import time
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / "orchestra_state.json"

def set_orchestra_status(status: str):
    """
    Status: 'RUNNING' or 'PAUSED'
    """
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump({"status": status, "timestamp": time.time()}, f)
    except:
        pass

def get_orchestra_status():
    """
    Returns 'RUNNING' or 'PAUSED'
    """
    if not STATE_FILE.exists():
        return "RUNNING"
        
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            
        # Safety: Auto-resume after 5 minutes of no updates
        if time.time() - data.get("timestamp", 0) > 300:
            return "RUNNING"
            
        return data.get("status", "RUNNING")
    except:
        return "RUNNING"
