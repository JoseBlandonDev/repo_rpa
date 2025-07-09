#!/bin/bash

# Script para gestionar el Sistema RPA
# Uso: ./gestionar_rpa.sh

clear
echo "🎯 GESTOR DEL SISTEMA RPA"
echo "=========================="
echo ""

# Función para mostrar el estado
mostrar_estado() {
    echo "📊 Estado actual del sistema:"
    sudo systemctl status rpa_system --no-pager -l
    echo ""
}

# Función para ver logs
ver_logs() {
    echo "📋 Últimos 10 logs del sistema:"
    sudo journalctl -u rpa_system -n 10 --no-pager
    echo ""
}

# Función para ver logs en tiempo real
logs_tiempo_real() {
    echo "🔍 Mostrando logs en tiempo real..."
    echo "Presiona Ctrl+C para salir"
    echo ""
    sudo journalctl -u rpa_system -f
}

# Función para detener el sistema
detener_sistema() {
    echo "⏹️ Deteniendo el sistema RPA..."
    sudo systemctl stop rpa_system
    echo "✅ Sistema detenido"
    echo ""
}

# Función para iniciar el sistema
iniciar_sistema() {
    echo "▶️ Iniciando el sistema RPA..."
    sudo systemctl start rpa_system
    echo "✅ Sistema iniciado"
    echo ""
}

# Función para reiniciar el sistema
reiniciar_sistema() {
    echo "🔄 Reiniciando el sistema RPA..."
    sudo systemctl restart rpa_system
    echo "✅ Sistema reiniciado"
    echo ""
}

# Menú principal
while true; do
    echo "Selecciona una opción:"
    echo ""
    echo "1️⃣  Ver estado del sistema"
    echo "2️⃣  Ver logs recientes"
    echo "3️⃣  Ver logs en tiempo real"
    echo "4️⃣  Detener sistema"
    echo "5️⃣  Iniciar sistema"
    echo "6️⃣  Reiniciar sistema"
    echo "7️⃣  Ver archivo de log"
    echo "8️⃣  Salir"
    echo ""
    read -p "Ingresa el número de la opción: " opcion
    
    case $opcion in
        1)
            mostrar_estado
            ;;
        2)
            ver_logs
            ;;
        3)
            logs_tiempo_real
            ;;
        4)
            detener_sistema
            mostrar_estado
            ;;
        5)
            iniciar_sistema
            mostrar_estado
            ;;
        6)
            reiniciar_sistema
            mostrar_estado
            ;;
        7)
            echo "📄 Contenido del archivo de log:"
            tail -20 rpa_system.log
            echo ""
            ;;
        8)
            echo "👋 ¡Hasta luego!"
            exit 0
            ;;
        *)
            echo "❌ Opción no válida. Intenta de nuevo."
            echo ""
            ;;
    esac
    
    read -p "Presiona Enter para continuar..."
    clear
    echo "🎯 GESTOR DEL SISTEMA RPA"
    echo "=========================="
    echo ""
done 