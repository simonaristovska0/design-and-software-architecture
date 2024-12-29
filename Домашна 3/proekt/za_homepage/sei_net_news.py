import requests
from bs4 import BeautifulSoup
import csv

# URL of the page to scrape
url = "https://www.mse.mk/"  # Replace with the correct URL

# Send a GET request to fetch the webpage content
response = requests.get(url)
response.raise_for_status()

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the container for SEI-Net news
news_section = soup.find("div", class_="seiNetNews")
news_items = news_section.find_all("li", class_="flex-item-3x4") if news_section else []

# Extract the required details for each news item
news_data = []
for news_item in news_items:
    try:
        # Extract the full text of the news item
        news_text_tag = news_item.find("h4")
        full_text = news_text_tag.text.strip() if news_text_tag else None

        if full_text:  # Only add if there's actual text
            news_data.append(full_text)
    except Exception as e:
        print(f"Error processing news item: {e}")
        continue  # Skip this item and move to the next one

# Save the extracted news to a CSV file
output_file = "sei_net_news_only.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["News"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in news_data:
        writer.writerow({"News": item})

print(f"SEI-Net news data saved to {output_file}")