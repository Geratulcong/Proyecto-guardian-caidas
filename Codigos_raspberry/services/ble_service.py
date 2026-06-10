from bleak import BleakScanner, BleakClient
import asyncio
import json
import time

DEVICE_NAME = "Sensor-Cadera"

CHARACTERISTIC_UUID = "19b10001-0000-1000-8000-00805f9b34fb"


class BLEService:

    COOLDOWN_CAIDA = 30 * 60  # 30 minutos

    def __init__(self):
        self.client = None
        self.last_data_time = time.time()
        self.modelo_caida_service = None
        self.ultima_alerta_caida = 0

    async def enviar_mensaje_caida(self, probabilidad):
        print("Enviando mensaje de caída...")

        # Aquí después conectas tu WhatsApp, API o servicio de notificación
        print(f"ALERTA: Se detectó una caída. Probabilidad: {probabilidad:.2f}")

    async def notification_handler(self, sender, data):

        try:
            self.last_data_time = time.time()

            mensaje = data.decode()
            sensor_data = json.loads(mensaje)

            datos_sensor = [
                sensor_data["ax"],
                sensor_data["ay"],
                sensor_data["az"],
                sensor_data["gx"],
                sensor_data["gy"],
                sensor_data["gz"]
            ]

            resultado = self.modelo_caida_service.predecir(datos_sensor)

            if resultado is None:
                print("Llenando ventana del modelo...")
                return

            print(f"Probabilidad caída: {resultado['probabilidad']:.2f}")

            if resultado["caida"]:

                tiempo_actual = time.time()

                if tiempo_actual - self.ultima_alerta_caida < self.COOLDOWN_CAIDA:
                    print("Caída detectada, pero alerta bloqueada por 30 minutos")
                    return

                self.ultima_alerta_caida = tiempo_actual

                print("CAÍDA DETECTADA")

                await self.enviar_mensaje_caida(
                    resultado["probabilidad"]
                )

        except Exception as e:
            print(f"Error BLE: {e}")

    async def conectar(self, modelo_caida_service):

        self.modelo_caida_service = modelo_caida_service

        while True:

            try:
                print("Buscando Arduino...")

                devices = await BleakScanner.discover()

                target = None

                for device in devices:
                    if device.name == DEVICE_NAME:
                        target = device
                        break

                if target is None:
                    print("Arduino no encontrado")
                    await asyncio.sleep(5)
                    continue

                print(f"Conectando a {target.address}")

                self.client = BleakClient(target.address)

                await self.client.connect()

                print("BLE conectado")

                await self.client.start_notify(
                    CHARACTERISTIC_UUID,
                    self.notification_handler
                )

                while self.client.is_connected:

                    await asyncio.sleep(1)

                    tiempo_sin_datos = time.time() - self.last_data_time

                    if tiempo_sin_datos > 10:
                        print("Sensor desconectado")
                        await self.client.disconnect()
                        break

            except Exception as e:
                print(f"Error conexión BLE: {e}")

            print("Reintentando conexión...")

            await asyncio.sleep(5)

    async def desconectar(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            self.client = None
            print("BLE desconectado")