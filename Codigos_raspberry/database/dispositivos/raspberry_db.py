from database.connection import get_connection


class RaspberryDB:

    def actualizar_estado(
        self,
        raspberry_id,
        estado_arduino,
        estado_pagina_web,
        nivel_bateria
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        UPDATE Raspberry_Pi
        SET
            raspberry_estado_arduino = ?,
            raspberry_estado_pagina_web = ?,
            raspberry_nivel_bateria = ?
        WHERE raspberry_id = ?
        """

        cursor.execute(sql, (
            estado_arduino,
            estado_pagina_web,
            nivel_bateria,
            raspberry_id
        ))

        conn.commit()

        conn.close()