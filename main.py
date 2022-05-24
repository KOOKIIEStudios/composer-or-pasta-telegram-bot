"""Simple bot implementation for the Composer or Pasta game"""
import random

from telegram import Update
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
import keyboard_model
from game import (
	States,
	Game,
)


kookiie_logger = logger.get_logger(__name__)
kookiie_logger.info("COMPOSER OR PASTA TELEGRAM BOT")
kookiie_logger.info("===============================")
kookiie_logger.info("Logger successfully loaded in main.")
data = data_handler.load_player_data()
COMPOSERS = data_handler.load_composer()
COMPOSER_KEYS = list(COMPOSERS.keys())
kookiie_logger.info("Composer keys cached.")
PASTAS = data_handler.load_pasta()
PASTA_KEYS = list(PASTAS.keys())
kookiie_logger.info("Pasta keys cached.")
kookiie_logger.info("Data loaded.")
active_games: list[Game] = []


# Active game list-related functions ------------------------------------------
def get_game(chat_id: int) -> Game | None:
	"""Get a particular game from the list of active games"""
	for game in active_games:
		if game.chat_id == chat_id:
			return game
	return None


def get_user(chat_id: int, user_id: int) -> int | None:
	"""Get a user from an active game"""
	return active_games[chat_id].players.get(user_id)


def add_player(chat_id: int, user_id: int, full_name: str) -> None:
	"""Add a player to an active game"""
	active_games[chat_id].players[user_id] = full_name


# Question/Answer generation: -------------------------------------------------
def set_question(game: Game) -> None:
	first_roll = random.randint(1, 100)
	if first_roll > 80:  # arbitrary number; pasta
		pasta = random.choice(PASTA_KEYS)
		game.correct_answer = (keyboard_model.KeyboardText.PASTA, pasta)
		return
	composer = random.choice(COMPOSER_KEYS)
	game.correct_answer = (keyboard_model.KeyboardText.COMPOSER, composer)


# Main bot sequence -----------------------------------------------------------
def fetch_token() -> str:
	# Load token
	with open("token.txt", "r") as token_file:
		token = token_file.read()
	if not token:
		kookiie_logger.error("Token is empty! Please add the Telegram Bot token to token.txt!")
	else:
		kookiie_logger.info("Token successfully loaded in main.")
	return token


def start(update: Update, _: CallbackContext) -> None:
	"""Greet user when a user first talks to the bot"""
	update.message.reply_text("To start a game, use the command /newgame")


def get_player_high_score(update: Update, _: CallbackContext) -> None:
	"""Send the highest score recorded for the player"""
	player = data.get_player_high_score(update.message.from_user.id)
	update.message.reply_text(
		f"Hi, {player.get('Name')}.\n"
		f"Your high score is: {player.get('High score')}, "
		f"through a total of {player.get('Number of games played')} games."
	)


def get_high_score(update: Update, _: CallbackContext) -> None:
	"""Send the highest score in the leaderboard"""
	update.message.reply_text(
		f"*The highest score in the leaderboard is:*\n{data.get_highest_score()}",
		parse_mode="MarkdownV2",
	)


def handle_join_button(update: Update, _: CallbackContext) -> int:
	"""Join button clicked"""
	query = update.callback_query
	user = query.from_user
	chat_id = update.effective_chat.id

	query.answer()  # clear the progress bar, if there was a query
	add_player(chat_id, user.id, user.full_name)
	return States.SEND_INVITE  # continue checking for joins


def handle_start_button(update: Update, _: CallbackContext) -> int:
	"""Start button clicked"""
	query = update.callback_query
	user = query.from_user
	chat_id = update.effective_chat.id

	query.answer()  # clear the progress bar, if there was a query
	if not get_user(chat_id, user.id):  # if player isn't in the game, assume they want to join
		add_player(chat_id, user.id, user.full_name)
	query.edit_message_text("Game started.")

	return send_duration_menu(update)


def send_duration_menu(update: Update):
	"""Let the user choose how many rounds to play"""
	update.effective_chat.send_message(
		"Select the length/duration that you would like to play.",
		reply_markup=keyboard_model.GAME_LENGTH_MENU,
	)
	return States.GET_GAME_LENGTH


def start_new_game(update: Update, _: CallbackContext) -> int:
	"""Start a new game

	Determine the chat type, and direct the bot to the appropriate course of action
	"""
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
	active_games.append(Game(update.message.chat_id))
	if chat_type == "private":
		return send_duration_menu(update)
	# if group/supergroup chat, offer multiplayer options:
	update.message.reply_text(
		"Tap 'Join' to join the game, and 'Start' once all players have joined.",
		reply_markup=keyboard_model.JOIN_INVITE_MENU,
	)
	return States.SEND_INVITE


