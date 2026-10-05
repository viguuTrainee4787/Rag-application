def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_chunks(pages):

    documents = []

    for page in pages:

        chunks = chunk_text(page["text"])

        for chunk_id, chunk in enumerate(chunks):

            documents.append({
                "text": chunk,
                "page": page["page"],
                "chunk_id": chunk_id
            })

    return documents
from pdf_loader import extract_text_from_pdf


if __name__ == "__main__":

    pdf_path = "data_rag/1902.06197v1.pdf"

    pages = extract_text_from_pdf(pdf_path)

    documents = create_chunks(pages)

    print("Number of pages:", len(pages))

    print("Number of chunks:", len(documents))

    for document in documents[:5]:

        print("\n==============================")
        print("PAGE:", document["page"])
        print("CHUNK:", document["chunk_id"])
        print("==============================")

        print(document["text"][:500])