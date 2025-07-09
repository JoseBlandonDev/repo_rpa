#!/bin/bash

# Script para ejecutar el sistema RPA
# Ubicación: /root/rpa_system/rpa_runner.sh

cd /root/rpa_system
python3 rpa/main.py >> /var/log/rpa_system.log 2>&1 