import requests

from app.schemas.patient import PatientSaveSchema, ListPatientViewSchema, PatientViewSchema
from app.schemas.patient_filter import PatientFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.address import AddressSchema

from app.usecase import API_PATIENT_URL



class PatientUseCase:

    def list_patients(self, filter_patient: PatientFilterSchema) -> ListPatientViewSchema | StatusResponseSchema:
        
        try:

            filter_dict = filter_patient.json()
            response = requests.post(f'{API_PATIENT_URL}/patient/list', json=filter_dict)
           
            if response.status_code == 204:
                return StatusResponseSchema(code=204, message="Paciente não encontrado.")

            list_data = response.json()
            if response.status_code != 200:
                return StatusResponseSchema.model_validate(list_data)

            return ListPatientViewSchema.model_validate(list_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o paciente", details=f"{error}")



    def create_patient(self, patient_data: PatientSaveSchema) -> StatusResponseSchema:

        try:

            patient_dict = patient_data.json()
            response = requests.post(f'{API_PATIENT_URL}/patient/create', json=patient_dict)
            status_data = response.json()
            return StatusResponseSchema.model_validate(status_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao criar o paciente", details=f"{error}")

    def update_patient(self, id: int, patient_data: PatientSaveSchema) -> StatusResponseSchema:

        try:

            patient_dict = patient_data.json()
            response = requests.put(f'{API_PATIENT_URL}/patient/{id}', json=patient_dict)
            status_data = response.json()
            return StatusResponseSchema.model_validate(status_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao atualizar o paciente", details=f"{error}")

    def delete_patient(self, id: int) -> StatusResponseSchema:
        
        try:

            response = requests.delete(f'{API_PATIENT_URL}/patient/{id}')
            status_data = response.json()
            return StatusResponseSchema.model_validate(status_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o paciente", details=f"{error}")


    def get_patient(self, id: int) -> PatientViewSchema | StatusResponseSchema:

        try:
            
            response = requests.get(f'{API_PATIENT_URL}/patient/{id}')
            patient_data = response.json()
            if response.status_code != 200:
                return StatusResponseSchema.model_validate(patient_data)
            
            return PatientViewSchema.model_validate(patient_data)

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o paciente", details=f"{error}")


