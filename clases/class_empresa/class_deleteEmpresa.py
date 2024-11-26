from flask import jsonify
import models
from models import db

from models import Empresas

class Delete_Empresa:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idEmpresa
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def delete(self, datos):
        try:
            if not datos:
                return jsonify({"status": False, "message": "No se ha enviado ningun dato"}), 400
            
            idEmpresa = datos.get('idEmpresa')
            if not idEmpresa:
                idEmpresa = datos.get('id_empresa')
                
            if not idEmpresa:
                return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa)"}), 400
            
            empresa = Empresas.query.filter_by(idEmpresa = idEmpresa).first()
            if not empresa: 
                return jsonify({"status": False, "message": "No se ha encontrado ningua empresa con el idEmpresa: " + idEmpresa}), 400
            
            db.session.delete(empresa)
            db.session.commit()
            data = jsonify({"status": True, "message": "Se ha eliminado correctamente la empresa"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    