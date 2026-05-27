import asyncio

from services.ble_service import BLEService


ble_service = BLEService()

asyncio.run(
    ble_service.conectar()
)