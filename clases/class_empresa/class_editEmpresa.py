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
            
            print(datos)
            idEmpresa = datos.get('id_empresa')
            id_usuario = datos.get('id_usuario')
            nombre = datos.get('nombre')
            sector = datos.get('sector')
            correo = datos.get('correo')
            telefono = datos.get('telefono')
            sitio_web = datos.get('sitio_web')
            descripcion = datos.get('descripcion') 
            
            if not idEmpresa:
                idEmpresa = datos.get('idEmpresa')
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa:
                    return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
                idEmpresa = empresa.idEmpresa
                
            
            empresa = Empresas.query.filter_by(idEmpresa = idEmpresa).first()
            if not empresa: 
                return jsonify({"status": False, "message": "No se ha encontrado ningua empresa con el idEmpresa: " + idEmpresa}), 400
        
    
            empresa.nombre = nombre if nombre else empresa.nombre
            empresa.sector = sector if sector else empresa.sector
            empresa.correo = correo if correo else empresa.correo
            empresa.telefono = telefono if telefono else empresa.telefono
            empresa.sitio_web = sitio_web if sitio_web else empresa.sitio_web
            empresa.descripcion = descripcion if descripcion else empresa.descripcion
        
            db.session.commit()
            
        
            data = jsonify({"status": True, "message": "Empresa editada correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
        except KeyError:
            # Manejar el error cuando 'idEmpresa' no está presente
            return jsonify({"status": False, "message": f"No se ha proporcionado algún dato obligatorio: {e}"}), 400
    
    