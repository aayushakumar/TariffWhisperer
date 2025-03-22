import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

class CBPRetriever:
    def __init__(self, index_path="data/faiss_index/cbp_index.faiss", metadata_path="data/faiss_index/cbp_metadata.json"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)

        self.chunk_texts = [m["title"] for m in self.metadata]  # optional override

    def search(self, query: str, k: int = 5):
        embedding = self.model.encode([query])
        D, I = self.index.search(np.array(embedding), k)

        results = []
        for i in I[0]:
            if i < len(self.metadata):
                result = {
                    "text": self.chunk_texts[i],
                    "url": self.metadata[i].get("url"),
                    "title": self.metadata[i].get("title"),
                    "date": self.metadata[i].get("date")
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
        print(f"Text: {r['text'][:300]}...\n")
