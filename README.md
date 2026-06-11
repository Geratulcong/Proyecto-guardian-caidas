# 🚨 Guardian Anticaídas - App de Emergencia

Sistema integrado de detección de caídas con alertas por BLE y web.

## 📋 Resumen del Proyecto

### Componentes principales:

1. **Arduino (con sensor IMU)**
   - Detecta caídas mediante acelerómetro
   - Se comunica con Raspberry por Bluetooth (BLE)

2. **Raspberry Pi**
   - Corre `main.py` para monitoreo
   - Conecta con Arduino por BLE
   - Acceso a base de datos MariaDB

3. **Servidor Web**
   - Aloja `app.py` (API Flask)
   - Aloja `index.html` (página web)
   - Contiene MariaDB (base de datos)

4. **Navegador (Cliente Web)**
   - Accede a `index.html`
   - Se conecta a API REST
   - Se sincroniza con Raspberry por Bluetooth

## 🏗️ Arquitectura

```
┌────────────────┐
│    Arduino     │
│  (Sensor IMU)  │
└────────┬───────┘
         │ BLE
         ▼
┌────────────────────┐     ┌──────────────────────────┐
│  Raspberry Pi      │     │    Servidor Web          │
│  - main.py         │     │  - app.py (Flask)        │
│  - BLE Service     │────►│  - MariaDB               │
│  - ML Models       │     │  - index.html            │
└────────────────────┘     └────────┬─────────────────┘
                                    │ HTTP/REST
                                    ▼
                            ┌──────────────────┐
                            │   Navegador      │
                            │   (Cliente Web)  │
                            └──────────────────┘
```

## 📁 Estructura del proyecto

```
Proyecto-microprocesadores1/
├── train_cnn.ipynb                      # Notebook para entrenar modelo CNN
├── train_lstm.ipynb                     # Notebook para entrenar modelo LSTM
│
├── Codigos Arduino/
│   └── sensor_cadera_ble.ino           # Código del Arduino
│
├── Codigos_raspberry/
│   ├── main.py                         # Punto de entrada principal
│   ├── app.py                          # Servidor Flask (API)
│   ├── requirements.txt                # Dependencias Python
│   ├── .env.example                    # Variables de entorno (ejemplo)
│   ├── CONFIG.md                       # Configuración del sistema
│   ├── INSTRUCCIONES_USUARIOS.md       # Guía del sistema de usuarios
│   │
│   ├── database/
│   │   ├── connection.py               # Conexión a MariaDB
│   │   ├── crear_database.sql          # Script de creación BD
│   │   ├── crear_tablas.sql            # Script de creación tablas
│   │   ├── dispositivos/               # BD de dispositivos
│   │   ├── usuario/                    # BD de usuarios
│   │   └── evento/                     # BD de eventos
│   │
│   ├── ml_models/
│   │   ├── modelo_caidas.tflite        # Modelo TensorFlow Lite
│   │   └── modelo_lstm_caidas.h5       # Modelo LSTM
│   │
│   ├── models/
│   │   ├── arduino.py
│   │   ├── usuario.py
│   │   ├── evento_caida.py
│   │   └── ...
│   │
│   ├── services/
│   │   ├── ble_service.py              # Servicio de Bluetooth
│   │   ├── ml_service.py               # Servicio de ML
│   │   ├── connectivity_service.py     # Servicio de WiFi
│   │   └── ...
│   │
│   ├── test/
│   │   └── test_db.py
│   │
│   └── Pagina App de emergencia/
│       ├── index.html                  # Página web principal
│       └── launch.json
│
└── Documentos/
    └── Datos/
        ├── datos_capturados_caidas.csv
        └── datos_capturados_normales.csv
```

## 🚀 Inicio rápido

### Requisitos
- Python 3.8+
- Arduino IDE
- MariaDB 10.3+
- Navegador moderno (Chrome, Edge, Firefox)
- Raspberry Pi 4+

### 1. Configurar Base de Datos

```bash
# En la Raspberry o servidor de BD
mysql -u root -p < crear_database.sql
mysql -u root -p < crear_tablas.sql
```

### 2. Instalar dependencias

```bash
cd Codigos_raspberry
pip install -r requirements.txt
```

### 3. Cargar firmware en Arduino

```
- Abre Arduino IDE
- Carga: Codigos Arduino/sensor_cadera_ble.ino
- Sube al Arduino
```

### 4. Ejecutar Raspberry Pi

```bash
python main.py
```

### 5. Ejecutar servidor web

```bash
python app.py
```

### 6. Acceder a la página

```
http://TU_IP_SERVIDOR:5000/Pagina%20App%20de%20emergencia/index.html
```

## 🔐 Autenticación de Usuarios

La página web usa **Google Sign-In** con Firebase:

1. Usuario inicia sesión con Google
2. Se verifica/crea automáticamente en la BD
3. Se guarda `usuario_id` en localStorage
4. Usuario completa su perfil
5. Sistema de alertas vinculado a su cuenta

Para más detalles, ver: [INSTRUCCIONES_USUARIOS.md](INSTRUCCIONES_USUARIOS.md)

## ⚙️ Configuración

Ver: [CONFIG.md](CONFIG.md)

Variables de entorno disponibles:
- `SERVER_IP`: IP del servidor (default: 0.0.0.0)
- `SERVER_PORT`: Puerto del servidor (default: 5000)
- `DB_HOST`: Host de MariaDB
- `DB_PORT`: Puerto de MariaDB
- `DB_USER`: Usuario de BD
- `DB_PASSWORD`: Contraseña de BD
- `DB_NAME`: Nombre de la BD

## 📊 Características principales

✅ Detección de caídas por IMU
✅ Comunicación BLE Arduino-Raspberry
✅ ML con TensorFlow Lite
✅ API REST (Flask)
✅ Base de datos MariaDB
✅ Autenticación Google
✅ Alertas y notificaciones
✅ Dashboard web responsive
✅ Configuración WiFi por BLE

## 🐛 Solución de problemas

### "No se conecta a BLE"
- Verifica Bluetooth esté activado
- Comprueba que Arduino esté cerca
- Reinicia el dispositivo

### "Error de BD"
- Verifica que MariaDB esté corriendo
- Comprueba credenciales en `database/connection.py`
- Crea la BD con los scripts SQL

### "API no responde"
- Asegúrate que `app.py` esté corriendo
- Verifica puerto 5000 no esté bloqueado
- Revisa logs de Flask

## 📞 Contacto y soporte

Para preguntas o reportar bugs, contacta al equipo de desarrollo.

---

**Versión:** 1.0
**Última actualización:** 2026-06-11
