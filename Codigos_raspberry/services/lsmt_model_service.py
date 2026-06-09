import numpy as np
import tensorflow as tf


class ModeloCaidaService:

    WINDOW_SIZE = 40

    def __init__(self):
        self.interpreter = tf.lite.Interpreter(
            model_path="models/modelo_caidas.tflite"
        )

        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.buffer = []

    def predecir(self, datos_sensor):

        self.buffer.append(datos_sensor)

        if len(self.buffer) < self.WINDOW_SIZE:
            return None

        if len(self.buffer) > self.WINDOW_SIZE:
            self.buffer.pop(0)

        entrada = np.array(
            self.buffer,
            dtype=np.float32
        ).reshape(1, self.WINDOW_SIZE, 6)

        self.interpreter.set_tensor(
            self.input_details[0]["index"],
            entrada
        )

        self.interpreter.invoke()

        salida = self.interpreter.get_tensor(
            self.output_details[0]["index"]
        )

        probabilidad = salida[0][0]

        return {
            "caida": bool(probabilidad > 0.5),
            "probabilidad": float(probabilidad)
        }