from __future__ import annotations

"""
Message formatting & thread utilities
"""

from typing import Union, List, Dict, Any, Optional

from .._config import nanograph_verbose
from loguru import logger


# -----------------------------------------------------------------------------


def determine_if_batch(
        messages : Union[
            str, # converted to a user message
            Dict[str, Any], 
            List[Dict[str, Any]],
            List[List[Dict[str, Any]]],
        ]
) -> bool:
    
    if isinstance(messages, str):
        return False
    
    if not isinstance(messages, List):
        return False
    
    # determines if the messages are a batch of messages
    return isinstance(messages[0], List)


def format_messages(
        messages : Union[
            str, # converted to a user message
            Dict[str, Any], 
            List[Dict[str, Any]],
            List[List[Dict[str, Any]]],
        ]
) -> Union[
    List[Dict[str, Any]],
    List[List[Dict[str, Any]]],
]:
    
    if isinstance(messages, str):
        return [{"role": "user", "content": messages}]
    
    if determine_if_batch(messages):
        for thread_idx, thread in enumerate(messages):
            for message in thread:
                if not isinstance(message, Dict) or "role" not in message:
                    logger.error(f"One or more messages in the input batch list are not valid for thread {thread_idx}: {message}")
                    raise ValueError("Invalid message format")
        return messages
    
    # NOTE:
    # really really light check 
    # this specific function does not check the `content` field
    if isinstance(messages, Dict) and "role" in messages:
        return [messages]
    
    elif not isinstance(messages, List):
        logger.error(f"Invalid messages format: {messages}")
        raise ValueError("Invalid messages format")

    for message in messages:
        if not isinstance(message, Dict) or "role" not in message:
            logger.error(f"One or more messages in the input list are not valid: {message}")
            raise ValueError("Invalid message format")
        
    return messages
