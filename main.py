"""Simple bot implementation for the Composer or Pasta game"""
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

import data_handler
import logger
from game import (
	GameLength,
	States,
	Game,
)


kookiie_logger = logger.get_logger(__name__)
kookiie_logger.info("COMPOSER OR PASTA TELEGRAM BOT")
kookiie_logger.info("===============================")
kookiie_logger.info("Logger successfully loaded in main.")
data = data_handler.load_player_data()
COMPOSERS = data_handler.load_composer()
PASTAS = data_handler.load_pasta()
kookiie_logger.info("Data loaded.")
active_games: list[Game] = []


def get_game(chat_id: int) -> Game | None:
	"""Get a particular game from the list of active games"""
	for game in active_games:
		if game.chat_id == chat_id:
			return game
	return None


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


def populate(update: Update, context: CallbackContext) -> None:
	"""Populate player data with random details (TEMPORARY METHOD FOR TESTING)"""
	data.update_player(314, "Pi", 159)
	update.message.reply_text("Added placeholder data.")


def saved_data(update: Update, context: CallbackContext) -> None:
	"""Populate player data with random details (TEMPORARY METHOD FOR TESTING)"""
	update.message.reply_text("Data: " + str(data))


def save(update: Update, context: CallbackContext) -> None:
	"""Save user data (TEMPORARY METHOD FOR TESTING)"""
	update.message.reply_text("Attempt to save the data - check logs for details.")
	data_handler.save_player_data(data)


def start_new_game(update: Update, context: CallbackContext) -> int:
	# Sanity checks:
	if get_game(update.message.chat_id):
		update.message.reply_text(
			"There is already an active game in this chat.\n"
			"Use the /cancel command, if you would like to terminate the current game."
		)
		return ConversationHandler.END
	chat_type = update.message.chat.type
	if chat_type == "channel":
		update.message.reply_text(
			"ERROR: This feature is not intended for use in channels."
		)
		return ConversationHandler.END

	# Start new game sequence:
	if chat_type == "private":
		return States.GET_GAME_LENGTH
	return States.SEND_INVITE  # Group/Supergroup chat


def is_player(user_id: int, chat_id: int) -> bool:
	"""Check if a particular user is currently playing in the active game"""
	game = get_game(chat_id)
	if not game:  # no active games - sanity check
		return False
	for player in game.players:
		if user_id == player:
			return True
	return False


def cancel(update: Update, context: CallbackContext) -> int | None:
	"""Cancels and ends the game/conversation."""
	chat_id = update.message.chat_id
	user = update.message.from_user

	# Nothing to cancel:
	if not get_game(chat_id):
		update.message.reply_text(
			"There is no active game in this chat.\n"
			"Please use the /newgame command to start a new game."
		)
		return ConversationHandler.END

	# Cancel the current active game in the chat:
	if is_player(user.id, chat_id):
		kookiie_logger.info("User %s canceled the game/conversation.", user.full_name)
		update.message.reply_text("The active game has been terminated")
		return ConversationHandler.END

	update.message.reply_text(
		f"I'm sorry, {user.first_name}, "
		"but only people who are playing the game can cancel it."
	)  # catch-all
	return


def unknown(update: Update, context: CallbackContext) -> None:
	"""Handle unknown commands"""
	context.bot.send_message(
		chat_id=update.effective_chat.id,
		text="""Hmm... I don't seem to recognise this command!
		Perhaps I'm under the influence of the Confundus Charm..."""
	)


def main() -> None:
	"""Main sequence of the bot"""
	# Start the updater/dispatcher to listen for messages
	# Create the Updater and pass it your bot token.
	updater = Updater(fetch_token(), use_context=True)
	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("save", save))
	dispatcher.add_handler(CommandHandler("saved", saved_data))
	dispatcher.add_handler(CommandHandler("populate", populate))
	# TODO: Insert conversation handler here
	conversation_handler = ConversationHandler(
		entry_points=[CommandHandler("newgame", start_new_game)],
		states={

		},
		fallbacks=[CommandHandler('cancel', cancel)],
	)
	dispatcher.add_handler(MessageHandler(Filters.command, unknown))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == "__main__":
	main()
