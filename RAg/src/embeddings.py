from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts):

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()
if __name__ == "__main__":

    test_texts = [
        "PCB defect detection using deep learning",
        "YOLO is an object detection model",
        "The DeepPCB dataset contains PCB defect images"
    ]

    embeddings = generate_embeddings(test_texts)

    print("Number of texts:", len(embeddings))

    print("Embedding dimension:", len(embeddings[0]))

    print("\nFirst embedding:")
    print(embeddings[0][:10])