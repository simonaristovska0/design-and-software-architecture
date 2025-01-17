import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page
url = "https://www.mse.mk/"

# Send a GET request to the website
response = requests.get(url)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Locate the table by class or ID
    table = soup.find("table", class_="table table-bordered table-condensed table-striped")

    # Extract table headers
    headers = [th.text.strip() for th in table.find_all("th")]

    # Extract table rows
    rows = []
    for row in table.find_all("tr")[1:]:  # Skip the header row
        cols = [td.text.strip() for td in row.find_all("td")]
        rows.append(cols)

    # Convert to a DataFrame for better manipulation
    df = pd.DataFrame(rows, columns=headers)

    # Save to CSV
    df.to_csv("mse_table.csv", index=False, encoding="utf-8-sig")

    # Print the DataFrame
    print(df)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
