from flask import Flask, request, jsonify
from flask_cors import CORS
from config import DevelopmentConfig
from models import db, Empresas
from sqlalchemy import create_engine, text
from sqlalchemy.sql import func
import pandas as pd
from models import Contratistas, Contratos, ContratosContratistas, Paquetes, Usuario, Empresas, Documentos

import locale, os
from datetime import date, timedelta, datetime

from clases.sign_up import Sign_up
from clases.class_sign_in import Sign_in

from clases.class_contratos import class_editar_contrato, class_crear_contrato, class_eliminar_contrato, class_listar_contratos, class_get_contrato, class_listar_contratos_ALL
from clases.class_contratistas import class_getContratistas, class_createContratistas,class_deleteContratistas,class_editContratistas, class_getContratista, class_listarContratistas
from clases.class_empresa import class_getEmpresa, class_listarEmpresas , class_crearEmpresa, class_deleteEmpresa, class_editEmpresa
from clases.class_paquetes import class_crearPaquete, class_listarPaquetes, class_editarPaquete, class_eliminarPaquete, class_listarPaquetes_all, class_getPaquete

from clases.class_servicios import class_crearServicio, class_editarServicio, class_eliminarServicio, class_listarServicios
from clases.class_documentos import class_crearDocumento, class_editarDocumento, class_listarDocumento, class_eliminarDocumento, class_listarDocumentos_All, class_getDocumento
from clases.class_graficas import routes

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
GRAFICAS_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GRAFICAS_FOLDER'] = GRAFICAS_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        idEmpresa = request.args.get('idEmpresa')
        
        if not idEmpresa: 
            idEmpresa = request.args.get('id_empresa')
        
        get_empresa = class_getEmpresa.Get_Empresa()
        data = get_empresa.Get(id_usuario, idEmpresa)
        
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
            idEmpresa = request.args.get('id_empresa')
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
    
@app.route('/api/contratistas/listarcontratistas-all', methods=['GET'])
def listar_contratistas_ALL():
    try:
        obj = class_listarContratistas.Listar_Contratistas()
        data = obj.Listar()
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    
    
@app.route('/api/contratistas/getcontratista', methods=['GET'])
def get_contratistas():
    try:
        idContratista = request.args.get('idContratista')
        
        if not idContratista:
            idContratista = request.args.get('id_contratista')
            
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
            idEmpresa = request.args.get('id_empresa')
        
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
    
@app.route('/api/contratos/getcontratosALL', methods=['GET'])
def listar_contratos_ALL():
    try:
        obj = class_listar_contratos_ALL.Listar_Contratos_ALL()
        data = obj.Listar()
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


#PAQUETES
@app.route('/api/paquetes/paquete', methods=['POST'])
def crear_paquete():
    try:
        datos = request.get_json()
        obj_crear = class_crearPaquete.Crear_Paquete()
        data = obj_crear.Crear(datos)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/paquetes/paquete', methods=['PUT'])
def editar_paquete():
    try:
        datos = request.get_json()
        editar= class_editarPaquete.Editar_Paquete()
        data = editar.Editar(datos)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/paquetes/paquete', methods=['GET'])
def get_paquete():
    try:
        idPaquete = request.args.get('idPaquete')
        listar = class_getPaquete.Get_Paquete()
        data = listar.Get(idPaquete)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/paquetes/paquetescontrato', methods=['GET'])
def listar_paquete_contrato():
    try:
        idContrato = request.args.get('idContrato')
        if not idContrato:
            idContrato = request.args.get('id_contrato')
        listar = class_listarPaquetes.Listar_Paquete()
        data = listar.Listar(idContrato)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/paquetes/listarpaquetes', methods=['GET'])
def listar_paquetes():
    try:
        listar = class_listarPaquetes_all.Listar_Paquete()
        data = listar.Listar()
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/paquetes/paquete', methods=['DELETE'])
def eliminar_paquete():
    try:
        datos = request.get_json()
        eliminar = class_eliminarPaquete.Eliminar_Paquete()
        data = eliminar.Eliminar(datos)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
# ///////////////////////////SERVICIOS
@app.route('/api/servicios/servicio', methods=['POST'])
def crear_servicio():
    try:
        datos = request.get_json()
        obj_crear = class_crearServicio.Crear_Servicio()
        data = obj_crear.Crear(datos)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    
