# Document RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for querying your own PDF/image documents using OpenAI and local vector search (ChromaDB).

---

## Features

- **Document ingestion:** Extracts, chunks, and embeds text from PDFs (and images with OCR if Tesseract is installed).
- **Local vector search:** Uses ChromaDB for fast, private, local similarity search.
- **OpenAI-powered answers:** Uses GPT-4 to answer questions based on your documents.
- **Streamlit UI:** Simple web interface for asking questions and viewing source context.

---

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd ai_doc_rag
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
pip install chromadb streamlit
```

> **Note:** If you see deprecation warnings for LangChain, you can update to the new packages as needed.

### 3. Environment variables

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=your-pinecone-key   # (not used with Chroma, but may be required by some scripts)
PINECONE_ENVIRONMENT=us-east-1-aws   # (not used with Chroma, but may be required by some scripts)
```

### 4. Install Tesseract for OCR

If you want to process images, install Tesseract:

- **macOS:** `brew install tesseract`
- **Ubuntu:** `sudo apt-get install tesseract-ocr`

---

## Usage

### 1. Ingest your documents

Place your PDFs (and images) in the `data/` folder.

Run the ingestion script to process and embed your documents:

```sh
python src/ingest.py
```

### 2. Check your Chroma database

To see what’s stored:

```sh
python src/check_chroma.py
```

### 3. Run the chatbot UI

```sh
streamlit run src/main.py
```

Open the local URL shown in your terminal (e.g., http://localhost:8501).

---

## File Structure

- `src/ingest.py` — Ingests and embeds documents into Chroma
- `src/check_chroma.py` — Shows what’s in your Chroma database
- `src/main.py` — Streamlit web app for Q&A
- `src/rag_chain.py` — RAG chain logic (retrieval + LLM)
- `utils/logger.py` — Logging utility
- `data/` — Place your PDFs/images here
- `chroma_db/` — Local Chroma vector database

---

## Troubleshooting

- **No module named 'utils':**  
  Run with `PYTHONPATH=.` or use the provided code (which adds the project root to `sys.path`).
- **No documents in Chroma:**  
  Run `python src/ingest.py` after placing files in `data/`.
- **Tesseract errors:**  
  Install Tesseract if you want OCR for images.
- **Deprecation warnings:**  
  You can update to the new `langchain-huggingface` and `langchain-chroma` packages as needed.

---

## Credits

- Built with [LangChain](https://github.com/langchain-ai/langchain), [ChromaDB](https://www.trychroma.com/), [Streamlit](https://streamlit.io/), and [OpenAI](https://openai.com/). 
