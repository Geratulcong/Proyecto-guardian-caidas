from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from uuid import uuid4
import os
from database.usuario.usuario_db import UsuarioDB
from database.dispositivos.raspberry_db import RaspberryDB

# Configurar rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_FOLDER = os.path.join(BASE_DIR, 'Pagina App de emergencia')

app = Flask(__name__, static_folder=WEB_FOLDER, static_url_path='')
CORS(app)

usuario_db = UsuarioDB()
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
    """
    try:
        datos = request.json
        
        if 'telefono' in datos:
            usuario_db.actualizar_telefono(usuario_id, datos['telefono'])
        
        return jsonify({
            'mensaje': 'Usuario actualizado correctamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
