import asyncio

class WifiService:

    async def eliminar_perfil_wifi(self, ssid):

        proceso = await asyncio.create_subprocess_exec(
            "sudo", "nmcli",
            "connection", "delete", ssid,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        await proceso.communicate()


    async def conectar_wifi(self, ssid, password):

        print(f"Conectando WiFi a {ssid}")

        # Elimina perfil guardado anterior
        await self.eliminar_perfil_wifi(ssid)

        proceso = await asyncio.create_subprocess_exec(
            "sudo", "nmcli",
            "device", "wifi",
            "connect", ssid,
            "password", password,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proceso.communicate()

        if proceso.returncode == 0:
            print("WiFi conectado correctamente")
            print(stdout.decode())
            return True

        print("Error conectando WiFi")
        print(stderr.decode())
        return False