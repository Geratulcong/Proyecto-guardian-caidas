# Configuración del Sistema

## Arquitectura
```
┌─────────────────────┐
│   Navegador Web     │
│  (Página HTML)      │
└──────────┬──────────┘
           │ HTTP/REST
           ▼
┌─────────────────────────────────┐
│    Servidor Web (app.py)        │
│  - Flask API (puerto 5000)      │
│  - MariaDB                      │
└─────────────────────────────────┘
           ▲
           │ Bluetooth (BLE)
           │
┌─────────────────────┐
│   Raspberry Pi      │
│  - main.py          │
│  - Arduino (BLE)    │
└─────────────────────┘
```

## Configuración de la BD

La base de datos está configurada en `database/connection.py`:

```python
mariadb.connect(
    host="127.0.0.1",      # O la IP del servidor
    port=3306,
    user="raspberry",
    password="1234",
    database="detector_caidas"
)
```

Si la BD está en otra máquina, cambia `host` por su IP.

## Variables de entorno

Puedes configurar el servidor con variables de entorno:

```bash
# Windows (PowerShell)
$env:SERVER_IP = "0.0.0.0"
$env:SERVER_PORT = "5000"
python app.py

# Linux/Mac
export SERVER_IP=0.0.0.0
export SERVER_PORT=5000
python app.py
```

Por defecto:
- `SERVER_IP`: 0.0.0.0 (escucha en todas las interfaces)
- `SERVER_PORT`: 5000

## Despliegue

### Opción 1: Mismo servidor (Recomendado)
```bash
# En el servidor web
cd Codigos_raspberry
pip install -r requirements.txt
python app.py
```

Luego accede a `http://TU_IP_SERVIDOR/Pagina%20App%20de%20emergencia/index.html`

### Opción 2: Servidores separados
1. **Servidor BD (Raspberry)**:
   - Asegúrate que MariaDB esté corriendo
   - IP: 192.168.1.7

2. **Servidor Web**:
   - Cambia en `database/connection.py`:
     ```python
     host="192.168.1.7"  # IP de la Raspberry
     ```
   - Ejecuta `python app.py`

3. **Navegador**:
   - Accede a `http://IP_DEL_SERVIDOR:5000/Pagina%20App%20de%20emergencia/index.html`

## Conexión de la página HTML a la API

La página detecta automáticamente la URL de la API:

```javascript
// En index.html
const protocol = window.location.protocol;
const hostname = window.location.hostname;
const API_BASE_URL = `${protocol}//${hostname}:5000`;
```

La página siempre se conecta a la API en el puerto 5000 del mismo servidor.

## Endpoints disponibles

- `POST /api/usuarios/verificar-o-crear` - Crear o recuperar usuario
- `GET /api/usuarios/<usuario_id>` - Obtener datos del usuario
- `PUT /api/usuarios/<usuario_id>` - Actualizar datos del usuario
- `GET /api/health` - Verificar estado del servidor
