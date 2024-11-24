from flask import jsonify
import models
from models import db

from models import Documentos

class Listar_Documentos:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idContrato
    @return 
        ERROR
            status, message
        NO ERROR
            status, documentos
    '''
    def Listar(self, idContrato):
        try:            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del idPaquete (idPaquete)"}), 400
            
            documentos = Documentos.query.filter_by(idContrato=idContrato).all()
            
            if not documentos:
                return jsonify({"status": False, "message": f"No se han encontrado documentos con el ID de contrato: {idContrato}"}), 200
            
            documentos_data = {
                { 
                    "idDocumento": documento.idDocumento,
                    "nombre": documento.nombre,
                    "url": documento.url,
                    "idContrato": documento.idContrato,
                }
                for documento in documentos
            }
            
            data = jsonify({"status": True, "documentos": documentos_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    