import os

from pdf_loader import extract_text_from_pdf
from chunker import create_chunks
from embeddings import generate_embeddings
from database import add_documents


PDF_DIRECTORY = "data_rag"


def ingest_pdf(pdf_path):

    print(f"\nProcessing: {pdf_path}")

    # 1. Extract PDF
    pages = extract_text_from_pdf(pdf_path)

    print(f"Pages extracted: {len(pages)}")

    # 2. Create chunks
    documents = create_chunks(pages)
    for document in documents:
        document["source"] = os.path.basename(pdf_path)
    print(f"Chunks created: {len(documents)}")

    # 3. Generate embeddings
    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = generate_embeddings(texts)

    print("Embeddings generated")

    # 4. Store in vector database
    add_documents(
        documents,
        embeddings
    )

    print("Stored in ChromaDB")


def ingest_all_pdfs():

    for filename in os.listdir(PDF_DIRECTORY):

        if filename.lower().endswith(".pdf"):

            pdf_path = os.path.join(
                PDF_DIRECTORY,
                filename
            )

            ingest_pdf(pdf_path)


if __name__ == "__main__":

    ingest_all_pdfs()