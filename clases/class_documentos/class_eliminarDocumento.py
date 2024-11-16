from flask import jsonify
import models
from models import db

from models import Documentos

class Eliminar_Documento:
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
            idDocumento = datos.get('idDocumento')
            
            if not idDocumento:
                return jsonify({"status": False, "message": "No se ha enviado el ID del documento (idDocumento)"}), 400
            
            documento= Documentos.query.filter_by(idDocumento=idDocumento).first()
            if not documento:
                return jsonify({"status": False, "message": f"No se ha encontrado ningun documento con el ID: {idDocumento}"}), 400
            db.session.delete(documento)
            db.session.commit()
            data = jsonify({"status": True, "message": "Documento eliminado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    