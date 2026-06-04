from database.dispositivos.connection import get_connection


class ArduinoDB:

    def actualizar_estado(
        self,
        arduino_id,
        arduino_estado
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        UPDATE Arduino
        SET arduino_estado = ?
        WHERE arduino_id = ?
        """

        cursor.execute(sql, (
            arduino_estado,
            arduino_id
        ))

        conn.commit()

        conn.close()