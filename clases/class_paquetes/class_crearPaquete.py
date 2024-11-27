from flask import jsonify
import models
from models import db

from models import Paquetes

class Crear_Paquete:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idContrato
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_new_empresa
    '''
    def Crear(self, datos):
        try:
            nombre = datos.get('nombre')
            costo = datos.get('costo')
            idContrato = datos.get('idContrato')
            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            if not nombre or not costo:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre, costo)"}), 400
            
            newPaquete = Paquetes(
                nombre=nombre,
                costo=costo,
                idContrato=idContrato
            )
            db.session.add(newPaquete)
            db.session.commit()
            id_new_paquete = newPaquete.idPaquete
            data = jsonify({"status": True, "id_new_paquete": id_new_paquete}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    