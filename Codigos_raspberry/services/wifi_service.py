import subprocess
import re
from typing import List, Dict


class WifiService:
    """Servicio para gestionar conexiones WiFi en el Raspberry Pi"""

    def escanear_redes(self) -> List[Dict]:
        """Escanea redes WiFi disponibles"""
        try:
            output = subprocess.run(
                ['sudo', 'iwlist', 'wlan0', 'scan'],
                capture_output=True,
                text=True,
                timeout=15
            )
            
            redes = self._parsear_escaneo(output.stdout)
            return redes
        
        except Exception as e:
            print(f"Error escaneando redes: {e}")
            return []

    def _parsear_escaneo(self, output: str) -> List[Dict]:
        """Parsea salida de iwlist scan"""
        redes = []
        current_net = {}
        
        for line in output.split('\n'):
            line = line.strip()
            
            if 'ESSID' in line:
                essid = re.search(r'ESSID:"([^"]*)"', line)
                if essid:
                    current_net['ssid'] = essid.group(1)
            
            if 'Signal level' in line:
                signal = re.search(r'Signal level[=:](\S+)', line)
                if signal:
                    current_net['signal'] = signal.group(1)
                    if current_net.get('ssid'):
                        redes.append(current_net)
                    current_net = {}
        
        return redes

    def conectar_wifi(self, ssid: str, password: str) -> bool:
        """Conecta a una red WiFi especificada"""
        try:
            # Generar configuración wpa_supplicant
            config = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={{
    ssid="{ssid}"
    psk="{password}"
    key_mgmt=WPA-PSK
}}
"""
            
            # Guardar configuración
            config_path = '/etc/wpa_supplicant/wpa_supplicant.conf'
            with open(config_path, 'w') as f:
                f.write(config)
            
            # Permisos correctos
            subprocess.run(['sudo', 'chmod', '600', config_path], timeout=5)
            
            # Reiniciar wpa_supplicant
            subprocess.run(
                ['sudo', 'systemctl', 'restart', 'wpa_supplicant'],
                timeout=10
            )
            
            # Esperar conexión
            import time
            time.sleep(5)
            
            # Verificar
            if self._verificar_conexion():
                print(f"WiFi conectado: {ssid}")
                return True
            else:
                print(f"No se pudo conectar a {ssid}")
                return False
        
        except Exception as e:
            print(f"Error conectando WiFi: {e}")
            return False

    def _verificar_conexion(self) -> bool:
        """Verifica si hay conexión a internet"""
        try:
            result = subprocess.run(
                ['ping', '-c', '1', '8.8.8.8'],
                timeout=5,
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False

    def obtener_configuracion_actual(self) -> Dict:
        """Obtiene configuración WiFi actual"""
        try:
            output = subprocess.run(
                ['iwconfig', 'wlan0'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            config = {'ssid': 'No conectado', 'signal': '-'}
            
            for line in output.stdout.split('\n'):
                if 'ESSID' in line:
                    essid = re.search(r'ESSID:"([^"]*)"', line)
                    if essid:
                        config['ssid'] = essid.group(1)
                
                if 'Signal level' in line:
                    signal = re.search(r'Signal level[=:](\S+)', line)
                    if signal:
                        config['signal'] = signal.group(1)
            
            return config
        
        except Exception as e:
            print(f"Error obteniendo configuración: {e}")
            return {'ssid': 'Error', 'signal': '-'}

    def desconectar_wifi(self) -> bool:
        """Desconecta la red WiFi actual"""
        try:
            subprocess.run(
                ['sudo', 'ip', 'link', 'set', 'wlan0', 'down'],
                timeout=5
            )
            print("WiFi desconectado")
            return True
        except Exception as e:
            print(f"Error desconectando: {e}")
            return False

    def guardar_perfil(self):
        """Guardando perfil"""
        print("Guardando perfil")