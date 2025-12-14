# JARVIS: The Knowledge Orchestra 🎻

This is a **Local AI Research System** built on Llama 3.1, LanceDB, and Python.
It consists of two parts:
1.  **Orchestra**: A swarm of agents that research topics 24/7.
2.  **Chatbot**: A text-interface to query the massive Brain.

---

## � TECHNOLOGY STACK

The system is built on a high-performance, local-first stack designed for privacy and massive scale.

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Language Implementation** | **Python 3.12** | Selected for stability and ecosystem compatibility (over 3.14). |
| **Intelligence Engine** | **Llama 3.1 (8B)** | Running locally via **Ollama**. Provides privacy and zero-latency reasoning. |
| **Vector Memory** | **LanceDB** | **Disk-based vector store**. Chosen allowing infinite knowledge without crashing RAM. |
| **Search Engine** | **DuckDuckGo API** | accurate, rate-limit friendly web search without tracking. |
| **Scraper** | **BeautifulSoup4** | Lightweight HTML parsing for extracting text from websites. |
| **Coordinator** | **Python Threading** | Manages parallel agents in the Orchestra. |
| **Document Generation** | **python-docx** | Programmatic creation of Word reports. |

---

## ⚖️ REALITY CHECK: JARVIS vs. CHATGPT

Let's be honest. You are running an 8 Billion parameter model on a gaming PC. OpenAI runs Trillion parameter models on supercomputers.

| Feature | 🤖 JARVIS (Local Llama 3.1) | 🧠 ChatGPT / Gemini |
| :--- | :--- | :--- |
| **Raw Intelligence** | ** moderate**. Like a smart undergrad. Good at summaries, okay at logic. | **Super-Human**. PhD level reasoning, coding, and creativity. |
| **Privacy** | **ABSOLUTE**. Your data never leaves your PC. | **Zero**. Your data is used for training. |
| **Cost** | **Free** (Electricity only). | $20/month subscription. |
| **Integration** | **High**. Can open apps, type keys, see your screen, and control your PC. | **Low**. Cloud-based. Cannot control your mouse/keyboard. |
| **Memory** | **Infinite & Specific**. You control exactly what it learns. | **Limited**. Opaque memory mechanism. |
| **Uptime** | **Always On**. Runs 24/7 in background. | Rate limits, timeouts. |

**The Verdict:**
- If you need to solve a complex math proof or write a novel: **Use ChatGPT**.
- If you want a privacy-focused Research Assistant that builds a database of *exactly* what you care about and never forgets it: **Use JARVIS**.

---

## 🧠 STRATEGIC DESIGN DECISIONS

These key architecture choices were made to evolve the AI from a "Chatbot" to a "Super-Intelligence".

### 1. The "Orchestra" Model vs. Single Assistant
**Decision:** Instead of one assistant doing one thing at a time, we built a **Multi-Agent Swarm**.
**Result:** 4+ Agents hunt for information in parallel. The AI learns 4x faster than a human could efficiently search.

### 2. Infinite Recursive Curiosity
**Decision:** We removed the "Stop when done" logic.
**Result:** When the AI learns a topic (e.g., "Physics"), it *self-generates* new sub-topics (e.g., "Quantum Mechanics") and adds them to its queue. It never stops learning.

### 3. "Verified Truth" Protocol
**Decision:** We explicitly **BLOCKED** social media (Reddit, Twitter) and unreliable sources (Wikipedia, News).
**Result:** The Brain only consumes high-quality, verified data. A "Critic Agent" uses Llama 3.1 to cross-reference facts before saving them.

### 4. Disk-Based Memory (LanceDB)
**Decision:** We rejected in-memory vector stores (like FAISS in RAM) in favor of LanceDB.
**Result:** You can run this system for **years**, accumulating Terabytes of knowledge, and it will run on the same consumer hardware.

### 5. "Hush Mode" Coordination
**Decision:** The system monitors your typing.
**Result:** Background agents PAUSE instantly when you interact, giving 100% of system resources to answering your question, then RESUME automatically.

---

## �🛠️ HOW TO BUILD FROM SCRATCH

If you lose this code, follow these exact steps to rebuild it.

### 1. Prerequisites
- **OS**: Windows 10/11
- **GPU**: NVIDIA RTX (Recommended) for local LLM speed.
- **Python**: Version **3.12** (Required for LanceDB/Torch compatibility).
- **Ollama**: Download from [ollama.com](https://ollama.com).

### 2. Install AI Models
Open a terminal and run:
```powershell
ollama pull llama3.1
ollama pull llama3.2-vision
```

### 3. Project Structure
Create a folder `JARVIS` and these sub-folders/files:
```text
JARVIS/
├── core/
│   ├── __init__.py           (Empty file)
│   ├── brain.py              (LanceDB Vector Store logic)
│   ├── coordination.py       (Pause/Resume logic)
│   ├── actions.py            (Web Search & Word Docs)
│   └── llm_stream.py         (Ollama Connection)
├── brain_data/               (Auto-created database folder)
├── chatbot.py                (The User Interface)
├── orchestra.py              (The Research Agents)
├── autolearn.py              (Helper functions for scraping)
├── topic_to_learn            (Text file with list of topics)
└── requirements.txt          (List of python libraries)
```

### 4. Dependencies (`requirements.txt`)
Create `requirements.txt` with this content:
```text
ollama
lancedb
duckduckgo-search
beautifulsoup4
requests
python-docx
mss
Pillow
sentence-transformers
scikit-learn
```

### 5. Installation
Run this command in the `JARVIS` folder:
```powershell
py -3.12 -m pip install -r requirements.txt
```

### 6. The Code Logic (Quick Reference)

**A. `core/brain.py`**
- Initialize `lancedb.connect("brain_data/lancedb")`.
- `learn(text)`: Embeds text using `sentence-transformers` and saves to DB.
- `recall(query)`: Searches DB vectors.

**B. `orchestra.py`**
- Loops through `topic_to_learn`.
- Spawns `CuriousAgent` threads.
- **Loop**: Search -> Scrape -> LLM Verify -> Brain.learn().
- **Coordination**: Checks `core.coordination.get_orchestra_status()`.

**C. `chatbot.py`**
- Accepts user input.
- Sets `coordination` to "PAUSED" when user types.
- Queries `Brain.recall()`.
- Generates answer with Ollama.

### 7. Running the System
You need **TWO** terminals.

**Terminal 1 (The Researcher):**
```powershell
py -3.12 orchestra.py
# Scrapes the web 24/7.
```

**Terminal 2 (The Interface):**
```powershell
py -3.12 chatbot.py
# Chat with your AI.
```
