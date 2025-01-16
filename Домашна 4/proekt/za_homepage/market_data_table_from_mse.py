import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.mse.mk/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", class_="table table-bordered table-condensed table-striped market-summary")
if not table:
    print("Table not found on the page.")
    exit()

rows = table.find("tbody").find_all("tr")

table_data = []
for row in rows:
    columns = row.find_all("td")
    if len(columns) == 2:
        key = columns[0].text.strip()  # (e.g., "Датум")
        value = columns[1].text.strip()  # (e.g., "27.12.2024")
        table_data.append({"Field": key, "Value": value})

output_file = "market_summary.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Field", "Value"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in table_data:
        writer.writerow(data)

print(f"Market summary table data saved to {output_file}")
