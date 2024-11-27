from flask import jsonify
import models
from models import db

from models import Paquetes

class Editar_Paquete:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idContrato
    @return 
        ERROR
            status, message
        NO ERROR
            status, id_new_empresa
    '''
    def Editar(self, datos):
        try:
            idPaquete = datos.get('idPaquete')
            nombre = datos.get('nombre')
            costo = datos.get('costo')
            idContrato = datos.get('idContrato')
            
            if not idPaquete:
                return jsonify({"status": False, "message": "No se ha enviado el ID de paquete (idPaquete)"}), 400
            
            if not idContrato:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            if not nombre or not costo:
                return jsonify({"status": False, "message": "Faltan datos obligatorios (nombre, costo)"}), 400
            
            
            paquete = Paquetes.query.filter_by(idPaquete=idPaquete).first()
            paquete.nombre = nombre if nombre else paquete.nombre
            paquete.costo = costo if costo else paquete.costo
            paquete.idContrato = idContrato if idContrato else paquete.idContrato
            
            db.session.commit()
            data = jsonify({"status": True, "message": "Paquete editado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    