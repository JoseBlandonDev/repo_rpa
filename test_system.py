#!/usr/bin/env python3
"""
Archivo de prueba para el Sistema de Automatización RPA
Permite verificar que todos los componentes del sistema funcionan correctamente.
"""

import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

# Agregar el directorio rpa al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'rpa'))

# Importar módulos del sistema
from rpa.database import Database
from rpa.email_reader import EmailReader
from rpa.driver_web import WebDriver

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_database():
    """
    Prueba la funcionalidad de la base de datos.
    """
    logger.info("🧪 Probando base de datos...")
    try:
        db = Database()
        
        # Probar inserción de registro
        test_record = {
            'sender': 'test@example.com',
            'subject': 'Test Subject',
            'link': 'https://example.com/test',
            'status': 'TEST',
            'observations': 'Registro de prueba'
        }
        
        db.insert_record(**test_record)
        logger.info("✅ Inserción en base de datos exitosa")
        
        # Probar obtención de estadísticas
        stats = db.get_statistics()
        logger.info(f"✅ Estadísticas obtenidas: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de base de datos: {str(e)}")
        return False

def test_email_reader():
    """
    Prueba la funcionalidad del lector de correos.
    """
    logger.info("🧪 Probando lector de correos...")
    try:
        email_reader = EmailReader()
        
        # Probar conexión IMAP
        connection = email_reader.connect()
        if connection:
            logger.info("✅ Conexión IMAP exitosa")
            connection.logout()
        else:
            logger.warning("⚠️ No se pudo conectar a IMAP (verificar configuración)")
        
        # Probar extracción de links
        test_email_content = """
        Hola, aquí tienes un link: https://www.netflix.com/watch/123456
        Y otro link: https://example.com/test
        """
        
        links = email_reader.extract_links(test_email_content)
        logger.info(f"✅ Links extraídos: {links}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de lector de correos: {str(e)}")
        return False

def test_web_driver():
    """
    Prueba la funcionalidad del driver web.
    """
    logger.info("🧪 Probando driver web...")
    try:
        web_driver = WebDriver()
        
        # Probar inicialización del driver
        driver = web_driver.initialize_driver()
        if driver:
            logger.info("✅ Driver web inicializado correctamente")
            
            # Probar navegación a una página simple
            driver.get("https://httpbin.org/html")
            title = driver.title
            logger.info(f"✅ Navegación exitosa - Título: {title}")
            
            # Cerrar driver
            driver.quit()
            logger.info("✅ Driver web cerrado correctamente")
        else:
            logger.warning("⚠️ No se pudo inicializar el driver web")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de driver web: {str(e)}")
        return False

def test_configuration():
    """
    Prueba que la configuración esté correctamente cargada.
    """
    logger.info("🧪 Probando configuración...")
    try:
        load_dotenv()
        
        required_vars = [
            'IMAP_SERVER',
            'IMAP_PORT', 
            'EMAIL_ADDRESS',
            'EMAIL_PASSWORD',
            'SENDER_FILTER',
            'LINK_PATTERN',
            'BUTTON_SELECTOR',
            'TIMEOUT_SECONDS',
            'DB_PATH'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.warning(f"⚠️ Variables de entorno faltantes: {missing_vars}")
            logger.info("💡 Copia env.example a .env y configura las variables")
        else:
            logger.info("✅ Todas las variables de entorno están configuradas")
        
        return len(missing_vars) == 0
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de configuración: {str(e)}")
        return False

def main():
    """
    Función principal que ejecuta todas las pruebas del sistema.
    """
    logger.info("🚀 Iniciando pruebas del sistema RPA...")
    
    tests = [
        ("Configuración", test_configuration),
        ("Base de datos", test_database),
        ("Lector de correos", test_email_reader),
        ("Driver web", test_web_driver)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Ejecutando prueba: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ Error inesperado en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Resumen de resultados
    logger.info(f"\n{'='*50}")
    logger.info("📊 RESUMEN DE PRUEBAS")
    logger.info(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\nResultado final: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        logger.info("🎉 ¡Todas las pruebas pasaron! El sistema está listo para usar.")
    else:
        logger.warning("⚠️ Algunas pruebas fallaron. Revisa los logs para más detalles.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 