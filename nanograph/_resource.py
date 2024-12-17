from __future__ import annotations

"""
LiteLLM & Instructor Resources for nanograph

This module manages the initialization and global access of LiteLLM and Instructor clients
as singleton resources. The Instructor helper patches LiteLLM completion methods and provides
the `Instructor` class for structured output functionality.

All LLM completions and resources pull from this shared resource.
"""

from typing import Union
from loguru import logger

from ._config import nanograph_verbose


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


def get_resource() -> _LiteLLMResource:
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

            if nanograph_verbose:
                logger.debug("`LiteLLM` resource imported & initialized successfully")

        except Exception as e:
            raise RuntimeError("Failed to initialize LiteLLM client.") from e

        _litellm_initialized = True

    if nanograph_verbose:
        logger.info("`LiteLLM` resource loaded successfully")

    return _resource_instance



if __name__ == "__main__":

    get_resource()

    nanograph_verbose = True

    get_resource()
