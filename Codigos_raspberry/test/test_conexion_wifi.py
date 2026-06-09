import subprocess

def conectar_wifi(ssid, password):
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


conectar_wifi("CasaLopezMoraga-BITRED_2.4G", "geronimo0602")