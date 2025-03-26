from unittest.mock import MagicMock
from app.schemas.address import AddressZipCodeSchema
from app.schemas.status import StatusResponseSchema

def mock_find_address_by_zipcode_success():
    mock = MagicMock()
    mock.return_value = AddressZipCodeSchema(
        zipcode="12345",
        address="123 Main St",
        neighborhood="Central",
        city= "Springfield",
        state="IL",
        number="10"
    )
    return mock

def mock_find_address_by_zipcode_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details=None,
        message="Cep não encontrado."
    )
    return mock
