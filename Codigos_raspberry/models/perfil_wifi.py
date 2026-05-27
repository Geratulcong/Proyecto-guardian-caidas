from uuid import UUID


class PerfilWifi:

    def __init__(
        self,
        perfil_id: UUID,
        raspberry_id: UUID,
        perfil_ssid: str,
        perfil_contrasena: str,
        perfil_seguridad: str
    ):

        self.perfil_id = perfil_id
        self.raspberry_id = raspberry_id
        self.perfil_ssid = perfil_ssid
        self.perfil_contrasena = perfil_contrasena
        self.perfil_seguridad = perfil_seguridad

    def gestionar_conexion_wifi(self):
        print("Gestionando conexión WiFi")