# JARVIS API Documentation

JARVIS is running locally on `http://localhost:8000`.
You can communicate with him using standard HTTP requests from Python, JavaScript, C++, or any other language.

## 1. Simple Question (GET)
**Endpoint:** `/ask`
**Best for:** Quick answers, fetching data.
**Format:** Returns plain text.

### Python Example
```python
import requests

response = requests.get("http://localhost:8000/ask", params={"q": "What is the price of NVDA?"})
print(response.text)
# Output: "The current price of NVDA is..."
```

### JavaScript (Node/Browser) Example
```javascript
fetch("http://localhost:8000/ask?q=Who made you?")
  .then(res => res.text())
  .then(text => console.log(text));
```

---

## 2. Advanced Chat (POST)
**Endpoint:** `/chat`
**Best for:** Conversational apps, specifying persona (Friend/AI).
**Format:** Returns JSON `{ "response": "...", "actions_triggered": [] }`

### Python Example
```python
import requests

payload = {
    "message": "Should I call my ex?",
    "persona": "friend"  # Options: "friend" or "ai"
}

response = requests.post("http://localhost:8000/chat", json=payload)
data = response.json()
print(data["response"]) 
# Output: "Don't do it, Sir! Bad idea."
```

### JavaScript Example
```javascript
const payload = {
    message: "Write a python script",
    persona: "ai"
};

fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
})
.then(res => res.json())
.then(data => console.log(data.response));
```

## 3. Actions (POST)
**Endpoint:** `/action`
**Best for:** Controlling the PC.

```python
requests.post("http://localhost:8000/action", params={"command": "OPEN: spotify"})
```
