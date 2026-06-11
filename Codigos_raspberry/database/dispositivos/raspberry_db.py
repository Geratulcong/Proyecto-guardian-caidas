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
        WHERE raspberry_id = %s
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
            raspberry_estado_arduino = %s,
            raspberry_estado_pagina_web = %s,
            raspberry_nivel_bateria = %s
        WHERE raspberry_id = %s
        """

        cursor.execute(sql, (
            estado_arduino,
            estado_pagina_web,
            nivel_bateria,
            raspberry_id
        ))

        conn.commit()

        conn.close()

    def crear_raspberry(self, raspberry_id):
        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Raspberry_PI (
            raspberry_id,
            usuario_id,
            raspberry_estado_arduino,
            raspberry_estado_pagina_web,
            raspberry_nivel_bateria
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            raspberry_id,
            None,
            "Desconectado",
            "Desconectado",
            100
        ))


        conn.commit()

        conn.close()