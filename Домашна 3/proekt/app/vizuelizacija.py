from django.http import HttpResponse
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO, StringIO
import base64
import matplotlib
matplotlib.use("Agg")

import os
from django.conf import settings

def kod_za_generiranje_dijagram(filename):
    import matplotlib.dates as mdates
    import matplotlib.ticker as mticker

    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    df = pd.read_csv(data_file_path)
    df = df.head(15)
    df = df.astype(str)

    # Clean column names and strip whitespaces
    df.columns = df.columns.str.strip()
    df['Датум'] = df['Датум'].str.strip()

    # Parse 'Датум' to datetime with desired format
    df['Датум'] = pd.to_datetime(df['Датум'], format='%d.%m.%Y')

    # Clean numeric columns: Replace commas and convert to float
    numeric_cols = df.columns.drop('Датум')
    for col in numeric_cols:
        for i in range(len(df)):
            df.loc[i, col] = df.loc[i, col].replace(',', '')
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Sort DataFrame by 'Датум' to ensure reverse plotting works correctly
    df = df.sort_values(by='Датум', ascending=False)

    # Scale 'Просечна цена' to make the values more readable
    df['Просечна цена'] = df['Просечна цена'] * 1000

    # Create a minimalistic plot
    plt.figure(figsize=(10, 6))
    plt.plot(df['Датум'], df['Просечна цена'], color="#5E72E4", linewidth=2)

    # Remove gridlines and frame
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.tick_params(left=False, bottom=False)  # Remove ticks

    # Adjust x-axis to display fewer dates
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))  # Show every 2nd date
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %m %Y'))
    plt.xticks(rotation=45, ha="right", fontsize=10,color="gray")

    # Add a custom y-axis formatter to display prices as "XXXX ден."
    def format_price(x, _):
        return f"{int(x):,} ден."

    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(format_price))

    plt.yticks(fontsize=10,color="gray")

    # plt.xticks(rotation=45, ha="right", fontsize=10, color="gray")

    # Add a simple title
    #data_for_KMB.csv

    issuer = filename.replace("data_for_","").replace(".csv","")
    plt.title(f'{issuer} во изминатиот месец', fontsize=14, fontweight='bold', pad=20)

    # Save the plot to a bytes buffers
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight', transparent=True)
    buffer.seek(0)
    img_data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return img_data


def format_price(x, _):
    return f"{int(x):,} ден."