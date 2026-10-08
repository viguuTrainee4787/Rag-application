import json
import base64
import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5vl:7b"

METADATA_FILE = "extracted_images/image_metadata.json"
OUTPUT_FILE = "extracted_images/image_descriptions.json"


def analyze_image(image_path):
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    prompt = """
Analyze this image carefully.

Describe:
1. What the image contains.
2. Whether it is a PCB-related figure, diagram, chart, table, or other image.
3. Any important text visible in the image.
4. Any important technical information shown in the image.

Give a concise but useful technical description that can later be used by a RAG system.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"]


if __name__ == "__main__":

    # Load metadata
    with open(METADATA_FILE, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    # Load previous results if they exist
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            results = json.load(file)
    else:
        results = []

    # Create a set of already processed images
    processed_images = {
        item["image_path"]
        for item in results
    }

    total_images = len(metadata)

    print(f"Total images: {total_images}")
    print(f"Already processed: {len(processed_images)}")
    print(f"Remaining: {total_images - len(processed_images)}")

    # Process images one by one
    for index, image_info in enumerate(metadata, start=1):

        image_path = image_info["image_path"]

        # Skip already processed images
        if image_path in processed_images:
            print(
                f"\n[{index}/{total_images}] SKIPPING - Already processed:"
            )
            print(image_path)
            continue

        print("\n========================================")
        print(f"Processing image {index}/{total_images}")
        print("========================================")
        print(image_path)

        try:
            description = analyze_image(image_path)

            result = {
                "source": image_info["source"],
                "page": image_info["page"],
                "image_number": image_info["image_number"],
                "image_path": image_path,
                "description": description
            }

            results.append(result)

            # Save immediately after every image
            with open(
                OUTPUT_FILE,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    results,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print("\nDescription generated successfully.")
            print(f"Saved progress: {len(results)}/{total_images}")

        except Exception as error:

            print("\nERROR processing image:")
            print(image_path)
            print(error)

            print("\nContinuing with the next image...")
            continue

    print("\n========================================")
    print("IMAGE PROCESSING COMPLETE")
    print("========================================")
    print(f"Total images: {total_images}")
    print(f"Successfully processed: {len(results)}")
    print(f"Output file: {OUTPUT_FILE}")