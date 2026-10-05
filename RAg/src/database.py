import chromadb


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="pdf_documents"
)


def add_documents(documents, embeddings):

    ids = []
    texts = []
    metadatas = []

    for document in documents:

        ids.append(
            f"{document['source']}_page_{document['page']}_chunk_{document['chunk_id']}"
        )

        texts.append(document["text"])

        metadatas.append({
            "source": document["source"],
            "page": document["page"],
            "chunk_id": document["chunk_id"]
        })

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )


if __name__ == "__main__":

    print("ChromaDB initialized successfully.")

    print("Collection name:", collection.name)

    print("Number of documents:", collection.count())