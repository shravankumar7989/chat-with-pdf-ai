# Chat with PDF AI 🤖📄

**Ask questions about your PDF documents using AI and Retrieval-Augmented Generation (RAG).**

Chat with PDF AI is a web application that lets users upload PDF documents and ask questions about their content. It retrieves relevant passages from the document and uses a local language model to generate context-based answers.

## ✨ Features

- 📄 Upload PDF documents through a web interface.
- 🔍 Extract and process text from PDF files.
- 🧩 Split text into overlapping chunks.
- 🧠 Generate semantic embeddings using Sentence Transformers.
- 🗄️ Store and retrieve document chunks using ChromaDB.
- 💬 Ask natural-language questions about document content.
- 📚 Display relevant source passages and page references.
- 🖥️ Run the language model locally using Ollama.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Flask | Backend and API |
| HTML, CSS, JavaScript | User interface |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embeddings |
| ChromaDB | Vector storage and semantic retrieval |
| Ollama | Local language model |
| Qwen 2.5 (3B) | Answer generation |

## 🧠 How It Works

1. **Upload:** The user uploads a PDF document.
2. **Extract:** Text is extracted from the document.
3. **Chunk:** The text is divided into smaller, overlapping sections.
4. **Embed:** Each section is converted into a vector embedding.
5. **Store:** The embeddings and associated metadata are stored in ChromaDB.
6. **Retrieve:** When the user asks a question, the application retrieves relevant sections.
7. **Generate:** The retrieved context is sent to the local Qwen model through Ollama.
8. **Answer:** The application returns an answer with relevant source information.

## 🏗️ Project Structure

```text
pdf-RAG/
├── app.py
├── 01_extract_text.py
├── 02_create_embeddings.py
├── 03_test_search.py
├── 04_store_in_chroma.py
├── 05_search_chroma.py
├── 06_chat_with_pdf.py
├── 07_improved_chat.py
├── requirements.txt
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── data/          # Local generated data
└── uploads/       # Uploaded PDF files
```

## ⚙️ Run Locally

### Prerequisites

- Python 3
- Git
- Ollama installed and running
- The `qwen2.5:3b` model

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd pdf-RAG
```

Replace `YOUR_REPOSITORY_URL` with this repository's HTTPS URL.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the language model

```bash
ollama pull qwen2.5:3b
```

Ensure Ollama is running before starting the application.

### 5. Start the application

```bash
python app.py
```

Open your browser and visit:

`http://127.0.0.1:5000`

**Note:** A fresh installation may require initializing the ChromaDB collection and preparing document data. The existing local database and uploaded PDFs are not included in this repository.

## 🔒 Privacy and Local Execution

The application is designed to use a local Ollama model. Uploaded documents and generated vector data are stored locally by the application and are not included in this Git repository.

Actual data handling depends on your local configuration.

## 🚀 Future Improvements

- Document management and deletion.
- Better retrieval accuracy and source citations.
- Document-specific conversation history.
- Support for multiple documents and collections.
- Improved error handling and user experience.
- Optional cloud deployment.

## 👨‍💻 About

This project explores Retrieval-Augmented Generation, semantic search, vector databases, PDF processing, and local large language models through a practical web application.
