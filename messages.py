from __future__ import annotations

"""
library level utilities
"""

from typing import Any, Literal, Union, Sequence, List

from ..types.completions.message import Message
from . import rich_logging as logging


@logging.decorators.utility
def construct_message(
    content: Any, role: Literal["system", "user", "assistant", "tool"] = "user"
) -> Message:
    return Message(role=role, content=content)


@logging.decorators.utility
def validate_thread_of_messages(messages: Sequence[Message]) -> Sequence[Message]:
    for message in messages:
        if "role" not in message:
            raise ValueError("message must have a role")

    return messages


@logging.decorators.utility
def format_messages(
    messages: Union[str, Message, Sequence[Message], Sequence[Sequence[Message]]],
) -> Union[Sequence[Message], Sequence[Sequence[Message]]]:
    """
    Inherits messages and corrects them if necessary
    """

    if isinstance(messages, str):
        return [construct_message(messages)]

    elif not isinstance(messages, List):
        if "role" in messages:
            return [messages]
        else:
            raise ValueError(
                "messages must be a string, message, or a list of messages"
            )

    elif isinstance(messages, List):
        if not isinstance(messages[0], List):
            return validate_thread_of_messages(messages)

        else:
            formatted_threads = []
            for thread in messages:
                formatted_threads.append(validate_thread_of_messages(thread))

            return formatted_threads


@logging.decorators.utility
def inherit_messages_from_kwargs(messages: Any = None, *args: Any, **kwargs: Any):
    if messages is None:
        if "messages" in kwargs and kwargs["messages"]:
            messages = kwargs.pop("messages")
        else:
            return None

    # format messages
    messages = format_messages(messages)

    # return messages
    return messages


@logging.decorators.utility
def add_context_to_messages(
    messages: Union[Sequence[Message], Sequence[Sequence[Message]]], context: str
) -> Union[Sequence[Message], Sequence[Sequence[Message]]]:
    """
    Adds context to messages by either:
    1. Appending to the last system message if one exists
    2. Creating a new system message at the start if none exists
    Works with both single message sequences and batches of message sequences.

    Args:
        messages: Single sequence of messages or batch of message sequences
        context: Context string to add to system message

    Returns:
        Messages with context added to system message
    """

    def _add_context_to_sequence(msg_sequence: Sequence[Message]) -> Sequence[Message]:
        # Convert to list for modification
        msg_list = list(msg_sequence)

        # Find last system message if it exists
        system_idx = None
        for i, msg in enumerate(msg_list):
            if msg["role"] == "system":
                system_idx = i

        if system_idx is not None:
            # Append to existing system message
            msg_list[system_idx]["content"] += f"\n\n{context}"
        else:
            # Create new system message at start
            msg_list.insert(0, construct_message(context, role="system"))

        return msg_list

    # Handle both single sequences and batches
    if not messages or not isinstance(messages[0], (list, tuple)):
        return _add_context_to_sequence(messages)
    else:
        return [_add_context_to_sequence(seq) for seq in messages]


@logging.decorators.utility
def swap_system_prompt(
    messages: Sequence[Message],
    prompt: str,
) -> Sequence[Message]:
    """
    Swaps the system prompt in a message sequence.
    Replaces the last or most recent system prompt in the list and removes any previous ones if found.
    If no system prompts are found, adds the new system prompt at the beginning of the list.

    Args:
        messages: Sequence of messages
        prompt: New system prompt to replace the existing one

    Returns:
        Sequence of messages with the system prompt swapped
    """

    # Convert to list for modification
    msg_list = list(messages)

    # Find all system messages
    system_indices = [i for i, msg in enumerate(msg_list) if msg["role"] == "system"]

    if system_indices:
        # Replace the last system message with the new prompt
        last_system_idx = system_indices[-1]
        msg_list[last_system_idx] = construct_message(prompt, role="system")

        # Remove any previous system messages
        for idx in reversed(system_indices[:-1]):
            del msg_list[idx]
    else:
        # Add new system message at the beginning if none exists
        msg_list.insert(0, construct_message(prompt, role="system"))

    return msg_list
