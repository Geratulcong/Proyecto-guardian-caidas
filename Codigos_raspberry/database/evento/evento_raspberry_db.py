from Codigos_raspberry.database.connection import get_connection


class EventoRaspberryDB:

    def registrar_evento(
        self,
        evento_raspberry_id,
        raspberry_id,
        evento_tipo
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Evento_Raspberry (
            evento_raspberry_id,
            raspberry_id,
            evento_tipo
        )
        VALUES (?, ?, ?)
        """

        cursor.execute(sql, (
            evento_raspberry_id,
            raspberry_id,
            evento_tipo
        ))

        conn.commit()

        conn.close()