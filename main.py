"""Simple bot implementation for the Composer or Pasta game
"""
import logger


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
	CallbackContext,
	CallbackQueryHandler,
	CommandHandler,
	ConversationHandler,
	Filters,
	MessageHandler,
	Updater,
)


kookiie_logger = logger.get_logger(__name__)
kookiie_logger.info("COMPOSER OR PASTA TELEGRAM BOT")
kookiie_logger.info("===============================")
kookiie_logger.info("Logger successfully loaded in main.")


def fetch_token() -> str:
	# Load token
	with open("token.txt", "r") as token_file:
		token = token_file.read()
	if not token:
		kookiie_logger.error("Token is empty! Please add the Telegram Bot token to token.txt!")
	else:
		kookiie_logger.info("Token successfully loaded in main.")
	return token


def start(update: Update, context: CallbackContext) -> None:
	"""Greet user when a user first talks to the bot"""
	update.message.reply_text("To start a game, use the command /newgame")


def unknown(update: Update, context: CallbackContext) -> None:
	"""Handle unknown commands"""
	context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main() -> None:
	"""Main sequence of the bot"""
	# Start the updater/dispatcher to listen for messages
	# Create the Updater and pass it your bot token.
	updater = Updater(fetch_token(), use_context=True)
	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", start))
	# TODO: Insert conversation handler here
	dispatcher.add_handler(MessageHandler(Filters.command, unknown))

	# Start the Bot
	# updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	# updater.idle()


if __name__ == "__main__":
	main()
