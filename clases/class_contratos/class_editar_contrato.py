from flask import jsonify
import models
from models import db

from models import Contratos, ContratosContratistas, Empresas, Contratistas


###############################PENDIENTE
class Editar_Contrato:
    
    #DeclaraciÃ³n de contructor de la clase
    def __init__(self) -> None:
        self.usuario = ''
        self.correo = ''
        self.contrasena= ''
    
    '''
    @param datos
        idContrato
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
            status, message
    '''
    
    def EditarContrato(self, datos):
        try:
            nombre = datos['nombre']
            tipo = datos['tipo']
            lugar=datos['lugar']
            fecha_inicio = datos['fecha_inicio']
            fecha_entrega = datos['fecha_entrega']
            color = datos['color']
            idEmpresa = datos['idEmpresa']
            id_usuario = datos['id_usuario']
            id_contrato = datos['id_contrato']
            idContratista = datos['idContratista']
            
            if not id_contrato: 
                return jsonify({"status": False, "message": "No se ha enviado el ID del contrato (id_contrato)"}), 400
            
            if not idContratista: 
                return jsonify({"status": False, "message": "No se ha enviado el ID del contratista (idContratista)"}), 400
            
            if not idEmpresa:
                if not id_usuario:
                    return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
                empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
                if not empresa:
                    return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
                idEmpresa = empresa.idEmpresa
            
            contrato = Contratos.query.filter_by(idContrato=id_contrato).first()
            if not contrato:
                return jsonify({"status": False, "message": f"No se ha encontrado un contrato el ID: {id_contrato}" }), 400

            contrato.nombre = nombre if nombre else contrato.nombre
            contrato.tipo = tipo if tipo else contrato.tipo
            contrato.lugar = lugar if lugar else contrato.lugar
            contrato.color = color if color else contrato.color
            contrato.fecha_inicio = fecha_inicio if fecha_inicio else contrato.fecha_inicio
            contrato.fecha_entrega = fecha_entrega if fecha_entrega else contrato.fecha_entrega
            relacion = ContratosContratistas.query.filter_by(idContrato=id_contrato).first()
            if relacion:
                relacion.idContratista = idContratista
            else:
                nueva_relacion = ContratosContratistas(idContrato=id_contrato, idContratista=idContratista)
                db.session.add(nueva_relacion)
                
            db.session.commit()

            data = jsonify({"status": True, "message": "Contrato editado correctamente"})
            
            return data
            
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500  # Devolver el error
    
    