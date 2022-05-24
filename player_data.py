"""The class PlayerData models the format for player data storage"""


class PlayerData(dict):
	"""A dictionary with convenience methods for storing gameplay data"""

	def update_player(self, user_id: int, name: str, high_score: int) -> None:
		"""Adds/replaces entries in the dictionary, with the intended format"""
		if user_id not in self:
			self.update({
				user_id: {
					"Name": name,
					"High score": high_score,
					"Number of games played": 1,
				}
			})
		else:
			old_score = self.get(user_id).get("High score")
			new_score = high_score if high_score > old_score else old_score
			new_plays = self.get(user_id).get("Number of games played") + 1
			self.update({
				user_id: {
					"Name": name,
					"High score": new_score,
					"Number of games played": new_plays,
				}
			})

	def get_player_high_score(self, user_id: int) -> dict:
		"""Get the high score for a player"""
		return self.get(user_id)

	def get_highest_score(self) -> str:
		"""Get the player with the highest score, and the relevant details"""
		player = max(self, key=lambda v: self[v]["High score"])
		return '\n'.join([': '.join(i) for i in sorted(player.items())])
