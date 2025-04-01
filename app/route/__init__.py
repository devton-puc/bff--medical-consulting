from flask_openapi3 import Tag

# Tags para organizar a documentação
patient_tag = Tag(name="Patient", description="Operações relacionadas a pacientes")
zipcode_tag = Tag(name="ZipCode", description="Operações para busca de CEP")
appointment_tag = Tag(name="Appointment", description="Operações relacionadas a consulta de pacientes")
medication_tag =  Tag(name="Medication", description="Operações geração de medicamentos")
