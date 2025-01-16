import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.mse.mk/"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="table table-bordered table-condensed table-striped")

    headers = [th.text.strip() for th in table.find_all("th")]

    rows = []
    for row in table.find_all("tr")[1:]:
        cols = [td.text.strip() for td in row.find_all("td")]
        rows.append(cols)

    df = pd.DataFrame(rows, columns=headers)

    df.to_csv("mse_table.csv", index=False, encoding="utf-8-sig")

    print(df)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
