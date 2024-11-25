from flask import Flask, request, jsonify
from flask_cors import CORS
from config import DevelopmentConfig
from models import db, Empresas

import locale

from clases.sign_up import Sign_up
from clases.class_sign_in import Sign_in

from clases.class_contratos import class_editar_contrato, class_crear_contrato, class_eliminar_contrato, class_listar_contratos, class_get_contrato, class_listar_contratos_ALL
from clases.class_contratistas import class_getContratistas, class_createContratistas,class_deleteContratistas,class_editContratistas, class_getContratista
from clases.class_empresa import class_getEmpresa, class_listarEmpresas , class_crearEmpresa, class_deleteEmpresa, class_editEmpresa
from clases.class_paquetes import class_crearPaquete, class_listarPaquetes, class_editarPaquete, class_eliminarPaquete

from clases.class_servicios import class_crearServicio, class_editarServicio, class_eliminarServicio, class_listarServicios
from clases.class_documentos import class_crearDocumento, class_editarDocumento, class_listarDocumento, class_eliminarDocumento
from clases.class_graficas import routes

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
        idEmpresa = request.args.get('idEmpresa')
        
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
        data = obj_crear.def_crear_contrato(datos)
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
def listar_paquete():
    try:
        idContrato = request.args.get('idContrato')
        listar = class_listarPaquetes.Listar_Paquete()
        data = listar.Listar(idContrato)
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
        datos = request.get_json()
        obj_crear = class_crearDocumento.Crear_Documento()
        data = obj_crear.Crear(datos)
        return data
    
    except Exception as e:
        db.session.rollback()  # Hacer rollback si ocurre un error
        return jsonify({"error": str(e)}), 500  # Devolver el error
    
    
@app.route('/api/documentos/editardocumento', methods=['PUT'])
def editar_documento():
    try:
        datos = request.get_json()
        editar= class_editarDocumento.Editar_Documento()
        data = editar.Editar(datos)
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



# class Servicios(db.Model):
#     __tablename__ = 'Servicios'
#     idServicio = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(50), nullable=False)
#     idPaquete = db.Column(db.Integer, db.ForeignKey('Paquetes.idPaquete'), nullable=False)
#     # servicio_paquete = db.relationship('Paquetes', backref='serivicio', cascade="all, delete-orphan")

    
# class Documentos(db.Model):
#     __tablename__ = 'Documentos'
#     idDocumento = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(50), nullable=False)
    
#     idContrato = db.Column(db.Integer, db.ForeignKey('Contratos.idContrato'), nullable=False)





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






    
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)


