#!/bin/bash

# Script para ejecutar el sistema RPA
# Este script es llamado por cron cada 10 minutos

# Cambiar al directorio del proyecto
cd /root/rpa_system

# Activar el entorno virtual
source venv/bin/activate

# Ejecutar el sistema RPA
python rpa/main.py

# Log de ejecución
echo "$(date): Sistema RPA ejecutado" >> /tmp/rpa_cron.log 