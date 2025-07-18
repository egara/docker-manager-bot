# src/main.py

"""
This is the main entry point of the application.

Initializes and runs the Telegram bot.
"""
import os
from src.bot.bot import TelegramBot
from src.config.settings import TELEGRAM_TOKEN

if __name__ == "__main__":
    # --- Execution Configuration ---
    # Set the USE_WEBHOOK environment variable to "true" to enable webhook mode.
    USE_WEBHOOK = os.getenv("USE_WEBHOOK", "false").lower() == "true"
    
    # Public URL for the webhook (e.g., the one provided by ngrok).
    # Required if USE_WEBHOOK is true.
    PUBLIC_URL = os.getenv("PUBLIC_URL", None)
    
    # Port for the webhook.
    # Used if USE_WEBHOOK is true.
    PORT = int(os.getenv("PORT", 8443))

    # Create an instance of the Telegram bot with the configuration token
    bot = TelegramBot(TELEGRAM_TOKEN)
    
    # Start the bot
    if USE_WEBHOOK:
        bot.run(use_webhook=True, public_url=PUBLIC_URL, port=PORT)
    else:
        bot.run()
