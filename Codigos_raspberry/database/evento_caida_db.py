from database.connection import get_connection


class EventoCaidaDB:

    def registrar_evento(self, evento_id, raspberry_id):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Evento_Caida (
            evento_id,
            raspberry_id
        )
        VALUES (?, ?)
        """

        cursor.execute(sql, (
            evento_id,
            raspberry_id
        ))

        conn.commit()

        conn.close()