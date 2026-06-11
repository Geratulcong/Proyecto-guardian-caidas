# Sistema de Autenticación y Creación de Usuarios

## 🏗️ Arquitectura

```
Navegador → Página HTML (index.html)
              ↓ (HTTP/REST)
         Servidor Web (app.py + MariaDB)
              ↓ (Bluetooth)
         Raspberry Pi (main.py + Arduino)
```

## Descripción
Este sistema automatiza la creación de usuarios en la base de datos cuando inicias sesión con Google en la página web de emergencia.

## 📋 Componentes

### 1. Servidor Flask (`app.py`)
Corre en el mismo servidor que la página web y MariaDB.

Endpoints:
- **POST /api/usuarios/verificar-o-crear**: Verifica si un usuario existe por email. Si no existe, lo crea automáticamente.
- **GET /api/usuarios/<usuario_id>**: Obtiene los datos de un usuario específico
- **PUT /api/usuarios/<usuario_id>**: Actualiza los datos del usuario (teléfono)
- **GET /api/health**: Verifica que el servidor esté activo

### 2. Página Web (`index.html`)
- Integración con Firebase Google Auth
- Cuando un usuario inicia sesión con Google, automáticamente se crea en la BD si no existe
- Guarda los datos del usuario en localStorage
- Permite actualizar datos del usuario (nombre, apellido, teléfono)
- Se conecta por Bluetooth con Arduino/Raspberry para datos en tiempo real

### 3. Base de Datos (MariaDB)
- Usa la tabla `Usuario` con UUID como identificador único
- Cada usuario nuevo recibe un UUID único al registrarse con Google

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.8+
- MariaDB 10.3+
- Navegador moderno con soporte para Bluetooth Web API

### Paso 1: Instalar dependencias
```bash
cd Codigos_raspberry
pip install -r requirements.txt
```

### Paso 2: Configurar la base de datos
Verifica que MariaDB esté corriendo y accesible desde `database/connection.py`:

```python
mariadb.connect(
    host="127.0.0.1",  # O la IP del servidor
    port=3306,
    user="raspberry",
    password="1234",
    database="detector_caidas"
)
```

### Paso 3: Ejecutar el servidor Flask
```bash
python app.py
```

El servidor correrá en:
- En desarrollo: `http://localhost:5000`
- En producción: `http://TU_IP_SERVIDOR:5000`

### Paso 4: Acceder a la página web
Abre en el navegador:
```
http://TU_IP_SERVIDOR:5000/Pagina%20App%20de%20emergencia/index.html
```

O si está en el mismo localhost:
```
http://localhost:5000/Pagina%20App%20de%20emergencia/index.html
```

## 🔄 Flujo de funcionamiento

1. **Usuario inicia sesión con Google**
   - Hace click en "Iniciar sesión con Google"
   - Se abre el popup de Google Auth
   - Firebase valida las credenciales

2. **Verificación en BD**
   - JavaScript detecta el nuevo usuario autenticado
   - Envía POST a `/api/usuarios/verificar-o-crear`
   - Con el email y nombre del usuario de Google

3. **Creación o recuperación del usuario**
   - Servidor verifica si el email existe
   - Si NO existe: crea nuevo usuario con UUID único
   - Si SÍ existe: recupera los datos existentes
   - Retorna usuario_id

4. **Almacenamiento local**
   - usuario_id se guarda en localStorage
   - Se permite editar nombre, apellido y teléfono

5. **Actualización de datos**
   - Usuario completa sus datos en la vista "Usuario"
   - Al hacer click en "Guardar Datos", se valida localmente
   - Se envía PUT a `/api/usuarios/<usuario_id>`
   - Se actualiza la BD

## 📁 Estructura de archivos

```
Codigos_raspberry/
├── app.py                          # Servidor Flask con API
├── requirements.txt                # Dependencias Python
├── INSTRUCCIONES_USUARIOS.md      # Este archivo
├── CONFIG.md                       # Configuración del sistema
├── main.py                         # Script principal de Raspberry
├── database/
│   ├── connection.py               # Conexión a MariaDB
│   ├── usuario/
│   │   ├── usuario_db.py           # Clase UsuarioDB
│   │   └── contacto_db.py          # Clase ContactoDB
│   └── ...
└── Pagina App de emergencia/
    └── index.html                  # Página web con JS
```

## 🔐 Seguridad

- Todos los endpoints tienen validación básica de entrada
- Los datos se validan en la BD antes de crear/actualizar
- CORS habilitado solo para peticiones necesarias
- Firebase maneja la autenticación segura
- Los UUID son únicos e imposibles de predecir

## 🐛 Solución de problemas

### "No se puede conectar a la BD"
- Verifica que MariaDB esté corriendo
- Comprueba que la IP y puerto sean correctos en `database/connection.py`
- Asegúrate que el usuario `raspberry` tenga permisos

### "Error al crear usuario en BD"
- Verifica que la tabla `Usuario` exista
- Comprueba que el email no esté duplicado
- Revisa los logs de MariaDB

### "La página no se conecta a la API"
- Verifica que app.py esté corriendo
- Comprueba que el puerto 5000 no esté bloqueado
- Revisa la consola del navegador (F12) para errores

### "Bluetooth no funciona"
- Usa un navegador compatible (Chrome, Edge, etc.)
- Activa Bluetooth en tu dispositivo
- Asegúrate que Arduino/Raspberry esté emitiendo BLE
