# 🚀 Comandos Rápidos - Sistema RPA

## ⚡ Comandos Esenciales (Copia y pega)

### ✅ Verificar si está funcionando
```bash
sudo systemctl status rpa_system
```

### ⏹️ Detener el sistema
```bash
sudo systemctl stop rpa_system
```

### ▶️ Iniciar el sistema
```bash
sudo systemctl start rpa_system
```

### 🔄 Reiniciar el sistema
```bash
sudo systemctl restart rpa_system
```

### 📊 Ver logs en tiempo real
```bash
sudo journalctl -u rpa_system -f
```

### 📋 Ver logs recientes
```bash
sudo journalctl -u rpa_system -n 20
```

---

## 🎮 Gestor Interactivo

Para usar el gestor con menú:
```bash
./gestionar_rpa.sh
```

---

## 🆘 Emergencias

### Detener todo inmediatamente
```bash
sudo systemctl stop rpa_system
sudo pkill -f "python3 rpa/main.py"
```

### Reiniciar completamente
```bash
sudo systemctl restart rpa_system
sudo systemctl status rpa_system
```

---

## 📈 Información del Sistema

### Ver archivo de log
```bash
tail -20 rpa_system.log
```

### Ver base de datos
```bash
ls -la rpa_database.db
```

### Ver logs de hoy
```bash
sudo journalctl -u rpa_system --since today
```

---

## 💡 Tips

- **Siempre usa `sudo`** antes de los comandos
- **Presiona `Ctrl + C`** para salir de logs en tiempo real
- **El sistema se reinicia automáticamente** si se detiene
- **Los logs se guardan automáticamente**

---

**🎯 ¡Solo necesitas estos comandos para gestionar tu sistema RPA!** 