def get_length(update: Update, _: CallbackContext) -> int:
	"""Determine the duration of the game"""
	query = update.callback_query
	chat_id = update.effective_chat.id

	query.answer()  # clear the progress bar, if there was a query
	rounds_per_player = query.data
	game = get_game(chat_id)
	game.set_total_rounds(rounds_per_player)
	game.initialise_order()
	game.initialise_scores()

	new_message = f"*Game Duration:* {rounds_per_player}\n*Players:*\n```\n"
	for player in game.players.values():
		new_message += f"{player}\n"
	new_message += "```"

	query.edit_message_text(
		new_message,
		parse_mode="MarkdownV2",
	)
	return send_question(update)


def send_question(update: Update) -> int:
	"""Generate a question, and send it to the chat"""
	game = get_game(update.effective_chat.id)
	if not game:  # no active games - sanity check
		kookiie_logger.error("No active games")
	if game.is_ended():
		return end_game(update)

	set_question(game)
	update.effective_chat.send_message(
		f"*{game.get_current_player_name()}*, is '_{game.correct_answer[1]}_' the name of a composer or a type of pasta?",
		parse_mode="MarkdownV2",
		reply_markup=keyboard_model.GAME_ANSWER_MENU,
	)
	game.increment_round_number()
	return States.CHECK_ANSWER


def check_answer(update: Update, _: CallbackContext) -> int:
	"""Check if the answer is correct, and handle the scoring"""
	query = update.callback_query
	user = query.from_user
	game = get_game(update.effective_chat.id)

	query.answer()  # clear the progress bar, if there was a query
	if not user.id == game.get_current_player():
		kookiie_logger.debug(f"Wrong player clicked on an answer. Expected {game.get_current_player_name()}, Received {user.full_name}")
		return States.CHECK_ANSWER  # not the intended player for the round

	if query.data == game.correct_answer[0]:
		game.increment_current_player_score()
		query.edit_message_text("That is the correct answer!")
	else:
		query.edit_message_text("Aww.. I'm afraid that's not correct.")

	game.increment_round_number()
	return send_question(update)


def end_game(update: Update) -> int:
	"""Tabulate the results, and save it"""
	game = get_game(update.effective_chat.id)
	message = f"*GAME OVER*\nScores:\n"
	for player_id, player_name in game.players.items():
		# old_score = self.get(user_id).get("High score")
		# 			new_score = high_score if high_score > old_score else old_score
		optional = "    ___New High Score!_\r__" if game.scores.get(player_id) > data.get_player_high_score(player_id) else ""
		message += f"*{player_name}_: {game.scores.get(player_id)}{optional}\n"
	message += "\nThank you for playing!"
	update.effective_chat.send_message(message)

	# update scores to IO
	for player_id, player_name in game.players.items():
		data.update_player(player_id, player_name, game.scores.get(player_id))
	data_handler.save_player_data(data)
	return ConversationHandler.END


def is_player(user_id: int, chat_id: int) -> bool:
	"""Check if a particular user is currently playing in the active game"""
	game = get_game(chat_id)
	if not game:  # no active games - sanity check
		return False
	for player in game.players:
		if user_id == player:
			return True
	return False


def cancel(update: Update, _: CallbackContext) -> int | None:
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
		update.message.reply_text("The active game has been terminated.")
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
	dispatcher.add_handler(CommandHandler("myhiscore", get_player_high_score))
	dispatcher.add_handler(CommandHandler("hiscore", get_high_score))
	conversation_handler = ConversationHandler(
		entry_points=[CommandHandler("newgame", start_new_game)],
		states={
			States.SEND_INVITE: [
				CallbackQueryHandler(handle_join_button, pattern=f"^{keyboard_model.KeyboardText.JOIN}$"),
				CallbackQueryHandler(handle_start_button, pattern=f"^{keyboard_model.KeyboardText.START}$"),
			],
			States.GET_GAME_LENGTH: [CallbackQueryHandler(get_length)],
			States.CHECK_ANSWER: [CallbackQueryHandler(check_answer)],
		},
		fallbacks=[CommandHandler('cancel', cancel)],
	)
	dispatcher.add_handler(conversation_handler)  # For update-handling
	dispatcher.add_handler(MessageHandler(Filters.command, unknown))

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == "__main__":
	main()
