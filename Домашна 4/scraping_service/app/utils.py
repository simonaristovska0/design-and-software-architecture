from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta
import os


def scrape_data(raw_html):
    """Helper function to scrape data from HTML using BeautifulSoup."""
    list_data = []
    soup = BeautifulSoup(raw_html, 'html.parser')
    rows = soup.select("tbody tr")
    for row in rows:
        row_data = [td.text.strip() for td in row.select("td")]
        list_data.append(row_data)
    return list_data


def scrape_to_csv(issuer_code, start_date=date.today() - timedelta(days=365 * 10)):
    """Scrapes historical data for the given issuer and saves it to a CSV file."""
    print(f"Starting scrape for {issuer_code} from {start_date} to {date.today()}")
    attribute_names = ['Датум', 'Цена на последна трансакција', 'Мак.', 'Мин.', 'Просечна цена', '%пром.', 'Количина',
                       'Промет во БЕСТ во денари', 'Вкупен промет во денари']

    DATA_FOLDER = "./data/"
    csv_path = os.path.join(DATA_FOLDER, f"data_for_{issuer_code}.csv")
    end_date = date.today()
    full_data = []

    while end_date > start_date:
        current_start = max(end_date - timedelta(days=365), start_date)
        url = f"https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}?FromDate={current_start}&ToDate={end_date}"
        print(f"Fetching data from {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            raw_html = response.text
            list_data = scrape_data(raw_html)
            if list_data:
                print(f"Scraped {len(list_data)} rows")
                full_data.extend(list_data)
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            break

        end_date = current_start - timedelta(days=1)

    if full_data:
        print(f"Saving {len(full_data)} rows to CSV for {issuer_code}")
        new_data_df = pd.DataFrame(full_data, columns=attribute_names)
        new_data_df.to_csv(csv_path, mode='w', index=False)
    else:
        print(f"No data scraped for {issuer_code}")
