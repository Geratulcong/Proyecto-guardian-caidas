import asyncio
import json

from bless import BlessServer
from bless import GATTCharacteristicProperties, GATTAttributePermissions

from Codigos_raspberry.services import wifi_service
from services.wifi_service import WifiService
from services.raspberry_service import RaspberryService
from database.dispositivos.perfil_wifi_db import PerfilWifiDB
from database.dispositivos.raspberry_db import RaspberryDB

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
WIFI_CHAR_UUID = "87654321-4321-4321-4321-123456789abc"


class SetupBLEService:

    def __init__(self):

        self.configuracion_recibida = None
        self.wifi_conectado = False

    def recibir_datos_wifi(self, characteristic, value, **kwargs):

        try:

            mensaje = value.decode("utf-8")

            datos = json.loads(mensaje)

            print("Datos recibidos desde la página:")
            print(datos)

            self.configuracion_recibida = datos

        except Exception as e:

            print(f"Error recibiendo configuración BLE: {e}")

    async def iniciar(self):

        print("Modo configuración BLE iniciado")

        server = BlessServer(name="Detector-Caidas-Setup")

        server.write_request_func = self.recibir_datos_wifi

        await server.add_new_service(SERVICE_UUID)

        await server.add_new_characteristic(
            SERVICE_UUID,
            WIFI_CHAR_UUID,
            GATTCharacteristicProperties.write | GATTCharacteristicProperties.write_without_response,
            bytearray(),
            GATTAttributePermissions.writeable
)

        await server.start()

        print("Raspberry anunciándose por BLE")
        print("Esperando datos desde la página...")

        while self.configuracion_recibida is None:

            await asyncio.sleep(1)

        print("Configuración recibida correctamente")

        ssid = self.configuracion_recibida.get("ssid")
        password = self.configuracion_recibida.get("password")
        usuario_id = self.configuracion_recibida.get("usuario_id")
        print(f"SSID: {ssid}")
        print(f"Usuario ID: {usuario_id}")

        wifi_service = WifiService()

        conectado = await wifi_service.conectar_wifi(ssid, password)

        if not conectado:
            print("Esperando unos segundos para verificar conexión real...")
            await asyncio.sleep(8)

            conectado = await wifi_service.verificar_conexion()     

        if conectado:

            raspberry_id = RaspberryService.obtener_id()

            raspberry_db = RaspberryDB()
            datos_raspberry = raspberry_db.obtener_raspberry(raspberry_id)

            if not datos_raspberry:
                raspberry_db.crear_raspberry(
                    raspberry_id=raspberry_id,
                    usuario_id=usuario_id
                )
                print("Raspberry registrada y vinculada al usuario")
            else:
                raspberry_db.vincular_usuario(
                    raspberry_id=raspberry_id,
                    usuario_id=usuario_id
                )
                print("Raspberry existente vinculada al usuario")

            perfil_wifi_db = PerfilWifiDB()

        await server.stop()

        return self.wifi_conectado