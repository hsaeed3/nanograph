"""
message utility tests
"""

import pytest
from loguru import logger
from nanograph._utils import messages as utils_messages


def test_utils_messages_determine_if_batch():

    non_batch = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm fine, thank you!"},
    ]

    batch = [
        [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm fine, thank you!"},
        ],
        [
            {"role": "user", "content": "What is the weather in Tokyo?"},
            {"role": "assistant", "content": "The weather in Tokyo is sunny."},
        ],
    ]

    logger.info(f"Non-Batch; Expected: False")
    logger.info(utils_messages.determine_if_batch(non_batch))

    logger.info(f"Batch; Expected: True")
    logger.info(utils_messages.determine_if_batch(batch))

    assert utils_messages.determine_if_batch(non_batch) is False
    assert utils_messages.determine_if_batch(batch) is True


def test_utils_messages_format_messages():

    string_message = "Hello, how are you?"
    dict_message = {"role": "user", "content": "Hello, how are you?"}
    list_message = [{"role": "user", "content": "Hello, how are you?"}]

    normal_message = [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm fine, thank you!"},
    ]

    batch_message = [
        [
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm fine, thank you!"},
        ],
        [
            {"role": "user", "content": "What is the weather in Tokyo?"},
            {"role": "assistant", "content": "The weather in Tokyo is sunny."},
        ],
    ]

    assert utils_messages.format_messages(string_message) == [dict_message]
    assert utils_messages.format_messages(list_message) == list_message
    assert utils_messages.format_messages(dict_message) == [dict_message]

    assert utils_messages.format_messages(normal_message) == normal_message
    assert utils_messages.format_messages(batch_message) == batch_message


if __name__ == "__main__":
    test_utils_messages_determine_if_batch()