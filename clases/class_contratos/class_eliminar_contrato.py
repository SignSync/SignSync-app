from flask import jsonify
import models
from models import db

from models import Contratos, ContratosContratistas

'''
@param idContrato
@return 
    ERROR
        status, message
    NO ERROR
        status, message
'''

class Eliminar_Contrato:
    #DeclaraciÃ³n de contructor de la clase
    def __init__(self) -> None:
        self.usuario = ''
    
    def EliminarContrato(self, datos):
        try:
            #CHECA SI HAY DATOS 
            idContrato = datos['idContrato']
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
               
               
            contrato = Contratos.query.filter_by(idContrato=idContrato).first()
            if not contrato:
                return jsonify({"status": False, "message": "Contrato no encontrado"}), 404
            
            contrato_contratistas = ContratosContratistas.query.filter_by(idContrato=idContrato).all()
            
            for enlace in contrato_contratistas:
                db.session.delete(enlace)
                    
            db.session.delete(contrato)
            db.session.commit()
            
            data = jsonify({"status": True, "message": "Contrato eliminado correctamente"})
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    