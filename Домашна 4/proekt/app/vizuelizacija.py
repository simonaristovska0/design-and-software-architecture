from django.http import HttpResponse
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO, StringIO
import base64
import matplotlib

matplotlib.use("Agg")

from django.http import JsonResponse
import pandas as pd
import os
from django.conf import settings


def kod_za_generiranje_dijagram(filename, kolku_unazad_vo_denovi, atribbute):
    kolku_unazad_vo_denovi = int(kolku_unazad_vo_denovi)

    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    df = pd.read_csv(data_file_path)
    df = df.head(kolku_unazad_vo_denovi)

    df.columns = df.columns.str.strip()
    df['Датум'] = df['Датум'].str.strip()

    df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')

    if atribbute == 'Цена на последна трансакција' or atribbute == 'Просечна цена':
        df[atribbute] = df[atribbute].str.replace('.', '').str.replace(',', '.').astype(float)
    if atribbute in ['Промет во БЕСТ во денари', 'Вкупен промет во денари']:
        df[atribbute] = df[atribbute].astype(str)
        df[atribbute] = df[atribbute].str.replace('.', '').astype(int)
    if atribbute == '%пром.':
        df[atribbute] = df[atribbute].str.replace(',', '.').astype(float)

    # OVAA# df['Просечна цена'] = df['Просечна цена'].str.replace('.', '').str.replace(',', '.').astype(float)    # Sort DataFrame by 'Датум' to ensure reverse plotting works correctly
    df = df.sort_values(by='Датум', ascending=False)

    labels = df['Датум'].dt.strftime('%d %b %Y').tolist()  # Convert dates to "DD Mon" format
    # OVAA# data = df['Просечна цена'].tolist()
    data = df[atribbute].tolist()
    response_data = {
        "labels": labels,
        "datasets": [{
            "label": "Просечна цена",
            "data": data,
            "borderColor": "#5E72E4",
            "borderWidth": 2,
            "fill": False,
        }]
    }

    return JsonResponse(response_data)


def kod_za_generiranje_tabela(filename):
    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    df = pd.read_csv(data_file_path)

    # Select the first 7 rows
    df = df.head(7)

    # Clean and format the data
    df.columns = df.columns.str.strip()
    df['Датум'] = df['Датум'].str.strip()
    df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y').dt.strftime('%d %b %Y')

    # Convert the DataFrame to a list of dictionaries
    result = df.to_dict(orient='records')

    return JsonResponse(result, safe=False)

def generate_karticki_dashboard(filename):
    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    df = pd.read_csv(data_file_path)

    last_transaction_price = df.iloc[0]['Цена на последна трансакција']
    last_transaction_price = float(last_transaction_price.replace('.', '').replace(',', '.'))
    previous_month_price = df.iloc[30]['Цена на последна трансакција']
    previous_month_price = float(previous_month_price.replace('.', '').replace(',', '.'))
    last_transaction_change = f"{last_transaction_price - previous_month_price:.2f}"

    # Get percent change
    # data['%пром.'] = data['%пром.'].str.replace(',', '.').astype(float)
    percent_change = float(df.iloc[0]['%пром.'].replace(',', '.'))
    percent_change_last_month = percent_change - float(df.iloc[30]['%пром.'].replace(',', '.'))

    total_turnover = int(df.iloc[0]['Вкупен промет во денари'].replace('.', ''))
    total_turnover_last_month = total_turnover - int(df.iloc[30]['Вкупен промет во денари'].replace('.', ''))

    t1, t2, t3 = None, None, None
    if last_transaction_price > 0:
        t1 = f"{float(last_transaction_change):+.2f}"
    elif last_transaction_price < 0:
        t1 = f"{float(last_transaction_change):-.2f}"
    else:
        t1 = f"{float(last_transaction_change):.2f}"

    if percent_change_last_month > 0:
        t2 = f"{float(percent_change_last_month):+.2f}"
    elif percent_change_last_month < 0:
        t2 = f"{float(percent_change_last_month):-.2f}"
    else:
        t2 = f"{float(percent_change_last_month):.2f}"

    if total_turnover_last_month > 0:
        t3 = f"{float(total_turnover_last_month):+.2f}"
    elif total_turnover_last_month < 0:
        t3 = f"{float(total_turnover_last_month):-.2f}"
    else:
        t3 = f"{float(total_turnover_last_month):.2f}"
    # Return the data
    return JsonResponse({
        "lastTransactionPrice": f"{last_transaction_price:,.2f}",
        "lastTransactionChange": t1,
        "percentChange": f"{percent_change:,.2f}",
        "percentChangeLastMonth": t2,
        "totalTurnover": f"{total_turnover}",
        "totalTurnoverLastMonth": t3
    })


def format_price(x, _):
    return f"{int(x):,} ден."
