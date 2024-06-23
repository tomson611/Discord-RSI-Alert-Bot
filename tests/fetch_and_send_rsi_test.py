from unittest.mock import patch, AsyncMock

import pandas as pd
import pytest

from bot import fetch_and_send_rsi, SYMBOL


@pytest.fixture
def mock_discord_channel():
    with patch('bot.bot.get_channel') as mock_get_channel:
        mock_channel = AsyncMock()
        mock_get_channel.return_value = mock_channel
        yield mock_channel


@pytest.fixture
def mock_fetch_klines():
    with patch('bot.fetch_klines') as mock_fetch_klines:
        yield mock_fetch_klines


@pytest.fixture
def mock_calculate_rsi():
    with patch('bot.calculate_rsi') as mock_calculate_rsi:
        yield mock_calculate_rsi


@pytest.mark.asyncio
async def test_fetch_and_send_rsi_above_threshold(mock_fetch_klines, mock_calculate_rsi, mock_discord_channel):
    mock_fetch_klines.return_value = pd.DataFrame({
        'timestamp': [1622505600000, 1622509200000],
        'open': [100, 105],
        'high': [110, 115],
        'low': [90, 95],
        'close': [105, 110],
        'volume': [1000, 1500]
    })
    mock_calculate_rsi.return_value = 75

    await fetch_and_send_rsi()

    mock_discord_channel.send.assert_called_once_with(f"Alert: Current RSI for {SYMBOL} is 75.00")


@pytest.mark.asyncio
async def test_fetch_and_send_rsi_below_threshold(mock_fetch_klines, mock_calculate_rsi, mock_discord_channel):
    mock_fetch_klines.return_value = pd.DataFrame({
        'timestamp': [1622505600000, 1622509200000],
        'open': [100, 105],
        'high': [110, 115],
        'low': [90, 95],
        'close': [105, 110],
        'volume': [1000, 1500]
    })
    mock_calculate_rsi.return_value = 25

    await fetch_and_send_rsi()

    mock_discord_channel.send.assert_called_once_with(f"Alert: Current RSI for {SYMBOL} is 25.00")


@pytest.mark.asyncio
async def test_fetch_and_send_rsi_no_alert_needed(mock_fetch_klines, mock_calculate_rsi, mock_discord_channel):
    mock_fetch_klines.return_value = pd.DataFrame({
        'timestamp': [1622505600000, 1622509200000],
        'open': [100, 105],
        'high': [110, 115],
        'low': [90, 95],
        'close': [105, 110],
        'volume': [1000, 1500]
    })
    mock_calculate_rsi.return_value = 50

    await fetch_and_send_rsi()

    mock_discord_channel.send.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_and_send_rsi_fetch_klines_failure(mock_fetch_klines, mock_calculate_rsi, mock_discord_channel):
    mock_fetch_klines.return_value = None

    await fetch_and_send_rsi()

    mock_discord_channel.send.assert_not_called()


@pytest.mark.asyncio
async def test_fetch_and_send_rsi_calculate_rsi_failure(mock_fetch_klines, mock_calculate_rsi, mock_discord_channel):
    mock_fetch_klines.return_value = pd.DataFrame({
        'timestamp': [1622505600000, 1622509200000],
        'open': [100, 105],
        'high': [110, 115],
        'low': [90, 95],
        'close': [105, 110],
        'volume': [1000, 1500]
    })
    mock_calculate_rsi.return_value = None

    await fetch_and_send_rsi()

    mock_discord_channel.send.assert_not_called()
