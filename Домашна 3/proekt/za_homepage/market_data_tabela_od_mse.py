import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage containing the table
url = "https://www.mse.mk/"  # Replace this with the correct URL of the page

# Send a GET request to fetch the HTML content
response = requests.get(url)
response.raise_for_status()  # Raise an exception if the request fails

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Locate the table by its class
table = soup.find("table", class_="table table-bordered table-condensed table-striped market-summary")
if not table:
    print("Table not found on the page.")
    exit()

# Extract table rows
rows = table.find("tbody").find_all("tr")

# Extract data from the rows
table_data = []
for row in rows:
    columns = row.find_all("td")
    if len(columns) == 2:  # Ensure the row has two columns
        key = columns[0].text.strip()  # First column: header (e.g., "Датум")
        value = columns[1].text.strip()  # Second column: data (e.g., "27.12.2024")
        table_data.append({"Field": key, "Value": value})

# Save the extracted data to a CSV file
output_file = "market_summary.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Field", "Value"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in table_data:
        writer.writerow(data)

print(f"Market summary table data saved to {output_file}")