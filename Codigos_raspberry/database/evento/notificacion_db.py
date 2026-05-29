from database.connection import get_connection


class EventoCaidaDB:

    def registrar_evento(
        self,
        evento_id,
        raspberry_id,
        tipo_evento,
        mensaje
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Evento_Caida (
            evento_id,
            raspberry_id,
            evento_tipo,
            mensaje
        )
        VALUES (?, ?, ?, ?)
        """

        cursor.execute(sql, (
            evento_id,
            raspberry_id,
            tipo_evento,
            mensaje
        ))

        conn.commit()

        conn.close()