import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load rulings
def load_rulings(path="data/cbp_rulings.jsonl"):
    rulings = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
                if obj.get("text"):
                    rulings.append(obj)
            except:
                continue
    return rulings

# Chunk text if needed (can skip if short)
def chunk_ruling(ruling, chunk_size=500):
    text = ruling["text"]
    if len(text) <= chunk_size:
        return [text]
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_and_store(rulings, faiss_dir="data/faiss_index/"):
    os.makedirs(faiss_dir, exist_ok=True)

    texts = []
    metadata = []

    for ruling in rulings:
        chunks = chunk_ruling(ruling)
        for chunk in chunks:
            texts.append(chunk)
            metadata.append({
                "title": ruling.get("title"),
                "url": ruling.get("url"),
                "date": ruling.get("date")
            })

    print(f"[✓] Total chunks to embed: {len(texts)}")

    # Embed text
    embeddings = model.encode(texts, show_progress_bar=True)

    # Store in FAISS
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    # Save index
    faiss.write_index(index, os.path.join(faiss_dir, "cbp_index.faiss"))

    # Save metadata
    with open(os.path.join(faiss_dir, "cbp_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f)

    print(f"[✓] Stored {len(texts)} entries in FAISS at {faiss_dir}")

if __name__ == "__main__":
    rulings = load_rulings("data/cbp_rulings.jsonl")
    embed_and_store(rulings)
