from uuid import UUID


class EventoRaspberry:

    def __init__(
        self,
        evento_raspberry_id: UUID,
        raspberry_id: UUID,
        evento_tipo: str
    ):

        self.evento_raspberry_id = evento_raspberry_id
        self.raspberry_id = raspberry_id
        self.evento_tipo = evento_tipo

    def monitorear_conectividad(self):
        print("Monitoreando conectividad")

    def monitorear_bateria(self):
        print("Monitoreando batería")