@app.route('/api/servicios/servicio', methods=['PUT'])
def editar_servicio():
    try:
        datos = request.get_json()
        editar= class_editarServicio.Editar_Servicio()
        data = editar.Editar(datos)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/servicios/servicio', methods=['GET'])
def listar_servicio():
    try:
        idPaquete = request.args.get('idPaquete')
        listar = class_listarServicios.Listar_Servicios()
        data = listar.Listar(idPaquete)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/servicios/servicios', methods=['DELETE'])
def eliminar_servicio():
    try:
        datos = request.get_json()
        eliminar = class_eliminarServicio.Eliminar_Servicio()
        data = eliminar.Eliminar(datos)
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

# //////////////////////DOCUMENTOS



@app.route('/api/documentos/creardocumento', methods=['POST'])
def registrar_documento():
    try:
        # datos = request.get_json()
        nombre = request.form.get('nombre')
        id_contrato = request.form.get('idContrato')

        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": False, 'message': 'No selected file'}), 400
        
        if file:
            # Guardar archivo en la carpeta de uploads
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        
        obj_crear = class_crearDocumento.Crear_Documento()
        data = obj_crear.Crear(nombre, id_contrato, file_path)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    
@app.route('/api/documentos/editardocumento', methods=['PUT'])
def editar_documento():
    try:
        idDocumento = request.form.get('idDocumento')
        nombre = request.form.get('nombre')
        id_contrato = request.form.get('idContrato')
        
        if not idDocumento or not nombre or not id_contrato:
            return jsonify({"status": False, "message": "Datos incompletos"}), 400

        file_path = None
        file = request.files.get('file')  # Usa get para evitar errores si no existe
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
        print(file_path)
        
        editar= class_editarDocumento.Editar_Documento()
        data = editar.Editar(idDocumento, nombre, id_contrato, file_path)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/documentos/listardocumentos', methods=['GET'])
def listar_documentos():
    try:
        idContrato = request.args.get('idContrato')
        listar = class_listarDocumento.Listar_Documentos()
        data = listar.Listar(idContrato)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/documentos/getdocumento', methods=['GET'])
def get_documento():
    try:
        idDocumento = request.args.get('idDocumento')
        listar = class_getDocumento.Get_Documentos()
        data = listar.Get(idDocumento)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/documentos/listardocumentosall', methods=['GET'])
def listar_documentos_all():
    try:
        listar = class_listarDocumentos_All.Listar_Documentos()
        data = listar.Listar()
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error

@app.route('/api/documentos/deletedocumento', methods=['DELETE'])
def eliminar_documento():
    try:
        datos = request.get_json()
        eliminar = class_eliminarDocumento.Eliminar_Documento()
        data = eliminar.Eliminar(datos)
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error


#/////////////////////////GRAFICAS
@app.route('/api/graficos', methods=['GET'])
def dashboard():
    try:
        grafico = request.args.get('grafico')
        tabla = request.args.get('tabla')
        grafica = routes.Recuperar_Grafica()
        print(grafico)
        data = grafica.dashboard(grafico, tabla)
        return data
        
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
@app.route('/api/graficos/update', methods=['POST'])
def importar_csv():
    tabla = request.form.get('tabla')
    if not tabla:
        return jsonify({"status": False, 'message': 'Faltan datos obligatorios (tabla)'}), 400
    
    archivo = request.files['file']
    if archivo.filename == '':
        return jsonify({"status": False, 'message': 'No se ha enviado el archivo (file)'}), 400
        
    model_mapping = {
        'grafico_aceptabilidad': 'aceptabilidad',
        'grafico_crecimiento': 'crecimiento',
        'grafico_funcionabilidad': 'funcionalidad',
        'grafico_rentabilidad': 'rentabilidad',
        'grafico_satisfaccion': 'satisfaccion',
        'grafico_viabilidad':'viabilidad'
    }
    
    model = model_mapping.get(tabla.lower())
    if archivo:
        archivo_path = os.path.join(app.config['GRAFICAS_FOLDER'], archivo.filename)
        archivo.save(archivo_path)
            
        engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, echo=True)
        connection = engine.connect()
        transaction = connection.begin()
             # Paso 1: Eliminar la tabla si existe
        try:
            filepath = f"json/{model}.json"
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"Archivo '{model}.json' eliminado exitosamente.")
            else:
                print(f"El archivo '{model}.json' no existe.")

            connection.execute(text(f"DROP TABLE IF EXISTS {tabla}"))
            archivo_csv = pd.read_csv(archivo_path)
            archivo_csv.to_sql(name=tabla, con=connection, if_exists='fail')

            transaction.commit()
            return jsonify({"status": True, "message": "Grafica actualizada correctamente"}), 201
        except Exception as e:
            db.session.rollback()  # Hacer rollback si ocurre un error
            return jsonify({"error": str(e)}), 500 #vierte la transacción en caso de error
            
        finally:
            connection.close()  # Cierra la conexión


    
