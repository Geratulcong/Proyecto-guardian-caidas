import subprocess

def conectar_wifi(ssid, password):

    # Intentar eliminar una conexión guardada con el mismo nombre
    subprocess.run(
        ["sudo", "nmcli", "connection", "delete", ssid],
        capture_output=True,
        text=True
    )

    try:
        resultado = subprocess.run(
            [
                "sudo",
                "nmcli",
                "device",
                "wifi",
                "connect",
                ssid,
                "password",
                password
            ],
            capture_output=True,
            text=True,
            check=True
        )

        print("WiFi conectado correctamente")
        print(resultado.stdout)
        return True

    except subprocess.CalledProcessError as e:
        print("Error conectando WiFi")
        print(e.stderr)
        return False