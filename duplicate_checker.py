"""This module checks if there are clashing composer and pasta names"""
import logger


def check(composer_keys: list, pasta_keys: list) -> None:
	kookiie_logger = logger.get_logger(__name__)
	kookiie_logger.info("Logger successfully loaded in checker.")
	composers = set(composer_keys)
	pastas = set(pasta_keys)
	clashing_names = composers.intersection(pastas)
	if clashing_names:
		kookiie_logger.error(f"There are clashing composer and pasta names: {str(clashing_names)}")
	else:
		kookiie_logger.debug("No clashing composer and pasta names found.")
