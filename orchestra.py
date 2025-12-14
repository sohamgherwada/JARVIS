"""
JARVIS Knowledge Orchestra (Smart Agents)
Agents with Curiosity, Time Limits, and Relevance Filters.
"""
import sys
import os
import time
import random
import threading
import queue
import ollama
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolearn import get_topics, scrape_url, DDGS
from core.brain import Brain
from core.vision import Vision
from core.coordination import get_orchestra_status

class CuriousAgent:
    def __init__(self, agent_id, brain):
        self.id = agent_id
        self.brain = brain
        self.model = "mixtral"
        self.vision = Vision()
        
    def think(self, prompt):
        try:
            res = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
            return res['message']['content']
        except:
            return ""

    def evaluate_importance(self, topic, text):
        """
        Ask LLM: Is this information critical for expert understanding?
        """
        if len(text) < 200: return False # Too short
        
        prompt = f"""
        TOPIC: {topic}
        CONTENT SNIPPET: {text[:500]}...
        
        Task: Decide if this content is RELEVANT and USEFUL for the topic.
        Criterion: Returns facts, definitions, or explanations.
        
        Reply with exactly "YES" or "NO".
        """
        response = self.think(prompt).strip().upper()
        return "YES" in response

    def research_loop(self, topic, max_duration=120):
        """
        Research a topic for a limited time (max_duration seconds).
        """
        start_time = time.time()
        print(f"   🎻 Agent {self.id}: Starting deep dive on '{topic}' (Limit: {max_duration}s)")
        
        # 1. Hypothesize Questions
        hypo_prompt = f"Generate 3 specific, expert-level search queries to find ACADEMIC RESEARCH or SCHOLARLY ARTICLES to understand '{topic}' deeply. Include terms like 'journal', 'research paper', or 'overview'. Return only the queries, one per line."
        queries_text = self.think(hypo_prompt)
        queries = [q.strip() for q in queries_text.split('\n') if q.strip()]
        
        for q in queries:
            # Check Time
            if time.time() - start_time > max_duration:
                print(f"   ⌛ Agent {self.id}: Time limit reached for '{topic}'.")
                break
                
            print(f"   🔍 Agent {self.id} searching: {q}")
            
            # 2. Search
            try:
                # Text Search
                results = DDGS().text(q, max_results=3)
                
                # VISUAL LEARNING INJECTION
                # If topic suggests visual data, look for images
                if any(k in topic.lower() for k in ["physics", "math", "diagram", "chart", "biology", "structure"]):
                    print(f"   🖼️ Visual Search: Seeking diagrams for '{topic}'...")
                    img_results = DDGS().images(q, max_results=2)
                    for img in img_results:
                        desc = self.vision.analyze_image_from_url(img['image'], prompt=f"Explain this {topic} diagram/image in technical detail.")
                        if desc:
                            self.brain.learn(f"[VISUAL MEMORY] Image of {topic}: {desc}", source=f"vision:{img['image']}")
            except:
                results = []  # Fallback if search fails
                continue
                
            for r in results:
                # Check Time again
                if time.time() - start_time > max_duration: break
                
                # 3. Scrape
                try:
                    content = scrape_url(r['href'])
                except:
                    content = None
                    
                if content:
                    # 4. Filter Importance
                    is_important = self.evaluate_importance(topic, content)
                    
                    if is_important:
                        # 5. Synthesize & Store
                        # We store the raw credible content + meta
                        self.brain.learn(content, source=f"orchestra:{topic}")
                        print(f"      💎 Agent {self.id}: Found GEM! Stored info about {topic}.")
                    else:
                        print(f"      🗑️ Agent {self.id}: Discarded trivial info.")
                        
                time.sleep(1) 

class Orchestra:
    def __init__(self, max_agents=3):
        self.max_agents = max_agents
        self.brain = Brain()
        self.topics = get_topics()
        self.work_queue = queue.Queue()
        
        # Mix topics
        start_topics = self.topics if self.topics else ["Artificial Intelligence", "Rocket Science"]
        for t in start_topics:
            self.work_queue.put(t)
            
    def agent_worker(self, agent_id):
        agent = CuriousAgent(agent_id, self.brain)
        
        while True:
            # COORDINATION CHECK
            status = get_orchestra_status()
            if status == "PAUSED":
                # print(f"   🎻 Agent {agent_id}: Paused for User Chat...")
                time.sleep(3)
                continue
                
            try:
                # Infinite wait for work
                topic = self.work_queue.get(timeout=3) 
            except queue.Empty:
                # If truly empty, refill with base topics to re-verify
                time.sleep(5)
                continue
                
            try:
                agent.research_loop(topic, max_duration=120)
                
                # Recursive Expansion: Add 1 new related topic
                new_idea = agent.think(f"Based on {topic}, suggest 1 advanced related sub-topic to research next. Return ONLY the topic name.")
                if new_idea and len(new_idea) < 50:
                    print(f"   🎻 Agent {agent_id}: Proposed new topic '{new_idea.strip()}'")
                    self.work_queue.put(new_idea.strip())
            except Exception as e:
                print(f"   ⚠️ Agent {agent_id} crashed (restarting): {e}")
                
            self.work_queue.task_done()
            
    def start_symphony(self):
        print(f"🎼 Starting the Infinite Knowledge Symphony with {self.max_agents} agents...")
        # Pre-fill queue
        for t in self.topics:
            self.work_queue.put(t)
            
        with ThreadPoolExecutor(max_workers=self.max_agents) as executor:
            for i in range(self.max_agents):
                executor.submit(self.agent_worker, i+1)
        
        # Keep main thread alive
        while True:
            time.sleep(60)

if __name__ == "__main__":
    if not os.path.exists("topic_to_learn"):
         with open("topic_to_learn", "w") as f:
             f.write("Quantum Physics\nNeuroscience")
             
    conductor = Orchestra(max_agents=5) 
    conductor.start_symphony()
