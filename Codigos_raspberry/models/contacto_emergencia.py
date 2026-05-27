from uuid import UUID


class ContactoEmergencia:

    def __init__(
        self,
        contacto_id: UUID,
        usuario_id: UUID,
        contacto_nombre: str,
        contacto_apellido: str,
        contacto_telefono: str,
        contacto_estado: bool = True
    ):

        self.contacto_id = contacto_id
        self.usuario_id = usuario_id
        self.contacto_nombre = contacto_nombre
        self.contacto_apellido = contacto_apellido
        self.contacto_telefono = contacto_telefono
        self.contacto_estado = contacto_estado

    def enviar_alerta(self):
        print("Enviando alerta...")