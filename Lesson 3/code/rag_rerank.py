import os
import faiss
import numpy as np
import nltk
import json
import re
from google import genai
from google.genai import types
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer


client = genai.Client(api_key="")

# Download NLTK assets
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))


def load_documents(folder="data"):
    all_sentences = []
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                text = f.read()
                for sentence in sent_tokenize(text):
                    words = word_tokenize(sentence)
                    clean = [w for w in words if w.lower() not in stop_words and w.isalnum()]
                    all_sentences.append(" ".join(clean))
    print("All sentences:", all_sentences)
    return all_sentences


def create_faiss(sentences, model):
    embeddings = model.encode(sentences)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype(np.float32))
    return index, embeddings


def retrieve(query, model, index, sentences, k=10):
    """
    Retrieve MORE candidates than you will finally use.
    Then reranking will select the best subset.
    """
    query_embed = model.encode([query])
    D, I = index.search(np.array(query_embed).astype(np.float32), k)
    print(f"D, I:{D, I}")
    return [sentences[i] for i in I[0]]


def _safe_extract_json(text: str) -> dict:
    """
    Gemini may return JSON inside fences or with extra text.
    Try to extract a JSON object robustly.
    """
    text = text.strip()
    # Strip markdown code fences
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE | re.MULTILINE).strip()

    # Try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find first {...} block
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass

    return {}


def rerank_with_gemini(chunks, question, top_n=3):
    """
    Rerank retrieved chunks using Gemini:
    - Gemini scores each chunk for relevance to the question
    - Returns top_n chunks by score
    """
    if not chunks:
        return []

    # Keep prompt short-ish to reduce cost/latency.
    # We ask Gemini to output STRICT JSON with per-chunk scores.
    prompt = f"""You are a reranker for a Retrieval-Augmented Generation system.

Given a QUESTION and a list of CHUNKS, score each chunk by how useful it is for answering the question.
Score range: 0.0 (not useful) to 1.0 (highly useful).

Return ONLY valid JSON in the following format (no markdown, no extra text):
{{
  "scores": [
    {{"index": 0, "score": 0.0}},
    ...
  ]
}}

QUESTION:
{question}

CHUNKS:
""" + "\n".join([f"[{i}] {c}" for i, c in enumerate(chunks)])

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0),  # Disable "thinking"
            temperature=0.0,  # more deterministic scoring
        ),
    )

    raw = (response.text or "").strip()
    data = _safe_extract_json(raw)

    scores_list = data.get("scores", [])
    # Build a dict index -> score (fallback 0.0)
    score_map = {i: 0.0 for i in range(len(chunks))}
    for item in scores_list:
        try:
            idx = int(item.get("index"))
            sc = float(item.get("score"))
            if 0 <= idx < len(chunks):
                # clamp
                score_map[idx] = max(0.0, min(1.0, sc))
        except Exception:
            continue

    # Sort chunks by score desc
    reranked = sorted(
        [(chunks[i], score_map[i], i) for i in range(len(chunks))],
        key=lambda x: x[1],
        reverse=True,
    )

    print("\n--- Reranking scores (Gemini) ---")
    for chunk, sc, idx in reranked:
        print(f"[{idx}] score={sc:.3f} :: {chunk[:120]}{'...' if len(chunk) > 120 else ''}")

    return [chunk for chunk, _, _ in reranked[:top_n]]


def ask_gemini(context, question):
    prompt = f"""Use the following context to answer the question clearly.
If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:"""
    print("Prompt:", prompt)
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disable "thinking"
        ),
    )
    return (response.text or "").strip()


def main():

    print("Loading documents...")
    sentences = load_documents()

    print("Creating FAISS index...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index, _ = create_faiss(sentences, model)

    # You can tune these:
    retrieve_k = 12   # retrieve more candidates
    rerank_top_n = 3  # keep best after reranking

    while True:
        q = input("\nAsk something (or type 'exit'): ")
        if q.lower() == "exit":
            break

        # 1) Retrieve (FAISS)
        retrieved_chunks = retrieve(q, model, index, sentences, k=retrieve_k)
        print("\nRetrieved (pre-rerank):\n", "\n".join(retrieved_chunks))

        # 2) Rerank (Gemini)
        top_chunks = rerank_with_gemini(retrieved_chunks, q, top_n=rerank_top_n)

        # 3) Build context from reranked chunks
        context = "\n".join(top_chunks)
        print("\nReranked Context:\n", context)

        # 4) Answer (Gemini)
        answer = ask_gemini(context, q)
        print("\nGemini Answer:\n", answer)


if __name__ == "__main__":
    main()
