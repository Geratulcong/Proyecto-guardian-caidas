from database.connection import get_connection


class ContactoDB:

    def obtener_contactos(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                contacto_id,
                usuario_id,
                contacto_nombre,
                contacto_apellido,
                contacto_telefono,
                contacto_estado
            FROM Contacto_Emergencia
        """)

        contactos = cursor.fetchall()

        conn.close()

        return contactos

    def guardar_contacto(
        self,
        contacto_id,
        usuario_id,
        contacto_nombre,
        contacto_apellido,
        contacto_telefono,
        contacto_estado
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Contacto_Emergencia (
            contacto_id,
            usuario_id,
            contacto_nombre,
            contacto_apellido,
            contacto_telefono,
            contacto_estado
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            contacto_id,
            usuario_id,
            contacto_nombre,
            contacto_apellido,
            contacto_telefono,
            contacto_estado
        ))

        conn.commit()

        conn.close()