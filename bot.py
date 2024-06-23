import logging
import discord
import ccxt
import pandas as pd
from ta.momentum import RSIIndicator
from discord.ext import commands, tasks
from keys import TOKEN, CHANNEL_ID


logging.basicConfig(level=logging.INFO)  # Configure basic logging

SYMBOL = 'SOL/USDT'
TIMEFRAME = '1h'  # 1-hour interval
PERIOD = 14

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
exchange = ccxt.bybit()


def fetch_klines():
    """Fetches OHLCV data from the exchange for the specified symbol and timeframe.

    Returns:
        pandas.DataFrame: A DataFrame containing OHLCV data or None on error.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=500)
        data_frame = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        return data_frame
    except ccxt.NetworkError as e:
        logging.error(f"Network error fetching data: {e}")
        return None
    except ccxt.ExchangeError as e:
        logging.error(f"Exchange error: {e}")
        return None
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return None


def calculate_rsi(data_frame):
    """Calculates the RSI value for the provided DataFrame and period.

    Args:
        data_frame (pandas.DataFrame): DataFrame containing closing price data.

    Returns:
        float: The RSI value or None on error.
    """
    try:
        data_frame['rsi'] = RSIIndicator(data_frame['close'], window=PERIOD).rsi()
        return data_frame['rsi'].iloc[-1]
    except KeyError as e:
        logging.error(f"Key error: {e}")
        return None
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return None


@tasks.loop(minutes=1)
async def fetch_and_send_rsi():
    data_frame = fetch_klines()  # Use the fetched data_frame

    if data_frame is not None:
        current_rsi = calculate_rsi(data_frame)
        if current_rsi is not None and (current_rsi > 70 or current_rsi < 30):
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                try:
                    await channel.send(f"Alert: Current RSI for {SYMBOL} is {current_rsi:.2f}")
                except discord.HTTPException as e:
                    logging.error(f"Failed to send message: {e}")
            else:
                logging.info("Channel not found")
        elif current_rsi is not None:
            logging.info(f"RSI is {current_rsi:.2f}, no alert needed.")
        else:
            logging.error("RSI calculation returned None.")
    else:
        logging.info("Failed to fetch K-line data.")


@bot.event
async def on_ready():
    logging.info("Bot is ready.")
    fetch_and_send_rsi.start()


bot.run(TOKEN)
