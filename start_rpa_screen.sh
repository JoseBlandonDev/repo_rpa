#!/bin/bash

# Script para ejecutar el sistema RPA usando screen
# Ubicación: /root/rpa_system/start_rpa_screen.sh

cd /root/rpa_system

# Crear una nueva sesión de screen llamada "rpa_system"
screen -dmS rpa_system bash -c "while true; do python3 rpa/main.py; sleep 60; done"

echo "Sistema RPA iniciado en sesión de screen 'rpa_system'"
echo "Para ver los logs: screen -r rpa_system"
echo "Para detener: screen -X -S rpa_system quit" 