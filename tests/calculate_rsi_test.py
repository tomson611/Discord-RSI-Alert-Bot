import numpy as np
import pandas as pd
from bot import calculate_rsi


def test_calculate_rsi_success():
    data = {
        'timestamp': [1622505600000, 1622509200000, 1622512800000, 1622516400000, 1622520000000],
        'open': [100, 105, 110, 115, 120],
        'high': [110, 115, 120, 125, 130],
        'low': [90, 95, 100, 105, 110],
        'close': [105, 110, 115, 120, 125],
        'volume': [1000, 1500, 2000, 2500, 3000]
    }
    df = pd.DataFrame(data)
    rsi = calculate_rsi(df)
    assert rsi is not None
    assert isinstance(rsi, float)


def test_calculate_rsi_key_error():
    data = {
        'timestamp': [1622505600000, 1622509200000, 1622512800000],
        'open': [100, 105, 110],
        'high': [110, 115, 120],
        'low': [90, 95, 100],
        'volume': [1000, 1500, 2000]
    }
    df = pd.DataFrame(data)
    rsi = calculate_rsi(df)
    assert rsi is None


def test_calculate_rsi_unexpected_error():
    data = {
        'timestamp': [1622505600000, 1622509200000, 1622512800000],
        'open': [100, 'invalid_data', 110],
        'high': [110, 115, 120],
        'low': [90, 95, 100],
        'close': [105, 110, 115],
        'volume': [1000, 1500, 2000]
    }
    df = pd.DataFrame(data)
    rsi = calculate_rsi(df)
    assert rsi is None or np.isnan(rsi)