from flask import jsonify
import models
from models import db

from models import Contratistas

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
            id_empresa = datos.get('idEmpresa')
            
            if not nombre or not edad or not ocupacion or not id_empresa:
                return jsonify({"status": False, "message": "No se han enviado todos los datos obligatorios"}), 400
        
            newContratista = Contratistas(
                nombre=nombre,
                edad=edad,
                ocupacion = ocupacion,
                domicilio = domicilio,
                telefono = telefono,
                id_empresa = id_empresa
            )
            db.session.add(newContratista)
            db.session.commit()
            
            id_nuevo_contratista = newContratista.idContratista
            
            data = jsonify({"status": True, "idContratista": id_nuevo_contratista}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error