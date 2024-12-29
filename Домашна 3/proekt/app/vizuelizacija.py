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

# def kod_za_generiranje_dijagram(filename): OVOJ VRAKA SLIKA
#     import matplotlib.dates as mdates
#     import matplotlib.ticker as mticker
#
#     data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
#     df = pd.read_csv(data_file_path)
#     df = df.head(15)
#     df = df.astype(str)
#
#     # Clean column names and strip whitespaces
#     df.columns = df.columns.str.strip()
#     df['Датум'] = df['Датум'].str.strip()
#
#     # Parse 'Датум' to datetime with desired format
#     df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')
#
#     # Clean numeric columns: Replace commas and convert to float
#     numeric_cols = df.columns.drop('Датум')
#     for col in numeric_cols:
#         for i in range(len(df)):
#             df.loc[i, col] = df.loc[i, col].replace(',', '')
#         df[col] = pd.to_numeric(df[col], errors='coerce')
#
#     # Sort DataFrame by 'Датум' to ensure reverse plotting works correctly
#     df = df.sort_values(by='Датум', ascending=False)
#
#     # Scale 'Просечна цена' to make the values more readable
#     df['Просечна цена'] = df['Просечна цена'] * 1000
#
#     # Create a minimalistic plot
#     plt.figure(figsize=(10, 6))
#     plt.plot(df['Датум'], df['Просечна цена'], color="#5E72E4", linewidth=2)
#
#     # Remove gridlines and frame
#     plt.gca().spines["top"].set_visible(False)
#     plt.gca().spines["right"].set_visible(False)
#     plt.gca().spines["left"].set_visible(False)
#     plt.gca().spines["bottom"].set_visible(False)
#     plt.tick_params(left=False, bottom=False)  # Remove ticks
#
#     # Adjust x-axis to display fewer dates
#     plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))  # Show every 2nd date
#     plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %m %Y'))
#     plt.xticks(rotation=45, ha="right", fontsize=10,color="gray")
#
#     # Add a custom y-axis formatter to display prices as "XXXX ден."
#     def format_price(x, _):
#         return f"{int(x):,} ден."
#
#     plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_price))
#
#     plt.yticks(fontsize=10,color="gray")
#
#     # plt.xticks(rotation=45, ha="right", fontsize=10, color="gray")
#
#     # Add a simple title
#     #data_for_KMB.csv
#
#     issuer = filename.replace("data_for_","").replace(".csv","")
#     plt.title(f'{issuer} во изминатиот месец', fontsize=14, fontweight='bold', pad=20)
#
#     # Save the plot to a bytes buffers
#     buffer = BytesIO()
#     plt.savefig(buffer, format="png", bbox_inches='tight', transparent=True)
#     buffer.seek(0)
#     img_data = base64.b64encode(buffer.read()).decode('utf-8')
#     buffer.close()
#
#     return img_data
#


# data.drop(["Мак.", "Мин."], axis=1, inplace=True)
# data['Промет во БЕСТ во денари'] = data['Промет во БЕСТ во денари'].astype(str)
# data['Вкупен промет во денари'] = data['Вкупен промет во денари'].astype(str)
#
# parse(data, ['Цена на последна трансакција', 'Просечна цена'])    GOTOVO
# data['%пром.'] = data['%пром.'].str.replace(',', '.').astype(float)
# data['Промет во БЕСТ во денари'] = data['Промет во БЕСТ во денари'].str.replace('.', '').astype(int) G
# data['Вкупен промет во денари'] = data['Вкупен промет во денари'].str.replace('.', '').astype(int) G
def kod_za_generiranje_dijagram(filename,kolku_unazad_vo_denovi,atribbute):
    kolku_unazad_vo_denovi = int(kolku_unazad_vo_denovi)

    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    df = pd.read_csv(data_file_path)
    df = df.head(kolku_unazad_vo_denovi)

    df.columns = df.columns.str.strip()
    df['Датум'] = df['Датум'].str.strip()

    df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')

    if atribbute == 'Цена на последна трансакција' or atribbute == 'Просечна цена':
        df[atribbute] = df[atribbute].str.replace('.', '').str.replace(',', '.').astype(float)
    if atribbute in ['Промет во БЕСТ во денари','Вкупен промет во денари']:
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


# def kod_za_generiranje_dijagram(filename): OVOJ NE VRAKA JSON
#     data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
#     df = pd.read_csv(data_file_path)
#     df = df.head(15)
#
#     # Clean column names and strip whitespaces
#     df.columns = df.columns.str.strip()
#     df['Датум'] = df['Датум'].str.strip()
#
#     # Parse 'Датум' to datetime with desired format
#     df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')
#
#     # Sort DataFrame by 'Датум' to ensure reverse plotting works correctly
#     df = df.sort_values(by='Датум', ascending=False)
#
#     # Scale 'Просечна цена' to make the values more readable
#     df['Просечна цена'] = df['Просечна цена'] * 1000
#
#     # Prepare data for JSON output
#     labels = df['Датум'].dt.strftime('%d %b').tolist()  # Convert dates to "DD Mon" format
#     data = df['Просечна цена'].tolist()
#
#     # Construct data dictionary
#     response_data = {
#         "labels": labels,
#         "datasets": [{
#             "label": "Просечна цена",
#             "data": data,
#             "borderColor": "#5E72E4",
#             "borderWidth": 2,
#             "fill": False,
#         }]
#     }
#
#     return response_data

def generate_karticki_dashboard(filename):
    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    df = pd.read_csv(data_file_path)

    last_transaction_price = df.iloc[0]['Цена на последна трансакција']
    last_transaction_price = float(last_transaction_price.replace('.','').replace(',','.'))
    previous_month_price = df.iloc[30]['Цена на последна трансакција']
    previous_month_price = float(previous_month_price.replace('.','').replace(',','.'))
    last_transaction_change = f"{last_transaction_price - previous_month_price:.2f}"



    # Get percent change
    # data['%пром.'] = data['%пром.'].str.replace(',', '.').astype(float)
    percent_change = float(df.iloc[0]['%пром.'].replace(',', '.'))
    percent_change_last_month = percent_change - float(df.iloc[30]['%пром.'].replace(',', '.'))


    total_turnover = int(df.iloc[0]['Вкупен промет во денари'].replace('.', ''))
    total_turnover_last_month = total_turnover - int(df.iloc[30]['Вкупен промет во денари'].replace('.', ''))

    t1,t2,t3 = None,None,None
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