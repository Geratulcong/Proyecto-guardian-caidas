import subprocess


class ConnectivityService:

    async def verificar_conexion(self) -> bool:
        """Verifica si hay conexión WiFi"""
        try:
            # Intenta ping a Google DNS
            result = subprocess.run(
                ["ping", "-c", "1", "8.8.8.8"],
                timeout=5,
                capture_output=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error verificando conexión: {e}")
            return False

    def monitorear_conectividad(self, client):

        if client and client.is_connected:
            print("BLE conectado")
            return True

        print("BLE desconectado")
        return False

    async def reconectar(self, ble_service):

        print("Reconectando...")

        try:
            await ble_service.conectar()
            print("Reconexión exitosa")

        except Exception as e:
            print(f"Error reconectando: {e}")