#/////////////// PERFIL
from clases.class_perfil import class_changepassword, class_editperfil, class_listarUsers, class_deleteUser, class_getUser, class_crearUsuario

@app.route('/api/perfil/createUser', methods=['POST'])
def create_user():
    try:
        datos = request.get_json()
        obj = class_crearUsuario.Create_User()
        data = obj.Create(datos)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500

@app.route('/api/perfil/editar', methods=['PUT'])
def editar_perfil():
    try:
        datos = request.get_json()
        editar= class_editperfil.Edit_Perfil()
        data = editar.Edit(datos)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/perfil/cambiarpassword', methods=['PUT'])
def cambiar_password():
    try:
        datos = request.get_json()
        editar= class_changepassword.Cambiar_Contrasena()
        data = editar.Change(datos)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500

@app.route('/api/perfil/listar', methods=['GET'])
def listar_usuarios():
    try:
        obj = class_listarUsers.Listar_Usuarios()
        data = obj.Listar()
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/perfil/getuser', methods=['GET'])
def get_usuario():
    try:
        id_user = request.args.get('id_user')
        obj = class_getUser.Get_Usuarios()
        data = obj.Get(id_user)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/api/perfil/deleteuser', methods=['DELETE'])
def delete_usuarios():
    try:
        data = request.get_json()
        id_user = data.get('id_user')
        print(id_user)
        obj = class_deleteUser.Delete_Usuarios()
        data = obj.Detele(id_user)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500


#/////////////////////////////BASE DE DATOS --- DEV
from clases.class_bd import class_listarTablas


@app.route('/api/bd/listartablas', methods=['GET'])
def listar_tablas():
    try:
        obj = class_listarTablas.Listar_Tablas()
        data = obj.Listar()
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500


#PROCESOS

from clases.class_procesos import class_proceso_uno, class_proceso_dos

@app.route('/api/contratos/contratocostos', methods=['GET'])
def contratos_costos():
    try:
        idContratista = request.args.get('idContratista')
        if not idContratista:
            idContratista = request.args.get('id_contratista')
        
        # print(idContratista)
        obj = class_proceso_uno.Listar_Contratos()
        data = obj.Listar(idContratista)
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics/registrosdiarios', methods=['GET'])
def registros_diarios():
    try:
        obj = class_proceso_dos.registros_diarios()
        data = obj.Listar()
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics/distribucion-sexo', methods=['GET'])
def distribucion_sexo():
    try:
        results = db.session.query(
            Usuario.sexo, 
            func.count(Usuario.id_user).label('total')
        ).group_by(Usuario.sexo).all()
        
        metrics = [{'sexo': row.sexo, 'total': row.total} for row in results]
        data = jsonify({"status": True, "metricas": metrics}), 201
        
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500


@app.route('/api/metrics/edad-promedio', methods=['GET'])
def edad_promedio():
    try:
        cumpleanos = db.session.query(Usuario.fecha_nacimiento).filter(Usuario.fecha_nacimiento != None).all()
        
        today = date.today()
        ages = [
            (today.year - bd[0].year) - ((today.month, today.day) < (bd[0].month, bd[0].day))
            for bd in cumpleanos
        ]
        
        avg_age = sum(ages) / len(ages) if ages else None
        data = jsonify({'edad_promedio': round(avg_age, 2) if avg_age else None}), 201
        
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500

@app.route('/api/metrics/timeregistros', methods=['GET'])
def usuarios_recientes():
    try:    
        cutoff_date = datetime.now() - timedelta(days=30)
        usuarios_recientes = db.session.query(
            func.count(Usuario.id_user)
        ).filter(Usuario.created_date >= cutoff_date).scalar()
        
        # metrics = [{'sexo': row.sexo, 'total': row.total} for row in results]
        data = jsonify({'usuarios_recientes': usuarios_recientes}), 201
        
        return data
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500



    
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


