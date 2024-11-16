from flask import jsonify
import models
from models import db

from models import Servicios, Contratos

class Crear_Servicio:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idContrato
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_new_servicio
    '''
    def Crear(self, datos):
        try:
            nombre = datos.get('nombre')
            costo = datos.get('costo')
            idPaquete = datos.get('idPaquete')
            
            if not idPaquete:
                return jsonify({"status": False, "message": "No se ha enviado el ID del paquete (idContrato)"}), 400
            
            if not nombre:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre, sector, telefono o correo)"}), 400
            
            newServicio = Servicios(
                nombre=nombre,
                costo=costo,
                idPaquete=idPaquete
            )
            db.session.add(newServicio)
            db.session.commit()
            id_new_servicio = newServicio.idServicio
            data = jsonify({"status": True, "id_new_servicio": id_new_servicio}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    