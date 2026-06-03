from services.wifi_service import WifiService
from services.setup_ble_service import SetupBLEService
from services.ble_service import BLEService

async def main():

    wifi = WifiService()

    conectado = await wifi.verificar_conexion()

    if not conectado:

        setup = SetupBLEService()

        await setup.iniciar()

    ble = BLEService()

    await ble.conectar()