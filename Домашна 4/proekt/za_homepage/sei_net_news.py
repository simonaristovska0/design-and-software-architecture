import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.mse.mk/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, "html.parser")

news_section = soup.find("div", class_="seiNetNews")
news_items = news_section.find_all("li", class_="flex-item-3x4") if news_section else []

news_data = []
for news_item in news_items:
    try:
        news_text_tag = news_item.find("h4")
        full_text = news_text_tag.text.strip() if news_text_tag else None

        if full_text:
            news_data.append(full_text)
    except Exception as e:
        print(f"Error processing news item: {e}")
        continue

output_file = "sei_net_news_only.csv"
with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["News"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in news_data:
        writer.writerow({"News": item})

print(f"SEI-Net news data saved to {output_file}")