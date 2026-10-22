
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path

# Part 1: Load the chunks saved by our previous script
input_path = Path("data/chunks.json")

with input_path.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Chunks loaded:", len(chunks))

if not chunks:
    raise ValueError("No chunks found. Run 01_extract_text.py first.")

# Part 2: Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Part 3: Extract the text from every chunk
texts = [chunk["text"] for chunk in chunks]

# Part 4: Convert the text into numerical vectors
embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    normalize_embeddings=True,
    show_progress_bar=True
)

# Part 5: Save the vectors for later use
output_path = Path("data/embeddings.npy")
np.save(output_path, embeddings)

# Part 6: Validate the result
print("\n===== EMBEDDING REPORT =====")
print("Number of chunks:", len(chunks))
print("Embedding matrix shape:", embeddings.shape)
print("Vector dimensions:", embeddings.shape[1])
print("All values finite:", np.isfinite(embeddings).all())
print("First vector preview:", embeddings[0][:5])
print("Saved embeddings to:", output_path)
