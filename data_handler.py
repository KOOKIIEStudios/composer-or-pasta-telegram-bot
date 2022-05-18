"""Handle player data load/saves"""

from pathlib import Path

from ruamel.yaml import YAML

import logger
from player_data import PlayerData


kookiie_logger = logger.get_logger(__name__)
kookiie_logger.info("Logger successfully loaded in data handler.")
PLAYER_DATA_DIRECTORY = Path(".", "player_data.yaml")
COMPOSER_DATA_DIRECTORY = Path(".", "composer_data.yaml")
PASTA_DATA_DIRECTORY = Path(".", "pasta_data.yaml")
yaml = YAML(typ="safe", pure=True)


def load_data(path: Path) -> PlayerData | dict:
	try:
		with open(path, "r") as file_data:
			data = yaml.load(file_data)
			data = data if data is not None else {}
		kookiie_logger.debug("Data loaded from file.")
		return data
	except Exception as e:
		kookiie_logger.error(f"Error! The following exception was encountered while trying to read a YAML file: {e}")
		return {}


def load_player_data() -> PlayerData:
	kookiie_logger.info("Loading player save data from file...")
	if not PLAYER_DATA_DIRECTORY.is_file():
		kookiie_logger.debug("No save data found!")
		return PlayerData({})  # No save data
	return PlayerData(load_data(PLAYER_DATA_DIRECTORY))


def load_composer() -> dict:
	kookiie_logger.info("Loading composer data from file...")
	if not COMPOSER_DATA_DIRECTORY.is_file():
		kookiie_logger.error("No composer data found!")
		return {}
	return load_data(COMPOSER_DATA_DIRECTORY)


def load_pasta() -> dict:
	kookiie_logger.info("Loading pasta data from file...")
	if not PASTA_DATA_DIRECTORY.is_file():
		kookiie_logger.error("No pasta data found!")
		return {}
	return load_data(PASTA_DATA_DIRECTORY)


def save_player_data(player_data: PlayerData) -> None:
	try:
		yaml.dump(dict(player_data), PLAYER_DATA_DIRECTORY)
		kookiie_logger.debug("Data saved to file.")
	except Exception as e:
		kookiie_logger.error(f"Error! The following exception was encountered while trying to dump a YAML file: {e}")
