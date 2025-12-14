"""
JARVIS Brain (RAG System)
Stores knowledge in LanceDB (Disk-based Vector Store) for infinite scaling.
"""
import os
import json
import numpy as np
import lancedb
from pathlib import Path
from datetime import datetime

# We verify ollama import here
try:
    import ollama
except ImportError:
    print("❌ Critical: Ollama python package not installed.")

BRAIN_DIR = Path(__file__).parent.parent / "brain_data"
BRAIN_DIR.mkdir(exist_ok=True)
DB_PATH = BRAIN_DIR / "lancedb"

class Brain:
    def __init__(self):
        print("🧠 Initializing Neural Pathways (LanceDB + Ollama)...")
        try:
            # We use Ollama for embeddings (nomic-embed-text)
            self.embed_model = "nomic-embed-text" 
            
            # Test connection
            ollama.embeddings(model=self.embed_model, prompt="startup_check")
            self.has_model = True
            print("   ✅ Ollama Embeddings Connected.")
        except Exception as e:
            print(f"⚠️ Embedding model error: {e}")
            print("   (Make sure 'ollama pull nomic-embed-text' was run)")
            self.has_model = False
            
        # Connect to LanceDB
        self.db = lancedb.connect(str(DB_PATH))
        self.table = None
        
        # Open table if exists
        try:
            if "knowledge" in self.db.table_names():
                self.table = self.db.open_table("knowledge")
        except:
            pass

    def learn(self, text: str, source: str = "user"):
        """Ingest text into the brain"""
        if not self.has_model:
            print("❌ ERROR: Brain has no embedding model. Cannot learn.")
            return
        if not text.strip():
            return
            
        print(f"🧠 Learning from {source}...")
        
        # Chunking
        raw_chunks = [text[i:i+500] for i in range(0, len(text), 400)]
        embeddings = []
        
        try:
            for chunk in raw_chunks:
                res = ollama.embeddings(model=self.embed_model, prompt=chunk)
                embeddings.append(res['embedding'])
        except Exception as e:
            print(f"❌ Error generating embeddings: {e}")
            return
        
        data = []
        for i, chunk in enumerate(raw_chunks):
            entry = {
                "vector": embeddings[i],
                "text": chunk,
                "source": source,
                "timestamp": datetime.now().isoformat()
            }
            data.append(entry)
            
        if self.table is None:
            # Create table
            try:
                self.table = self.db.create_table("knowledge", data)
            except Exception as e:
                print(f"❌ Error creating table: {e}")
        else:
            try:
                self.table.add(data)
            except Exception as e:
                print(f"❌ Error adding data (Possible dimension mismatch?): {e}")
            
        print(f"   ✓ Absorbed {len(raw_chunks)} new concepts.")

    def recall(self, query: str, top_k=3, threshold=0.5):
        """
        Retrieve relevant knowledge with metadata.
        threshold: Max distance for relevance (lower = stricter). 
                   0.0 = exact match, 1.0 = somewhat loosely related.
        """
        if not self.has_model or self.table is None:
            return []
            
        try:
            res = ollama.embeddings(model=self.embed_model, prompt=query)
            query_embedding = res['embedding']
            
            # Search
            results = self.table.search(query_embedding).limit(top_k).to_list()
            
            # Filter by relevance (Distance check)
            # Note: LanceDB returns '_distance'. Lower is closer.
            filtered = [r for r in results if r['_distance'] < threshold]
            
            if len(filtered) < len(results):
                print(f"      (Filtered {len(results)-len(filtered)} irrelevant memories)")
                
            return filtered 
        except Exception as e:
            # print(f"Recall error: {e}")
            return []

# Test
if __name__ == "__main__":
    b = Brain()
