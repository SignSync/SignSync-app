from flask import jsonify
import models
from models import db

from models import Documentos

class Crear_Documento:
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
    def Crear(self, nombre, idContrato, file):
        try:
            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            if not file:
                return jsonify({'error': 'No se envio el filepath'}), 400
            
            if not nombre:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre)"}), 400
            
            newDocumento = Documentos(
                nombre=nombre,
                url=file,
                idContrato=idContrato
            )
            db.session.add(newDocumento)
            db.session.commit()
            id_new_documento = newDocumento.idDocumento
            data = jsonify({"status": True, "id_new_documento": id_new_documento}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    