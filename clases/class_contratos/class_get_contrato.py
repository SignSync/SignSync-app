from flask import jsonify
import models
from models import db
import datetime

from models import Contratos, Empresas
class Get_Contrato:
    #Declaración de contructor de la clase
    def __init__(self) -> None:
        self.idEmpresa = ''
            
    '''
    @param idempresa
    @return contratos_alldata
    '''
    def Get(self, idContrato):
        try:
            if not idContrato: 
                return jsonify({"status": False, "message": "No se ha enviado el id del contrato"}), 400
            contrato = Contratos.query.filter_by(idContrato=idContrato).first()
            
            if not contrato: 
                return jsonify({"status": False, "message": f"No se ha encontrado contratos con el idEmpresa: {idContrato}"}), 400
            
            contratos_alldata = []
        
            
            start = contrato.fecha_inicio <= datetime.datetime.now().date()  # Determinar si ha comenzado
            fecha_entrega = contrato.fecha_entrega
            dias_restantes = (fecha_entrega - datetime.datetime.now().date()).days
                
            contrato_data = {
                "idContrato": contrato.idContrato,  # Asegúrate de reemplazar 'id' con el nombre correcto de la columna primaria
                "nombre": contrato.nombre,
                "tipo": contrato.tipo,
                "lugar": contrato.lugar,
                "fecha_inicio": contrato.fecha_inicio.isoformat(),  # Convertir fecha a string
                "fecha_entrega": contrato.fecha_entrega.isoformat(),  # Convertir fecha a string
                "color": contrato.color,
                "id_empresa": contrato.id_empresa
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
    
    