import asyncio
from xmlrpc import client

from services.connectivity_service import ConnectivityService
from services.ble_service import BLEService


ble_service = BLEService()
connectivity_service = ConnectivityService()

async def main():

    conectado = connectivity_service.monitorear_conectividad(
        ble_service.client
    )

    if not conectado:
        await connectivity_service.reconectar(ble_service)

asyncio.run(main())