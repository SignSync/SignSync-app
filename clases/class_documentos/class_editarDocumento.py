from flask import jsonify
import models
from models import db

from models import Documentos

class Editar_Documento:
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
    def Editar(self, idDocumento, nombre, idContrato, file_path):
        try:
            
            if not idDocumento:
                return jsonify({"status": False, "message": "No se ha enviado el ID del documento (idDocumento)"}), 400
            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            if not nombre or not file_path:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre, url)"}), 400
            
            documento = Documentos.query.filter_by(idDocumento=idDocumento).first()
            if not documento:
                return jsonify({"status": False, "message": f"No se ha encontrado ningún documento con el ID {idDocumento}"}), 400
            
            
            documento.nombre = nombre if nombre else documento.nombre
            documento.url = file_path if file_path else documento.url
            documento.idContrato = idContrato if idContrato else documento.idContrato 
                       
            db.session.commit()
            data = jsonify({"status": True, "message": "Documento editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    