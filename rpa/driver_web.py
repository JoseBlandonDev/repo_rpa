#!/usr/bin/env python3
"""
Módulo para automatización web
Contiene funciones para abrir páginas web y hacer clic en botones usando Selenium.
"""

import os
import time
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class WebDriver:
    """
    Clase para manejar la automatización web usando Selenium.
    """
    
    def __init__(self):
        """
        Inicializa el driver web con configuración desde variables de entorno.
        """
        load_dotenv()
        
        self.button_selector = os.getenv('BUTTON_SELECTOR', 'button')
        self.timeout = int(os.getenv('TIMEOUT_SECONDS', '10'))
        self.driver = None
        
    def _setup_driver(self) -> webdriver.Chrome:
        """
        Configura y retorna una instancia del driver de Chrome en modo headless.
        
        Returns:
            webdriver.Chrome: Driver configurado
        """
        chrome_options = Options()
        
        # Configuración para modo headless y VPS
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        
        # Configuraciones adicionales para estabilidad
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        # chrome_options.add_argument('--disable-javascript')  # Descomenta si no necesitas JS
        
        # Configuraciones para evitar descargas automáticas
        chrome_options.add_argument('--disable-background-downloads')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        
        # Configuración para usar cache local y evitar descargas
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.timeout)
            return driver
            
        except Exception as e:
            logger.error(f"Error inicializando Chrome driver: {str(e)}")
            raise
    
    def click_button_on_page(self, url: str) -> bool:
        """
        Abre una URL y hace clic en el botón especificado por el selector CSS.
        
        Args:
            url: URL de la página a abrir
            
        Returns:
            bool: True si se hizo clic exitosamente, False en caso contrario
        """
        try:
            logger.info(f"Abriendo URL: {url}")
            
            # Inicializar driver
            self.driver = self._setup_driver()
            
            # Navegar a la URL
            self.driver.get(url)
            logger.info("Página cargada exitosamente")
            
            # Esperar a que el botón esté presente y hacer clic
            wait = WebDriverWait(self.driver, self.timeout)
            button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.button_selector))
            )
            
            logger.info(f"Botón encontrado con selector: {self.button_selector}")
            
            # Hacer clic en el botón
            button.click()
            logger.info("Clic realizado exitosamente")
            
            # Esperar un momento para que la acción se complete
            time.sleep(2)
            
            return True
            
        except TimeoutException:
            logger.error(f"Timeout esperando el botón con selector: {self.button_selector}")
            return False
            
        except WebDriverException as e:
            logger.error(f"Error del driver web: {str(e)}")
            return False
            
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return False
            
        finally:
            # Cerrar el driver
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info("Driver cerrado")
                except Exception as e:
                    logger.warning(f"Error cerrando driver: {str(e)}")
    
    def get_page_title(self, url: str) -> Optional[str]:
        """
        Obtiene el título de una página web.
        
        Args:
            url: URL de la página
            
        Returns:
            Optional[str]: Título de la página o None si hay error
        """
        try:
            self.driver = self._setup_driver()
            self.driver.get(url)
            title = self.driver.title
            return title
            
        except Exception as e:
            logger.error(f"Error obteniendo título de la página: {str(e)}")
            return None
            
        finally:
            if self.driver:
                self.driver.quit() 