from flask import jsonify
import models
from models import db

from models import Empresas

class Crear_Empresa:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idUsuario
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_new_empresa
    '''
    def Crear(self, datos):
        try:
            id_usuario = datos.get('id_usuario')
            nombre = datos.get('nombre')
            sector = datos.get('sector')
            correo = datos.get('correo')
            telefono = datos.get('telefono')
            sitio_web = datos.get('sitio_web')
            descripcion = datos.get('descripcion') 
            
            if not id_usuario:
                return jsonify({"status": False, "message": "No se ha enviado el ID del usuario (id_usuario)"}), 400
            
            if not nombre or not sector or not telefono or not correo:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre, sector, telefono o correo)"}), 400
            
            newEmpresa = Empresas(
                nombre=nombre,
                sector=sector,
                correo=correo,
                telefono=telefono,
                sitio_web=sitio_web,
                descripcion=descripcion,
                id_usuario=id_usuario
            )
            db.session.add(newEmpresa)
            db.session.commit()
            id_new_empresa = newEmpresa.idEmpresa
            data = jsonify({"status": True, "id_new_empresa": id_new_empresa}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    