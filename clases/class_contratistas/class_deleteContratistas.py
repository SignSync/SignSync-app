from flask import jsonify
import models
from models import db

from models import Empresas, Contratistas

class Delete_Contratistas:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idContratista *
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def delete(self, datos):
        try:
            idContratista = datos['idContratista']
            
            if not idContratista:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contratista (idContratista)"}), 400
            
            contratista = Contratistas.query.filter_by(idContratista =idContratista).first()
            
            if not contratista: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún contratista con el id de contratista: {idContratista}"}), 400
            
            db.session.delete(contratista)
            db.session.commit()
            
            data = jsonify({"status": True, "message": "Contratista eliminado correctamente"}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error