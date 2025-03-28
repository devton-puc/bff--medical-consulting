from flask import jsonify

from app.logs.logger import logger
from app.route import patient_tag, zipcode_tag
from app.schemas.address import AddressZipCodeSchema, ZipCodePathSchema
from app.schemas.status import StatusResponseSchema
from app.usecase.address_usecase import AddressUseCase


class AddressRoute:

    def __init__(self):
        self.address_usecase = AddressUseCase()

    def init_routes(self, app): 
        @app.get('/bff/zipcode/<int:zipcode>', tags=[zipcode_tag],
                 responses={
                     200: AddressZipCodeSchema,
                     400: StatusResponseSchema,
                     500: StatusResponseSchema
                 })
        def find_address_by_zipcode(path: ZipCodePathSchema):
            logger.debug(f"Buscando o endereço de CEP: [{path.zipcode}]")
            response = self.address_usecase.find_address_by_zipcode(path.zipcode)
            if isinstance(response, AddressZipCodeSchema):
                logger.debug(f"Buscando o endereço de CEP: [{path.zipcode}]: Dados retornados")
                return jsonify(response.model_dump()), 200
            else:
                logger.debug(
                    f"Buscando o endereço do paciente: status code [{response.code}] - mensagem: [{response.model_dump()}]")
                return jsonify(response.model_dump()), response.code
