from __future__ import annotations

"""
LiteLLM & Instructor Resources for Seaside

This module manages the initialization and global access of LiteLLM and Instructor clients
as singleton resources. The Instructor helper patches LiteLLM completion methods and provides
the `Instructor` class for structured output functionality.

All LLM completions and resources pull from this shared resource.
"""

from typing import Union
from instructor.client import from_litellm, Instructor, AsyncInstructor
from instructor.mode import Mode

from ._logging import styles, console, logger, levels, decorators


# ------------------------------------------------------------
# Global Flags & Resource Instance
# ------------------------------------------------------------

_litellm_initialized = False
_resource_instance: _LiteLLMResource | None = None


# ------------------------------------------------------------
# LiteLLM Client Resource
# ------------------------------------------------------------


class _LiteLLMResource:
    """
    Internal LiteLLM client resource wrapper.

    Handles initialization of the LiteLLM library and sets configuration flags
    for compatibility between LLM providers.
    """

    def __init__(self):
        import litellm

        self.litellm = litellm

        # LiteLLM configuration flags
        self.litellm.drop_params = True
        self.litellm.modify_params = True


# ------------------------------------------------------------
# Get Client Resource
# ------------------------------------------------------------


@decorators.core
def get_litellm_resource(verbose: bool = False) -> _LiteLLMResource:
    """
    Returns the global LiteLLM resource singleton, initializing it if necessary.

    Args:
        verbose (bool): Whether to print verbose output.

    Returns:
        _LiteLLMResource: The global resource singleton.
    """
    global _litellm_initialized
    global _resource_instance

    if not _litellm_initialized:
        try:
            _resource_instance = _LiteLLMResource()

            if logger.isEnabledFor(levels.DEBUG):
                logger.debug("_LiteLLMResource imported successfully.")

            if verbose:
                console.print(
                    f"{styles.STRING_MAIN('LiteLLMResource')} imported successfully."
                )
        except Exception as e:
            raise RuntimeError("Failed to initialize LiteLLM client.") from e

        _litellm_initialized = True

    if logger.isEnabledFor(levels.DEBUG):
        logger.debug("_LiteLLMResource loaded successfully.")

    if verbose:
        console.print(
            f"{styles.STRING_MAIN('LiteLLMResource')} loaded successfully."
        )

    return _resource_instance


# ------------------------------------------------------------
# Get Instructor Client
# ------------------------------------------------------------


@decorators.core
def get_instructor_resource(
    instructor_mode: str = "tool_call",
    _resource: _LiteLLMResource = get_litellm_resource(),
    _async: bool = False,
    verbose: bool = False,
) -> Union[Instructor, AsyncInstructor]:
    """
    Returns an `Instructor` resource, patched with LiteLLM's completion or acompletion method.

    Args:
        instructor_mode (str): The mode to use for Instructor's structured output functionality.
        _resource (_LiteLLMResource): The initialized LiteLLM resource to use.
        _async (bool): Whether to use the async version of the Instructor client.
        verbose (bool): Whether to print verbose output.

    Returns:
        Instructor: The synchronous Instructor client.
        AsyncInstructor: The asynchronous Instructor client.

    Raises:
        ValueError: If an invalid instructor_mode is provided.
    """
    if instructor_mode not in Mode._value2member_map_:
        raise ValueError(f"Invalid instructor mode: [bold]{instructor_mode}[/bold]")

    if _async:
        client = from_litellm(_resource.litellm.acompletion, mode=Mode(instructor_mode))

        if logger.isEnabledFor(levels.DEBUG):
            logger.debug("AsyncInstructor client created successfully.")

        if verbose:
            console.print(
                f"{styles.STRING_MAIN('AsyncInstructor')} client created successfully."
            )
    else:
        client = from_litellm(_resource.litellm.completion, mode=Mode(instructor_mode))

        if logger.isEnabledFor(levels.DEBUG):
            logger.debug("Instructor client created successfully.")

        if verbose:
            console.print(
                f"{styles.STRING_MAIN('Instructor')} client created successfully."
            )

    if verbose:
        console.print(
            f"{styles.STRING_MAIN('get_instructor_resource')} called successfully."
        )

    return client
