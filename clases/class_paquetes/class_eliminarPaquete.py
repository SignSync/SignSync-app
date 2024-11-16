from flask import jsonify
import models
from models import db

from models import Paquetes

class Eliminar_Paquete:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idUsuario = ''
            
    '''
    @param idContrato
    @return 
        ERROR
            status, message
        NO ERROR
            status, message
    '''
    def Eliminar(self, datos):
        try:
            idPaquete = datos.get('idPaquete')
            
            if not idPaquete:
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (idContrato)"}), 400
            
            contrato = Paquetes.query.filter_by(idPaquete=idPaquete).first()
            if not contrato:
                return jsonify({"status": False, "message": f"No se ha encontrado ningun paquete con el ID: {idPaquete}"}), 400
            db.session.delete(contrato)
            db.session.commit()
            data = jsonify({"status": True, "message": "Paquete eliminado correctamente"}), 201
            
            return data
            
        except Exception as e:
            print(str(e))
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    