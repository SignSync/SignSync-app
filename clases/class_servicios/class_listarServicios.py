from flask import jsonify
import models
from models import db

from models import Servicios

class Listar_Servicios:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_new_empresa
    '''
    def Listar(self, idPaquete):
        try:            
            if not idPaquete:
                return jsonify({"status": False, "message": "No se ha enviado el ID del idPaquete (idPaquete)"}), 400
            
            servicios = Servicios.query.filter_by(idPaquete=idPaquete).all()
            
            if not servicios:
                return jsonify({"status": False, "message": f"No se han encontrado servicios con el ID de paquete: {idPaquete}"}), 200
            
            servicios_data = {
                { 
                    "idServicio": servicio.idServicio,
                    "nombre": servicio.nombre,
                    "costo": servicio.costo,
                    "idPaquete": servicio.idPaquete,
                }
                for servicio in servicios
            }
            
            data = jsonify({"status": True, "servicios": servicios_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    