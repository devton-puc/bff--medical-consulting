from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema
from app.schemas.symptoms import SymptomsSchema
import json

from app.usecase import API_APPOINTMENT_URL

import requests
from pydantic import BaseModel
from typing import List, Dict
from app.logs.logger import logger


class MedicationUseCase:
    
    def generate_medications(self, symptoms: SymptomsSchema) -> list[MedicationSchema] | StatusResponseSchema:

        try:
            symptoms_dict = symptoms.json()
            response = requests.post(f'{API_APPOINTMENT_URL}/appointment/medications/generate',json=symptoms_dict)
            medications_data = response.json()
            if response.status_code != 200:
                return StatusResponseSchema.model_validate(medications_data)
            
            return medications_data

        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter o paciente", details=f"{error}")


