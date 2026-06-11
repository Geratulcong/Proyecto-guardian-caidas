from database.connection import get_connection


class EventoCaidaDB:

    def registrar_evento(
        self,
        evento_id,
        raspberry_id,
        evento_tipo
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Evento_Caida (
            evento_id,
            raspberry_id,
            evento_tipo
        )
        VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (
            evento_id,
            raspberry_id,
            evento_tipo
        ))

        conn.commit()

        conn.close()