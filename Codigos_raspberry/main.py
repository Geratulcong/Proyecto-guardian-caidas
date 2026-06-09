import asyncio
from uuid import UUID

from models.raspberry_pi import RaspberryPi, EstadoOperacion
from services.connectivity_service import ConnectivityService
from services.ble_service import BLEService
from services.raspberry_service import RaspberryService
from services.setup_ble_service import SetupBLEService
from database.dispositivos.raspberry_db import RaspberryDB
from services.lsmt_model_service import ModeloCaidaService


RASPBERRY_ID = RaspberryService.obtener_id()

print(f"Serial Raspberry: {RASPBERRY_ID}")

ble_service = BLEService()
connectivity_service = ConnectivityService()
raspberry_db = RaspberryDB()
modelo_caida_service = ModeloCaidaService()

async def main():

    conectado = await connectivity_service.verificar_conexion()

    if not conectado:

        print("Sin WiFi. Iniciando configuración por BLE...")

        setup = SetupBLEService()

        wifi_configurado = await setup.iniciar()

        if not wifi_configurado:

            print("No se pudo configurar WiFi")
            return

    print("WiFi disponible. Conectando a BD...")

    datos = raspberry_db.obtener_raspberry(RASPBERRY_ID)

    if not datos:

        print(f"Registrando Raspberry {RASPBERRY_ID}")

        raspberry_db.crear_raspberry(RASPBERRY_ID)

        datos = raspberry_db.obtener_raspberry(RASPBERRY_ID)

    raspberry = RaspberryPi(
        raspberry_id=datos[0],
        usuario_id=UUID(datos[1]) if datos[1] else None,
        raspberry_estado_arduino=datos[2],
        raspberry_estado_pagina_web=datos[3],
        raspberry_nivel_bateria=float(datos[4])
    )

    print(f"Raspberry cargado: {raspberry.raspberry_id}")

    raspberry.cambiar_estado(EstadoOperacion.MONITOREO)

    print("Iniciando BLE con Arduino...")

    await ble_service.conectar(modelo_caida_service)


asyncio.run(main())