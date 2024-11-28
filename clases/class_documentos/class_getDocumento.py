from flask import jsonify
import models
from models import db

from models import Documentos

class Get_Documentos:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idDocumento
    @return 
        ERROR
            status, message
        NO ERROR
            status, documento
    '''
    def Get(self, idDocumento):
        try:            
            documento = Documentos.query.filter_by(idDocumento=idDocumento).first()
            
            if not documento:
                return jsonify({"status": False, "message": f"No se han encontrado el documento con el id {idDocumento}."}), 200
            
            documentos_data = [
                { 
                    "idDocumento": documento.idDocumento,
                    "nombre": documento.nombre,
                    "url": documento.url,
                    "idContrato": documento.idContrato,
                }
            ]
            
            data = jsonify({"status": True, "documento": documentos_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    