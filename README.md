# Sistema de Automatización RPA

Sistema automatizado para leer correos electrónicos, extraer links y realizar acciones web automáticamente con capacidades de reportes y notificaciones.

## 🎯 ¿Qué hace el sistema?

1. **Lee correos no leídos** desde una cuenta de correo (IMAP)
2. **Filtra correos** por remitente específico (ej: `netflix.com`)
3. **Extrae links** usando patrones configurables
4. **Abre páginas web** con Selenium (modo headless)
5. **Hace clic en botones** usando selectores CSS configurables
6. **Registra todo** en base de datos SQLite con logs detallados
7. **Genera reportes** en formato Excel con estadísticas
8. **Envía notificaciones** por email con reportes adjuntos
9. **Maneja errores** y recuperación automática

## 📁 Estructura del proyecto

```
rpa_system/
├── rpa/                    # Módulo principal del sistema RPA
│   ├── __init__.py         # Inicializador del módulo
│   ├── main.py             # Archivo principal que orquesta todo
│   ├── email_reader.py     # Lectura de correos electrónicos
│   ├── driver_web.py       # Automatización web con Selenium
│   ├── database.py         # Manejo de base de datos SQLite
│   └── notifier.py         # Sistema de notificaciones por email
├── config/                 # Configuraciones del sistema
│   └── env.example         # Ejemplo de variables de entorno
├── requirements.txt        # Dependencias del proyecto
├── rpa_runner.sh          # Script de ejecución del sistema
├── start_rpa_screen.sh    # Script para ejecutar en screen
├── rpa_system.service     # Archivo de servicio systemd
├── .gitignore             # Archivos a ignorar en Git
├── db_cleanup.flag        # Flag para limpieza de base de datos
├── rpa_system.log         # Logs del sistema
├── rpa_database.db        # Base de datos SQLite
├── reporte_rpa.xlsx       # Reporte generado por el sistema
└── README.md              # Esta documentación
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/JoseBlandonDev/repo_rpa.git
cd repo_rpa/rpa_system
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
cp config/env.example .env
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

# Configuración de la base de datos
DB_PATH=rpa_database.db

# Configuración para notificaciones (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASS=tu_contraseña_de_aplicacion
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
python3 rpa/main.py
```

### Ejecución con script
```bash
chmod +x rpa_runner.sh
./rpa_runner.sh
```

### Ejecución en background con screen
```bash
chmod +x start_rpa_screen.sh
./start_rpa_screen.sh
```

### Ejecución como servicio systemd
```bash
# Copiar el archivo de servicio
sudo cp rpa_system.service /etc/systemd/system/

# Recargar systemd
sudo systemctl daemon-reload

# Habilitar y iniciar el servicio
sudo systemctl enable rpa_system
sudo systemctl start rpa_system

# Verificar estado
sudo systemctl status rpa_system
```

### Ejecución automática con cron
```bash
# Editar crontab
crontab -e

# Agregar línea para ejecutar cada 5 minutos
*/5 * * * * cd /ruta/a/rpa_system && python3 rpa/main.py >> /tmp/rpa.log 2>&1
```

## 📊 Monitoreo y Reportes

### Logs del sistema
Los logs se guardan en `rpa_system.log` con información detallada de cada ejecución.

### Base de datos
La base de datos `rpa_database.db` contiene:
- Registros de todos los correos procesados
- Estado de cada procesamiento
- Errores y observaciones
- Estadísticas del sistema
- Timestamps de ejecución

### Reportes Excel
El sistema genera automáticamente reportes en formato Excel (`reporte_rpa.xlsx`) con:
- Estadísticas de procesamiento
- Registros exitosos y fallidos
- Resumen de actividades por fecha
- Métricas de rendimiento

### Consultar estadísticas
```python
from rpa.database import Database

db = Database()
stats = db.get_statistics()
print(f"Total registros: {stats['total_records']}")
print(f"Registros de hoy: {stats['today_records']}")
print(f"Procesos exitosos: {stats['successful_processes']}")
print(f"Procesos fallidos: {stats['failed_processes']}")
```

### Notificaciones por email
El sistema puede enviar reportes por email usando el módulo `notifier.py`:

```python
from rpa.notifier import send_report_email

# Enviar reporte a un email específico
send_report_email("destinatario@ejemplo.com", "reporte_rpa.xlsx")
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

### Configurar notificaciones
```env
# Configuración SMTP para notificaciones
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=tu_correo@gmail.com
EMAIL_PASS=tu_contraseña_de_aplicacion
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
chmod +x rpa_runner.sh
chmod +x start_rpa_screen.sh
chmod 600 .env
```

### Logs detallados
```bash
python3 rpa/main.py --debug
```

### Verificar estado del servicio
```bash
sudo systemctl status rpa_system
sudo journalctl -u rpa_system -f
```

### Limpiar base de datos
```bash
# Crear flag para limpieza
echo "1" > db_cleanup.flag
```

## 📦 Dependencias

El proyecto utiliza las siguientes dependencias principales:

- **pandas**: Manipulación y análisis de datos
- **openpyxl**: Generación de reportes Excel
- **python-dotenv**: Manejo de variables de entorno
- **imap-tools**: Lectura de correos electrónicos
- **selenium**: Automatización web
- **webdriver-manager**: Gestión automática de drivers
- **beautifulsoup4**: Parsing de HTML

## 🔮 Funcionalidades implementadas

- ✅ **Sistema de base de datos** con SQLite
- ✅ **Generación de reportes** en Excel
- ✅ **Sistema de notificaciones** por email
- ✅ **Logs detallados** del sistema
- ✅ **Scripts de ejecución** automatizados
- ✅ **Servicio systemd** para ejecución en background
- ✅ **Manejo de errores** y recuperación
- ✅ **Configuración flexible** con variables de entorno

## 🔮 Futuras mejoras

- [ ] Bot de Telegram para administración
- [ ] Interfaz web para monitoreo
- [ ] Notificaciones por SMS
- [ ] Múltiples cuentas de correo
- [ ] Procesamiento en paralelo
- [ ] API REST para integración
- [ ] Dashboard en tiempo real
- [ ] Integración con servicios cloud

## 📝 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor:
- Abre un issue en GitHub
- Incluye logs detallados del error
- Describe los pasos para reproducir el problema

---

**Nota**: Este sistema está diseñado para funcionar en VPS sin interfaz gráfica y es compatible con futuras integraciones de Telegram y otros servicios de mensajería. 