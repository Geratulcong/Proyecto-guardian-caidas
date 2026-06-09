from bleak import BleakScanner, BleakClient
import asyncio
import json
import time

DEVICE_NAME = "Sensor-Cadera"

CHARACTERISTIC_UUID = "19b10001-0000-1000-8000-00805f9b34fb"


class BLEService:

    def __init__(self):
        self.client = None
        self.last_data_time = time.time()
        self.modelo_caida_service = None

    async def notification_handler(self, sender, data):

        try:
            self.last_data_time = time.time()

            mensaje = data.decode()
            sensor_data = json.loads(mensaje)

            datos_sensor = [
                sensor_data["cadera_ax"],
                sensor_data["cadera_ay"],
                sensor_data["cadera_az"],
                sensor_data["cadera_gx"],
                sensor_data["cadera_gy"],
                sensor_data["cadera_gz"]
            ]

            resultado = self.modelo_caida_service.predecir(datos_sensor)

            if resultado is None:
                print("Llenando ventana del modelo...")
                return

            print(f"Probabilidad caída: {resultado['probabilidad']:.2f}")

            if resultado["caida"]:
                print("CAÍDA DETECTADA")

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