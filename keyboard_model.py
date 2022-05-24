"""This module represents the inline keyboard templates used for the game"""
from enum import Enum

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from game import GameLength


class KeyboardText(Enum):
	"""This class models inline keyboard button callback values"""

	JOIN: str = "JOIN"
	START: str = "START"
	COMPOSER: str = "COMPOSER"
	PASTA: str = "PASTA"


JOIN_INVITE_MENU = InlineKeyboardMarkup(
	[[
		InlineKeyboardButton("Join", callback_data=KeyboardText.JOIN),
		InlineKeyboardButton("Start", callback_data=KeyboardText.START),
	]]
)


GAME_LENGTH_MENU = InlineKeyboardMarkup(
	[[
		InlineKeyboardButton("Short", callback_data=GameLength.SHORT.name),
		InlineKeyboardButton("Medium", callback_data=GameLength.MEDIUM.name),
		InlineKeyboardButton("Long", callback_data=GameLength.LONG.name),
	]]
)


GAME_ANSWER_MENU = InlineKeyboardMarkup(
	[[
		InlineKeyboardButton("Composer", callback_data=KeyboardText.COMPOSER),
		InlineKeyboardButton("Pasta", callback_data=KeyboardText.PASTA),
	]]
)
