"""
config tests
"""


import pytest
from nanograph import _config as config


# ensure cache dir creation
def test_config_cache_dir_created():

    import os

    # get cache dir
    cache_dir = os.path.expanduser("~/.cache/nanograph")
    config.ensure_nanograph_config()

    assert os.path.exists(cache_dir)


