import pytest
from unittest.mock import patch
from app import app

from tests.mock.address_mock import (
    mock_find_address_by_zipcode_success,
    mock_find_address_by_zipcode_failure_404,
)


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


class TestAddressRoute:

    def test_should_return_http200_find_address_by_zipcode_when_success(self, client):
        with patch("app.usecase.address_usecase.AddressUseCase.find_address_by_zipcode", mock_find_address_by_zipcode_success()):
            response = client.get("/bff/zipcode/22222222")
            assert response.status_code == 200

    def test_should_return_http404_find_address_by_zipcode_when_not_found(self, client):
        with patch("app.usecase.address_usecase.AddressUseCase.find_address_by_zipcode", mock_find_address_by_zipcode_failure_404()):
            response = client.get("/bff/zipcode/999")
            assert response.status_code == 404
