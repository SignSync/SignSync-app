from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_cors import CORS
from config import DevelopmentConfig
from io import BytesIO
from models import db

import models, locale, base64, os
from werkzeug.security import generate_password_hash, check_password_hash

import matplotlib.pyplot as ptl
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})
app.config.from_object(DevelopmentConfig)
locale.setlocale(locale.LC_TIME, 'es_ES')

#DECORADORES O RUTAS
@app.route('/api', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/sign-up', methods=['POST'])
def register_user():
    try:
        datos = request.get_json() #Recuperar DATA
        #CHECA SI HAY DATOS 
        if not datos or 'usuario' not in datos or 'correo' not in datos or 'contrasena' not in datos:
            return jsonify({"error": "Faltan datos"}), 400
        
        
        usuario = datos['usuario']
        correo = datos['correo']
        contrasena = datos['contrasena']
        
        hashed_password = generate_password_hash(contrasena)
        newUser = models.Usuario(usuario = usuario, correo = correo, contrasena=hashed_password)
        
        db.session.add(newUser)
        db.session.commit()
        id_nuevo_user = newUser.id_user
        
        data = {"message": "Usuario registrado correctamente", "id": id_nuevo_user}
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    return jsonify(data)

@app.route('/api/sign-in', methods=['POST'])
def login_user():
    try:
        datos = request.get_json() #Recuperar DATA
        #CHECA SI HAY DATOS 
        if 'correo' not in datos or 'contrasena' not in datos:
            return jsonify({"error": "Faltan datos"}), 400
        
        correo = datos['correo']
        contrasena = datos['contrasena']
        
        user = models.Usuario.query.filter_by(correo=correo).first()
        print(user)
        if user:
            if check_password_hash(user.contrasena, contrasena):
                session['user_id'] = user.id_user
                session['user_name'] = user.usuario
                session['user_email'] = user.correo
                data = {"message": "Login correctamente ", 'correo':user.correo}
            else:
                #message_error = 'Contraseña o correo electronico no validos'
                data = {"message": "Contraseña o correo electornico no validos."}
        else:
            #message_error = 'Correo electronico no registrado'
            data = {"message": "Correo electronico no registrado"}
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    return jsonify(data)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


