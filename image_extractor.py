import os
import fitz


PDF_DIRECTORY = "data_rag"
OUTPUT_DIRECTORY = "extracted_images"


def extract_images_from_pdf(pdf_path):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    output_folder = os.path.join(
        OUTPUT_DIRECTORY,
        pdf_name
    )

    os.makedirs(output_folder, exist_ok=True)

    document = fitz.open(pdf_path)

    total_images = 0

    for page_number, page in enumerate(document, start=1):

        images = page.get_images(full=True)

        for image_number, image_info in enumerate(images, start=1):

            xref = image_info[0]

            image_data = document.extract_image(xref)

            image_bytes = image_data["image"]
            image_extension = image_data["ext"]

            image_filename = (
                f"page_{page_number}_"
                f"img_{image_number}."
                f"{image_extension}"
            )

            image_path = os.path.join(
                output_folder,
                image_filename
            )

            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)

            total_images += 1

            print(
                f"Extracted: "
                f"{pdf_name} | "
                f"Page {page_number} | "
                f"Image {image_number}"
            )

    document.close()

    print(
        f"\nTotal images extracted from "
        f"{pdf_name}: {total_images}"
    )


def extract_all_images():

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True
    )

    for filename in os.listdir(PDF_DIRECTORY):

        if filename.lower().endswith(".pdf"):

            pdf_path = os.path.join(
                PDF_DIRECTORY,
                filename
            )

            print("\n==============================")
            print(f"Processing: {filename}")
            print("==============================")

            extract_images_from_pdf(pdf_path)


if __name__ == "__main__":
    extract_all_images()