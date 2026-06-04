import asyncio
from uuid import UUID

from models.raspberry_pi import RaspberryPi, EstadoOperacion
from services.connectivity_service import ConnectivityService
from services.ble_service import BLEService
from database.dispositivos.raspberry_db import RaspberryDB
from database.dispositivos.connection import get_connection
from services.raspberry_service import RaspberryService
from services.setup_ble_service import SetupBLEService

# ID del Raspberry Pi (obtener de configuración, variable de entorno, etc.)
RASPBERRY_ID = RaspberryService.obtener_id()
print(f"Serial Raspberry: {RASPBERRY_ID}")

ble_service = BLEService()
connectivity_service = ConnectivityService()
raspberry_db = RaspberryDB()


async def main():
    global raspberry
    
    # Obtener Raspberry de la BD
    datos = raspberry_db.obtener_raspberry(RASPBERRY_ID)

    if not datos:

        print(f"Registrando Raspberry {RASPBERRY_ID}")

        raspberry_db.crear_raspberry(RASPBERRY_ID)

        datos = raspberry_db.obtener_raspberry(RASPBERRY_ID)
    
    # Crear instancia con datos de la BD
    raspberry = RaspberryPi(
        raspberry_id=datos[0],
        usuario_id=UUID(datos[1]) if datos[1] else None,
        raspberry_estado_arduino=datos[2],
        raspberry_estado_pagina_web=datos[3],
        raspberry_nivel_bateria=float(datos[4])
    )
    
    print(f"Raspberry cargado: {raspberry.raspberry_id}")
    
    while True:
        # Verificar conexión WiFi
        conectado = False  #await connectivity_service.verificar_conexion()
        print(f"Conexión WiFi: {'Sí' if conectado else 'No'}")
        if conectado:
            # WiFi conectado → Cambiar a MONITOREO
            if raspberry.estado_operacion != EstadoOperacion.MONITOREO:
                raspberry.cambiar_estado(EstadoOperacion.MONITOREO)
                print("Iniciando BLE...")
                await ble_service.conectar()
        else:
            if raspberry.estado_operacion != EstadoOperacion.CONFIGURACION:
                raspberry.cambiar_estado(EstadoOperacion.CONFIGURACION)
                print("Esperando configuración WiFi...")

                await ble_service.desconectar()

                setup = SetupBLEService()
                await setup.iniciar()
        
        await asyncio.sleep(5)


asyncio.run(main())