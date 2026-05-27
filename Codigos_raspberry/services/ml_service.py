import joblib
import numpy as np


class MLService:

    def __init__(self):

        self.model = joblib.load("ml/model.pkl")

    def detectar_caida(self, datos_sensor):

        datos = np.array([
            [
                datos_sensor["ax"],
                datos_sensor["ay"],
                datos_sensor["az"],
                datos_sensor["gx"],
                datos_sensor["gy"],
                datos_sensor["gz"]
            ]
        ])

        prediccion = self.model.predict(datos)

        return prediccion[0]