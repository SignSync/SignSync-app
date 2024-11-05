from flask import jsonify
import models
from models import db

from models import Empresas

class Listar_Empresas:
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
    def Get(self):
        try:
            empresas = Empresas.query.all()
            if not empresas: 
                return jsonify({"status": False, "message": "No se ha encontrado ninguna empresa"}), 400
            empresas_data = [
                {
                    "idEmpresa": empresa.idEmpresa,
                    "nombre": empresa.nombre,
                    "sector": empresa.sector,
                    "correo": empresa.correo,
                    "telefono": empresa.telefono,
                    "sitio_web": empresa.sitio_web,
                    "descripcion": empresa.descripcion,
                    "id_usuario": empresa.id_usuario
                }
                for empresa in empresas
            ]
        
            data = jsonify({"status": True, "empresa": empresas_data}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    