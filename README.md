# Discord RSI Alert Bot

This is a Discord bot that fetches OHLCV data for a specified cryptocurrency symbol from the Bybit exchange, calculates the Relative Strength Index (RSI), and sends an alert message to a Discord channel if the RSI crosses certain thresholds.

## Features

* Fetches OHLCV data for a specified symbol and timeframe from Bybit.
* Calculates the RSI using the TA-Lib library.
* Sends an alert message to a Discord channel if the RSI exceeds 70 (overbought) or drops below 30 (oversold).
* Runs periodically every minute.

## Installation
### Prerequisites
* Python 3.7+
* Docker (optional, for running in a container)

### Local installation

1. Clone the repository:

```bash
git clone https://github.com/tomson611/Discord-RSI-Alert-Bot.git
cd discord-rsi-alert-bot
```
2. Create a virtual environment:

```bash
python -m venv venv
```
3. Activate the virtual environment:

* On Windows:

```bash
venv\Scripts\activate
```
* On macOS/Linux:

```
source venv/bin/activate
```
4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Create a keys.py file and add your Discord bot token and channel ID:

```python
TOKEN = 'your_discord_bot_token'
CHANNEL_ID = your_discord_channel_id
```
6. Run the bot:

```python
python bot.py
```

### Running with Docker

1. Clone the repository:

```bash
git clone https://github.com/tomson611/Discord-RSI-Alert-Bot.git
cd discord-rsi-alert-bot
```
2. Create a keys.py file and add your Discord bot token and channel ID:

```python
TOKEN = 'your_discord_bot_token'
CHANNEL_ID = your_discord_channel_id
```
3. Build the Docker image:

```bash
docker build -t discord-rsi-alert-bot .
```

4. Run the Docker container:

```bash
docker run -d --name discord-rsi-alert-bot discord-rsi-alert-bot
```

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License. See the [LICENSE](/LICENSE file for details.
