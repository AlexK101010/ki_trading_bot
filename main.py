import time
from trading_bot import TradingBot
from config import COINS

if __name__ == "__main__":
    bot = TradingBot(coins=COINS)

    print("🤖 KI-Trading-Bot läuft...")

    try:
        while True:
            bot.run_strategy()
            time.sleep(bot.min_trade_interval)
    except KeyboardInterrupt:
        print("🛑 Bot wurde manuell gestoppt.")
