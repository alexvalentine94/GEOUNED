import logging
import os

formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(funcName)s :: %(lineno)d :: %(message)s")


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    # Create the log_files directory
    log_dir = os.path.join(os.getcwd(), 'log_files')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, log_file)

    handler = logging.FileHandler(log_file)  
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
