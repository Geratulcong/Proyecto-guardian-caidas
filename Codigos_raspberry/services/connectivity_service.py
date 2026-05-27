class ConnectivityService:

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