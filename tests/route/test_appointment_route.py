import pytest
from unittest.mock import patch
from app import app
from tests.mock.appointment_mock import (
    mock_list_appointments_success,
    mock_list_appointments_failure_204,
    mock_list_appointments_failure_500,
    mock_get_appointment_success,
    mock_get_appointment_failure_404,
    mock_get_appointment_failure_500,
    mock_create_appointment_success,
    mock_create_appointment_failure_500,
    mock_update_appointment_success,
    mock_update_appointment_failure_404,
    mock_update_appointment_failure_500,
    mock_delete_appointment_success,
    mock_delete_appointment_failure_404,
    mock_delete_appointment_failure_500,
)

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


class TestAppointmentRoute:

    def test_should_return_http200_list_appointments_when_success(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.list_appointments", mock_list_appointments_success()):
            filter_data = {
                "page": 1,
                "per_page": 5,
                "symptoms": "febre"
            }
            response = client.post("/bff/appointment/list", json=filter_data)
            assert response.status_code == 200
            assert 'appointments' in response.json

    def test_should_return_http204_list_appointments_when_no_appointments_found(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.list_appointments", mock_list_appointments_failure_204()):
            filter_data = {
                "page": 1,
                "per_page": 5,
                "symptoms": "febre"
            }
            response = client.post("/bff/appointment/list", json=filter_data)
            assert response.status_code == 204

    def test_should_return_http500_list_appointments_when_error(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.list_appointments", mock_list_appointments_failure_500()):
            filter_data = {
                "page": 1,
                "per_page": 5,
                "symptoms": "febre"
            }
            response = client.post("/bff/appointment/list", json=filter_data)
            assert response.status_code == 500

    def test_should_return_http200_get_appointment_when_success(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.get_appointment", mock_get_appointment_success()):
            response = client.get("/bff/appointment/1")
            assert response.status_code == 200
            assert 'id' in response.json

    def test_should_return_http404_get_appointment_when_not_found(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.get_appointment", mock_get_appointment_failure_404()):
            response = client.get("/bff/appointment/1")
            assert response.status_code == 404

    def test_should_return_http500_get_appointment_when_error(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.get_appointment", mock_get_appointment_failure_500()):
            response = client.get("/bff/appointment/1")
            assert response.status_code == 500

    def test_should_return_http200_create_appointment_when_success(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.create_appointment", mock_create_appointment_success()):
            new_appointment = {
                "date_time": "2000-02-02T00:00:00",
                "doctor_crm": "123456",
                "id": 1,
                "patient_id": 1,
                "symptoms": "febre"
            }
            response = client.post("/bff/appointment/create", json=new_appointment)
            assert response.status_code == 201

    def test_should_return_http400_create_appointment_when_error(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.create_appointment", mock_create_appointment_failure_500()):
            new_appointment = {
                "date_time": "2000-02-02T00:00:00",
                "doctor_crm": "123456",
                "id": 1,
                "patient_id": 1,
                "symptoms": "febre"
            }
            response = client.post("/bff/appointment/create", json=new_appointment)
            assert response.status_code == 500

    def test_should_return_http404_update_appointment_when_not_found(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.update_appointment", mock_update_appointment_failure_404()):
            updated_appointment = {
                "date_time": "2000-02-02T00:00:00",
                "doctor_crm": "123456",
                "id": 1,
                "patient_id": 1,
                "symptoms": "febre"
            }
            response = client.put("/bff/appointment/999", json=updated_appointment)
            assert response.status_code == 404

    def test_should_return_http500_update_appointment_when_error(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.update_appointment", mock_update_appointment_failure_500()):
            updated_appointment = {
                "date_time": "2000-02-02T00:00:00",
                "doctor_crm": "123456",
                "id": 1,
                "patient_id": 1,
                "symptoms": "febre"
            }
            response = client.put("/bff/appointment/1", json=updated_appointment)
            assert response.status_code == 500

    def test_should_return_http200_delete_appointment_when_success(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.delete_appointment", mock_delete_appointment_success()):
            response = client.delete("/bff/appointment/1")
            assert response.status_code == 200

    def test_should_return_http404_delete_appointment_when_not_found(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.delete_appointment", mock_delete_appointment_failure_404()):
            response = client.delete("/bff/appointment/999")
            assert response.status_code == 404

    def test_should_return_http500_delete_appointment_when_error(self, client):
        with patch("app.usecase.appointment_usecase.AppointmentUseCase.delete_appointment", mock_delete_appointment_failure_500()):
            response = client.delete("/bff/appointment/1")
            assert response.status_code == 500