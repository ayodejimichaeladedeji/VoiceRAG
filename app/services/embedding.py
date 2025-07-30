import os
import fitz
import uuid
from google import genai
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

existing_indexes = [ix.name for ix in pc.list_indexes()]

if os.getenv("INDEX_NAME") not in existing_indexes:
    pc.create_index(
        name=os.getenv("INDEX_NAME"),
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(os.getenv("INDEX_NAME"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def embed_texts(texts: list[str]):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config={
            'output_dimensionality': 1536
        }
    )
    return response.embeddings

def parse_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    return " ".join(page.get_text() for page in doc)


def chunk_text(text: str, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks


def embed_and_store(file_path: str):
    text = parse_pdf(file_path)
    chunks = chunk_text(text)

    embeddings = embed_texts(chunks)

    vectors = []
    for chunk, embedding in zip(chunks, embeddings):
        vectors.append({
            "id": str(uuid.uuid4()),
            "values": embedding.values,
            "metadata": {"text": chunk}
        })

    index.upsert(vectors)

    return {"num_chunks": len(chunks), "uploaded": len(vectors)}

def preview_vectors(query, top_k=5):
    query_embedding_obj = embed_texts(query)[0]
    query_vector = query_embedding_obj.values

    result = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    response = []
    for i, match in enumerate(result.get("matches", []), 1):
        response.append({
            "vector_number": i,
            "id": match["id"],
            "score": match["score"],
            "text": match["metadata"].get("text")
        })
    return response
