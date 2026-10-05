# Rag-application
# PDF RAG Application

A Retrieval-Augmented Generation (RAG) application for asking questions about information contained in PDF research papers.

The current application extracts text from PDFs, divides the text into chunks, creates embeddings, stores them in ChromaDB, retrieves relevant information for a user question, and uses a local Qwen 2.5 7B model through Ollama to generate a grounded answer.

---

## 1. Project Goal

The main goal of this project is to build a RAG application that can:

* Read information from PDF documents
* Extract and process the PDF text
* Divide large documents into smaller chunks
* Convert chunks into vector embeddings
* Store the embeddings in a vector database
* Retrieve relevant information for a question
* Generate an answer using the retrieved information
* Show the PDF, page, and chunk used for the answer
* Provide a simple user interface

The current PDFs are related to PCB inspection and PCB defect detection research.

---

## 2. RAG Architecture

The current system works as follows:

```text
                    PDF Documents
                          │
                          ▼
                  PDF Text Extraction
                          │
                          ▼
                      Chunking
                          │
                          ▼
                     Embeddings
                          │
                          ▼
                      ChromaDB
                          │
                          │
                    User Question
                          │
                          ▼
                  Question Embedding
                          │
                          ▼
                 Similarity Retrieval
                          │
                          ▼
                  Relevant PDF Chunks
                          │
                          ▼
                   Ollama + Qwen 2.5 7B
                          │
                          ▼
                    Generated Answer
                          │
                          ▼
                 Answer + PDF Sources
```

---

## 3. Technologies Used

### Python

Python is used to implement the complete RAG pipeline.

### PyMuPDF

Used for extracting text from PDF documents.

### Sentence Transformers

Used to generate vector embeddings.

Current embedding model:

```text
all-MiniLM-L6-v2
```

The embedding dimension is:

```text
384
```

### ChromaDB

Used as the vector database for storing:

* PDF chunks
* embeddings
* source information
* page numbers
* chunk IDs

### Ollama

Used to run the local LLM.

Current model:

```text
qwen2.5:7b
```

### Streamlit

Used to create the current web-based user interface.

---

## 4. Project Structure

Current project structure:

```text
RAg/
│
├── chroma_db/
│
├── data_rag/
│   ├── 1901.08204v1.pdf
│   ├── 1902.06197v1.pdf
│   └── 2102.10777v1.pdf
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── chunker.py
│   ├── database.py
│   ├── embeddings.py
│   ├── ingestion.py
│   ├── pdf_loader.py
│   └── rag.py
│
├── test/
│   └── test_rag.py
│
├── readme.md
│
└── requirements.text
```

---

# 5. Step-by-Step Implementation

## Step 1 — PDF Text Extraction

File:

```text
src/pdf_loader.py
```

PyMuPDF is used to open the PDF and extract text page by page.

Each extracted page is stored with:

```text
page number
text
```

Example:

```python
{
    "page": 1,
    "text": "..."
}
```

This allows the application to remember which page the information came from.

---

## Step 2 — Text Chunking

File:

```text
src/chunker.py
```

Large PDF pages are divided into smaller chunks.

Current configuration:

```text
Chunk size: 1000 characters
Overlap: 200 characters
```

The overlap helps preserve information that may be split between two chunks.

Each chunk contains:

```text
text
page
chunk_id
```

---

## Step 3 — Embeddings

File:

```text
src/embeddings.py
```

The application uses:

```text
all-MiniLM-L6-v2
```

to convert text into numerical vectors.

Example:

```text
Text
 ↓
Embedding Model
 ↓
384-dimensional vector
```

Embeddings allow the system to compare the meaning of the user's question with the meaning of stored PDF chunks.

---

## Step 4 — ChromaDB

File:

```text
src/database.py
```

ChromaDB is used as the vector database.

The persistent database is stored in:

```text
./chroma_db
```

The collection is:

```text
pdf_documents
```

Each stored document contains:

```text
PDF text
Embedding
Source PDF
Page number
Chunk ID
```

Document IDs include the PDF source so that chunks from different PDFs do not collide.

Example:

```text
1902.06197v1.pdf_page_1_chunk_0
```

---

## Step 5 — PDF Ingestion

File:

```text
src/ingestion.py
```

The ingestion pipeline performs:

```text
PDF
 ↓
Extract pages
 ↓
Create chunks
 ↓
Generate embeddings
 ↓
Store in ChromaDB
```

All PDFs inside:

```text
data_rag/
```

are processed.

The current dataset contains three PDF research papers.

The latest successful ingestion produced:

```text
1901.08204v1.pdf → 52 chunks
1902.06197v1.pdf → 32 chunks
2102.10777v1.pdf → 28 chunks

Total → 112 chunks
```

---

# 6. Retrieval

Retrieval is implemented in:

```text
src/rag.py
```

When the user asks a question:

```text
Question
   ↓
Question embedding
   ↓
ChromaDB similarity search
   ↓
Top 8 relevant chunks
```

The current retrieval value is:

```python
top_k=8
```

The retrieved chunks are then passed to the LLM.

---

# 7. LLM Answer Generation

The current local LLM is:

```text
Qwen 2.5 7B
```

It is running through:

```text
Ollama
```

Ollama API:

```text
http://localhost:11434/api/generate
```

The RAG prompt instructs the model to:

