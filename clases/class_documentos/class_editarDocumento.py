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
    def Editar(self, datos):
        try:
            idDocumento = datos.get('idDocumento')
            nombre = datos.get('nombre')
            url = datos.get('url')
            idContrato = datos.get('idContrato')
            
            if not idDocumento:
                return jsonify({"status": False, "message": "No se ha enviado el ID del documento (idDocumento)"}), 400
            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            if not nombre or not url:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre, url)"}), 400
            
            
            documento = Documentos.query.filter_by(idDocumento=idDocumento).first()
            if not documento:
                return jsonify({"status": False, "message": f"No se ha encontrado ningún documento con el ID {idDocumento}"}), 400
            
            
            documento.nombre = nombre if nombre else documento.nombre
            documento.costo = url if url else url.costo
            documento.idPaquete = idContrato if idContrato else documento.idContrato 
                       
            db.session.commit()
            data = jsonify({"status": True, "message": "Servicio editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    