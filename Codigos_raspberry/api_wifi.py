"""
API Flask para gestionar WiFi del Raspberry Pi
Endpoints para escanear, conectar y obtener estado de redes WiFi
"""

from flask import Flask, jsonify, request
from services.wifi_service import WifiService
import threading

app = Flask(__name__)
wifi_service = WifiService()


@app.route('/api/wifi/scan', methods=['GET'])
def scan_redes():
    """Escanea redes WiFi disponibles"""
    try:
        redes = wifi_service.escanear_redes()
        return jsonify(redes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/wifi/connect', methods=['POST'])
def conectar_red():
    """Conecta a una red WiFi"""
    try:
        datos = request.get_json()
        ssid = datos.get('ssid')
        password = datos.get('password')
        
        if not ssid or not password:
            return jsonify({'success': False, 'error': 'SSID y contraseña requeridos'}), 400
        
        resultado = wifi_service.conectar_wifi(ssid, password)
        
        return jsonify({'success': resultado}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/wifi/current', methods=['GET'])
def obtener_red_actual():
    """Obtiene la red WiFi actual"""
    try:
        config = wifi_service.obtener_configuracion_actual()
        return jsonify(config), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/wifi/disconnect', methods=['POST'])
def desconectar():
    """Desconecta la red WiFi actual"""
    try:
        resultado = wifi_service.desconectar_wifi()
        return jsonify({'success': resultado}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def iniciar_servidor(puerto=5000):
    """Inicia el servidor Flask"""
    app.run(host='0.0.0.0', port=puerto, debug=False)


if __name__ == '__main__':
    iniciar_servidor()
