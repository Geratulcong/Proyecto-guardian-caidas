import asyncio
import json

from bless import BlessServer
from bless.backends.characteristic import BlessGATTCharacteristic
from bless.backends.service import BlessGATTService
from bless import GATTCharacteristicProperties, GATTAttributePermissions


SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
WIFI_CHAR_UUID = "87654321-4321-4321-4321-123456789abc"


class SetupBLEService:

    def __init__(self):

        self.configuracion_recibida = None

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
            GATTCharacteristicProperties.write,
            None,
            GATTAttributePermissions.writeable
        )

        await server.start()

        print("Raspberry anunciándose por BLE")
        print("Esperando datos desde la página...")

        while self.configuracion_recibida is None:

            await asyncio.sleep(1)

        print("Configuración recibida correctamente")

        await server.stop()

        return self.configuracion_recibida