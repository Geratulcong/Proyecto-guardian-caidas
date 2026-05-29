from uuid import UUID


class EventoCaida:

    def __init__(
        self,
        evento_id: UUID,
        raspberry_id: UUID,
        evento_tipo: str
    ):

        self.evento_id = evento_id
        self.raspberry_id = raspberry_id
        self.evento_tipo = evento_tipo

    def detectar_caida(self):
        print("Caída detectada")