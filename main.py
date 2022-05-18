"""Simple bot implementation for the Composer or Pasta game
"""
import logger


kookiie_logger = logger.get_logger("main")
kookiie_logger.info("COMPOSER OR PASTA TELEGRAM BOT")
kookiie_logger.info("===============================")
kookiie_logger.info("Logger successfully loaded in main.")


with open("token.txt", "r") as token_file:
	TOKEN = token_file.read()
if not TOKEN:
	kookiie_logger.error("Token is empty! Please add the Telegram Bot token to token.txt!")
else:
	kookiie_logger.info("Token successfully loaded in main.")

