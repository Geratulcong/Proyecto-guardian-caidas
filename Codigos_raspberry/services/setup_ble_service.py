import asyncio

class SetupBLEService:

    async def iniciar(self):

        print("Modo configuración BLE iniciado")

        while True:
            print("Esperando datos desde la página...")
            await asyncio.sleep(5)