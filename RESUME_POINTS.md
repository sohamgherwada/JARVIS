# JARVIS - Autonomous Multi-Agent AI System

## Project Summary
Architected and built "JARVIS," a local, privacy-focused autonomous Super-Intelligence system capable of continuous learning, multi-modal interaction (Text/Voice/Vision), and PC automation. The system utilizes a Multi-Agent "Orchestra" for background research, a Vector Database (LanceDB) for long-term memory (RAG), and a FastAPI backend for external integration.

## Key Technologies & Skills
*   **AI & LLMs**: Python, Ollama (Mixtral 8x7B, Mistral, Llava), Prompt Engineering, Context Window Management.
*   **RAG Architecture**: LanceDB (Vector DB), Semantic Search, Embeddings (nomic-embed-text), Data Deduplication.
*   **Multi-Agent Systems**: Threaded Orchestration (`ThreadPoolExecutor`), Autonomous Web Scraping (`duckduckgo-search`, `BeautifulSoup`), Self-Correction/Verification Loops.
*   **Backend & API**: FastAPI, Uvicorn, REST API Design, Pydantic, JSON.
*   **Computer Vision**: Multimodal AI (Llava), Screen Capture (`mss`), Image Processing (`Pillow`), OCR.
*   **Automation**: System Control (`pyautogui`), Dynamic Command Execution, App Management.

## Bullet Points for Resume
*   **Developed a Local RAG System**: Implemented a Retrieval-Augmented Generation pipeline using LanceDB and Ollama, allowing the AI to retain and recall thousands of verified knowledge chunks with semantic search and real-time deduplication.
*   **Engineered a Multi-Agent "Knowledge Orchestra"**: Created a concurrent multi-agent framework where "Curious Agents" autonomously hypothesize questions, scrape the web for academic sources, verify credibility, and synthesize findings into the knowledge base without human intervention.
*   **Built a Predictive "Oracle" Engine**: Designed a probabilistic forecasting module that aggregates real-time data from multiple web searches (stats, betting odds, news) to generate high-confidence predictions with percentage probabilities.
*   **Implemented Multimodal capabilities**: Integrated Vision LLMs (Llava) to allow the system to "see" and analyze screen content and educational diagrams referenced via URLs.
*   **Deployed REST API Interface**: Exposed core AI functionalities via a robust FastAPI server, enabling external software integration and modular interaction with the JARVIS core.
*   **Optimized for Consumer Hardware**: Tuned model selection (Mixtral vs Mistral) and implemented lazy-loading and resource management to ensure stable performance on local hardware.
