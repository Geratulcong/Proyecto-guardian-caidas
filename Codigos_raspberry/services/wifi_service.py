import asyncio

class WifiService:

    async def conectar_wifi(self, ssid, password):

        print(f"Conectando WiFi a {ssid}")

        proceso = await asyncio.create_subprocess_exec(
            "sudo", "nmcli", "device", "wifi", "connect", ssid, "password", password,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proceso.communicate()

        if proceso.returncode == 0:
            print("WiFi conectado correctamente")
            return True

        print("Error conectando WiFi")
        print(stderr.decode())
        return False