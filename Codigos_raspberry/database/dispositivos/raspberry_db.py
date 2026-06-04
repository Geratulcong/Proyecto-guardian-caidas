from database.connection import get_connection


class RaspberryDB:

    def obtener_raspberry(self, raspberry_id):
        """Obtiene un Raspberry de la BD"""
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT 
            raspberry_id,
            usuario_id,
            raspberry_estado_arduino,
            raspberry_estado_pagina_web,
            raspberry_nivel_bateria
        FROM Raspberry_PI
        WHERE raspberry_id = ?
        """

        cursor.execute(sql, (raspberry_id,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado

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