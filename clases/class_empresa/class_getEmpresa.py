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
    def Get(self, id_usuario, idEmpresa):
        try:
            if not id_usuario and not idEmpresa:
                return jsonify({"status": False, "message": "No se ha enviado el ID del usuario ni el ID de empresa (id_usuario, idEmpresa)"}), 400
            
            if id_usuario and not idEmpresa: 
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa: 
                    return jsonify({"status": False, "message": "No se ha encontrado ningua empresa con el id_usuario: " + id_usuario}), 400
            
                empresa_data = {
                    "idEmpresa": empresa.idEmpresa,
                    "nombre": empresa.nombre,
                    "sector": empresa.sector,
                    "correo": empresa.correo,
                    "telefono": empresa.telefono,
                    "sitio_web": empresa.sitio_web,
                    "descripcion": empresa.descripcion,
                    "id_usuario": empresa.id_usuario
                }
            
                data = jsonify({"status": True, "empresa": empresa_data}), 201
            
            if not id_usuario and idEmpresa: 
                empresa = Empresas.query.filter_by(idEmpresa=idEmpresa).first()
                if not empresa: 
                    return jsonify({"status": False, "message": f"No se ha encontrado ningua empresa con el idEmpresa: {idEmpresa}"}), 400
            
                empresa_data = {
                    "idEmpresa": empresa.idEmpresa,
                    "nombre": empresa.nombre,
                    "sector": empresa.sector,
                    "correo": empresa.correo,
                    "telefono": empresa.telefono,
                    "sitio_web": empresa.sitio_web,
                    "descripcion": empresa.descripcion,
                    "id_usuario": empresa.id_usuario
                }
                data = jsonify({"status": True, "empresa": empresa_data}), 201
                
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    