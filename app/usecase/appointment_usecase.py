import requests

from app.logger import logger
from app.schemas.appointment import AppointmentSaveSchema, ListAppointmentViewSchema, AppointmentViewSchema
from app.schemas.appointment_filter import AppointmentFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema

from app.usecase import API_APPOINTMENT_URL



class AppointmentUseCase:

    def list_appointments(self, filter_appointment: AppointmentFilterSchema) -> ListAppointmentViewSchema | StatusResponseSchema:
        
        try:

            filter_dict = filter_appointment.json()
            response = requests.post(f'{API_APPOINTMENT_URL}/appointment/list', json=filter_dict)
           
            if response.status_code == 204:
                return StatusResponseSchema(code=204, message="Consulta não encontrado.")

            list_data = response.json()
            if response.status_code != 200:
                return StatusResponseSchema.model_validate(list_data)

            return ListAppointmentViewSchema.model_validate(list_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o Consulta", details=f"{error}")



    def create_appointment(self, appointment_data: AppointmentSaveSchema) -> StatusResponseSchema:

        try:

            appointment_dict = appointment_data.json()
            response = requests.post(f'{API_APPOINTMENT_URL}/appointment/create', json=appointment_dict)
            status_data = response.json()
            return StatusResponseSchema.model_validate(status_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao criar o Consulta", details=f"{error}")

    def update_appointment(self, id: int, appointment_data: AppointmentSaveSchema) -> StatusResponseSchema:

        try:

            appointment_dict = appointment_data.json()
            response = requests.put(f'{API_APPOINTMENT_URL}/appointment/{id}', json=appointment_dict)
            status_data = response.json()
            return StatusResponseSchema.model_validate(status_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao atualizar o Consulta", details=f"{error}")

    def delete_appointment(self, id: int) -> StatusResponseSchema:
        
        try:

            response = requests.delete(f'{API_APPOINTMENT_URL}/appointment/{id}')
            status_data = response.json()
            return StatusResponseSchema.model_validate(status_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o Consulta", details=f"{error}")


    def get_appointment(self, id: int) -> AppointmentViewSchema | StatusResponseSchema:

        try:
            logger.debug(f"Consultando consulta: Buscando por [{API_APPOINTMENT_URL}]")
            response = requests.get(f'{API_APPOINTMENT_URL}/appointment/{id}')
            appointment_data = response.json()
            if response.status_code != 200:
                return StatusResponseSchema.model_validate(appointment_data)
            
            return AppointmentViewSchema.model_validate(appointment_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o Consulta", details=f"{error}")


