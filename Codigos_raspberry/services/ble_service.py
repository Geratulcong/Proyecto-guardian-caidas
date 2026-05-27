from bleak import BleakScanner
from bleak import BleakClient

import asyncio
import json


DEVICE_NAME = "Sensor-Cadera"

CHARACTERISTIC_UUID = "19b10001-0000-1000-8000-00805f9b34fb"


class BLEService:

    async def notification_handler(self, sender, data):

        try:

            mensaje = data.decode()

            sensor_data = json.loads(mensaje)

            print(sensor_data)

        except Exception as e:

            print(f"Error BLE: {e}")

    async def conectar(self):

        devices = await BleakScanner.discover()

        target = None

        for device in devices:

            if device.name == DEVICE_NAME:
                target = device
                break

        if target is None:

            print("Arduino no encontrado")
            return

        print(f"Conectando a {target.address}")

        async with BleakClient(target.address) as client:

            print("BLE conectado")

            await client.start_notify(
                CHARACTERISTIC_UUID,
                self.notification_handler
            )

            while True:

                await asyncio.sleep(1)