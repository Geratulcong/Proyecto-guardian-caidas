from tensorflow.keras.models import load_model
import numpy as np


class ModeloCaidaService:

    WINDOW_SIZE = 40

    def __init__(self):
        self.modelo = load_model("models/modelo_lstm_caidas.h5")
        self.buffer = []

    def predecir(self, datos_sensor):
        """
        datos_sensor:
        [cadera_ax, cadera_ay, cadera_az, cadera_gx, cadera_gy, cadera_gz]
        """

        self.buffer.append(datos_sensor)

        if len(self.buffer) < self.WINDOW_SIZE:
            return None

        if len(self.buffer) > self.WINDOW_SIZE:
            self.buffer.pop(0)

        entrada = np.array(self.buffer).reshape(1, self.WINDOW_SIZE, 6)

        probabilidad = self.modelo.predict(entrada, verbose=0)[0][0]

        return {
            "caida": bool(probabilidad > 0.5),
            "probabilidad": float(probabilidad)
        }