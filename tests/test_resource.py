
import pytest
from nanograph import _resource as resource


def test_resource_is_singleton():

    # get resource instances
    resource_1 = resource.get_resource()
    resource_2 = resource.get_resource()

    assert resource_1 is resource_2
