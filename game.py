"""This module contains representation of game attributes"""
import enum


class GameLength(enum.Enum):
	"""This class models the number of rounds per player"""
	
	short: int = 10
	medium: int = 20
	long: int = 50


class Game:
	"""This class models individual game rounds"""

	def __init__(self, chat_id: int) -> None:
		self.chat_id: int = chat_id

	total_rounds: int
	current_round: int = 0
	players: dict[int, str]
	scores: dict[int, int]
	order: dict[int, int]
	correct_answer: dict[str, str]

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
		self.current_round = self.current_round + 1

	def is_ended(self) -> bool:
		return self.total_rounds == self.current_round
