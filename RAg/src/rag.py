import requests

from database import collection
from embeddings import generate_embeddings


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:7b"

def expand_query(query):
    query_lower = query.lower()

    expansions = []

    if "golden pcb" in query_lower:
        expansions.extend([
            "reference PCB",
            "template PCB",
            "defect-free PCB",
            "standard image",
            "reference board"
        ])

    if "reference pcb" in query_lower:
        expansions.extend([
            "template PCB",
            "golden PCB",
            "defect-free PCB",
            "standard image"
        ])

    if "image registration" in query_lower:
        expansions.extend([
            "image alignment",
            "PCB alignment",
            "template alignment",
            "registration of test image with template"
        ])

    if "registration" in query_lower:
        expansions.extend([
            "alignment",
            "image alignment",
            "template alignment"
        ])

    if expansions:
        return query + " " + " ".join(expansions)

    return query
def retrieve_documents(query, top_k=8):
    expanded_query = expand_query(query)

    query_embedding = generate_embeddings([expanded_query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results



def generate_answer(question, context):

    prompt = f"""
You are a helpful assistant answering questions about PCB research papers.

Your task is to answer the user's question using ONLY the information
contained in the provided context.

Rules:
1. Answer using only the provided context.
2. Do not use outside knowledge.
3. Do not invent facts that are not supported by the context.
4. Match the meaning of the question to the information in the context,
   even when the exact words are different.
5. Treat synonyms and equivalent terminology as the same concept when
   the context clearly supports that meaning.
6. For example, if the question asks about "golden PCB", and the context
   describes a "reference PCB", "template PCB", "standard image", or
   "defect-free template", explain the concept using the terminology
   found in the context.
7. If the context contains enough information to explain the concept,
   answer the question clearly using that information.
8. Only say:
"I could not find the answer in the provided PDF documents."
when the context genuinely does not contain enough information to answer.
Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]




def ask_question(question):
    results = retrieve_documents(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    print("\n" + "=" * 80)
    print("RETRIEVED CHUNKS")
    print("=" * 80)

    for i, (document, metadata) in enumerate(zip(documents, metadatas)):
        print(f"\n--- CHUNK {i + 1} ---")
        print(
            f"Source: {metadata['source']} | "
            f"Page: {metadata['page']} | "
            f"Chunk: {metadata['chunk_id']}"
        )
        print(document)

    context = "\n\n".join(documents)

    answer = generate_answer(question, context)

    return answer, metadatas

if __name__ == "__main__":

    questions = [
        "What is image registration in PCB inspection?",
     "Why is image registration important for PCB defect detection?",
    "What is template matching in PCB inspection?",
    "What is a golden PCB or reference PCB?",
    "What is the difference between a reference-based and non-reference-based inspection method?",
    "What is the purpose of image subtraction in PCB inspection?",
     "What is adaptive thresholding?",
    "How does thresholding help in PCB defect detection?",
     "What is the role of feature extraction in PCB inspection?",
    "What is the role of CNN in PCB defect detection?",
     "How is deep learning used for PCB defect detection?",
     "What is YOLO and how is it used for PCB inspection?",
    "What are the advantages of using YOLO for PCB defect detection?",
     "What is component detection in PCB inspection?",
     "How are PCB components classified in the inspection process?"
    ]

    for question in questions:

        answer, sources = ask_question(question)

        print("\n" + "=" * 70)
        print("QUESTION:")
        print(question)

        print("\nANSWER:")
        print(answer)

        print("\nSOURCES:")

        for source in sources:

            print(
                f"- {source['source']} | "
                f"Page {source['page']} | "
                f"Chunk {source['chunk_id']}"
            )

        print("=" * 70)