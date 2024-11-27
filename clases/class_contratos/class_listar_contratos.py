from flask import jsonify
import models
from models import db
import datetime

from models import Contratos, ContratosContratistas
class Listar_Contrato:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idempresa
    @return contratos_alldata
    '''
    def Listar(self, idEmpresa):
        try:
            contratos = Contratos.query.filter_by(id_empresa=idEmpresa).all()
            if not contratos: 
                return jsonify({"status": False, "message": "No se ha encontrado contratos con el idEmpresa: " + idEmpresa}), 400
            contratos_alldata = []
        
            for contrato in contratos:
                start = contrato.fecha_inicio <= datetime.datetime.now().date()  # Determinar si ha comenzado
                fecha_entrega = contrato.fecha_entrega
                dias_restantes = (fecha_entrega - datetime.datetime.now().date()).days
                
                idContratista = None
                contratos_contratistas = ContratosContratistas.query.filter_by(idContrato = contrato.idContrato).first()
                if contratos_contratistas:
                    idContratista = contratos_contratistas.idContratista
                
                
                contrato_data = {
                    "idContrato": contrato.idContrato,  # Asegúrate de reemplazar 'id' con el nombre correcto de la columna primaria
                    "nombre": contrato.nombre,
                    "tipo": contrato.tipo,
                    "lugar": contrato.lugar,
                    "fecha_inicio": contrato.fecha_inicio.isoformat(),  # Convertir fecha a string
                    "fecha_entrega": contrato.fecha_entrega.isoformat(),  # Convertir fecha a string
                    "color": contrato.color,
                    "id_empresa": contrato.id_empresa,
                    "idContratista": idContratista
                    
                }
                
                contratos_alldata.append({
                    'contrato_data': contrato_data,
                    'dias_restantes': dias_restantes,
                    'contrato_inicio': start,
                })
            
            data = jsonify({"status": True, "contratos": contratos_alldata}), 201
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    