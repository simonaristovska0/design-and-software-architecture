import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date
import os
from concurrent.futures import ThreadPoolExecutor
import random

# First filter
# Returning only issuer codes, excluding issuers
def FILTER_1_fetch_issuer_codes():
    url = "https://www.mse.mk/mk/stats/symbolhistory/kmb"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    issuer_codes = []
    for option in soup.select('select#Code option'):
        code = option.get('value')
        contains_digit = any(char.isdigit() for char in code)
        if not contains_digit:
            issuer_codes.append(code)
    return issuer_codes

# Third filter
# The third filter is accepting two arguments:
# If it is called only with the issuer_code, it is filling the database(writing in the csv file)
# with data from the past 10 years till now.
# In the other case, when we have the data till a certain date(different from today) in the csv file,
# we are only filling the data with the most recent information till today.
def FILTER_3_scrape_to_csv(issuer_code, od_date=date.today() - datetime.timedelta(days=365 * 10)):
    attribute_names = ['Датум', 'Цена на последна трансакција', 'Мак.', 'Мин.', 'Просечна цена', '%пром.', 'Количина',
                       'Промет во БЕСТ во денари', 'Вкупен промет во денари']
    data_folder_path = './Data/'
    if not os.path.exists(data_folder_path):
        os.makedirs(data_folder_path)

    output_csv_file = os.path.join(data_folder_path, f'data_for_{issuer_code}.csv')

    do_date = date.today()
    current_end = do_date
    full_data = []

    while current_end > od_date:
        current_start = max(current_end - datetime.timedelta(days=365), od_date)
        url = f'https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}?FromDate={current_start}&ToDate={current_end}'
        try:
            # response = requests.get(url, timeout=10)
            response = requests.get(url)
            response.raise_for_status()
            raw_html = response.text
            list_data = scrape_data(raw_html)
            if list_data:
                full_data.extend(list_data)
        except Exception as e:
            print(f'Fail za {url}')
            FILTER_3_scrape_to_csv(issuer_code,od_date)
            return

        current_end = current_start - datetime.timedelta(days=1)

    new_data_df = pd.DataFrame(full_data, columns=attribute_names)
    if not os.path.exists(output_csv_file):
        new_data_df.to_csv(output_csv_file, mode='w', index=False)
    else:
        existing_data = pd.read_csv(output_csv_file)
        if not new_data_df.empty:
            updated_data = pd.concat([new_data_df, existing_data], ignore_index=True).drop_duplicates()
            updated_data.to_csv(output_csv_file, index=False)


# Helper function
# Scraping data using Beautiful Soup
def scrape_data(raw_html):
    list = []
    soup = BeautifulSoup(raw_html, 'html.parser')
    rows = soup.select("tbody tr")
    table_data = []
    for row in rows:
        row_data = [td.text.strip() for td in row.select("td")]
        table_data.append(row_data)

    for row in table_data:
        list.append(row)
    return list


# Helper function
# If a csv file does not exist it returns False, elsewhere it returns the most recent date written in the csv file.
def return_the_last_date_if_it_exists(issuer_code):
    csv_path = f'./Data/data_for_{issuer_code}.csv'
    if not os.path.exists(csv_path):
        return False
    df = pd.read_csv(csv_path, parse_dates=['Датум'], dayfirst=True)
    last_date = df['Датум'][0].date()
    return last_date


# Second filter
# If the data is empty it is calling the third filter to fill all the data(from past then years, till today)
# , if not it is calling the third filter but with the last date in the excisting data(till today)
def FILTER_2_process_issuer(issuer_code):
    datum = return_the_last_date_if_it_exists(issuer_code)

    if datum is False:
        FILTER_3_scrape_to_csv(issuer_code)
    else:
        if datum != date.today():
            datum = datum + datetime.timedelta(days=1)
            FILTER_3_scrape_to_csv(issuer_code, datum)


if __name__ == '__main__':
    # Implemented a timer here
    start_time = time.time()

    issuer_codes = FILTER_1_fetch_issuer_codes()
    with ThreadPoolExecutor() as executor:
        executor.map(FILTER_2_process_issuer, issuer_codes)

    end_time = time.time()
    runtime = end_time - start_time
    print(f"Total runtime: {runtime:.2f} seconds")
