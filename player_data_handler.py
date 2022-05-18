"""Handle player data load/saves"""

from pathlib import Path

from ruamel.yaml import YAML

import logger
from player_data import PlayerData


kookiie_logger = logger.get_logger(__name__)
kookiie_logger.info("Logger successfully loaded in data handler.")
CURRENT_DIRECTORY = Path(".", "player_data.yaml")
yaml = YAML(typ="safe", pure=True)


def load_data() -> PlayerData:
	if not CURRENT_DIRECTORY.is_file():
		return PlayerData({})  # No save data
	try:
		with open(CURRENT_DIRECTORY, "r") as file_data:
			data = yaml.load(file_data)
		kookiie_logger.debug("Data loaded from file.")
		return PlayerData(data)
	except Exception as e:
		kookiie_logger.error(f"Error! The following exception was encountered while trying to read a YAML file: {e}")
		return PlayerData({})


def save_data(player_data: PlayerData) -> None:
	try:
		yaml.dump(player_data, CURRENT_DIRECTORY)
		kookiie_logger.debug("Data saved to file.")
	except Exception as e:
		kookiie_logger.error(f"Error! The following exception was encountered while trying to dump a YAML file: {e}")
