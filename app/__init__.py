from flask_openapi3 import OpenAPI, Info, APIBlueprint
from flask_cors import CORS

from app.route.patient_route import PatientRoute
from app.route.address_route import AddressRoute
from app.route.appointment_route import AppointmentRoute


info = Info(title="BFF Medical Consulting API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

PatientRoute().init_routes(app)
AddressRoute().init_routes(app)
AppointmentRoute().init_routes(app)
