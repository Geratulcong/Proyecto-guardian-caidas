from uuid import UUID


class EventoCaida:

    def __init__(
        self,
        evento_id: UUID,
        raspberry_id: UUID,
        evento_confirmado: bool
    ):

        self.evento_id = evento_id
        self.raspberry_id = raspberry_id
        self.evento_confirmado = evento_confirmado

    def detectar_caida(self):
        print("Caída detectada")