from flask import jsonify
import models
from models import db

from models import Servicios

class Eliminar_Servicio:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idContrato
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def Eliminar(self, datos):
        try:
            idServicio = datos.get('idServicio')
            
            if not idServicio:
                return jsonify({"status": False, "message": "No se ha enviado el ID del servicio (idServicio)"}), 400
            
            servicio= Servicios.query.filter_by(idServicio=idServicio).first()
            if not servicio:
                return jsonify({"status": False, "message": f"No se ha encontrado ningun servicio con el ID: {idServicio}"}), 400
            db.session.delete(servicio)
            db.session.commit()
            data = jsonify({"status": True, "message": "Servicio eliminado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    