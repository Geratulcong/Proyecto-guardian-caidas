from uuid import UUID


class RaspberryPi:

    def __init__(
        self,
        raspberry_id: UUID,
        usuario_id: UUID,
        raspberry_estado_arduino: str,
        raspberry_estado_pagina_web: str,
        raspberry_nivel_bateria: float
    ):

        self.raspberry_id = raspberry_id
        self.usuario_id = usuario_id
        self.raspberry_estado_arduino = raspberry_estado_arduino
        self.raspberry_estado_pagina_web = raspberry_estado_pagina_web
        self.raspberry_nivel_bateria = raspberry_nivel_bateria

    def conectar(self):
        print("Conectando BLE...")

    def conectar_wifi(self):
        print("Conectando WiFi...")