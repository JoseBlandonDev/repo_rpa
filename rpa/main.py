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
from imap_tools.mailbox import MailBox
from imap_tools.query import AND

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
        
        # Leer todos los correos no leídos (sin filtrar remitente)
        with MailBox(email_reader.imap_server).login(email_reader.email, email_reader.password) as mailbox:
            all_unread_emails = list(mailbox.fetch('(UNSEEN)', mark_seen=False, bulk=True))
        # Procesar solicitudes de reporte para cualquier remitente
        email_reader.process_report_requests(all_unread_emails)
        # Leer solo los correos no leídos del remitente filtrado para procesar URLs
        filtered_emails = [email for email in all_unread_emails if email.from_.lower() == email_reader.sender_filter.lower()]
        emails_to_process = [email for email in filtered_emails if not ("REPORTE" in email.subject.upper() or "REPORTE" in email.text.upper())]
        if not emails_to_process:
            logger.info("No se encontraron correos no leídos para procesar")
            return
        logger.info(f"Se encontraron {len(emails_to_process)} correos no leídos para procesar")
        
        # Procesar cada correo
        for email in emails_to_process:
            try:
                # Extraer link del correo
                link = email_reader.extract_link_from_email(email)
                
                if link:
                    logger.info(f"Link extraído: {link}")
                    
                    # Abrir link y hacer clic en botón
                    success = web_driver.click_button_on_page(link)
                    
                    if success:
                        db.insert_success_record(
                            sender=email.from_,
                            subject=email.subject,
                            link=link,
                            status="SUCCESS",
                            observations="Procesado correctamente"
                        )
                    else:
                        db.insert_failed_record(
                            sender=email.from_,
                            subject=email.subject,
                            link=link,
                            status="FAILED",
                            observations="Error al hacer clic en botón"
                        )
                    logger.info(f"Correo procesado: {email.subject}")
                else:
                    logger.warning(f"No se pudo extraer link del correo: {email.subject}")
                    db.insert_failed_record(
                        sender=email.from_,
                        subject=email.subject,
                        link="",
                        status="NO_LINK",
                        observations="No se encontró link válido"
                    )
                    
            except Exception as e:
                logger.error(f"Error procesando correo {email.subject}: {str(e)}")
                db.insert_failed_record(
                    sender=email.from_,
                    subject=email.subject,
                    link="",
                    status="ERROR",
                    observations=f"Error: {str(e)}",
                    error_details=str(e)
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