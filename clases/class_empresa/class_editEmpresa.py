from flask import jsonify
import models
from models import db

from models import Empresas

class Edit_Empresa:
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
    def Edit(self, datos):
        try:
            id_usuario = datos['id_usuario']
            idEmpresa = datos['idEmpresa']
            nombre = datos['nombre']
            sector = datos['sector']
            correo = datos['correo']
            telefono = datos['telefono']
            sitio_web = datos['sitio_web']
            descripcion = datos['descripcion']
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa:
                    return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
                idEmpresa = empresa.idEmpresa
            
            
            empresa = Empresas.query.filter_by(idEmpresa = idEmpresa).first()
            if not empresa: 
                return jsonify({"status": False, "message": "No se ha encontrado ningua empresa con el id_usuario: " + id_usuario}), 400
        
    
            empresa.nombre = nombre if nombre else empresa.nombre
            empresa.sector = sector if sector else empresa.sector
            empresa.correo = correo if correo else empresa.correo
            empresa.telefono = telefono if telefono else empresa.telefono
            empresa.sitio_web = sitio_web if sitio_web else empresa.sitio_web
            empresa.descripcion = descripcion if descripcion else empresa.descripcion
        
            data = jsonify({"status": True, "message": "Empresa editada correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    