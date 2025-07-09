#!/usr/bin/env python3
"""
Sistema de Automatización RPA - Archivo Principal
Orquesta todo el flujo de lectura de correos, extracción de links y automatización web.
"""

import os
import logging
import time
from datetime import datetime, date
from dotenv import load_dotenv

# Importar módulos del sistema
from email_reader import EmailReader
from driver_web import WebDriver
from database import Database

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rpa_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_emails():
    """
    Función que procesa los correos electrónicos.
    """
    try:
        # Cargar variables de entorno
        load_dotenv()
        
        # Inicializar componentes
        db = Database()
        email_reader = EmailReader()
        web_driver = WebDriver()
        
        # Leer correos no leídos
        logger.info("Leyendo correos no leídos...")
        emails = email_reader.get_unread_emails()
        
        if not emails:
            logger.info("No se encontraron correos no leídos")
            return
        
        logger.info(f"Se encontraron {len(emails)} correos no leídos")
        
        # Procesar cada correo
        for email in emails:
            try:
                # Extraer link del correo
                link = email_reader.extract_link_from_email(email)
                
                if link:
                    logger.info(f"Link extraído: {link}")
                    
                    # Abrir link y hacer clic en botón
                    success = web_driver.click_button_on_page(link)
                    
                    # Registrar en base de datos
                    db.insert_record(
                        sender=email.from_,
                        subject=email.subject,
                        link=link,
                        status="SUCCESS" if success else "FAILED",
                        observations="Procesado correctamente" if success else "Error al hacer clic en botón"
                    )
                    
                    logger.info(f"Correo procesado: {email.subject}")
                else:
                    logger.warning(f"No se pudo extraer link del correo: {email.subject}")
                    db.insert_record(
                        sender=email.from_,
                        subject=email.subject,
                        link="",
                        status="NO_LINK",
                        observations="No se encontró link válido"
                    )
                    
            except Exception as e:
                logger.error(f"Error procesando correo {email.subject}: {str(e)}")
                db.insert_record(
                    sender=email.from_,
                    subject=email.subject,
                    link="",
                    status="ERROR",
                    observations=f"Error: {str(e)}"
                )
        
        logger.info("Proceso completado")
        
    except Exception as e:
        logger.error(f"Error general en el sistema: {str(e)}")

def should_run_cleanup(flag_path: str) -> bool:
    """
    Determina si debe ejecutarse la limpieza de la base de datos (una vez al día).
    """
    today = date.today().isoformat()
    if not os.path.exists(flag_path):
        return True
    with open(flag_path, 'r') as f:
        last_run = f.read().strip()
    return last_run != today

def update_cleanup_flag(flag_path: str):
    """
    Actualiza el archivo de marca de tiempo de limpieza.
    """
    today = date.today().isoformat()
    with open(flag_path, 'w') as f:
        f.write(today)

def main():
    """
    Función principal que ejecuta el sistema RPA en modo continuo.
    """
    logger.info("Iniciando sistema RPA en modo continuo...")
    cleanup_flag = "db_cleanup.flag"
    db = Database()
    while True:
        try:
            # Limpieza automática una vez al día
            if should_run_cleanup(cleanup_flag):
                eliminados = db.delete_old_records(days=30)
                logger.info(f"Limpieza diaria: {eliminados} registros eliminados por antigüedad.")
                update_cleanup_flag(cleanup_flag)
            process_emails()
            logger.info("Esperando 60 segundos antes del siguiente ciclo...")
            time.sleep(60)  # Esperar 60 segundos (1 minuto)
        except KeyboardInterrupt:
            logger.info("Sistema detenido por el usuario")
            break
        except Exception as e:
            logger.error(f"Error en el ciclo principal: {str(e)}")
            logger.info("Esperando 60 segundos antes de reintentar...")
            time.sleep(60)

if __name__ == "__main__":
    main() 