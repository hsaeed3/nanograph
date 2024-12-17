from __future__ import annotations

__all__ = [
    "console",
    "logger",
    "setup_logging",
    "utility",
    "api_request",
    "log_execution",
    "resource",
    "main",
    "core",
]

"""
`nanograph` Logging & Decorators

This module uses `rich` for both logging and styled console outputs.
- `setup_logging`: Initializes Rich-based logging.
- `logger`: A pre-configured logger instance for the package.
- Decorators (`utility`, `api_request`, etc.): Log execution time, errors, and outcomes of functions.
"""

import logging
import time
import inspect
from functools import wraps
from typing import Callable, Any
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install


# --------------------------------------------------------------
# Levels
# --------------------------------------------------------------


class levels:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# --------------------------------------------------------------
# Styles
# --------------------------------------------------------------


class styles:
    @staticmethod
    def STRING_MAIN(message: Any) -> str:
        return f"[bold red]{message}[/bold red]"

    @staticmethod
    def STRING_VALUE_1(message: Any) -> str:
        return f"[italic dark_turquoise]{message}[/italic dark_turquoise]"

    @staticmethod
    def STRING_VALUE_2(message: Any) -> str:
        return f"[italic dark_cyan]{message}[/italic dark_cyan]"

    @staticmethod
    def STRING_VALUE_3(message: Any) -> str:
        return f"[italic dark_green]{message}[/italic dark_green]"

    @staticmethod
    def INT_1(message: Any) -> str:
        return f"[bold light_coral]{message}[/bold light_coral]"

    @staticmethod
    def INT_2(message: Any) -> str:
        return f"[bold light_steel_blue1]{message}[/bold light_steel_blue1]"

    @staticmethod
    def INT_3(message: Any) -> str:
        return f"[bold pale_violet_red1]{message}[/bold pale_violet_red1]"

    @staticmethod
    def TEXT(message: Any) -> str:
        return f"[dim italic]{message}[/dim italic]"


# --------------------------------------------------------------
# Console Setup
# --------------------------------------------------------------


console = Console()


class LogStyles:
    """Helper for quick styling in log messages."""

    @staticmethod
    def success(message: str) -> str:
        return f"[bold green]{message}[/bold green]"

    @staticmethod
    def error(message: str) -> str:
        return f"[bold red]{message}[/bold red]"

    @staticmethod
    def info(message: str) -> str:
        return f"[bold blue]{message}[/bold blue]"

    @staticmethod
    def highlight(message: str, color: str = "yellow") -> str:
        return f"[{color}]{message}[/{color}]"


# --------------------------------------------------------------
# Logging Setup
# --------------------------------------------------------------


def setup_logging(
    console: Console, level: str | int | None = logging.WARNING
) -> logging.Logger:
    """
    Configure Rich-based logging for the package.

    Args:
        console (Console): Rich console instance.
        level (str | int | None): Logging level (e.g., "INFO" or 20).

    Returns:
        logging.Logger: Configured logger instance.
    """
    install(console=console)

    # Resolve log level if provided as string
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.WARNING)

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                show_time=True,
                show_level=True,
                show_path=False,
                markup=True,
            )
        ],
    )

    logger = logging.getLogger("nanograph")
    logger.setLevel(level)
    return logger


# Pre-configured logger instance
logger = setup_logging(console, level=logging.INFO)


# --------------------------------------------------------------
# Base Logging Decorator
# --------------------------------------------------------------


def log_function(
    prefix: str, prefix_color: str = "green", level: int = logging.INFO
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Create a decorator for logging function execution details.

    Args:
        prefix (str): Prefix for log messages (e.g., "API REQUEST").
        prefix_color (str): Rich color for prefix styling.
        level (int): Log level (default: logging.INFO).

    Returns:
        Callable: Decorator for logging execution.
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                if prefix == "CORE":
                    # Get the module that called the function
                    frame = inspect.currentframe()
                    print(frame)
                    if frame:
                        caller_frame = frame.f_back.f_back  # Go up two frames to get caller
                        if caller_frame:
                            module = inspect.getmodule(caller_frame)
                            if module:
                                module_name = module.__name__
                                logger.log(
                                    level,
                                    f"[{prefix_color}]{prefix}[/{prefix_color}] Executing [bold]{func.__name__}[/bold] from module {module_name}",
                                )
                else:
                    logger.log(
                        level,
                        f"[{prefix_color}]{prefix}[/{prefix_color}] Executing [bold]{func.__name__}[/bold]",
                    )
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.log(
                    level,
                    f"[{prefix_color}]{prefix}[/{prefix_color}] [bold]{func.__name__}[/bold] completed in {duration:.2f}s",
                )
                return result
            except Exception as e:
                logger.error(
                    f"[bold red]{prefix} ERROR[/bold red] [bold]{func.__name__}[/bold] failed: {str(e)}"
                )
                raise

        return wrapper

    return decorator


# --------------------------------------------------------------
# Public Logging Decorators
# --------------------------------------------------------------

_utility = log_function("UTILITY", prefix_color="cyan", level=logging.DEBUG)
_api_request = log_function("API REQUEST", prefix_color="yellow", level=logging.INFO)
_log_execution = log_function("EXECUTION", prefix_color="green", level=logging.INFO)
_resource = log_function("RESOURCE", prefix_color="blue", level=logging.INFO)
_main = log_function("MAIN", prefix_color="magenta", level=logging.INFO)
_core = log_function("CORE", prefix_color="red", level=logging.CRITICAL)


class decorators:
    """
    decorator class for code readability
    """

    utility = _utility
    api_request = _api_request
    log_execution = _log_execution
    resource = _resource
    main = _main
    core = _core


# --------------------------------------------------------------
# Example Usage
# --------------------------------------------------------------

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

    @decorators.utility
    def example_utility():
        time.sleep(1)
        return "Utility example complete!"

    @decorators.core
    def example_api_request():
        time.sleep(2)
        return "API request complete!"

    @decorators.log_execution
    def example_log_execution():
        time.sleep(0.5)
        raise ValueError("Example error!")

    console.print(LogStyles.success("Starting Nanograph Logging Tests..."))
    console.print(LogStyles.info(example_utility()))
    console.print(LogStyles.highlight(example_api_request(), "cyan"))

    try:
        example_log_execution()
    except ValueError:
        console.print(LogStyles.error("Handled Example Error"))
