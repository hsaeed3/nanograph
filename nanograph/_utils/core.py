from __future__ import annotations

"""
nanograph/_utils/core.py

Library level core resources (logging/cache/configuration)
- Configures Rich Console into loguru logging
- Controls global library verbosity
- Ensures nanograph cache directory exists
- Ensures nanograph log file exists
"""

from typing import Any
from loguru import logger
import os
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install


# -----------------------------------------------------------------------------
# styles (let me have some fun)
# -----------------------------------------------------------------------------

class styles:
    """
    Quick use logging styles for conditional vars/flags
    """

    def str_bold(
        text : Any
    ):
        return f"[bold red1]{str(text)}[/bold red1]"
    
    def str_1(
        text : Any
    ):
        return f"[italic salmon1]{str(text)}[/italic salmon1]"
    
    def str_2(
        text : Any
    ):
        return f"[italic pink1]{str(text)}[/italic pink1]"
    
    def str_3(
        text : Any
    ):
        return f"[italic orange1]{str(text)}[/italic orange1]"
    
    def int_1(
        text : int
    ):
        return f"[bold medium_turquoise]{text}[/bold medium_turquoise]"
    
    def int_2(
        text : int
    ):
        return f"[bold aquamarine3]{text}[/bold aquamarine3]"
    
    def int_3(
        text : int
    ):
        return f"[bold dark_sea_green3]{text}[/bold dark_sea_green3]"
    
 
# -----------------------------------------------------------------------------
# global verbosity & logger config
# -----------------------------------------------------------------------------

# Global verbosity flag
nanograph_verbose = False

# Rich console instance
console = Console(markup = True)

# Install rich traceback
install(console=console)

# -----------------------------------------------------------------------------
# nanograph cache & config directory validation
# -----------------------------------------------------------------------------

_config_ensured = False

def validate_nanograph_cache_dir():
    """Ensure the nanograph cache directory and log file exist."""
    cache_dir = os.path.expanduser("~/.cache/nanograph")
    log_file = os.path.join(cache_dir, "logs.log")

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Ensure log file exists
    if not os.path.exists(log_file):
        logger.add(log_file)

def ensure_nanograph_config():
    """Ensure the nanograph configuration is initialized."""
    global _config_ensured
    if not _config_ensured:
        validate_nanograph_cache_dir()
        if nanograph_verbose:
            logger.info("`nanograph` configuration initialized successfully")
        _config_ensured = True

# Ensure nanograph config on import
ensure_nanograph_config()

# -----------------------------------------------------------------------------
# logging helper
# -----------------------------------------------------------------------------

def _get_logger_instance(name: str = "nanograph"):
    """Create and return a logger instance with a RichHandler."""
    # Remove all existing handlers
    logger.remove()

    # Add a new RichHandler
    logger.add(
        RichHandler(
            console=console,
            markup=True,
            show_time=False,
            show_level=False,
        )
    )

    return logger

def get_logger(name: str = "nanograph"):
    """Get a logger instance, ensuring configuration is initialized."""
    ensure_nanograph_config()
    return _get_logger_instance(name)

if __name__ == "__main__":
    logger = get_logger()
    logger.info("[bold plum3 italic]hello[/bold plum3 italic]")
