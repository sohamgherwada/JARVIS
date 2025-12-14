"""
JARVIS Verified Auto-Learner
Scrapes, Cross-References, and Verify knowledge using LLM.
"""
import sys
import os
import time
import random
import requests
import json
import ollama
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core.brain import Brain

TOPIC_FILE = os.path.join(os.path.dirname(__file__), "topic_to_learn")

def get_topics():
    if not os.path.exists(TOPIC_FILE):
        return []
    with open(TOPIC_FILE, 'r') as f:
        lines = f.readlines()
    topics = []
    for line in lines:
        clean = line.strip()
        if not clean: continue
        parts = clean.split(".")
        if len(parts) > 1 and parts[0].isdigit():
            clean = ".".join(parts[1:]).strip()
        topics.append(clean)
    return topics

def is_credible(url):
    # Strict blocklist: No social, no wiki, NO NEWS.
    blocklist = [
        "reddit.com", "quora.com", "twitter.com", 
        "facebook.com", "instagram.com", "tiktok.com", "pinterest.com",
        "medium.com", "stackexchange.com", "stackoverflow.com", "yahoo.com",
        "buzzfeed.com"
    ]
    domain = url.lower()
    for bad in blocklist:
        if bad in domain:
            return False
    return True

def scrape_url(url):
    if not is_credible(url):
        return None
    try:
        print(f"   🕷️ Scraping: {url[:60]}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join([p.get_text() for p in paragraphs])
        if len(text) < 500: return None
        return text[:15000] 
    except:
        return None

def verify_and_synthesize(topic, sources_text):
    """
    Uses LLM to cross-reference multiple sources and extract ONLY verified facts.
    """
    print(f"   ⚖️ Cross-Verifying {len(sources_text)} sources with Llama 3.1...")
    
    combined_input = ""
    for i, txt in enumerate(sources_text):
        combined_input += f"\n--- SOURCE {i+1} ---\n{txt[:2000]}\n"
        
    prompt = f"""
    You are a Strict Knowledge Curator.
    TOPIC: {topic}
    
    Task: Analyze the provided sources.
    1. Identify facts supported by multiple sources.
    2. Ignore opinions, ads, or unverified claims.
    3. Synthesize a dense, factual summary of the topic.
    
    Sources:
    {combined_input}
    
    Output ONLY the verified factual summary.
    """
    
    try:
        response = ollama.chat(model='mixtral', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        print(f"   ❌ LLM Error: {e}")
        return None

def run_learning_loop():
    brain = Brain()
    print(f"📚 Verified Auto-Learner Started.")
    
    while True:
        topics = get_topics()
        random.shuffle(topics)
        
        for topic in topics:
            print(f"\n🧠 RESEARCHING: {topic}")
            
            queries = [
                f"{topic} core concepts explained",
                f"{topic} comprehensive guide",
                f"{topic} scientific principles"
            ]
            
            for q in queries:
                print(f"🔍 Query: {q}")
                try:
                    # Get 5 results, keep Top 3 Credible
                    results = DDGS().text(q, max_results=8)
                    
                    found_sources = []
                    for r in results:
                        url = r['href']
                        content = scrape_url(url)
                        if content:
                            found_sources.append(content)
                        if len(found_sources) >= 3:
                            break
                    
                    if len(found_sources) >= 2:
                        # Synthesize
                        verified_knowledge = verify_and_synthesize(topic, found_sources)
                        
                        if verified_knowledge:
                            brain.learn(verified_knowledge, source=f"verified:{topic}")
                            print("      ✅ Verified Knowledge Stored.")
                        else:
                            print("      ⚠️ Failed to verify.")
                    else:
                        print("      ⚠️ Not enough credible sources found.")
                        
                except Exception as e:
                    print(f"   ⚠️ Loop Error: {e}")
                
                time.sleep(5)
            
            print(f"✅ Topic Complete: {topic}. Sleeping...")
            time.sleep(10)

if __name__ == "__main__":
    run_learning_loop()
