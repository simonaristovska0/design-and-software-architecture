import requests

BASE_URL = "http://127.0.0.1:8000"


def fetch_all_issuer_codes():
    """Fetch all issuer codes using the microservice."""
    url = f"{BASE_URL}/issuer-codes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("issuer_codes", [])
    except Exception as e:
        print(f"Error fetching issuer codes: {e}")
        return []


def process_all_issuers(issuer_codes):
    """Process each issuer by calling the process-issuer endpoint."""
    for issuer_code in issuer_codes:
        print(f"Processing issuer: {issuer_code}")
        try:
            # Pass issuer_code as a query parameter
            response = requests.post(
                f"{BASE_URL}/process-issuer?issuer_code={issuer_code}"
            )
            if response.status_code == 200:
                print(f"Successfully processed: {issuer_code}")
            else:
                print(f"Failed to process {issuer_code}: {response.json()}")
        except Exception as e:
            print(f"Error processing issuer {issuer_code}: {e}")


if __name__ == "__main__":
    # Fetch all issuer codes
    issuer_codes = fetch_all_issuer_codes()

    if not issuer_codes:
        print("No issuer codes found!")
    else:
        print(f"Found {len(issuer_codes)} issuers: {issuer_codes}")
        # Process each issuer
        process_all_issuers(issuer_codes)
