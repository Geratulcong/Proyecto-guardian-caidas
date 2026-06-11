from database.connection import get_connection


class NotificacionDB:

    def registrar_notificacion(
        self,
        notificacion_id,
        contacto_id,
        evento_id=None,
        evento_raspberry_id=None,
        canal="WhatsApp",
        estado="Pendiente",
        mensaje=""
    ):

        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO Notificacion (
            notificacion_id,
            contacto_id,
            evento_id,
            evento_raspberry_id,
            notificacion_canal,
            notificacion_estado,
            notificacion_mensaje
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            notificacion_id,
            contacto_id,
            evento_id,
            evento_raspberry_id,
            canal,
            estado,
            mensaje
        ))

        conn.commit()
        cursor.close()
        conn.close()