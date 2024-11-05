from flask import jsonify
import models
from models import db

from datetime import datetime

from models import Contratos, ContratosContratistas, Empresas

###############################PENDIENTE
class Crear_Contrato:
    
    #DeclaraciÃ³n de contructor de la clase
    def __init__(self) -> None:
        self.usuario = ''
    
    '''
        @param 
            idEmpresa || id_usuario
            idContratista
            nombre
            tipo
            lugar
            fecha_inicio
            fecha_entrega
            color
            
        @return
            ERROR 
            status, message
            NO ERROR
            status, idContrato_new
    '''
    def def_crear_contrato(self, datos):
        try:
            nombre = datos.get('nombre')
            tipo = datos.get('tipo')
            lugar=datos.get('lugar')
            fecha_inicio = datos.get('fecha_inicio')
            fecha_entrega = datos.get('fecha_entrega')
            color = datos.get('color')
            idEmpresa = datos.get('idEmpresa')
            id_usuario = datos.get('id_usuario')
            idContratista = datos.get('idContratista')
            
            if not idContratista: 
                return jsonify({"status": False, "message": "No se ha enviado el ID del contratista (idContratista)"}), 400
            
            if not nombre or not fecha_inicio or not fecha_entrega or not color:
                return jsonify({"status": False, "message": "Faltan campos obligatorios"}), 400
            fecha_entrega = datetime.strptime(fecha_entrega, '%d-%m-%Y').strftime('%Y-%m-%d')           
            fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y').strftime('%Y-%m-%d')
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa:
                    return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
                idEmpresa = empresa.idEmpresa
            
            newContract = Contratos(
                nombre=nombre,
                tipo=tipo,
                lugar=lugar,
                fecha_inicio=fecha_inicio,
                fecha_entrega=fecha_entrega,
                color=color,  # Se guarda el color seleccionado
                id_empresa=idEmpresa
            )
            db.session.add(newContract)
            db.session.commit()
            id_nuevo_contrato = newContract.idContrato
            
            newContratos_Contratistas = ContratosContratistas(
                idContrato=id_nuevo_contrato,
                idContratista=idContratista
            )
            db.session.add(newContratos_Contratistas)
            db.session.commit()
            
            data = jsonify({"status": True, "id_nuevo_contrato": id_nuevo_contrato})
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    