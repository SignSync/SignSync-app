from flask import jsonify
import models
from models import db

from models import Servicios

class Editar_Servicio:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idPaquete, nombre, costo, idServicio
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def Editar(self, datos):
        try:
            idPaquete = datos.get('idPaquete')
            nombre = datos.get('nombre')
            costo = datos.get('costo')
            idServicio = datos.get('idServicio')
            
            if not idPaquete:
                return jsonify({"status": False, "message": "No se ha enviado el ID de paquete (idPaquete)"}), 400
            
            if not idServicio:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            if not nombre:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre)"}), 400
            
            
            servicio = Servicios.query.filter_by(idServicio=idServicio).first()
            if not servicio:
                return jsonify({"status": False, "message": f"No se ha encontrado ningún servicio con el ID {idServicio}"}), 400
            
            
            servicio.nombre = nombre if nombre else servicio.nombre
            servicio.costo = costo if costo else servicio.costo
            servicio.idPaquete = idPaquete if idPaquete else servicio.idPaquete 
                       
            db.session.commit()
            data = jsonify({"status": True, "message": "Servicio editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    