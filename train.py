import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dropout, Flatten, Dense
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import seaborn as sns

#Configuracion cnn
WINDOW_SIZE = 40   # 2s a 20Hz
OVERLAP = 20       # 50%
TEST_SIZE = 0.2
EPOCHS = 15
BATCH_SIZE = 16


archivo_caidas   = Path(r"Codigos_raspberry\datos_limpios\datos_capturados_caidas (1).csv")
archivo_normales = Path(r"Codigos_raspberry\datos_limpios\datos_capturados_normales.csv")

ARCHIVOS = {
    archivo_caidas: 1,     # caída
    archivo_normales: 0    # normal
}

COLUMNAS = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']

datos_totales = []
etiquetas_totales = []

COLUMNAS = [
    'cadera_ax','cadera_ay','cadera_az','cadera_gx','cadera_gy','cadera_gz',
    'pierna_ax','pierna_ay','pierna_az','pierna_gx','pierna_gy','pierna_gz'
]

cols_giro = [
    'cadera_gx','cadera_gy','cadera_gz',
    'pierna_gx','pierna_gy','pierna_gz'
]

for archivo, etiqueta in ARCHIVOS.items():
    print(f"\n📄 Procesando: {archivo.name}")
    df = pd.read_csv(archivo)

    # Escalar giroscopio para dar mas prioridad al giroscopio
    df[cols_giro] *= 4.0

    for i in range(0, len(df) - WINDOW_SIZE + 1, OVERLAP):
        ventana = df.iloc[i:i+WINDOW_SIZE][COLUMNAS].values
        datos_totales.append(ventana)
        etiquetas_totales.append(etiqueta)


X = np.array(datos_totales, dtype=np.float32)
y = np.array(etiquetas_totales, dtype=np.int32)

unique, counts = np.unique(y, return_counts=True)
for clase, count in zip(unique, counts):
    nombre = "Normal" if clase == 0 else "Caída"

#Train test y split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=42, stratify=y
)

#Modelo CNN 
model = Sequential([
    Conv1D(32, 3, activation='relu', padding='same', input_shape=(WINDOW_SIZE, 12)),
    MaxPooling1D(2),
    
    Conv1D(64, 3, activation='relu', padding='same'),
    MaxPooling1D(2),
    Dropout(0.4),
    
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

#Entrenar modelo
early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=[early_stop],
    verbose=1
)


loss, acc = model.evaluate(X_test, y_test)
print(f"\n Pérdida: {loss:.4f} | Precisión: {acc:.4f}")

# Predicciones
y_pred = (model.predict(X_test) > 0.5).astype(int)

# Matriz de confusión
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal', 'Caída'],
            yticklabels=['Normal', 'Caída'])
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.title("Matriz de Confusión")
plt.tight_layout()
plt.savefig('matriz_confusion_arduino.png', dpi=150)
print("💾 Matriz guardada: matriz_confusion_arduino.png")

# Reporte
print("\n📋 Reporte de clasificación:")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Caída']))

#Guardar modelo
MODEL_PATH = "modelo_cnn_imu.h5"
model.save(MODEL_PATH)
print(f"\n💾 Modelo guardado: {MODEL_PATH}")

#distribucion de clases
unique, counts = np.unique(y, return_counts=True)
plt.figure(figsize=(6,4))
sns.barplot(x=['Normal', 'Caída'], y=counts)
plt.title("Distribución de Clases")
plt.ylabel("Cantidad de ventanas")
plt.tight_layout()
plt.savefig("class_distribution.png", dpi=150)
print("💾 Imagen guardada: class_distribution.png")


#matriz de confusion
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal', 'Caída'],
            yticklabels=['Normal', 'Caída'])
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.title("Matriz de Confusión")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=150)
print("💾 Imagen guardada: confusion_matrix.png")


#Grafico entrenamiento
plt.figure(figsize=(12,4))

# Loss
plt.subplot(1,2,1)
plt.plot(history.history['loss'], label='Train')
plt.plot(history.history['val_loss'], label='Val')
plt.title('Pérdida')
plt.xlabel('Época')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)

# Accuracy
plt.subplot(1,2,2)
plt.plot(history.history['accuracy'], label='Train')
plt.plot(history.history['val_accuracy'], label='Val')
plt.title('Precisión')
plt.xlabel('Época')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("training_metrics.png", dpi=150)
print("💾 Imagen guardada: training_metrics.png")

#Grafico de modelo
from tensorflow.keras.utils import plot_model

plot_model(
    model,
    to_file="arquitectura_cnn.png",
    show_shapes=True,
    show_layer_names=True,
    dpi=140
)
