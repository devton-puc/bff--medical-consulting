from flask import jsonify

from app.logs.logger import logger
from app.route import appointment_tag, zipcode_tag
from app.schemas import AppointmentSaveSchema, AppointmentViewSchema
from app.schemas.appointment import ListAppointmentViewSchema, IdAppointmentPathSchema
from app.schemas.appointment_filter import AppointmentFilterSchema
from app.schemas.status import StatusResponseSchema
from app.usecase.appointment_usecase import AppointmentUseCase


class AppointmentRoute:

    def __init__(self):
        self.usecase = AppointmentUseCase()

    def init_routes(self, app):
        @app.post('/bff/appointment/list', tags=[appointment_tag],
                  responses={
                      200: ListAppointmentViewSchema,
                      204: None,
                      500: StatusResponseSchema
                  })
        def list_appointments_route(body: AppointmentFilterSchema):
            """Lista os pacientes cadastrados filtrando pelo id do paciente."""
            logger.debug(f"Consultando consulta: Buscando por [{body.patient_id}]")
            response = self.usecase.list_appointments(body)
            if isinstance(response, ListAppointmentViewSchema):
                logger.debug(f"Consultando a consulta [{body.patient_id}]: Dados retornados")
                return jsonify(response.model_dump()), 200
            else:
                logger.debug(
                    f"Consultando a consulta: status code [{response.code}] - mensagem: ['{response.model_dump()}] '")
                return jsonify(response.model_dump()), response.code

        @app.get('/bff/appointment/<int:id_appointment>', tags=[appointment_tag],
                 responses={
                     200: AppointmentViewSchema,
                     404: StatusResponseSchema,
                     500: StatusResponseSchema
                 })
        def get_appointment_route(path: IdAppointmentPathSchema):
            """Busca um paciente pelo ID."""
            logger.debug(f"Buscando a consulta de id: [{path.id_appointment}]")
            response = self.usecase.get_appointment(path.id_appointment)
            if isinstance(response, AppointmentViewSchema):
                logger.debug(f"Buscando a consulta id:[{path.id_appointment}]: Dados retornados")
                return jsonify(response.model_dump()), 200
            else:
                logger.debug(
                    f"Buscando a consulta: status code [{response.code}] - mensagem: [{response.model_dump()}]")
                return jsonify(response.model_dump()), response.code

        @app.post('/bff/appointment/create', tags=[appointment_tag],
                  responses={
                      200: StatusResponseSchema,
                      400: StatusResponseSchema,
                      404: StatusResponseSchema,
                      500: StatusResponseSchema
                  })
        def create_appointment_route(body: AppointmentSaveSchema):
            """Cria um nova consulta."""
            response = self.usecase.create_appointment(body)
            logger.debug(f"Criando a consulta: status code [{response.code}] - mensagem: [{response.model_dump()}] '")
            return jsonify(response.model_dump()), response.code

        @app.put('/bff/appointment/<int:id_appointment>', tags=[appointment_tag],
                 responses={
                     200: StatusResponseSchema,
                     400: StatusResponseSchema,
                     404: StatusResponseSchema,
                     500: StatusResponseSchema
                 })
        def update_appointment_route(path: IdAppointmentPathSchema, body: AppointmentSaveSchema):
            """Atualiza um paciente existente."""
            logger.debug(f"Alterando a consulta de id: [{path.id_appointment}]")
            response = self.usecase.update_appointment(path.id_appointment, body)
            logger.debug(
                f"Atualizando a consulta: status code [{response.code}] - mensagem: [{response.model_dump()}]")
            return jsonify(response.model_dump()), response.code

        @app.delete('/bff/appointment/<int:id_appointment>', tags=[appointment_tag],
                    responses={
                        200: StatusResponseSchema,
                        404: StatusResponseSchema,
                        500: StatusResponseSchema
                    })
        def delete_appointment_route(path: IdAppointmentPathSchema):
            """Exclui um paciente."""
            logger.debug(f"Excluindo a consulta de id: [{path.id_appointment}]")
            response = self.usecase.delete_appointment(path.id_appointment)
            logger.debug(
                f"Excluindo a consulta: status code [{response.code}] - mensagem: [{response.model_dump()}]")
            return jsonify(response.model_dump()), response.code
 