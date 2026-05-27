import mariadb

try:

    conn = mariadb.connect(
        host="192.168.1.7",
        port=3306,
        user="raspberry",
        password="admin",
        database="detector_caidas"
    )

    print("Conexión exitosa")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Usuario")

    for row in cursor:
        print(row)

except mariadb.Error as e:

    print(f"Error conectando: {e}")