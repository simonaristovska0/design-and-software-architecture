# import pandas as pd
#
# def generate_rsi_signal(rsi_series):
#     """
#     Generate buy, sell, or neutral signal based on RSI values.
#     :param rsi_series: pandas Series of RSI values.
#     :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
#     """
#     return rsi_series.apply(lambda x: 'Buy' if x < 30 else 'Sell' if x > 70 else 'Neutral')
#
# def generate_cci_signal(cci_series):
#     """
#     Generate buy, sell, or neutral signal based on CCI values.
#     :param cci_series: pandas Series of CCI values.
#     :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
#     """
#     return cci_series.apply(lambda x: 'Buy' if x < -100 else 'Sell' if x > 100 else 'Neutral')
#
# def generate_stochastic_signal(stochastic_series):
#     """
#     Generate buy, sell, or neutral signal based on Stochastic Oscillator values.
#     :param stochastic_series: pandas Series of Stochastic %K values.
#     :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
#     """
#     return stochastic_series.apply(lambda x: 'Buy' if x < 20 else 'Sell' if x > 80 else 'Neutral')
#
# def generate_adx_signal(adx_series):
#     """
#     Generate strong, weak, or neutral trend signal based on ADX values.
#     :param adx_series: pandas Series of ADX values.
#     :return: pandas Series of signals ('Strong', 'Weak', 'Neutral').
#     """
#     return adx_series.apply(lambda x: 'Strong' if x > 25 else 'Weak')
#
# def generate_sma_signal(sma_short, sma_long):
#     """
#     Generate buy, sell, or neutral signal based on SMA crossover.
#     :param sma_short: pandas Series of short-term SMA values.
#     :param sma_long: pandas Series of long-term SMA values.
#     :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
#     """
#     signals = []
#     for short, long in zip(sma_short, sma_long):
#         if pd.notna(short) and pd.notna(long):
#             if short > long:
#                 signals.append('Buy')
#             elif short < long:
#                 signals.append('Sell')
#             else:
#                 signals.append('Neutral')
#         else:
#             signals.append('Neutral')
#     return pd.Series(signals)
import pandas as pd

def generate_rsi_signal(rsi_series):
    """
    Generate buy, sell, or neutral signal based on RSI values.
    :param rsi_series: pandas Series of RSI values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return rsi_series.apply(lambda x: 'Buy' if x < 30 else 'Sell' if x > 70 else 'Neutral')

def generate_cci_signal(cci_series):
    """
    Generate buy, sell, or neutral signal based on CCI values.
    :param cci_series: pandas Series of CCI values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return cci_series.apply(lambda x: 'Buy' if x < -100 else 'Sell' if x > 100 else 'Neutral')

def generate_stochastic_signal(stochastic_series):
    """
    Generate buy, sell, or neutral signal based on Stochastic Oscillator values.
    :param stochastic_series: pandas Series of Stochastic %K values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return stochastic_series.apply(lambda x: 'Buy' if x < 20 else 'Sell' if x > 80 else 'Neutral')

def generate_adx_signal(adx_series):
    """
    Generate strong, weak, or neutral trend signal based on ADX values.
    :param adx_series: pandas Series of ADX values.
    :return: pandas Series of signals ('Strong', 'Weak').
    """
    return adx_series.apply(lambda x: 'Strong' if x > 25 else 'Weak')

def generate_sma_signal(sma_short, sma_long):
    """
    Generate buy, sell, or neutral signal based on SMA crossover.
    :param sma_short: pandas Series of short-term SMA values.
    :param sma_long: pandas Series of long-term SMA values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    signals = []
    for short, long in zip(sma_short, sma_long):
        if pd.notna(short) and pd.notna(long):
            if short > long:
                signals.append('Buy')
            elif short < long:
                signals.append('Sell')
            else:
                signals.append('Neutral')
        else:
            signals.append('Neutral')
    return pd.Series(signals)

def generate_ema_signal(current_price, ema_series):
    """
    Generate buy, sell, or neutral signal based on EMA values.
    :param current_price: pandas Series of current prices.
    :param ema_series: pandas Series of EMA values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return current_price > ema_series.apply(lambda x: 'Buy' if x > ema_series else 'Sell')

def generate_wma_signal(current_price, wma_series):
    """
    Generate buy, sell, or neutral signal based on WMA values.
    :param current_price: pandas Series of current prices.
    :param wma_series: pandas Series of WMA values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return current_price > wma_series.apply(lambda x: 'Buy' if x > wma_series else 'Sell')

def generate_hma_signal(current_price, hma_series):
    """
    Generate buy, sell, or neutral signal based on HMA values.
    :param current_price: pandas Series of current prices.
    :param hma_series: pandas Series of HMA values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return hma_series.apply(lambda x: 'Buy' if current_price > hma_series else 'Neutral')

def generate_roc_signal(roc_series):
    """
    Generate buy, sell, or neutral signal based on ROC values.
    :param roc_series: pandas Series of ROC values.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return roc_series.apply(lambda x: 'Buy' if x > 0 else 'Sell' if x < 0 else 'Neutral')

def generate_median_price_signal(current_price, median_price_series):
    """
    Generate buy, sell, or neutral signal based on Median Price values.
    :param current_price: pandas Series of current prices.
    :param median_price_series: pandas Series of median prices.
    :return: pandas Series of signals ('Buy', 'Sell', 'Neutral').
    """
    return current_price.apply(lambda x: 'Buy' if x > median_price_series else 'Sell')
