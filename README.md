# Sistema de Automatización RPA

Sistema automatizado para leer correos electrónicos, extraer links y realizar acciones web automáticamente.

## 🎯 ¿Qué hace el sistema?

1. **Lee correos no leídos** desde una cuenta de correo (IMAP)
2. **Filtra correos** por remitente específico (ej: `netflix.com`)
3. **Extrae links** usando patrones configurables
4. **Abre páginas web** con Selenium (modo headless)
5. **Hace clic en botones** usando selectores CSS configurables
6. **Registra todo** en base de datos SQLite con logs detallados

## 📁 Estructura del proyecto

```
rpa_system/
├── main.py              # Archivo principal que orquesta todo
├── email_reader.py      # Lectura de correos electrónicos
├── driver_web.py        # Automatización web con Selenium
├── database.py          # Manejo de base de datos SQLite
├── requirements.txt     # Dependencias del proyecto
├── env.example          # Ejemplo de configuración
└── README.md           # Esta documentación
```

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
```bash
cd rpa_system
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Instalar Chrome y ChromeDriver
```bash
# En Ubuntu/Debian
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver

# O usar webdriver-manager (automático)
pip install webdriver-manager
```

### 4. Configurar variables de entorno
```bash
cp env.example .env
nano .env
```

## ⚙️ Configuración

Edita el archivo `.env` con tus credenciales:

```env
# Configuración del servidor IMAP
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993

# Credenciales del correo electrónico
EMAIL_ADDRESS=tu_correo@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicacion

# Filtros de correo
SENDER_FILTER=netflix.com
LINK_PATTERN=https?://[^\s<>"]+

# Configuración del navegador web
BUTTON_SELECTOR=button[type="submit"]
TIMEOUT_SECONDS=10
```

### 🔐 Configuración de Gmail

Para usar Gmail, necesitas una **contraseña de aplicación**:

1. Ve a [Configuración de Google](https://myaccount.google.com/)
2. Seguridad → Verificación en 2 pasos (activar)
3. Contraseñas de aplicación → Generar nueva
4. Usa esa contraseña en `EMAIL_PASSWORD`

## 🏃‍♂️ Uso

### Ejecución manual
```bash
python main.py
```

### Probar el sistema
```bash
python test_system.py
```

### Ejecución automática con cron
```bash
# Editar crontab
crontab -e

# Agregar línea para ejecutar cada 5 minutos
*/5 * * * * cd /ruta/a/rpa_system && python main.py >> /tmp/rpa.log 2>&1
```

## 📊 Monitoreo

### Logs del sistema
Los logs se guardan en `rpa_system.log` con información detallada de cada ejecución.

### Base de datos
La base de datos `rpa_database.db` contiene:
- Registros de todos los correos procesados
- Estado de cada procesamiento
- Errores y observaciones
- Estadísticas del sistema

### Consultar estadísticas
```python
from database import Database

db = Database()
stats = db.get_statistics()
print(f"Total registros: {stats['total_records']}")
print(f"Registros de hoy: {stats['today_records']}")
```

## 🔧 Personalización

### Cambiar selector del botón
Edita `BUTTON_SELECTOR` en `.env`:
```env
# Ejemplos de selectores CSS
BUTTON_SELECTOR=button[type="submit"]
BUTTON_SELECTOR=.btn-primary
BUTTON_SELECTOR=#confirm-button
BUTTON_SELECTOR=input[value="Confirmar"]
```

### Cambiar filtro de remitente
```env
SENDER_FILTER=amazon.com
SENDER_FILTER=@spotify.com
SENDER_FILTER=notifications@company.com
```

### Cambiar patrón de links
```env
# Links de Netflix
LINK_PATTERN=https://www\.netflix\.com/[^\s<>"]+

# Links específicos
LINK_PATTERN=https://example\.com/confirm/[^\s<>"]+
```

## 🐛 Solución de problemas

### Error de conexión IMAP
- Verifica credenciales en `.env`
- Asegúrate de usar contraseña de aplicación para Gmail
- Verifica configuración del servidor IMAP

### Error de Chrome/Selenium
- Instala Chrome: `sudo apt install chromium-browser`
- Instala ChromeDriver: `sudo apt install chromium-chromedriver`
- O usa webdriver-manager para instalación automática

### Error de permisos
```bash
chmod +x main.py
chmod 600 .env
```

### Logs detallados
```bash
python main.py --debug
```

## 🔮 Futuras mejoras

- [ ] Bot de Telegram para administración
- [ ] Interfaz web para monitoreo
- [ ] Notificaciones por email/SMS
- [ ] Múltiples cuentas de correo
- [ ] Procesamiento en paralelo
- [ ] API REST para integración

## 📝 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---

**Nota**: Este sistema está diseñado para funcionar en VPS sin interfaz gráfica y es compatible con futuras integraciones de Telegram. 