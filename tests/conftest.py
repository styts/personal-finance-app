import pytest
from application import app as myapp


@pytest.fixture
def app():
    return myapp
