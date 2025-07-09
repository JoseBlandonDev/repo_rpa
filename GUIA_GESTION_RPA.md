# 🎯 Guía de Gestión del Sistema RPA

Guía completa para gestionar el sistema RPA desde la terminal. **No necesitas conocimientos técnicos avanzados.**

---

## 📋 Índice Rápido

- [🔍 Verificar si está funcionando](#verificar-si-está-funcionando)
- [⏹️ Detener el sistema](#detener-el-sistema)
- [▶️ Iniciar el sistema](#iniciar-el-sistema)
- [🔄 Reiniciar el sistema](#reiniciar-el-sistema)
- [📊 Ver logs en tiempo real](#ver-logs-en-tiempo-real)
- [📈 Ver estadísticas](#ver-estadísticas)
- [🔧 Solucionar problemas](#solucionar-problemas)

---

## 🔍 Verificar si está funcionando

### Opción 1: Comando simple
```bash
sudo systemctl status rpa_system
```

**¿Qué significa la respuesta?**
- ✅ **`active (running)`** = El sistema está funcionando perfectamente
- ❌ **`inactive (dead)`** = El sistema está detenido
- ⚠️ **`failed`** = Hay un problema, necesita reiniciarse

### Opción 2: Verificar procesos
```bash
ps aux | grep python
```
**Busca una línea que contenga `rpa/main.py`** - si aparece, está funcionando.

---

## ⏹️ Detener el sistema

### Detener temporalmente
```bash
sudo systemctl stop rpa_system
```

### Verificar que se detuvo
```bash
sudo systemctl status rpa_system
```
**Debería mostrar: `inactive (dead)`**

---

## ▶️ Iniciar el sistema

### Iniciar el servicio
```bash
sudo systemctl start rpa_system
```

### Verificar que inició correctamente
```bash
sudo systemctl status rpa_system
```
**Debería mostrar: `active (running)`**

---

## 🔄 Reiniciar el sistema

### Reiniciar (detener + iniciar automáticamente)
```bash
sudo systemctl restart rpa_system
```

### Verificar después del reinicio
```bash
sudo systemctl status rpa_system
```

---

## 📊 Ver logs en tiempo real

### Ver logs actuales (últimos 20 mensajes)
```bash
sudo journalctl -u rpa_system -n 20
```

### Ver logs en tiempo real (como Netflix)
```bash
sudo journalctl -u rpa_system -f
```
**Para salir de esta vista: presiona `Ctrl + C`**

### Ver logs de hoy
```bash
sudo journalctl -u rpa_system --since today
```

---

## 📈 Ver estadísticas

### Ver el archivo de log del sistema
```bash
tail -20 rpa_system.log
```

### Ver la base de datos (información técnica)
```bash
ls -la rpa_database.db
```

---

## 🔧 Solucionar problemas

### Problema: El sistema no inicia
```bash
# 1. Verificar el error
sudo journalctl -u rpa_system -n 10

# 2. Reiniciar el servicio
sudo systemctl restart rpa_system

# 3. Verificar que funcionó
sudo systemctl status rpa_system
```

### Problema: El sistema se detiene constantemente
```bash
# 1. Ver logs de errores
sudo journalctl -u rpa_system --since "1 hour ago"

# 2. Reiniciar completamente
sudo systemctl stop rpa_system
sudo systemctl start rpa_system

# 3. Verificar estado
sudo systemctl status rpa_system
```

### Problema: No puedo ejecutar comandos
```bash
# Verificar que tienes permisos
whoami

# Si no eres root, usar sudo
sudo systemctl status rpa_system
```

---

## 🎯 Comandos de Emergencia

### Detener todo inmediatamente
```bash
sudo systemctl stop rpa_system
sudo pkill -f "python3 rpa/main.py"
```

### Reiniciar completamente
```bash
sudo systemctl stop rpa_system
sudo systemctl start rpa_system
sudo systemctl status rpa_system
```

### Ver qué está pasando ahora mismo
```bash
sudo journalctl -u rpa_system -f
```

---

## 📱 Comandos Rápidos (Copia y pega)

### ✅ Verificar estado
```bash
sudo systemctl status rpa_system
```

### ⏹️ Detener
```bash
sudo systemctl stop rpa_system
```

### ▶️ Iniciar
```bash
sudo systemctl start rpa_system
```

### 🔄 Reiniciar
```bash
sudo systemctl restart rpa_system
```

### 📊 Ver logs
```bash
sudo journalctl -u rpa_system -f
```

---

## 🆘 ¿Necesitas ayuda?

### Si algo no funciona:

1. **Copia y pega este comando para ver el error:**
   ```bash
   sudo journalctl -u rpa_system -n 20
   ```

2. **Reinicia el sistema:**
   ```bash
   sudo systemctl restart rpa_system
   ```

3. **Verifica que funcionó:**
   ```bash
   sudo systemctl status rpa_system
   ```

### Respuestas comunes:

- **"Unit not found"** = El servicio no está instalado
- **"Permission denied"** = Usa `sudo` antes del comando
- **"Connection refused"** = El sistema está detenido

---

## 💡 Tips útiles

- **Siempre usa `sudo`** antes de los comandos
- **Presiona `Ctrl + C`** para salir de los logs en tiempo real
- **El sistema se reinicia automáticamente** si se detiene
- **Los logs se guardan automáticamente** - no se pierden

---

**🎉 ¡Ya sabes gestionar tu sistema RPA!** 

El sistema está configurado para funcionar automáticamente, pero ahora puedes controlarlo cuando lo necesites. 