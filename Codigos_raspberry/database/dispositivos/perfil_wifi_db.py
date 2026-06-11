import uuid

from database.connection import get_connection


class PerfilWifiDB:

    def guardar_perfil(self, raspberry_id, ssid, seguridad="WPA2", estado=True):

        conn = get_connection()
        cursor = conn.cursor()

        perfil_id = str(uuid.uuid4())

        sql = """
        INSERT INTO Perfil_Wifi (
            perfil_id,
            raspberry_id,
            perfil_ssid,
            perfil_seguridad,
            perfil_estado
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            perfil_id,
            raspberry_id,
            ssid,
            seguridad,
            estado
        ))

        conn.commit()
        conn.close()