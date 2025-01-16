from fastapi import FastAPI, HTTPException
from app.utils import extract_pdf_text, get_issuer_codes

app = FastAPI()

@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to the Fundamental Analysis Service!"}


@app.get("/issuer-codes")
def fetch_issuer_codes():
    """Fetch issuer codes from the Macedonian Stock Exchange."""
    try:
        issuer_codes = get_issuer_codes()
        if not issuer_codes:
            raise HTTPException(status_code=404, detail="No issuer codes found.")
        return {"issuer_codes": issuer_codes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching issuer codes: {e}")


@app.post("/extract-text/")
def extract_text_from_pdf(file_path: str):
    """Extract text from a PDF file."""
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found.")
        extracted_text = extract_pdf_text(file_path)
        if not extracted_text:
            raise HTTPException(status_code=500, detail="Failed to extract text from PDF.")
        return {"file_path": file_path, "extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {e}")