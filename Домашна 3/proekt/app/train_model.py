import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    # plt.figure(figsize=(12, 6))
    # plt.plot(data.index, data['Цена на последна трансакција'])
    data = data["2023-06-06 00:00:00":].copy(deep=True)
    columns = data.columns
    lag = 7
    for i in range(1, lag + 1):
        for col in columns:
            data[f'{col}_prev_{i}'] = data[col].shift(i)
    data = data.dropna(axis=0)

    fetures_za_drop = data.columns[1:6]
    data.drop(fetures_za_drop, axis=1, inplace=True)
    X, Y = data.drop("Цена на последна трансакција", axis=1), data['Цена на последна трансакција']
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.3, shuffle=False)
    # plt.plot(X_train.index, Y_train)
    # plt.plot(X_val.index, Y_val)
    # plt.legend(['Train', 'Validation'])
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_val = scaler.transform(X_val)
    Y_train = scaler.fit_transform(Y_train.values.reshape(-1, 1))
    Y_val = scaler.transform(Y_val.values.reshape(-1, 1))
    X_train = X_train.reshape(X_train.shape[0], lag, X_train.shape[1] // lag)
    X_val = X_val.reshape(X_val.shape[0], lag, X_val.shape[1] // lag)

    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss=keras.losses.MeanSquaredError(), optimizer=keras.optimizers.Adam(),
                  metrics=[keras.metrics.MeanSquaredError(), keras.metrics.MeanAbsoluteError(),
                           keras.metrics.R2Score()])
    history = model.fit(X_train, Y_train, validation_data=(X_val, Y_val), batch_size=16, epochs=50, shuffle=False)

    # sns.lineplot(history.history['loss'][1:], label='loss')
    # sns.lineplot(history.history['val_loss'][1:], label='val_loss')
    preds = model.predict(X_val)
    preds = scaler.inverse_transform(preds)
    Y_val = scaler.inverse_transform(Y_val)

    plt.figure(figsize=(20, 10))
    plt.plot(Y_val, label='actual')
    plt.plot(preds, label='predicted')
    plt.legend()
    # plt.show()

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight', transparent=True)
    buffer.seek(0)
    img_data = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    print(img_data[:100])
    return img_data


def parse(data, columns):
    for c in columns:
        data[c] = data[c].str.replace('.','').str.replace(',','.').astype(float)
    return data