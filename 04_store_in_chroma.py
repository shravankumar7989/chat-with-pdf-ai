
import json
import numpy as np
import chromadb
from pathlib import Path

# Part 1: Load chunks and their embeddings
with Path("data/chunks.json").open("r", encoding="utf-8") as file:
    chunks = json.load(file)

embeddings = np.load("data/embeddings.npy")

# Part 2: Verify that the data matches
if len(chunks) != len(embeddings):
    raise ValueError("Chunk count and embedding count do not match.")

# Part 3: Create a persistent ChromaDB database
client = chromadb.PersistentClient(path="data/chroma_db")

# Part 4: Create or reuse a collection
collection = client.get_or_create_collection(
    name="pdf_chunks",
    metadata={"hnsw:space": "cosine"}
)

# Part 5: Store chunks in batches
batch_size = 100

for start in range(0, len(chunks), batch_size):
    end = min(start + batch_size, len(chunks))

    batch_chunks = chunks[start:end]
    batch_embeddings = embeddings[start:end]

    collection.upsert(
        ids=[f"chunk_{i}" for i in range(start, end)],
        documents=[chunk["text"] for chunk in batch_chunks],
        metadatas=[
            {
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"]
            }
            for chunk in batch_chunks
        ],
        embeddings=batch_embeddings.tolist()
    )

print("Chunks stored:", collection.count())
print("Database location: data/chroma_db")
