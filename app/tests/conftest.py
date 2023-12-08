from app import create_app
import pytest

@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    with flask_app.test_client() as test_client:
        yield test_client
