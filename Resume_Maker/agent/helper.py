from pypdf import PdfReader
import pdfplumber


def read_pdf_file(file_path):
    """
    Reads text content from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content from the PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Add newline between pages
        return text
    except Exception as e:
        return f"Error reading PDF file: {e}"

def extract_hyperlinks_from_pdf(file_path):
    """
    Extracts hyperlinks from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list: A list of extracted hyperlinks.
    """
    hyperlinks = set()
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.annots:
                    for annot in page.annots:
                        if annot.get("uri"):
                            hyperlinks.add(annot["uri"])

        ## add https://www. at start if not present and add it only to linkedin and github links and not to email kind of links
        hyperlinks = [link if (link.startswith("http") or "gmail" in link) else "https://www." + link for link in hyperlinks]   
        return hyperlinks
    except Exception as e:
        return f"Error extracting hyperlinks: {e}"
    

if __name__ == "__main__":
    sample_pdf_path = r"C:\Users\Sujith\Downloads\Enhancv_project\Rohith.pdf"  # Replace with your PDF file path
    extracted_text = read_pdf_file(sample_pdf_path)
    print("Extracted Text:")
    print(extracted_text)
    extracted_links = extract_hyperlinks_from_pdf(sample_pdf_path)
    print("Extracted Hyperlinks:") 
    print(extracted_links)
