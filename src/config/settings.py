# src/config/settings.py

"""
Configuration file for the Telegram bot.
"""
import os

# Read the Telegram bot token from an environment variable.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("Telegram bot token not found. Please set the TELEGRAM_TOKEN environment variable.")