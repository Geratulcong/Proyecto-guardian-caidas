from uuid import UUID


class Notificacion:

    def __init__(
        self,
        notificacion_id: UUID,
        contacto_id: UUID,
        evento_id: UUID = None,
        evento_raspberry_id: UUID = None,
        notificacion_mensaje: str = "",
        notificacion_canal: str = "WhatsApp",
        notificacion_estado: str = "Pendiente"
    ):

        self.notificacion_id = notificacion_id
        self.contacto_id = contacto_id

        self.evento_id = evento_id
        self.evento_raspberry_id = evento_raspberry_id

        self.notificacion_mensaje = notificacion_mensaje

        self.notificacion_canal = notificacion_canal
        self.notificacion_estado = notificacion_estado

    def enviar_notificacion(self):

        print(self.notificacion_mensaje)