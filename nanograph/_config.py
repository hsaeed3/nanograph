"""
library level configuration for nanograph
"""

from loguru import logger
import os


# global verbosity flag
global nanograph_verbose
nanograph_verbose = False

# Flag to track if configuration has been ensured
_config_ensured = False


# ensure nanograph cache directory exists
def validate_nanograph_cache_dir():
    cache_dir = os.path.expanduser("~/.cache/nanograph")
    log_file = os.path.join(cache_dir, "logs.log")

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        # create log file
        logger.add(log_file)

    else:
        # ensure log file exists in existing cache directory
        if not os.path.exists(log_file):
            logger.add(log_file)


# setup function
def ensure_nanograph_config():
    global _config_ensured
    if not _config_ensured:
        validate_nanograph_cache_dir()
        if nanograph_verbose:
            logger.info("`nanograph` configuration initialized successfully")
        _config_ensured = True


# Ensure configuration on import
ensure_nanograph_config()
