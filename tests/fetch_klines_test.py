from unittest.mock import patch
from bot import fetch_klines, ccxt


# Mocking the ccxt library in bot
@patch('bot.ccxt.bybit')
def test_fetch_klines_success(mock_bybit):
    # Mocking the return value of fetch_ohlcv
    mock_bybit().fetch_ohlcv.return_value = [
        [1622505600000, 100, 110, 90, 105, 1000],
        [1622509200000, 105, 115, 95, 110, 1500],
    ]
    with patch('bot.exchange', mock_bybit()):
        df = fetch_klines()
        assert df is not None
        assert df.shape == (2, 6)


@patch('bot.ccxt.bybit')
def test_fetch_klines_network_error(mock_bybit):
    # Simulating a network error
    mock_bybit().fetch_ohlcv.side_effect = ccxt.NetworkError('Network error')
    with patch('bot.exchange', mock_bybit()):
        df = fetch_klines()
        assert df is None


@patch('bot.ccxt.bybit')
def test_fetch_klines_exchange_error(mock_bybit):
    # Simulating an exchange error
    mock_bybit().fetch_ohlcv.side_effect = ccxt.ExchangeError('Exchange error')
    with patch('bot.exchange', mock_bybit()):
        df = fetch_klines()
        assert df is None
