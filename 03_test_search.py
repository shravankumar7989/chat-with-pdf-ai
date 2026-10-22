
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Part 1: Load the saved chunks
with Path("data/chunks.json").open("r", encoding="utf-8") as file:
    chunks = json.load(file)

# Part 2: Load the saved embeddings
embeddings = np.load("data/embeddings.npy")

# Part 3: Load the same model used to create the embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Part 4: Get a question from the user
question = input("Ask a question about your PDF: ")

# Part 5: Convert the question into a vector
question_embedding = model.encode(
    question,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# Part 6: Calculate similarity with every chunk
scores = embeddings @ question_embedding

# Part 7: Find the three highest-scoring chunks
top_indices = np.argsort(scores)[::-1][:5]

# Part 8: Display the results
print("\n===== SEARCH RESULTS =====")

for rank, index in enumerate(top_indices, start=1):
    chunk = chunks[index]

    print(f"\nResult {rank}")
    print(f"Similarity score: {scores[index]:.4f}")
    print(f"Source page: {chunk['page_number']}")
    print(chunk["text"])
    print("-" * 50)
