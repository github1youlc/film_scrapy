import logging
import sys


def get_logger(level=0, file=None):
	logger = logging.getLogger()
	stream_handler = logging.StreamHandler(sys.stdout)
	formatter = logging.Formatter("%(asctime)-15s: [%(levelname)s]: %(message)s")
	stream_handler.setFormatter(formatter)
	logger.addHandler(stream_handler)
	logger.setLevel(level)
	return logger


log = get_logger()
