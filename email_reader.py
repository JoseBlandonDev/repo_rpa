#!/usr/bin/env python3
"""
Módulo para lectura de correos electrónicos
Contiene funciones para conectar a IMAP, leer correos no leídos y extraer links.
"""

import os
import re
import logging
from typing import List, Optional
from imap_tools import MailBox, AND
from dotenv import load_dotenv
import quopri
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class EmailReader:
    """
    Clase para manejar la lectura de correos electrónicos via IMAP.
    """
    
    def __init__(self):
        """
        Inicializa el lector de correos con configuración desde variables de entorno.
        """
        load_dotenv()
        
        self.imap_server = os.getenv('IMAP_SERVER', 'imap.gmail.com')
        self.imap_port = int(os.getenv('IMAP_PORT', '993'))
        self.email = os.getenv('EMAIL_ADDRESS')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.sender_filter = os.getenv('SENDER_FILTER', 'netflix.com')
        self.link_pattern = os.getenv('LINK_PATTERN', r'https?://[^\s<>"]+')
        
        if not self.email or not self.password:
            raise ValueError("EMAIL_ADDRESS y EMAIL_PASSWORD deben estar configurados en .env")
    
    def get_unread_emails(self) -> List:
        """
        Obtiene todos los correos no leídos que coincidan con el filtro de remitente.
        
        Returns:
            List: Lista de correos no leídos filtrados
        """
        try:
            with MailBox(self.imap_server).login(self.email, self.password) as mailbox:
                # Filtrar correos no leídos del remitente específico
                emails = mailbox.fetch(
                    AND(
                        seen=False,
                        from_=self.sender_filter
                    )
                )
                
                # Convertir a lista para poder iterar múltiples veces
                email_list = list(emails)
                logger.info(f"Encontrados {len(email_list)} correos no leídos de {self.sender_filter}")
                
                return email_list
                
        except Exception as e:
            logger.error(f"Error conectando al servidor IMAP: {str(e)}")
            raise
    
    def extract_link_from_email(self, email) -> Optional[str]:
        """
        Extrae el link del botón rojo de Netflix decodificando el HTML y usando BeautifulSoup.
        """
        try:
            # 1. Buscar en el HTML (decodificando si es necesario)
            if email.html:
                html = email.html
                # Decodificar si está en quoted-printable
                if 'Content-Transfer-Encoding: quoted-printable' in str(email.headers) or '=3D' in html:
                    html = quopri.decodestring(html).decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                for a in soup.find_all('a', href=True):
                    if '/account/update-primary-location' in a['href']:
                        logger.info(f"Link correcto encontrado en HTML: {a['href']}")
                        return a['href']
            # 2. Buscar en el texto plano como respaldo
            if email.text:
                text = email.text
                if '=3D' in text:
                    text = quopri.decodestring(text).decode('utf-8', errors='ignore')
                links = re.findall(self.link_pattern, text)
                for link in links:
                    if '/account/update-primary-location' in link:
                        logger.info(f"Link correcto encontrado en texto: {link}")
                        return link
            logger.warning(f"No se encontró link válido en el correo: {email.subject}")
            return None
        except Exception as e:
            logger.error(f"Error extrayendo link del correo: {str(e)}")
            return None
    
    def mark_email_as_read(self, email) -> bool:
        """
        Marca un correo como leído.
        
        Args:
            email: Objeto de correo de imap-tools
            
        Returns:
            bool: True si se marcó correctamente, False en caso contrario
        """
        try:
            with MailBox(self.imap_server).login(self.email, self.password) as mailbox:
                mailbox.seen(email.uid, True)
                logger.info(f"Correo marcado como leído: {email.subject}")
                return True
                
        except Exception as e:
            logger.error(f"Error marcando correo como leído: {str(e)}")
            return False 