import os
import pytesseract
from PIL import Image
from datetime import datetime
import uuid
from pdf2image import convert_from_path
import fitz  # PyMuPDF

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    try:
        # First, try extracting text directly with PyMuPDF
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            text = page.get_text()
            full_text += text
        
        if full_text.strip():
            # Text extracted successfully
            return full_text
        else:
            # If no text found, fallback to OCR on each page as image
            print(f"No direct text found in {pdf_path}, falling back to OCR on images.")
            text = ""
            images = convert_from_path(pdf_path)
            for i, image in enumerate(images):
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
            return text
    except Exception as e:
        print(f"Error processing PDF {pdf_path}: {e}")
        return None

def process_documents_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        ext = filename.lower().split('.')[-1]
        text = None
        if ext in ["png", "jpg", "jpeg"]:
            text = extract_text_from_image(full_path)
        elif ext == "pdf":
            text = extract_text_from_pdf(full_path)
        else:
            # Skip unsupported file types for now
            continue

        if text:
            doc = {
                "document_id": str(uuid.uuid4()),
                "filename": filename,
                "timestamp": datetime.utcnow().isoformat(),
                "text": text
            }
            documents.append(doc)
    return documents

if __name__ == "__main__":
    folder = "./data"
    docs = process_documents_folder(folder)
    for d in docs:
        print(f"ID: {d['document_id']} | File: {d['filename']}\nText:\n{d['text'][:200]}...\n")
