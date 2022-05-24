"""This module contains representation of game attributes"""
from enum import Enum


class GameLength(Enum):
	"""This class models the number of rounds per player"""
	
	SHORT: int = 10
	MEDIUM: int = 20
	LONG: int = 50


class States(Enum):
	"""This models the different conversation/game states"""

	# Values are arbitrary, but currently in ascending order in case of future expansion
	SEND_INVITE: int = 0
	GET_GAME_LENGTH: int = 1
	CHECK_ANSWER: int = 2


class Game:
	"""This class models individual game rounds"""

	def __init__(self, chat_id: int) -> None:
		self.chat_id: int = chat_id

	total_rounds: int
	current_round: int = 0
	players: dict[int, str]
	scores: dict[int, int]
	order: dict[int, int]
	correct_answer: tuple[str, str]

	def set_total_rounds(self, length: str) -> None:
		self.total_rounds = len(self.players) * GameLength[length].value

	def initialise_order(self) -> None:
		player_ids = self.players.keys()
		for base_counter in range(0, self.total_rounds, len(player_ids)):
			for offset, player_id in enumerate(player_ids):
				self.order[base_counter + offset]: int = player_id

	def initialise_scores(self) -> None:
		for player_id in self.players.keys():
			self.scores[player_id]: int = 0

	def increment_round_number(self) -> None:
		self.current_round += 1

	def is_ended(self) -> bool:
		return self.total_rounds == self.current_round

	def get_current_player(self) -> int:
		return self.order.get(self.current_round)

	def get_current_player_name(self) -> str:
		return self.players.get(self.get_current_player())

	def increment_current_player_score(self) -> None:
		self.scores[self.get_current_player()] += 1
