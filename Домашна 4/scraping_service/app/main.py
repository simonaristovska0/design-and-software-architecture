from fastapi import FastAPI, HTTPException
from app.utils import scrape_to_csv
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.post("/process-issuer")
def process_issuer(issuer_code: str):
    """Process issuer data and save it to a CSV."""
    try:
        scrape_to_csv(issuer_code)
        return {"status": "success", "issuer_code": issuer_code}
    except Exception as e:
        print(f"Error processing issuer: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing issuer: {e}")


@app.get("/issuer-codes")
def fetch_issuer_codes():
    """Fetch issuer codes from the Macedonian Stock Exchange."""
    url = "https://www.mse.mk/mk/stats/symbolhistory/kmb"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        issuer_codes = []
        for option in soup.select('select#Code option'):
            code = option.get('value')
            contains_digit = any(char.isdigit() for char in code)
            if not contains_digit:
                issuer_codes.append(code)
        return {"issuer_codes": issuer_codes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching issuer codes: {e}")
