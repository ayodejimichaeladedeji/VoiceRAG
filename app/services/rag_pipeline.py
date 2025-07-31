import os
from google import genai
from pinecone import Pinecone
from services.embedding import embed_texts

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("INDEX_NAME"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def answer_with_rag(query: str, top_k: int = 5, score_threshold: float = 0.6) -> str:
    query_vector = embed_texts([query])[0].values

    results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    retrieved_texts = [
        match["metadata"]["text"]
        for match in results.get("matches", [])
        if match["score"] >= score_threshold
    ]

    if not retrieved_texts:
        prompt = f"Answer the following question:\n{query}\nAnswer:"
    else:
        context = "\n\n".join(retrieved_texts)
        prompt = f"""You are a helpful AI assistant.

Answer the following question using the context below.

Context:
{context}

Question: {query}
Answer:"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()