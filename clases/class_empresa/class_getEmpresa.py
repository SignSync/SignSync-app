from flask import jsonify
import models
from models import db

from models import Empresas

class Get_Empresa:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, empresa
    '''
    def Get(self, datos):
        try:
            id_usuario = datos['id_usuario']
            
            print(id_usuario)
            
            if not id_usuario:
                return jsonify({"status": False, "message": "No se ha enviado el ID del usuario (id_usuario)"}), 400
            
            empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
            if not empresa: 
                return jsonify({"status": False, "message": "No se ha encontrado ningua empresa con el id_usuario: " + id_usuario}), 400
        
            empresa_data = {
                "idEmpresa": empresa.idEmpresa,
                "nombre": empresa.nombre,
                "id_usuario": empresa.id_usuario
            }
        
            data = jsonify({"status": True, "empresa": empresa_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    