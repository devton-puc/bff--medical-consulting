import pytest
from unittest.mock import patch
from app.usecase.patient_usecase import PatientUseCase
from app.schemas.patient import PatientSaveSchema, ListPatientViewSchema, PatientViewSchema
from app.schemas.patient_filter import PatientFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.address import AddressSchema


class TestPatientUseCase:

    @pytest.fixture
    def usecase_mock(self):
        return PatientUseCase()

    @patch('app.usecase.patient_usecase.requests.post')    
    def test_should_list_patients_when_success(self, mock_post, usecase_mock):
        mock_list = {
            "page": 1,
            "patients": [
                {
                    "address": {
                        "address": "123 Main St",
                        "city": "Springfield",
                        "neighborhood": "Central",
                        "number": "10",
                        "state": "IL",
                        "zipcode": "12345"
                    },
                    "birth_date": "22/02/1990",
                    "email": "joana.dark@email.com",
                    "gender": "female",
                    "id": 1,
                    "name": "Joana Dark",
                    "phone": "2133448866",
                    "personal_id": "12345678900"
                }
            ],
            "per_page": 5,
            "total": 1
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_list
        filter_data = PatientFilterSchema(
            page=1,
            per_page=5,
            name=""
        )
        result = usecase_mock.list_patients(filter_data)
        assert isinstance(result, ListPatientViewSchema)

    @patch('app.usecase.patient_usecase.requests.post')    
    def test_should_list_patients_when_no_content(self, mock_post, usecase_mock):
        mock_status = {"code": 204, "message": "Paciente não encontrado."}
        mock_post.return_value.status_code = 204
        mock_post.return_value.json.return_value = mock_status

        filter_data = PatientFilterSchema(
            page=1,
            per_page=5,
            name=""
        )
        result = usecase_mock.list_patients(filter_data)
        assert isinstance(result, StatusResponseSchema)
        assert result.code == 204
        assert result.message == "Paciente não encontrado."

    @patch('app.usecase.patient_usecase.requests.post')    
    def test_should_list_patients_when_error(self, mock_post, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = mock_status

        filter_data = PatientFilterSchema(
            page=1,
            per_page=5,
            name=""
        )
        result = usecase_mock.list_patients(filter_data)
        assert isinstance(result, StatusResponseSchema)
        assert result.code == 500
        assert result.message == "erro generico."

    @patch('app.usecase.patient_usecase.requests.post')    
    def test_should_create_patient_when_success(self, mock_post, usecase_mock):
        mock_status = {"code": 201, "message": "paciente criado com sucesso."}
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_status

        address_data = AddressSchema(
            zipcode="12345-678",
            address="Rua das Flores",
            neighborhood="Centro",
            city="São Paulo",
            state="SP",
            number="100"
        )

        patient_data = PatientSaveSchema(
            name="John Doe",
            personal_id="12345678900",
            email="john.doe@example.com",
            phone="123456789",
            gender="male",
            birth_date="1990-01-01",
            address=address_data
        )
        result = usecase_mock.create_patient(patient_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 201
        assert result.message == "paciente criado com sucesso."

    @patch('app.usecase.patient_usecase.requests.post')    
    def test_should_create_patient_when_error(self, mock_post, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = mock_status

        address_data = AddressSchema(
            zipcode="12345-678",
            address="Rua das Flores",
            neighborhood="Centro",
            city="São Paulo",
            state="SP",
            number="100"
        )

        patient_data = PatientSaveSchema(
            name="John Doe",
            personal_id="12345678900",
            email="john.doe@example.com",
            phone="123456789",
            gender="male",
            birth_date="1990-01-01",
            address=address_data
        )
        result = usecase_mock.create_patient(patient_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 500
        assert result.message == "erro generico."

    @patch('app.usecase.patient_usecase.requests.put')
    def test_should_update_patient_when_success(self, mock_put, usecase_mock):
        mock_status = {"code": 200, "message": "paciente alterado com sucesso."}
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = mock_status

        address_data = AddressSchema(
            zipcode="98765-432",
            address="Avenida Paulista",
            neighborhood="Bela Vista",
            city="São Paulo",
            state="SP",
            number="50"
        )

        patient_data = PatientSaveSchema(
            name="Jane Doe",
            personal_id="12345678900",
            email="jane.doe@example.com",
            phone="987654321",
            gender="female",
            birth_date="1985-12-12",
            address=address_data
        )
        result = usecase_mock.update_patient(1, patient_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 200
        assert result.message == "paciente alterado com sucesso."

    @patch('app.usecase.patient_usecase.requests.put')
    def test_should_update_patient_when_not_found(self, mock_put, usecase_mock):
        mock_status = {"code": 404, "message": "paciente não encontrado."}
        mock_put.return_value.status_code = 404
        mock_put.return_value.json.return_value = mock_status

        address_data = AddressSchema(
            zipcode="98765-432",
            address="Avenida Paulista",
            neighborhood="Bela Vista",
            city="São Paulo",
            state="SP",
            number="50"
        )

        patient_data = PatientSaveSchema(
            name="Jane Doe",
            personal_id="12345678900",
            email="jane.doe@example.com",
            phone="987654321",
            gender="female",
            birth_date="1985-12-12",
            address=address_data
        )
        result = usecase_mock.update_patient(1, patient_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 404
        assert result.message == "paciente não encontrado."


    @patch('app.usecase.patient_usecase.requests.put')
    def test_should_update_patient_when_error(self, mock_put, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_put.return_value.status_code = 500
        mock_put.return_value.json.return_value = mock_status

        address_data = AddressSchema(
            zipcode="98765-432",
            address="Avenida Paulista",
            neighborhood="Bela Vista",
            city="São Paulo",
            state="SP",
            number="50"
        )

        patient_data = PatientSaveSchema(
            name="Jane Doe",
            personal_id="12345678900",
            email="jane.doe@example.com",
            phone="987654321",
            gender="female",
            birth_date="1985-12-12",
            address=address_data
        )
        result = usecase_mock.update_patient(1, patient_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 500
        assert result.message == "erro generico."

    @patch('app.usecase.patient_usecase.requests.get')    
    def test_should_return_patient_get_patient_when_success(self, mock_get, usecase_mock):
        mock_patient = {
            "id": 1,
            "name": "John Doe",
            "personal_id": "12345678900",
            "email": "john.doe@example.com",
            "phone": "123456789",
            "gender": "male",
            "birth_date": "1990-01-01",
            "address": {
                "zipcode": "12345-678",
                "address": "Rua das Flores",
                "neighborhood": "Centro",
                "city": "São Paulo",
                "state": "SP",
                "number": "100"
            }
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_patient

        result = usecase_mock.get_patient(1)

        assert isinstance(result, PatientViewSchema)
        assert result.id == 1
        assert result.name == "John Doe"
        assert result.address.zipcode == "12345-678"
        assert result.address.address == "Rua das Flores"
        assert result.address.neighborhood == "Centro"
        assert result.address.city == "São Paulo"
        assert result.address.state == "SP"
        assert result.address.number == "100"

    @patch('app.usecase.patient_usecase.requests.get')    
    def test_should_get_patient_when_not_found(self, mock_get, usecase_mock):
        mock_status = {"code": 404, "message": "paciente nao encontrado."}
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = mock_status
        result = usecase_mock.get_patient(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "paciente nao encontrado."

    @patch('app.usecase.patient_usecase.requests.get')    
    def test_should_get_patient_when_error(self, mock_get, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = mock_status
        result = usecase_mock.get_patient(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "erro generico."

    @patch('app.usecase.patient_usecase.requests.delete')    
    def test_should_delete_patient_when_success(self, mock_delete, usecase_mock):
        mock_status = {"code": 200, "message": "paciente excluido com sucesso."}
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = mock_status
        result = usecase_mock.delete_patient(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "paciente excluido com sucesso."

    @patch('app.usecase.patient_usecase.requests.delete')    
    def test_should_delete_patient_when_not_found(self, mock_delete, usecase_mock):
        mock_status = {"code": 404, "message": "paciente nao encontrado."}
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.json.return_value = mock_status
        result = usecase_mock.delete_patient(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "paciente nao encontrado."

    @patch('app.usecase.patient_usecase.requests.delete')    
    def test_should_delete_patient_when_error(self, mock_delete, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_delete.return_value.status_code = 500
        mock_delete.return_value.json.return_value = mock_status
        result = usecase_mock.delete_patient(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "erro generico."