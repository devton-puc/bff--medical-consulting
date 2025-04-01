import unittest
from unittest.mock import patch
from app.usecase.address_usecase import AddressUseCase
from app.schemas.address import AddressZipCodeSchema
from app.schemas.status import StatusResponseSchema


class TestAddressUseCase(unittest.TestCase):

    @patch('app.usecase.address_usecase.requests.get')
    def test_should_return_address_find_address_by_zipcode_when_success(self, mock_get):
        mock_response = {
            "cep": "01001-000",
            "logradouro": "Praça da Sé",
            "bairro": "Sé",
            "localidade": "São Paulo",
            "uf": "SP",
            "numero": "123",
            "complemento": "lado ímpar"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        usecase = AddressUseCase()
        result = usecase.find_address_by_zipcode("01001000")

        self.assertIsInstance(result, AddressZipCodeSchema)
        self.assertEqual(result.zipcode, "01001-000")
        self.assertEqual(result.address, "Praça da Sé")
        self.assertEqual(result.neighborhood, "Sé")
        self.assertEqual(result.city, "São Paulo")
        self.assertEqual(result.state, "SP")

    @patch('app.usecase.address_usecase.requests.get')
    def test_should_return_error_find_address_when_zipcode_not_found(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"erro": True}

        usecase = AddressUseCase()
        result = usecase.find_address_by_zipcode("00000000")

        self.assertIsInstance(result, StatusResponseSchema)
        self.assertEqual(result.code, 404)
        self.assertEqual(result.message, "Cep não encontrado.")

    @patch('app.usecase.address_usecase.requests.get')
    def test_should_return_error_find_address_when_invalid_format(self, mock_get):
        mock_get.return_value.status_code = 400

        usecase = AddressUseCase()
        result = usecase.find_address_by_zipcode("123")

        self.assertIsInstance(result, StatusResponseSchema)
        self.assertEqual(result.code, 400)
        self.assertEqual(result.message, "Cep enviado no formato inválido.")

    @patch('app.usecase.address_usecase.requests.get')    
    def test_should_return_error_find_address_when_generic_error(self, mock_get):
        mock_get.return_value.status_code = 500

        usecase = AddressUseCase()
        result = usecase.find_address_by_zipcode("99999999")

        self.assertIsInstance(result, StatusResponseSchema)
        self.assertEqual(result.code, 500)
        self.assertEqual(result.message, "A consulta dos correios retornou um erro não especificado.")

if __name__ == '__main__':
    unittest.main()
