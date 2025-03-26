import os
from dotenv import load_dotenv


if not os.getenv("VIACEP_API_URL"):
    load_dotenv()

VIACEP_API_URL = os.getenv("VIACEP_API_URL")
API_PATIENT_URL = os.getenv("API_PATIENT_URL")
API_APPOINTMENT_URL = os.getenv("API_APPOINTMENT_URL")