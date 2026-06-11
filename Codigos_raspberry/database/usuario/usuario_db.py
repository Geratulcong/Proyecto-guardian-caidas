from database.connection import get_connection


class UsuarioDB:

    def obtener_usuarios(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                usuario_id,
                usuario_nombre,
                usuario_email,
                usuario_telefono,
                usuario_activo,
                usuario_familiar_nombre,
                usuario_familiar_telefono
            FROM Usuario
        """)

        usuarios = cursor.fetchall()

        conn.close()

        return usuarios

    def registrar_usuario(
        self,
        usuario_id,
        usuario_nombre,
        usuario_email,
        usuario_telefono,
        usuario_activo,
        usuario_familiar_nombre,
        usuario_familiar_telefono
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Usuario (
            usuario_id,
            usuario_nombre,
            usuario_email,
            usuario_telefono,
            usuario_activo,
            usuario_familiar_nombre,
            usuario_familiar_telefono
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            usuario_id,
            usuario_nombre,
            usuario_email,
            usuario_telefono,
            usuario_activo,
            usuario_familiar_nombre,
            usuario_familiar_telefono
        )

        cursor.execute(sql, valores)

        conn.commit()

        conn.close()

    def actualizar_telefono(
        self,
        usuario_id,
        nuevo_telefono
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        UPDATE Usuario
        SET usuario_telefono = %s
        WHERE usuario_id = %s
        """

        cursor.execute(sql, (
            nuevo_telefono,
            usuario_id
        ))

        conn.commit()

        conn.close()