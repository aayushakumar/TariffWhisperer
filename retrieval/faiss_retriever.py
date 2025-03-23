import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

class CBPRetriever:
    def __init__(self, index_path="data/faiss_index/cbp_index.faiss", metadata_path="data/faiss_index/cbp_metadata.json"):
        # Initialize the model and load index
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Check if index exists, if not create dummy one
        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            print("⚠️ FAISS index or metadata not found. Using sample data.")
            self._create_dummy_index(index_path, metadata_path)
        
        self.index = faiss.read_index(index_path)
        
        # Load metadata including the full text of each document
        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
        
        # Extract text chunks for retrieval
        self.chunk_texts = []
        for item in self.metadata:
            if 'text' in item:
                self.chunk_texts.append(item['text'])
            else:
                self.chunk_texts.append(item.get('title', 'No text available'))

    def _create_dummy_index(self, index_path, metadata_path):
        """Create a dummy index with sample data if none exists"""
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        # Sample rulings data
        sample_data = [
            {"url": "https://rulings.cbp.gov/rulings/NY123456", 
             "title": "Classification of Cotton T-Shirts", 
             "date": "2023-02-15", 
             "text": "The product under consideration is a 100% cotton short-sleeve men's t-shirt. The ruling classifies it under HTSUS 6109.10.00.10 as 'T-shirts, singlets and other vests of cotton'."},
            {"url": "https://rulings.cbp.gov/rulings/NY654321", 
             "title": "Men's Polyester Shorts", 
             "date": "2022-12-01", 
             "text": "The item is a pair of polyester athletic shorts. Based on material and function, it falls under HTSUS 6203.43.4010."},
            {"url": "https://rulings.cbp.gov/rulings/HQ789123", 
             "title": "Electronic Fitness Tracker", 
             "date": "2023-03-10", 
             "text": "The device is a wrist-worn fitness tracker with a heart rate sensor, classified under HTSUS 8517.62.0090."}
        ]
        
        # Extract text for embedding
        texts = [item['text'] for item in sample_data]
        
        # Embed text
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(texts)
        
        # Create and save the index
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(np.array(embeddings))
        faiss.write_index(index, index_path)
        
        # Save metadata
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(sample_data, f)
            
        print(f"✅ Created dummy index with {len(sample_data)} sample entries")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for documents similar to the query"""
        # Encode the query
        embedding = self.model.encode([query])
        
        # Search the index
        D, I = self.index.search(np.array(embedding), k)
        
        # Collect results with their metadata
        results = []
        for i in I[0]:
            if i < len(self.metadata):
                # Create a new result dict with the full text and metadata
                result = {
                    "text": self.chunk_texts[i] if i < len(self.chunk_texts) else "",
                    "url": self.metadata[i].get("url", ""),
                    "title": self.metadata[i].get("title", ""),
                    "date": self.metadata[i].get("date", "")
                }
                results.append(result)
                
        return results

if __name__ == "__main__":
    retriever = CBPRetriever()
    query = input("🔍 Enter your customs classification query: ")
    results = retriever.search(query)

    print("\nTop Matches:")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r['title']} ({r['date']})")
        print(f"URL: {r['url']}")
        print(f"Text: {r['text'][:300]}...")