
import pymupdf

pdf_path = "data/sample.pdf"

pages = []

with pymupdf.open(pdf_path) as doc:
    for page_index, page in enumerate(doc):
        page_number = page_index + 1
        text = page.get_text()

        page_info = {
            "page_number": page_number,
            "text": text
        }

        pages.append(page_info)

print("Total pages extracted:", len(pages))

if pages:
    print("First page text:")
    print(pages[0]["text"])


chunks = []

chunk_size = 500
overlap = 100

for page_info in pages:
    text = page_info["text"]
    page_number = page_info["page_number"]

    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]

        if chunk_text.strip():
            chunks.append({
                "page_number": page_number,
                "chunk_index": chunk_index,
                "text": chunk_text
            })
            chunk_index += 1

        if end >= len(text):
            break

        start = end - overlap

print("Total chunks created:", len(chunks))

if chunks:
    print("First chunk:")
    print(chunks[0])
else:
    print("No chunks were created. Check whether your PDF contains extractable text.")



# Part 3: Validate the extracted pages and chunks

print("\n===== VALIDATION REPORT =====")

# 1. Check page extraction
print("Pages extracted:", len(pages))

pages_with_text = sum(
    1 for page in pages if page["text"].strip()
)

print("Pages containing text:", pages_with_text)

# 2. Check chunk quality
print("Total chunks:", len(chunks))

empty_chunks = sum(
    1 for chunk in chunks if not chunk["text"].strip()
)

print("Empty chunks:", empty_chunks)

unique_chunks = len(set(chunk["text"] for chunk in chunks))
print("Unique chunk texts:", unique_chunks)

# 3. Count chunks belonging to each page
chunks_per_page = {}

for chunk in chunks:
    page_number = chunk["page_number"]

    if page_number not in chunks_per_page:
        chunks_per_page[page_number] = 0

    chunks_per_page[page_number] += 1

print("\nChunks per page:")
for page_number, count in chunks_per_page.items():
    print(f"Page {page_number}: {count} chunks")

# 4. Check overlap between consecutive chunks
overlap_errors = 0

for i in range(1, len(chunks)):
    previous = chunks[i - 1]
    current = chunks[i]

    # Compare only chunks from the same page
    if (
        previous["page_number"] == current["page_number"]
        and current["chunk_index"] == previous["chunk_index"] + 1
    ):
        previous_text = previous["text"]
        current_text = current["text"]

        if previous_text[-overlap:] != current_text[:overlap]:
            overlap_errors += 1

print("\nOverlap mismatches:", overlap_errors)

# 5. Preview chunks without printing all 81
if chunks:
    sample_indexes = sorted(set([
        0,
        len(chunks) // 2,
        len(chunks) - 1
    ]))

    print("\n===== CHUNK PREVIEWS =====")

    for index in sample_indexes:
        chunk = chunks[index]

        print(
            f"\nChunk list position: {index}"
            f"\nSource page: {chunk['page_number']}"
            f"\nChunk index on page: {chunk['chunk_index']}"
        )

        print(chunk["text"][:250])


import json
from pathlib import Path

output_path = Path("data/chunks.json")

with output_path.open("w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print(f"\nSaved {len(chunks)} chunks to {output_path}")