from database.connection import get_connection
from uuid import uuid4


class ContactoDB:

    def obtener_contactos(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                contacto_id,
                usuario_id,
                contacto_nombre,
                contacto_telefono,
                contacto_estado
            FROM Contacto_Emergencia
        """)

        contactos = cursor.fetchall()

        conn.close()

        return contactos

    def obtener_contactos_usuario(self, usuario_id):
        """Obtiene todos los contactos de un usuario específico"""
        
        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                contacto_id,
                usuario_id,
                contacto_nombre,
                contacto_telefono,
                contacto_estado
            FROM Contacto_Emergencia
            WHERE usuario_id = %s
        """, (usuario_id,))

        contactos = cursor.fetchall()

        conn.close()

        return contactos

    def guardar_contacto(
        self,
        contacto_id,
        usuario_id,
        contacto_nombre,
        contacto_telefono,
        contacto_estado=True
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Contacto_Emergencia (
            contacto_id,
            usuario_id,
            contacto_nombre,
            contacto_telefono,
            contacto_estado
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            contacto_id,
            usuario_id,
            contacto_nombre,
            contacto_telefono,
            contacto_estado
        ))

        conn.commit()

        conn.close()

    def actualizar_contacto(
        self,
        contacto_id,
        contacto_nombre=None,
        contacto_telefono=None,
        contacto_estado=None
    ):
        """Actualiza los datos de un contacto"""
        
        conn = get_connection()

        cursor = conn.cursor()

        updates = []
        valores = []

        if contacto_nombre is not None:
            updates.append("contacto_nombre = %s")
            valores.append(contacto_nombre)


        if contacto_telefono is not None:
            updates.append("contacto_telefono = %s")
            valores.append(contacto_telefono)

        if contacto_estado is not None:
            updates.append("contacto_estado = %s")
            valores.append(contacto_estado)

        if not updates:
            conn.close()
            return False

        valores.append(contacto_id)

        sql = f"""
        UPDATE Contacto_Emergencia
        SET {', '.join(updates)}
        WHERE contacto_id = %s
        """

        cursor.execute(sql, valores)

        conn.commit()

        conn.close()

        return True

    def eliminar_contacto(self, contacto_id):
        """Elimina un contacto por su ID"""
        
        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        DELETE FROM Contacto_Emergencia
        WHERE contacto_id = %s
        """

        cursor.execute(sql, (contacto_id,))

        conn.commit()

        conn.close()

    def obtener_contactos_activos(self, usuario_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                contacto_id,
                usuario_id,
                contacto_nombre,
                contacto_telefono,
                contacto_estado
            FROM Contacto_Emergencia
            WHERE usuario_id = %s
            AND contacto_estado = TRUE
        """, (usuario_id,))

        contactos = cursor.fetchall()

        conn.close()

        return contactos