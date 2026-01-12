"""pytest configuration"""
import pytest
from app import create_app
from backend.mock_controller import MockArmController


@pytest.fixture
def mock_controller():
    return MockArmController()


@pytest.fixture
def app(mock_controller):
    app = create_app('testing', arm_controller=mock_controller)
    return app


@pytest.fixture
def client(app):
    return app.test_client()
