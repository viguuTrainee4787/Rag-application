import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extract text from every page of a PDF.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        if text.strip():

            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages


if __name__ == "__main__":

    pdf_path = "data_rag/1902.06197v1.pdf"

    pages = extract_text_from_pdf(pdf_path)

    print("Number of pages:", len(pages))

    for page in pages[:2]:

        print("\n==============================")
        print("PAGE:", page["page"])
        print("==============================")

        print(page["text"][:1000])