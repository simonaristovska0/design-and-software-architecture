
import pandas as pd
import numpy as np

def calculate_rsi(data, period=14):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_stochastic(data, period=14):
    low_min = data['low'].rolling(window=period).min()
    high_max = data['high'].rolling(window=period).max()
    stochastic_k = 100 * ((data['close'] - low_min) / (high_max - low_min))
    return stochastic_k

def calculate_cci(data, period=20):
    tp = (data['close'] + data['high'] + data['low']) / 3
    tp_sma = tp.rolling(window=period).mean()
    mean_deviation = (tp - tp_sma).abs().rolling(window=period).mean()
    cci = (tp - tp_sma) / (0.015 * mean_deviation)
    return cci

def calculate_adx(data, period=14):
    if len(data) < period:
        return pd.Series([None] * len(data))
    try:
        high_diff = data['high'].diff()
        low_diff = data['low'].diff()

        plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
        minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)

        atr = (data['high'] - data['low']).rolling(window=period).mean()
        plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).sum() / atr)
        minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).sum() / atr)

        dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
        adx = dx.rolling(window=period).mean()
        return adx
    except Exception as e:
        print(f"Error in ADX calculation: {str(e)}")
        return pd.Series([None] * len(data))

def calculate_sma(data, period=10):
    return data['close'].rolling(window=period).mean()

def calculate_ema(data, period=10):
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_wma(data, period=10):
    weights = np.arange(1, period + 1)
    return data['close'].rolling(window=period).apply(
        lambda prices: np.dot(prices, weights) / weights.sum(), raw=True
    )

def calculate_hma(data, period=10):
    half_period = int(period / 2)
    sqrt_period = int(np.sqrt(period))
    wma_half = calculate_wma(data, half_period)
    wma_full = calculate_wma(data, period)
    return calculate_wma(pd.DataFrame({'close': 2 * wma_half - wma_full}), sqrt_period)

def calculate_typical_price(data):
    return (data['close'] + data['high'] + data['low']) / 3

def calculate_roc(data, period=10):
    return (data['close'].pct_change(periods=period) * 100)