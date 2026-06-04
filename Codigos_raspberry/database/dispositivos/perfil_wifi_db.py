from database.dispositivos.connection import get_connection


class PerfilWifiDB:

    def guardar_perfil(
        self,
        perfil_id,
        raspberry_id,
        perfil_ssid,
        perfil_seguridad
    ):

        conn = get_connection()

        cursor = conn.cursor()

        sql = """
        INSERT INTO Perfil_Wifi (
            perfil_id,
            raspberry_id,
            perfil_ssid,
            perfil_seguridad
        )
        VALUES (?, ?, ?, ?)
        """

        cursor.execute(sql, (
            perfil_id,
            raspberry_id,
            perfil_ssid,
            perfil_seguridad
        ))

        conn.commit()

        conn.close()