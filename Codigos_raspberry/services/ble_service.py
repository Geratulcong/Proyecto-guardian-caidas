from bleak import BleakClient
import asyncio
import json

DEVICE_ADDRESS = "XX:XX:XX:XX:XX"
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

        async with BleakClient(DEVICE_ADDRESS) as client:

            print("Conectado BLE")

            await client.start_notify(
                CHARACTERISTIC_UUID,
                self.notification_handler
            )

            while True:
                await asyncio.sleep(1)