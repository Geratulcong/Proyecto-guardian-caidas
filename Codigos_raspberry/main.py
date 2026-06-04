import asyncio
from uuid import UUID
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from models.raspberry_pi import RaspberryPi, EstadoOperacion
from services.connectivity_service import ConnectivityService
from services.ble_service import BLEService
from database.dispositivos.raspberry_db import RaspberryDB


# ID del Raspberry Pi (obtener de configuración, variable de entorno, etc.)
RASPBERRY_ID = "12345678-1234-1234-1234-123456789012"  # Cambiar por el ID real

ble_service = BLEService()
connectivity_service = ConnectivityService()
raspberry_db = RaspberryDB()


async def main():
    global raspberry
    
    # Obtener Raspberry de la BD
    datos = raspberry_db.obtener_raspberry(RASPBERRY_ID)
    
    if not datos:
        print(f"Raspberry {RASPBERRY_ID} no encontrado en BD")
        return
    
    # Crear instancia con datos de la BD
    raspberry = RaspberryPi(
        raspberry_id=UUID(datos[0]),
        usuario_id=UUID(datos[1]),
        raspberry_estado_arduino=datos[2],
        raspberry_estado_pagina_web=datos[3],
        raspberry_nivel_bateria=float(datos[4])
    )
    
    print(f"Raspberry cargado: {raspberry.raspberry_id}")
    
    while True:
        # Verificar conexión WiFi
        conectado = await connectivity_service.verificar_conexion()
        
        if conectado:
            # WiFi conectado → Cambiar a MONITOREO
            if raspberry.estado_operacion != EstadoOperacion.MONITOREO:
                raspberry.cambiar_estado(EstadoOperacion.MONITOREO)
                print("Iniciando BLE...")
                await ble_service.conectar()
        else:
            # WiFi desconectado → Cambiar a CONFIGURACION
            if raspberry.estado_operacion != EstadoOperacion.CONFIGURACION:
                raspberry.cambiar_estado(EstadoOperacion.CONFIGURACION)
                print("Esperando configuración WiFi...")
                await ble_service.desconectar()
        
        await asyncio.sleep(5)


asyncio.run(main())