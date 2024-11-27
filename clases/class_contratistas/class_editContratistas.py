from flask import jsonify
import models
from models import db

from models import Empresas, Contratistas

class Edit_Contratistas:
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
        idContratista *
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def Edit(self, datos):
        try:
            idContratista = datos.get('idContratista')
            nombre = datos.get('nombre')
            edad = datos.get('edad')
            ocupacion = datos.get('ocupacion')
            domicilio = datos.get('domicilio')
            telefono = datos.get('telefono')
            # id_empresa = datos.get('id_empresa')
            
            
            if not idContratista:
                idContratista = datos.get('id_contratista')
            if not idContratista:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contratista (idContratista)"}), 400
            
            if not nombre or not edad or not ocupacion:
                return jsonify({"status": False, "message": "No se han enviado todos los datos obligatorios"}), 400
            
                
            contratista = Contratistas.query.filter_by(idContratista=idContratista).first()
            if not contratista: 
                return jsonify({"status": False, "message": f"No se ha encontrado ningún contratista con el ID de contratista: {idContratista}"}), 400
            
            contratista.nombre = nombre if nombre else contratista.nombre
            contratista.edad = edad if edad else contratista.edad
            contratista.ocupacion = ocupacion if ocupacion else contratista.ocupacion
            contratista.domicilio = domicilio if domicilio else contratista.domicilio
            contratista.telefono = telefono if telefono else contratista.telefono
            # contratista.id_empresa = id_empresa if id_empresa else contratista.id_empresa
            
            db.session.commit()
            
            data = jsonify({"status": True, "message": "Contratista editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error