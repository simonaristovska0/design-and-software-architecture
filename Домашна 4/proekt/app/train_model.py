import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.http import JsonResponse
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import seaborn as sns
from django.conf import settings
import os
from io import BytesIO
import base64
from sklearn.metrics import r2_score, mean_squared_error
from datetime import timedelta


def func(filename):
    data_file_path = os.path.join(settings.BASE_DIR, 'Data', filename)
    data = pd.read_csv(data_file_path)
    data.drop(["Мак.", "Мин."], axis=1, inplace=True)
    data['Промет во БЕСТ во денари'] = data['Промет во БЕСТ во денари'].astype(str)
    data['Вкупен промет во денари'] = data['Вкупен промет во денари'].astype(str)

    parse(data, ['Цена на последна трансакција', 'Просечна цена'])
    data['%пром.'] = data['%пром.'].str.replace(',', '.').astype(float)
    data['Промет во БЕСТ во денари'] = data['Промет во БЕСТ во денари'].str.replace('.', '').astype(int)
    data['Вкупен промет во денари'] = data['Вкупен промет во денари'].str.replace('.', '').astype(int)
    data["Датум"] = pd.to_datetime(data["Датум"], format='%d.%m.%Y')
    data.set_index(keys=["Датум"], inplace=True)
    data.sort_index(inplace=True)
    data = data["2023-06-06 00:00:00":].copy(deep=True)

    # Add a row with None values for tomorrow FUTURE PREDICTION
    tomorrow_date = data.index[-1] + timedelta(days=1)
    new_row = pd.DataFrame([[None] * len(data.columns)], columns=data.columns, index=[tomorrow_date])
    data = pd.concat([data, new_row])

    lag = 7
    columns = data.columns
    for i in range(1, lag + 1):
        for col in columns:
            data[f'{col}_prev_{i}'] = data[col].shift(i)

    # Separate the new row for tomorrow FUTURE PREDICTION
    new_row = data.loc[[tomorrow_date]].copy()
    data.drop(index=tomorrow_date, inplace=True)

    data = data.dropna(axis=0)

    fetures_za_drop = data.columns[1:6]
    data.drop(fetures_za_drop, axis=1, inplace=True)

    X, Y = data.drop("Цена на последна трансакција", axis=1), data['Цена на последна трансакција']
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.3, shuffle=False)

    skalar_future = MinMaxScaler()
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    skalar_future.fit(X_train)
    X_train = scaler.transform(X_train)
    X_val = scaler.transform(X_val)
    Y_train = scaler.fit_transform(Y_train.values.reshape(-1, 1))
    Y_val = scaler.transform(Y_val.values.reshape(-1, 1))
    X_train = X_train.reshape(X_train.shape[0], lag, X_train.shape[1] // lag)
    X_val = X_val.reshape(X_val.shape[0], lag, X_val.shape[1] // lag)

    # Prepare the input for tomorrow's prediction FUTURE PREDICTION
    print(new_row.drop(
        ['Цена на последна трансакција', 'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари',
         'Вкупен промет во денари'], axis=1))
    print(new_row.drop(
        ['Цена на последна трансакција', 'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари',
         'Вкупен промет во денари'], axis=1).values)
    new_row_input = new_row.drop(
        ['Цена на последна трансакција', 'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари',
         'Вкупен промет во денари'], axis=1).values
    new_row_input = skalar_future.transform(new_row_input)
    new_row_input = new_row_input.reshape(1, lag, new_row_input.shape[1] // lag)

    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss=keras.losses.MeanSquaredError(), optimizer=keras.optimizers.Adam(),
                  metrics=[keras.metrics.MeanSquaredError(), keras.metrics.MeanAbsoluteError()])
    model.fit(X_train, Y_train, validation_data=(X_val, Y_val), batch_size=16, epochs=50, shuffle=False)

    preds = model.predict(X_val)
    preds = scaler.inverse_transform(preds)
    Y_val = scaler.inverse_transform(Y_val)

    # Predict tomorrow's price FUTURE PREDICTION
    future_pred = model.predict(new_row_input)
    future_pred = scaler.inverse_transform(future_pred)

    # Extract dates for validation set
    validation_dates = X.index[-len(Y_val):].strftime('%Y-%m-%d').tolist()

    # Calculate statistics
    r2 = r2_score(Y_val, preds)
    mse = mean_squared_error(Y_val, preds)

    # Create JSON response
    response_data = {
        "labels": validation_dates,
        "datasets": [
            {
                "label": "Predictions",
                "data": preds.flatten().tolist(),
                "borderColor": "#F5365C",
                "fill": False
            },
            {
                "label": "Actual Validation",
                "data": Y_val.flatten().tolist(),
                "borderColor": "#5E72E4",
                "fill": False
            }
        ],
        "statistics": {
            "r2_score": round(r2, 3),
            "mean_squared_error": round(mse, 3)
        }
        ,
        "future_prediction": {
            "date": tomorrow_date.strftime('%Y-%m-%d'),
            "predicted_price": round(float(future_pred[0, 0]), 2)
        }
    }

    return JsonResponse(response_data)


def parse(data, columns):
    for c in columns:
        data[c] = data[c].str.replace('.', '').str.replace(',', '.').astype(float)
    return data
