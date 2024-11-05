from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_cors import CORS
import clases.sign_up
from config import DevelopmentConfig
from io import BytesIO
from models import db, Empresas

import models, locale, base64, os
from werkzeug.security import generate_password_hash, check_password_hash

import matplotlib.pyplot as ptl
import numpy as np

import clases
from clases.sign_up import Sign_up
from clases.class_sign_in import Sign_in

from clases.class_contratos import class_editar_contrato, class_crear_contrato, class_eliminar_contrato, class_listar_contratos, class_get_contrato
from clases.class_contratistas import class_getContratistas, class_createContratistas,class_deleteContratistas,class_editContratistas, class_getContratista
from clases.class_empresa import class_getEmpresa, class_listarEmpresas , class_crearEmpresa, class_deleteEmpresa, class_editEmpresa


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
app.config.from_object(DevelopmentConfig)
locale.setlocale(locale.LC_TIME, 'es_ES')

#DECORADORES O RUTAS
@app.route('/api', methods=['GET'])
def get_data():
    data = {"message": "Bienvenido a SIGN SYNC API!"}
    return data

@app.route('/api/sign-up', methods=['POST'])
def register_usuario():
    try:
        datos = request.get_json() #Recuperar DATA
        sign_up = Sign_up()
        data = sign_up.RegistrarUser(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error 

@app.route('/api/sign-in', methods=['POST'])
def login():
    try:
        datos = request.get_json() #Recuperar DATA
        sign_in = Sign_in()
        data = sign_in.loginUser(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    

    
#///////////////////////////EMPRESA
@app.route('/api/empresa/getempresa', methods=['GET'])
def get_Empresa():
    try:
        id_usuario = request.args.get('id_usuario')
        get_empresa = class_getEmpresa.Get_Empresa()
        data = get_empresa.Get(id_usuario)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/empresa/listarempresas', methods=['GET'])
def listar_Empresas():
    try:
        obj_empresa = class_listarEmpresas.Listar_Empresas()
        data = obj_empresa.Get()
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/empresa/createempresa', methods=['POST'])
def create_Empresa():
    try:
        datos = request.get_json() #Recuperar DATA
        
        creat_empresa = class_crearEmpresa.Crear_Empresa()
        data = creat_empresa.Crear(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/empresa/eliminarEmpresa', methods=['DELETE'])
def delete_Empresa():
    try:
        datos = request.get_json() #Recuperar DATA
        
        delete_empresa = class_deleteEmpresa.Delete_Empresa()
        data = delete_empresa.delete(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error    
    
@app.route('/api/empresa/editarEmpresa', methods=['PUT'])
def editar_Empresa():
    try:
        datos = request.get_json() #Recuperar DATA
        
        edit_empresa = class_editEmpresa.Edit_Empresa()
        data = edit_empresa.Edit(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error 

##CONTRATISTAS

@app.route('/api/contratistas/listarcontratistas', methods=['GET'])
def listar_contratistas():
    try:
        idEmpresa = request.args.get('idEmpresa')
        id_usuario = request.args.get('id_usuario')
            
        if not idEmpresa:
            if not id_usuario:
                return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
            empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
            idEmpresa = empresa.idEmpresa
            
        print(idEmpresa)
        get_contratistas = class_getContratistas.Get_Contratistas()
        data = get_contratistas.Get(idEmpresa)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    
@app.route('/api/contratistas/getcontratista', methods=['GET'])
def get_contratistas():
    try:
        idContratista = request.args.get('idContratista')
            
        print(idContratista)
        obj_contratistas = class_getContratista.Get_Contratista()
        data = obj_contratistas.Get(idContratista)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/contratistas/crearcontratistas', methods=['POST'])
def crear_contratistas():
    try:
        datos = request.get_json() #Recuperar DATA
        obj_contratistas = class_createContratistas.Create_Contratistas()
        data = obj_contratistas.Create(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/contratistas/editarcontratistas', methods=['PUT'])
def editar_contratistas():
    try:
        datos = request.get_json() #Recuperar DATA
        obj_contratistas = class_editContratistas.Edit_Contratistas()
        data = obj_contratistas.Edit(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/contratistas/eliminarcontratista', methods=['DELETE'])
def eliminar_contratistas():
    try:
        datos = request.get_json() #Recuperar DATA
        obj_contratistas = class_deleteContratistas.Delete_Contratistas()
        data = obj_contratistas.delete(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error



#////////////////////////////////CONTRATOS
@app.route('/api/contratos/listarcontratos', methods=['GET'])
def listar_contratos():
    try:
        idEmpresa = request.args.get('idEmpresa')
        id_usuario = request.args.get('id_usuario')
        
        if not idEmpresa:
            if not id_usuario:
                return jsonify({"status": False, "message": "No se ha enviado el ID de la empresa (idEmpresa) ni ID del usuario (id_usuario)"}), 400
            empresa = Empresas.query.filter_by(id_usuario=id_usuario).first()
            if not empresa:
                return jsonify({"status": False, "message": "No se ha encontrado la empresa para el ID del usuario"}), 404
            idEmpresa = empresa.idEmpresa
        
        listar_contrato = class_listar_contratos.Listar_Contrato()
        data = listar_contrato.Listar(idEmpresa)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/contratos/getcontrato', methods=['GET'])
def get_contrato():
    try:
        idContrato = request.args.get('idContrato')
        listar_contrato = class_get_contrato.Get_Contrato()
        data = listar_contrato.Get(idContrato)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/contratos/deletecontrato', methods=['DELETE'])
def eliminar_contrato():
    try:
        datos = request.get_json()
        obj_eliminar_contrato = class_eliminar_contrato.Eliminar_Contrato()
        data = obj_eliminar_contrato.EliminarContrato(datos)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/contratos/editcontrato', methods=['PUT'])
def editar_contrato():
    try:
        datos = request.get_json() #Recuperar DATA
        editar_contract = class_editar_contrato.Editar_Contrato()
        data = editar_contract.Editar(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/contratos/crearcontrato', methods=['POST'])
def crear_contrato():
    try:
        datos = request.get_json()
        obj_crear_contrato = class_crear_contrato.Crear_Contrato()
        data = obj_crear_contrato.def_crear_contrato(datos)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error







if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


