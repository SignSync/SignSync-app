from flask import jsonify
import models
from models import db
import datetime

from models import Contratos, Empresas
class Listar_Contratos_ALL:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idempresa
    @return contratos_alldata
    '''
    def Listar(self):
        try:
            contratos = Contratos.query.all()
            if not contratos: 
                return jsonify({"status": False, "message": "No se ha encontrado contratos"}), 400
            contratos_data = [
                {
                    "idContrato": contrato.idContrato,  # Asegúrate de reemplazar 'id' con el nombre correcto de la columna primaria
                    "nombre": contrato.nombre,
                    "tipo": contrato.tipo,
                    "lugar": contrato.lugar,
                    "fecha_inicio": contrato.fecha_inicio.isoformat(),  # Convertir fecha a string
                    "fecha_entrega": contrato.fecha_entrega.isoformat(),  # Convertir fecha a string
                    "color": contrato.color,
                    "id_empresa": contrato.id_empresa
                }
                for contrato in contratos
            ]
        
            
            
            data = jsonify({"status": True, "contratos": contratos_data}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    