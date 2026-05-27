from database.connection import get_connection


class UsuarioDB:

    def obtener_usuarios(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Usuario")

        usuarios = cursor.fetchall()

        conn.close()

        return usuarios