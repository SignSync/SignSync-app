from flask import jsonify
import models
from models import db

from models import Empresas, Contratistas

class Get_Contratistas:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idEmpresa
    @return 
        ERROR
            status, message
        NO ERROR
            status, contratistas
    '''
    def Get(self, datos):
        try:
            idEmpresa = datos['idEmpresa']
            id_usuario = datos['id_usuario']
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                idEmpresa = empresa.idEmpresa
                
            contratistas_empresa = Contratistas.query.filter_by(id_empresa=idEmpresa).all()
            
            if not contratistas_empresa: 
                return jsonify({"status": False, "message": "No se ha encontrado ningún contratista con el id de empresa: " + idEmpresa}), 400
        
            data = jsonify({"status": True, "empresa": contratistas_empresa}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error