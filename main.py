from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_cors import CORS
import clases.sign_up
from config import DevelopmentConfig
from io import BytesIO
from models import db

import models, locale, base64, os
from werkzeug.security import generate_password_hash, check_password_hash

import matplotlib.pyplot as ptl
import numpy as np

import clases
from clases.sign_up import Sign_up
from clases.class_sign_in import Sign_in

from clases.class_contratos import class_editar_contrato, class_crear_contrato, class_eliminar_contrato, class_listar_contratos  
from clases.class_contratistas import class_getContratisas
from clases.class_empresa import class_getEmpresa


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
    

    
#EMPRESA
@app.route('/api/empresa/getempresa', methods=['POST'])
def get_Empresa():
    try:
        datos = request.get_json() #Recuperar DATA
        
        print(datos)
        get_empresa = class_getEmpresa.Get_Empresa()
        data = get_empresa.Get(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
##CONTRATISTAS

@app.route('/api/contratistas/getcontratistas', methods=['POST'])
def get_contratistas():
    try:
        datos = request.get_json() #Recuperar DATA
        get_contratistas = class_getContratisas.Get_Contratistas()
        data = get_contratistas.Get(datos)
        
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/editar-contrato', methods=['POST'])
def editar_contrato():
    try:
        datos = request.get_json() #Recuperar DATA
        listar_contrato = class_listar_contratos.Listar_Contrato()
        data = listar_contrato.Listar(datos)
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    return jsonify(data)







if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


