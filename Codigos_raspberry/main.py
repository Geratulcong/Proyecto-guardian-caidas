import asyncio

from services.ble_service import BLEService

ble = BLEService()

asyncio.run(ble.conectar())