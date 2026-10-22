
import chromadb
from sentence_transformers import SentenceTransformer

# Part 1: Connect to the saved database
client = chromadb.PersistentClient(path="data/chroma_db")

# Part 2: Open our collection
collection = client.get_collection(name="pdf_chunks")

# Part 3: Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Chunks available:", collection.count())

while True:
    # Part 4: Get a question
    question = input("\nAsk a question (or type 'exit'): ")

    if question.lower().strip() == "exit":
        print("Goodbye!")
        break

    if not question.strip():
        print("Please enter a question.")
        continue

    # Part 5: Convert the question into an embedding
    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    # Part 6: Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    # Part 7: Display the retrieved passages
    print("\n===== SEARCH RESULTS =====")

    for rank, (document, metadata, distance) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ),
        start=1
    ):
        print(f"\nResult {rank}")
        print(f"Page: {metadata['page_number']}")
        print(f"Cosine distance: {distance:.4f}")
        print(document)
        print("-" * 50)

