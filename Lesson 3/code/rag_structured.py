import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ---------- 1) Load structured data ----------
df = pd.read_csv("animals.csv")

# ---------- 2) Convert each row -> "document text" ----------
# This is the core trick for structured datasets.
def row_to_text(row: pd.Series) -> str:
    return (
        f"ID: {row['id']}\n"
        f"Species: {row['species']}\n"
        f"Breed: {row['breed']}\n"
        f"Temperament: {row['temperament']}\n"
        f"AverageWeightKg: {row['avg_weight_kg']}\n"
        f"Notes: {row['notes']}\n"
    )

docs = [row_to_text(r) for _, r in df.iterrows()]

# ---------- 3) Embed documents (CPU-friendly model) ----------
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # small + good
doc_emb = model.encode(docs, normalize_embeddings=True)  # shape: (N, D)
doc_emb = np.asarray(doc_emb, dtype="float32")

# ---------- 4) Create a vector index (FAISS) ----------
dim = doc_emb.shape[1]
index = faiss.IndexFlatIP(dim)  # inner product works well with normalized embeddings (cosine)
index.add(doc_emb)

# ---------- 5) Query -> retrieve top-k rows ----------
def retrieve(query: str, k: int = 3):
    q_emb = model.encode([query], normalize_embeddings=True)
    q_emb = np.asarray(q_emb, dtype="float32")
    scores, ids = index.search(q_emb, k)
    results = []
    for rank, (i, s) in enumerate(zip(ids[0], scores[0]), start=1):
        results.append((rank, float(s), i, docs[i]))
    return results

def answer_without_llm(query: str):
    # For a basic class demo, we’ll just print the retrieved context.
    # Later you can send it into an LLM (Gemini/Local) to generate an answer.
    hits = retrieve(query, k=3)
    print("\n=== QUERY ===")
    print(query)
    print("\n=== TOP MATCHES ===")
    for rank, score, doc_id, doc_text in hits:
        print(f"\n--- Match #{rank} | score={score:.3f} | row_index={doc_id} ---")
        print(doc_text)

if __name__ == "__main__":
    # Try a few queries
    answer_without_llm("Which animal is calm and affectionate and good for indoor home?")
    answer_without_llm("I want a very active dog that needs lots of exercise and tasks.")
    answer_without_llm("Which breeds are intelligent and often used as working dogs?")
