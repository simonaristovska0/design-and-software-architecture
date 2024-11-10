import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, Float, MetaData, select
import time
from datetime import date
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor


import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")

# FIRST FILTER
# DONE
def fetch_issuer_codes():
    url = "https://www.mse.mk/mk/stats/symbolhistory/REPL"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    issuer_codes = []
    for option in soup.select('select#Code option'):
        code = option.get('value')
        contains_digit = any(char.isdigit() for char in code)
        if not contains_digit:
            issuer_codes.append(code)
    return issuer_codes





def za_siminjanje_csv_kmb(issuer_code, od_date=date.today() - datetime.timedelta(days=365 * 10)):
    download_path_for_csv_files = f'/Users/matejmitev/Desktop/diansProekt/{issuer_code}'
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_path_for_csv_files,  # Set the download path
        "download.prompt_for_download": False,  # Do not prompt for download
        "download.directory_upgrade": True,  # Automatically overwrite the download directory
        "safebrowsing.enabled": True  # Enable safe browsing
    }
    chrome_options.add_experimental_option("prefs", prefs)

    do_date = date.today()
    current_start = od_date

    # driver = webdriver.Chrome()
    driver = webdriver.Chrome(options=chrome_options)

    while current_start < do_date:
        current_end = min(current_start + datetime.timedelta(days=365), do_date)
        driver.get(
            f'https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}?FromDate={current_start}&ToDate={current_end}')
        print(f'https://www.mse.mk/mk/stats/symbolhistory/{issuer_code}?FromDate={current_start}&ToDate={current_end}')
        # print(driver.current_url)
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'btnExport'))
        )
        download_button.click()
        time.sleep(0.5)  # mora za da se dosiminjaat site, ova e najminimalno sho mozhe
        current_start = current_end + datetime.timedelta(days=1)
    driver.quit()


def od_excel_vo_csv_site_zaedno(issuer_code):
    old_file_path = f'/Users/matejmitev/Desktop/diansProekt/{issuer_code}/Историски податоци.xls'
    new_file_path = f'/Users/matejmitev/Desktop/diansProekt/{issuer_code}/Историски податоци (0).xls'
    os.rename(old_file_path, new_file_path)

    download_path_for_csv_files = f'/Users/matejmitev/Desktop/diansProekt/{issuer_code}'
    output_csv_file = os.path.join(download_path_for_csv_files, f'combined_{issuer_code}_data.csv')
    open(output_csv_file, 'w').close()

    for filename in sorted(os.listdir(download_path_for_csv_files), reverse=True):
        if filename.endswith('.xls'):
            file_path = os.path.join(download_path_for_csv_files, filename)
            # Read the Excel file
            df = pd.read_html(file_path)
            df = df[0]
            array = ["Цена на последна трансакција", "Мак.", "Мин.", "Просечна цена", "Промет во БЕСТ во денари",
                     "Вкупен промет во денари"]
            df["Количина"] = df["Количина"].astype(str)
            for i in range(0, len(df)):
                ############ kolicina
                num = df.loc[i, "Количина"]
                index = num.find(".")
                vrednost = num[index + 1:]
                if vrednost == '0':
                    num = num.replace(".0", "")
                else:
                    num = num.replace(".", ",")
                df.loc[i, "Количина"] = str(num)
                ##########
                df.loc[i, "%пром."] = float(df.loc[i, "%пром."]) / 100
                for el in array:
                    if not isinstance(df.loc[i, el], str):
                        df.loc[i, el] = str(df.loc[i, el]).replace(",", "g").replace(
                            ".", ",").replace("g", ".")
                    else:
                        df.loc[i, el] = df.loc[i, el].replace(",", "g").replace(
                            ".", ",").replace("g", ".")

            # Append the data to the CSV file
            df.to_csv(output_csv_file, mode='a', header=not os.path.exists(output_csv_file) or filename ==
                                                        sorted(os.listdir(download_path_for_csv_files))[-1],
                      index=False)

#brisam adin, alk, alkb, ameh
# aptk,atpp 22.10 go ima
def zemi_posleden_datum_ili_kazi_dali_ne_postoi(issuer_code,csv_path):
    directory_path = f'./{issuer_code}/'
    if not os.path.exists(directory_path):
        return False
    df = pd.read_csv(csv_path, parse_dates=['Датум'], dayfirst=True)
    last_date = df['Датум'][0].date()
    files = os.listdir(directory_path)
    for file in files:
        if file.endswith('.xls'):
            file_path = os.path.join(directory_path, file)
            os.remove(file_path)
    return last_date



def prepend_new_data_to_csv(issuer_code,csv_path):
    new_data = pd.read_html(f'./{issuer_code}/Историски податоци.xls')
    new_data = new_data[0]
    array = ["Цена на последна трансакција", "Мак.", "Мин.", "Просечна цена", "Промет во БЕСТ во денари",
             "Вкупен промет во денари"]
    new_data["Количина"] = new_data["Количина"].astype(str)
    for i in range(0, len(new_data)):
        ############ kolicina
        num = new_data.loc[i, "Количина"]
        index = num.find(".")
        vrednost = num[index + 1:]
        if vrednost == '0':
            num = num.replace(".0", "")
        else:
            num = num.replace(".", ",")
        new_data.loc[i, "Количина"] = str(num)
        ##########
        new_data.loc[i, "%пром."] = float(new_data.loc[i, "%пром."]) / 100
        for el in array:
            if not isinstance(new_data.loc[i, el], str):
                new_data.loc[i, el] = str(new_data.loc[i, el]).replace(",", "g").replace(
                    ".", ",").replace("g", ".")
            else:
                new_data.loc[i, el] = new_data.loc[i, el].replace(",", "g").replace(
                    ".", ",").replace("g", ".")


    existing_data = pd.read_csv(csv_path)
    updated_data = pd.concat([new_data, existing_data], ignore_index=True)
    updated_data.to_csv(csv_path, index=False)


def process_issuer(issuer_code):
    datum = zemi_posleden_datum_ili_kazi_dali_ne_postoi(issuer_code,f'./{issuer_code}/combined_{issuer_code}_data.csv')

    if datum is False:
        za_siminjanje_csv_kmb(issuer_code)
        od_excel_vo_csv_site_zaedno(issuer_code)
    else:

        if datum != date.today():
            datum = datum + datetime.timedelta(days=1)
            za_siminjanje_csv_kmb(issuer_code, datum)
            prepend_new_data_to_csv(issuer_code, f'./{issuer_code}/combined_{issuer_code}_data.csv')


if __name__ == '__main__':
    issuer_codes = fetch_issuer_codes()
    with ThreadPoolExecutor() as executor:
        executor.map(process_issuer, issuer_codes)

