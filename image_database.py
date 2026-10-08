import os
import json

IMAGE_DIRECTORY = "extracted_images"
OUTPUT_FILE = "extracted_images/image_metadata.json"


def create_image_metadata():

    metadata = []

    for pdf_name in os.listdir(IMAGE_DIRECTORY):

        pdf_folder = os.path.join(
            IMAGE_DIRECTORY,
            pdf_name
        )

        if not os.path.isdir(pdf_folder):
            continue

        for filename in os.listdir(pdf_folder):

            if not filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp")
            ):
                continue

            parts = filename.split("_")

            page_number = int(parts[1])
            image_number = int(
                os.path.splitext(parts[3])[0]
            )

            image_path = os.path.join(
                pdf_folder,
                filename
            )

            metadata.append({
                "source": pdf_name + ".pdf",
                "page": page_number,
                "image_number": image_number,
                "image_path": image_path
            })

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    print("Image metadata created successfully.")
    print("Total images:", len(metadata))
    print("Metadata file:", OUTPUT_FILE)


if __name__ == "__main__":
    create_image_metadata()