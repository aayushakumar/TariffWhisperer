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
        return [ruling]
    
    # If text is longer, create multiple chunks
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk_ruling = ruling.copy()
        chunk_ruling["text"] = text[i:i+chunk_size]
        chunk_ruling["chunk_id"] = i // chunk_size
        chunks.append(chunk_ruling)
    return chunks

def embed_and_store(rulings, faiss_dir="data/faiss_index/"):
    os.makedirs(faiss_dir, exist_ok=True)

    # Store chunked rulings with their metadata
    chunked_rulings = []
    
    for ruling in rulings:
        chunks = chunk_ruling(ruling)
        chunked_rulings.extend(chunks)

    print(f"[✓] Total chunks to embed: {len(chunked_rulings)}")
    
    # Extract text for embedding
    texts = [ruling["text"] for ruling in chunked_rulings]

    # Embed text
    embeddings = model.encode(texts, show_progress_bar=True)

    # Store in FAISS
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    # Save index
    faiss.write_index(index, os.path.join(faiss_dir, "cbp_index.faiss"))

    # Save metadata (including full text)
    with open(os.path.join(faiss_dir, "cbp_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(chunked_rulings, f)

    print(f"[✓] Stored {len(chunked_rulings)} entries in FAISS at {faiss_dir}")

if __name__ == "__main__":
    rulings = load_rulings("data/cbp_rulings.jsonl")
    embed_and_store(rulings)