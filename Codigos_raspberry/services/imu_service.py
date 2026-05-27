class IMUService:

    def procesar_datos(self, data):

        ax = data["ax"]
        ay = data["ay"]
        az = data["az"]

        gx = data["gx"]
        gy = data["gy"]
        gz = data["gz"]

        print("Datos procesados")