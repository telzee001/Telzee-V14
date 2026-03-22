FROM python:3.10-slim

# Install Freqtrade dependencies
RUN apt-get update && apt-get install -y gcc python3-dev
RUN pip install freqtrade technical python-telegram-bot

# Set working directory
WORKDIR /app
COPY . /app

# Start the bot
CMD ["freqtrade", "trade", "--config", "config.json", "--strategy", "TelzeeV14"]
