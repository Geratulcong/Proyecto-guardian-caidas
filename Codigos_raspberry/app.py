from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from uuid import uuid4
import os
from database.usuario.usuario_db import UsuarioDB
from database.usuario.contacto_db import ContactoDB
from database.dispositivos.raspberry_db import RaspberryDB

# Configurar rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_FOLDER = os.path.join(BASE_DIR, 'Pagina App de emergencia')

app = Flask(__name__, static_folder=WEB_FOLDER, static_url_path='')
CORS(app)

usuario_db = UsuarioDB()
contacto_db = ContactoDB()
raspberry_db = RaspberryDB()

# Configuración del servidor
SERVER_IP = os.getenv('SERVER_IP', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))


@app.route('/api/usuarios/verificar-o-crear', methods=['POST'])
def verificar_o_crear_usuario():
    """
    Verifica si un usuario existe por correo.
    Si no existe, lo crea con los datos de Google.
    Retorna el usuario_id.
    """
    try:
        datos = request.json
        
        if not datos or 'email' not in datos:
            return jsonify({'error': 'Email es requerido'}), 400
        
        email = datos.get('email')
        nombre = datos.get('nombre', 'Usuario')
        
        # Obtener todos los usuarios
        usuarios = usuario_db.obtener_usuarios()
        
        # Buscar si el email ya existe
        usuario_existente = None
        for usuario in usuarios:
            if usuario[2] == email:  # usuario_email está en posición 2
                usuario_existente = usuario
                break
        
        if usuario_existente:
            # El usuario ya existe
            return jsonify({
                'usuario_id': str(usuario_existente[0]),
                'estado': 'existente',
                'mensaje': 'Usuario ya existe'
            }), 200
        
        # Crear nuevo usuario
        usuario_id = str(uuid4())
        usuario_db.registrar_usuario(
            usuario_id=usuario_id,
            usuario_nombre=nombre,
            usuario_email=email,
            usuario_telefono='',
            usuario_activo=True,
            usuario_familiar_nombre='',
            usuario_familiar_telefono=''
        )
        
        return jsonify({
            'usuario_id': usuario_id,
            'estado': 'creado',
            'mensaje': 'Usuario creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/usuarios/<usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """
    Obtiene los datos de un usuario específico.
    """
    try:
        usuarios = usuario_db.obtener_usuarios()
        
        for usuario in usuarios:
            if str(usuario[0]) == usuario_id:
                return jsonify({
                    'usuario_id': str(usuario[0]),
                    'nombre': usuario[1],
                    'email': usuario[2],
                    'telefono': usuario[3],
                    'activo': usuario[4],
                    'familiar_nombre': usuario[5],
                    'familiar_telefono': usuario[6]
                }), 200
        
        return jsonify({'error': 'Usuario no encontrado'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/usuarios/<usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    """
    Actualiza los datos de un usuario.
    Puede actualizar: nombre, teléfono,familiar_nombre, familiar_telefono
    """
    try:
        datos = request.json
        
        # Obtener usuario actual
        usuarios = usuario_db.obtener_usuarios()
        usuario = None
        for u in usuarios:
            if str(u[0]) == usuario_id:
                usuario = u
                break
        
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar con los datos proporcionados
        nombre = datos.get('nombre')
        telefono = datos.get('telefono')
        familiar_nombre = datos.get('familiar_nombre')
        familiar_telefono = datos.get('familiar_telefono')
        
        # Usar el nuevo método de actualización múltiple
        usuario_db.actualizar_usuario(
            usuario_id=usuario_id,
            nombre=nombre,
            telefono=telefono,
            familiar_nombre=familiar_nombre,
            familiar_telefono=familiar_telefono
        )
        
        return jsonify({
            'mensaje': 'Usuario actualizado correctamente',
            'usuario_id': usuario_id,
            'datos_actualizados': {
                'nombre': nombre,
                'telefono': telefono,
                'familiar_nombre': familiar_nombre,
                'familiar_telefono': familiar_telefono
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ================ ENDPOINTS DE CONTACTOS ================

@app.route('/api/usuarios/<usuario_id>/contactos', methods=['GET'])
def obtener_contactos_usuario(usuario_id):
    """
    Obtiene todos los contactos de un usuario.
    """
    try:
        contactos = contacto_db.obtener_contactos_usuario(usuario_id)
        
        contactos_lista = []
        for c in contactos:
            contactos_lista.append({
                'contacto_id': str(c[0]),
                'usuario_id': str(c[1]),
                'nombre': c[2],
                'telefono': c[3],
                'estado': c[4]
            })
        
        return jsonify({
            'contactos': contactos_lista,
            'total': len(contactos_lista)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/usuarios/<usuario_id>/contactos', methods=['POST'])
def crear_contacto(usuario_id):
    """
    Crea un nuevo contacto de emergencia para un usuario.
    """
    try:
        datos = request.json
        
        if not datos or 'nombre' not in datos or 'telefono' not in datos:
            return jsonify({'error': 'nombre y telefono son requeridos'}), 400
        
        contacto_id = str(uuid4())
        
        contacto_db.guardar_contacto(
            contacto_id=contacto_id,
            usuario_id=usuario_id,
            contacto_nombre=datos['nombre'],
            contacto_telefono=datos['telefono'],
            contacto_estado=datos.get('estado', True)
        )
        
        return jsonify({
            'contacto_id': contacto_id,
            'mensaje': 'Contacto creado exitosamente'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contactos/<contacto_id>', methods=['PUT'])
def actualizar_contacto(contacto_id):
    """
    Actualiza un contacto de emergencia.
    """
    try:
        datos = request.json
        
        contacto_db.actualizar_contacto(
            contacto_id=contacto_id,
            contacto_nombre=datos.get('nombre'),
            contacto_telefono=datos.get('telefono'),
            contacto_estado=datos.get('estado')
        )
        
        return jsonify({
            'mensaje': 'Contacto actualizado correctamente',
            'contacto_id': contacto_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/contactos/<contacto_id>', methods=['DELETE'])
def eliminar_contacto(contacto_id):
    """
    Elimina un contacto de emergencia.
    """
    try:
        contacto_db.eliminar_contacto(contacto_id)
        
        return jsonify({
            'mensaje': 'Contacto eliminado correctamente',
            'contacto_id': contacto_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/raspberry/vincular', methods=['POST'])
def vincular_raspberry():
    datos = request.json

    usuario_id = datos.get("usuario_id")
    raspberry_id = datos.get("raspberry_id")

    raspberry_db.vincular_usuario(raspberry_id, usuario_id)
 
    return jsonify({
        "mensaje": "Raspberry vinculada correctamente",
        "raspberry_id": raspberry_id,
        "usuario_id": usuario_id
    }), 200


# ================ ENDPOINTS ESTÁTICOS ================

@app.route('/api/health', methods=['GET'])
def health():
    """
    Endpoint para verificar que el servidor está activo.
    """
    return jsonify({'status': 'ok'}), 200


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static(path):
    """
    Sirve archivos estáticos de la carpeta web.
    Si el archivo no existe o es una carpeta, sirve index.html
    """
    # Construir la ruta del archivo
    file_path = os.path.join(WEB_FOLDER, path)
    
    # Si es un archivo que existe, servirlo
    if os.path.isfile(file_path):
        return send_from_directory(WEB_FOLDER, path)
    
    # Si no existe, servir index.html
    if os.path.isfile(os.path.join(WEB_FOLDER, 'index.html')):
        return send_from_directory(WEB_FOLDER, 'index.html')
    
    return jsonify({'error': 'Archivo no encontrado'}), 404


if __name__ == '__main__':
    app.run(host=SERVER_IP, port=SERVER_PORT, debug=True)
