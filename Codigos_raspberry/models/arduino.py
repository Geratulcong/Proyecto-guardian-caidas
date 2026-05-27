from uuid import UUID


class Arduino:

    def __init__(
        self,
        arduino_id: UUID,
        raspberry_id: UUID,
        arduino_estado: str
    ):

        self.arduino_id = arduino_id
        self.raspberry_id = raspberry_id
        self.arduino_estado = arduino_estado

    def capturar_datos(self):
        print("Capturando datos IMU")

    def generar_json(self):
        print("Generando JSON")

    def activar_alerta_manual(self):
        print("Botón presionado")