* Use only the retrieved PDF context
* Avoid outside knowledge
* Avoid inventing information
* Understand equivalent terminology when supported by the context
* Clearly explain the answer
* State when the answer cannot be found in the provided PDFs

The fallback response is:

```text
I could not find the answer in the provided PDF documents.
```

This is important because the application should remain grounded in the PDF knowledge base.

---

# 8. Source Information

The application also returns the sources used for an answer.

For example:

```text
1901.08204v1.pdf | Page 4 | Chunk 0
```

This makes it possible to identify where the answer came from.

The source information contains:

```text
Source PDF
Page
Chunk ID
```

---

# 9. RAG Testing

A test file was created:

```text
test/test_rag.py
```

The application was tested with 20 questions covering concepts such as:

* DeepPCB dataset
* PCB defects
* Binaryzation
* SURF
* Image registration
* Template matching
* Golden/reference PCB
* Reference-based inspection
* Non-reference-based inspection
* Image subtraction
* Adaptive thresholding
* Thresholding
* Feature extraction
* CNN
* Deep learning
* YOLO
* Component detection
* Component classification

The questions were tested one by one to verify the quality of the RAG system.

The model is currently performing well enough to proceed with the application UI.

---

# 10. User Interface

The UI is implemented using:

```text
Streamlit
```

File:

```text
src/app.py
```

The current UI allows the user to:

1. Enter a question
2. Submit the question
3. Retrieve relevant PDF information
4. Generate an answer
5. Display the answer
6. Display the PDF sources

Current UI flow:

```text
User enters question
        ↓
       Ask
        ↓
   RAG pipeline
        ↓
    Answer
        ↓
     Sources
```

---

# 11. Installation

Install the required Python packages.

For the UI:

```powershell
pip install streamlit
```

Other required packages include the libraries used by the RAG pipeline, such as:

```text
PyMuPDF
sentence-transformers
chromadb
requests
```

Ollama must also be installed separately.

---

# 12. Ollama Setup

Check Ollama:

```powershell
ollama --version
```

Current version tested:

```text
0.35.1
```

Install the Qwen model:

```powershell
ollama pull qwen2.5:7b
```

Check installed models:

```powershell
ollama list
```

The expected model is:

```text
qwen2.5:7b
```

Ollama should be running before starting the RAG application.

---

# 13. Run PDF Ingestion

From the project root:

```powershell
python src/ingestion.py
```

This processes the PDFs in:

```text
data_rag/
```

and stores the resulting embeddings in:

```text
chroma_db/
```

---

# 14. Test the RAG

Run:

```powershell
python test/test_rag.py
```

This runs the predefined questions one by one.

---

# 15. Run the User Interface

From the project root:

```powershell
streamlit run src/app.py
```

Streamlit will start the web application and provide a local browser address.

---

# 16. Current Status

The following parts are completed:

```text
PDF extraction              ✅
Text chunking               ✅
Embedding generation        ✅
ChromaDB storage            ✅
PDF ingestion               ✅
Semantic retrieval           ✅
Top-8 retrieval              ✅
Ollama setup                 ✅
Qwen 2.5 7B                  ✅
RAG answer generation        ✅
Source information           ✅
20-question testing          ✅
Basic Streamlit UI           ✅
```

---

# 17. Important Design Decision

The current system intentionally keeps the RAG implementation simple.

The main RAG logic is:

```text
Question
   ↓
Embedding
   ↓
ChromaDB
   ↓
Top 8 chunks
   ↓
Qwen
   ↓
Answer
```

No unnecessary reranking or question-specific retrieval rules have been added.

This keeps the code easier to understand, maintain, test, and upgrade.

---

# 18. Future Improvements

The current basic RAG system is the foundation.

Possible future improvements include:

### UI improvements

* PDF upload
* PDF ingestion from the UI
* Chat interface
* Conversation history
* Clear conversation button
* Better source display
* Page-level source navigation

### RAG improvements

* Better chunking strategies
* Improved retrieval
* Metadata filtering
* Hybrid search
* Reranking if required
* Better evaluation methodology

### LLM upgrade

The current local model is:

```text
Qwen 2.5 7B
```

Later, the LLM layer can be replaced with a high-end API model such as:

```text
OpenAI GPT
```

or

```text
Anthropic Claude
```

The important point is that the existing:

```text
PDF → Chunking → Embeddings → ChromaDB → Retrieval
```

pipeline can remain largely unchanged.

Only the answer-generation layer needs to be replaced.

---

# 19. Final Architecture

Current architecture:

```text
                     ┌─────────────────┐
                     │   PDF Papers    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ PDF Extraction  │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    Chunking     │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   Embeddings    │
                     │ MiniLM-L6-v2    │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    ChromaDB     │
                     └────────┬────────┘
                              │
                              │
                        User Question
                              │
                              ▼
                     ┌─────────────────┐
                     │ Question        │
                     │ Embedding       │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Top-8 Retrieval │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │  Qwen 2.5 7B   │
                     │    Ollama       │
                     └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Answer + Source │
                     └─────────────────┘
```

---

## 20. Current Project Objective

The current objective is to complete and validate the basic RAG application first.

After the basic RAG is stable, the application can be improved with a more complete UI and eventually a higher-performance cloud LLM while preserving the core RAG architecture.
