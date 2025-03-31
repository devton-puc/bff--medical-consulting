import pytest
from unittest.mock import patch
from app.usecase.appointment_usecase import AppointmentUseCase
from app.schemas.appointment import AppointmentSaveSchema, ListAppointmentViewSchema, AppointmentViewSchema
from app.schemas.appointment_filter import AppointmentFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema


class TestAppointmentUseCase:

    @pytest.fixture
    def usecase_mock(self):
        return AppointmentUseCase()

    @patch('app.usecase.appointment_usecase.requests.post')    
    def test_should_list_appointments_when_success(self, mock_post, usecase_mock):
        mock_list = {
            "appointments": [
                {
                "date_time": "2000-02-02T00:00:00",
                "doctor_crm": "123456",
                "id": 1,
                "medications": [
                    {
                    "appointment_id": 1,
                    "dosage": "500mg",
                    "id": 10,
                    "instructions": "Tomar 1 comprimido a cada 8 horas",
                    "name": "Paracetamol"
                    },
                    {
                    "appointment_id": 1,
                    "dosage": "500mg",
                    "id": 11,
                    "instructions": "Tomar 1 comprimido com bastante l\u00edquido",
                    "name": "Aspirina"
                    }
                ],
                "patient_id": 1,
                "symptoms": "febre"
                },
                {
                "date_time": "2000-02-02T00:00:00",
                "doctor_crm": "123456",
                "id": 3,
                "medications": [
                    {
                    "appointment_id": 3,
                    "dosage": "500mg",
                    "id": 4,
                    "instructions": "Tomar 1 comprimido a cada 6 horas",
                    "name": "Paracetamol"
                    },
                    {
                    "appointment_id": 3,
                    "dosage": "200mg",
                    "id": 5,
                    "instructions": "Tomar 1 comprimido ap\u00f3s as refei\u00e7\u00f5es",
                    "name": "Ibuprofeno"
                    },
                    {
                    "appointment_id": 3,
                    "dosage": "1g",
                    "id": 6,
                    "instructions": "Tomar 1 c\u00e1psula somente em caso de dor",
                    "name": "Dipirona"
                    }
                ],
                "patient_id": 1,
                "symptoms": "dor de cabe\u00e7a"
                }
            ],
            "page": 1,
            "per_page": 5,
            "total": 2
        }

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_list
        filter_data = AppointmentFilterSchema(
            page=1,
            per_page=5,
            patient_id=1
        )
        result = usecase_mock.list_appointments(filter_data)
        assert isinstance(result, ListAppointmentViewSchema)

    @patch('app.usecase.appointment_usecase.requests.post')    
    def test_should_list_appointments_when_no_content(self, mock_post, usecase_mock):
        mock_status = {"code": 204, "message": "Consulta não encontrado."}
        mock_post.return_value.status_code = 204
        mock_post.return_value.json.return_value = mock_status

        filter_data = AppointmentFilterSchema(
            page=1,
            per_page=5,
            patient_id=1
        )
        result = usecase_mock.list_appointments(filter_data)
        assert isinstance(result, StatusResponseSchema)
        assert result.code == 204
        assert result.message == "Consulta não encontrado."

    @patch('app.usecase.appointment_usecase.requests.post')    
    def test_should_list_appointments_when_error(self, mock_post, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = mock_status

        filter_data = AppointmentFilterSchema(
            page=1,
            per_page=5,
            patient_id=1
        )
        result = usecase_mock.list_appointments(filter_data)
        assert isinstance(result, StatusResponseSchema)
        assert result.code == 500
        assert result.message == "erro generico."

    @patch('app.usecase.appointment_usecase.requests.post')    
    def test_should_create_appointment_when_success(self, mock_post, usecase_mock):
        mock_status = {"code": 201, "message": "consulta criado com sucesso."}
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = mock_status

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-04-01T12:00:00",
            symptoms="febre"
        )
        result = usecase_mock.create_appointment(appointment_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 201
        assert result.message == "consulta criado com sucesso."

    @patch('app.usecase.appointment_usecase.requests.post')    
    def test_should_create_appointment_when_error(self, mock_post, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = mock_status

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-04-01T12:00:00",
            symptoms="febre"
        )
        
        result = usecase_mock.create_appointment(appointment_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 500
        assert result.message == "erro generico."

    @patch('app.usecase.appointment_usecase.requests.put')
    def test_should_update_appointment_when_success(self, mock_put, usecase_mock):
        mock_status = {"code": 200, "message": "consulta alterado com sucesso."}
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = mock_status

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-04-01T12:00:00",
            symptoms="febre"
        )
        result = usecase_mock.update_appointment(1, appointment_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 200
        assert result.message == "consulta alterado com sucesso."

    @patch('app.usecase.appointment_usecase.requests.put')
    def test_should_update_appointment_when_not_found(self, mock_put, usecase_mock):
        mock_status = {"code": 404, "message": "consulta não encontrado."}
        mock_put.return_value.status_code = 404
        mock_put.return_value.json.return_value = mock_status

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-04-01T12:00:00",
            symptoms="febre"
        )
        result = usecase_mock.update_appointment(1, appointment_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 404
        assert result.message == "consulta não encontrado."


    @patch('app.usecase.appointment_usecase.requests.put')
    def test_should_update_appointment_when_error(self, mock_put, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_put.return_value.status_code = 500
        mock_put.return_value.json.return_value = mock_status

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-04-01T12:00:00",
            symptoms="febre"
        )
        result = usecase_mock.update_appointment(1, appointment_data)

        assert isinstance(result, StatusResponseSchema)
        assert result.code == 500
        assert result.message == "erro generico."

    @patch('app.usecase.appointment_usecase.requests.get')    
    def test_should_return_appointment_get_appointment_when_success(self, mock_get, usecase_mock):
        mock_appointment = {
            "date_time": "2025-03-25T15:00:00",
            "doctor_crm": "123456",
            "id": 1,
            "medications": [
                {
                   "appointment_id": 1,
                   "dosage": "500mg",
                   "id": 10,
                   "instructions": "Tomar 1 comprimido a cada 8 horas",
                   "name": "Paracetamol"
                },
                {
                   "appointment_id": 1,
                   "dosage": "500mg",
                   "id": 11,
                   "instructions": "Tomar 1 comprimido com bastante liquido",
                   "name": "Aspirina"
                }
            ],
            "patient_id": 1,
            "symptoms": "febre"
        }
              
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_appointment

        response = usecase_mock.get_appointment(1)

        assert isinstance(response, AppointmentViewSchema)
        assert response.id == 1
        assert response.patient_id == 1
        assert response.doctor_crm == "123456"
        assert response.date_time == "2025-03-25T15:00:00"
        assert response.symptoms == "febre"
        assert response.medications[0].name == "Paracetamol"
        assert response.medications[0].dosage == "500mg"
        assert response.medications[0].instructions == "Tomar 1 comprimido a cada 8 horas"
        assert response.medications[1].name == "Aspirina"
        assert response.medications[1].dosage == "500mg"
        assert response.medications[1].instructions == "Tomar 1 comprimido com bastante liquido"

    @patch('app.usecase.appointment_usecase.requests.get')    
    def test_should_get_appointment_when_not_found(self, mock_get, usecase_mock):
        mock_status = {"code": 404, "message": "consulta nao encontrado."}
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = mock_status
        result = usecase_mock.get_appointment(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "consulta nao encontrado."

    @patch('app.usecase.appointment_usecase.requests.get')    
    def test_should_get_appointment_when_error(self, mock_get, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = mock_status
        result = usecase_mock.get_appointment(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "erro generico."

    @patch('app.usecase.appointment_usecase.requests.delete')    
    def test_should_delete_appointment_when_success(self, mock_delete, usecase_mock):
        mock_status = {"code": 200, "message": "consulta excluido com sucesso."}
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = mock_status
        result = usecase_mock.delete_appointment(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "consulta excluido com sucesso."

    @patch('app.usecase.appointment_usecase.requests.delete')    
    def test_should_delete_appointment_when_not_found(self, mock_delete, usecase_mock):
        mock_status = {"code": 404, "message": "consulta nao encontrado."}
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.json.return_value = mock_status
        result = usecase_mock.delete_appointment(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "consulta nao encontrado."

    @patch('app.usecase.appointment_usecase.requests.delete')    
    def test_should_delete_appointment_when_error(self, mock_delete, usecase_mock):
        mock_status = {"code": 500, "message": "erro generico."}
        mock_delete.return_value.status_code = 500
        mock_delete.return_value.json.return_value = mock_status
        result = usecase_mock.delete_appointment(1)
        assert isinstance(result, StatusResponseSchema)
        assert result.message == "erro generico."