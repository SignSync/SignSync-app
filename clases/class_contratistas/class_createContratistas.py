from flask import jsonify
import models
from models import db

from models import Contratistas, Empresas

class Create_Contratistas:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param 
        nombre *
        edad *
        ocupacion * 
        domicilio
        telefono
        id_empresa *
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_contratista
    '''
    def Create(self, datos):
        try:
            nombre = datos.get('nombre')
            edad = datos.get('edad')
            ocupacion = datos.get('ocupacion')
            domicilio = datos.get('domicilio')
            telefono = datos.get('telefono')
            idEmpresa = datos.get('id_empresa')
            id_usuario = datos.get('id_usuario')
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa:
                    return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
                idEmpresa = empresa.idEmpresa
            
            
            if not nombre or not edad or not ocupacion or not idEmpresa:
                return jsonify({"status": False, "message": "No se han enviado todos los datos obligatorios"}), 400
        
            newContratista = Contratistas(
                nombre=nombre,
                edad=edad,
                ocupacion = ocupacion,
                domicilio = domicilio,
                telefono = telefono,
                id_empresa = idEmpresa
            )
            db.session.add(newContratista)
            db.session.commit()
            
            id_nuevo_contratista = newContratista.idContratista
            
            data = jsonify({"status": True, "idContratista": id_nuevo_contratista}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error