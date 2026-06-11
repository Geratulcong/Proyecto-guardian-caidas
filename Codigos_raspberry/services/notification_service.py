import requests
from uuid import uuid4

from database.evento.notificacion_db import NotificacionDB


class NotificationService:

    def __init__(self):
        self.notificacion_db = NotificacionDB()

    async def enviar_whatsapp(
        self,
        contacto_id,
        telefono,
        mensaje,
        evento_id=None,
        evento_raspberry_id=None
    ):

        url = "https://api.callmebot.com/whatsapp.php"

        payload = {
            "phone": telefono,
            "text": mensaje,
            "apikey": "9733456"
        }

        try:
            response = requests.get(url, params=payload, timeout=10)

            if response.status_code == 200:
                estado = "Enviado"
            else:
                estado = "Error"

        except Exception as e:
            estado = "Error"
            mensaje = f"{mensaje} | Error: {e}"

        self.notificacion_db.registrar_notificacion(
            notificacion_id=str(uuid4()),
            contacto_id=contacto_id,
            evento_id=evento_id,
            evento_raspberry_id=evento_raspberry_id,
            canal="WhatsApp",
            estado=estado,
            mensaje=mensaje
        )

        print("Estado notificación:", estado)

        return estado == "Enviado"