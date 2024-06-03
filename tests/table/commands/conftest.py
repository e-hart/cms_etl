import pytest
from pytest_mock import MockerFixture


@pytest.fixture(autouse=True)
def mock_print(mocker: MockerFixture):
    """Mock the console.print function."""
    return mocker.patch("cms_etl.utils.console.print")
