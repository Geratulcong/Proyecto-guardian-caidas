import numpy as np
from tensorflow.keras.models import load_model


class MLService:

    def __init__(self):

        self.model = load_model("ml/model.h5")

    def detectar_caida(self, ventana):

        datos = np.array(ventana)

        datos = datos.reshape(1, 100, 6)

        prediccion = self.model.predict(datos)

        return prediccion