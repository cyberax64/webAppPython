#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Version alternative de l'application utilisant CEF Python (Chromium Embedded Framework)
pour un rendu plus fidèle des pages web.

Nécessite l'installation de cefpython3 : pip install cefpython3
"""

import sys
import os
import platform
import configparser
import json
import http.cookiejar
from cefpython3 import cefpython as cef
import ctypes

# Fonction pour charger la configuration
def load_config():
    """Charge la configuration depuis le fichier config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not os.path.exists(config_path):
        print(f"Erreur: Le fichier de configuration '{config_path}' n'existe pas.")
        sys.exit(1)
    
    config.read(config_path, encoding='utf-8')
    
    try:
        url = config.get('WebApp', 'url')
        title = config.get('WebApp', 'window_title')
        width = config.getint('WebApp', 'window_width')
        height = config.getint('WebApp', 'window_height')
        return url, title, width, height
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Erreur dans le fichier de configuration: {e}")
        sys.exit(1)

def is_graphical_environment():
    """Détecte si l'environnement actuel est graphique"""
    system = platform.system()
    
    if system == "Windows":
        # Sur Windows, on suppose qu'un environnement graphique est toujours disponible
        return True
    elif system == "Darwin":
        # Sur macOS, on suppose qu'un environnement graphique est toujours disponible
        return True
    else:
        # Sur Linux, vérifier la variable d'environnement DISPLAY
        return "DISPLAY" in os.environ

class WebApp:
    def __init__(self, url, title, width, height):
        self.url = url
        self.title = title
        self.width = width
        self.height = height
        self.browser = None
        self.window_info = None
        self.cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies")
        os.makedirs(self.cookies_path, exist_ok=True)
        
        # Configuration de CEF
        settings = {
            "cache_path": self.cookies_path,
            "persist_session_cookies": True,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "product_version": "Chrome/91.0.4472.124",
            "log_severity": cef.LOGSEVERITY_WARNING,
            "persist_user_preferences": True,
            "remote_debugging_port": 0,
        }
        
        if platform.system() == "Windows":
            # DPI awareness pour Windows
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
            except:
                pass
        
        # Initialiser CEF
        cef.Initialize(settings=settings)
        
        # Créer la fenêtre
        self.create_window()
        
    def create_window(self):
        # Créer la fenêtre
        self.window_info = cef.WindowInfo()
        
        if platform.system() == "Windows":
            # Créer une fenêtre Windows
            window_title = self.title
            window_style = (
                0x00C00000 |  # WS_CAPTION
                0x00080000 |  # WS_SYSMENU
                0x00040000 |  # WS_SIZEBOX
                0x00020000 |  # WS_MINIMIZEBOX
                0x00010000    # WS_MAXIMIZEBOX
            )
            
            parent = 0
            rect = [0, 0, self.width, self.height]
            self.window_info.SetAsChild(parent, rect)
            self.window_info.SetAsPopup(parent, window_title)
            self.window_info.style = window_style
            
        elif platform.system() == "Linux":
            # Créer une fenêtre Linux
            parent = 0
            rect = [0, 0, self.width, self.height]
            self.window_info.SetAsChild(parent, rect)
            
        elif platform.system() == "Darwin":
            # Créer une fenêtre macOS
            parent = 0
            rect = [0, 0, self.width, self.height]
            self.window_info.SetAsChild(parent, rect)
        
        # Créer le navigateur
        browser_settings = {
            "web_security_disabled": False,
            "file_access_from_file_urls_allowed": True,
            "universal_access_from_file_urls_allowed": True,
        }
        
        self.browser = cef.CreateBrowserSync(
            window_info=self.window_info,
            url=self.url,
            settings=browser_settings
        )
        
        # Configurer le gestionnaire de fenêtre
        self.browser.SetClientHandler(ClientHandler(self.title))
        
        # Centrer la fenêtre
        if platform.system() == "Windows":
            window_handle = self.browser.GetWindowHandle()
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            screen_height = ctypes.windll.user32.GetSystemMetrics(1)
            x = (screen_width - self.width) // 2
            y = (screen_height - self.height) // 2
            ctypes.windll.user32.SetWindowPos(window_handle, 0, x, y, self.width, self.height, 0)
    
    def close(self):
        # Fermer le navigateur
        if self.browser:
            self.browser.CloseBrowser(True)
            self.browser = None
        
        # Fermer CEF
        cef.Shutdown()

class ClientHandler:
    def __init__(self, title):
        self.title = title
    
    def OnTitleChange(self, browser, title):
        # Mettre à jour le titre de la fenêtre
        if platform.system() == "Windows":
            window_handle = browser.GetWindowHandle()
            ctypes.windll.user32.SetWindowTextW(window_handle, self.title)

def main():
    # Vérifier si on est dans un environnement graphique
    if not is_graphical_environment():
        print("Aucun environnement graphique détecté. Exécution en mode test...")
        # Chargement de la configuration
        url, title, width, height = load_config()
        print(f"Configuration chargée avec succès:")
        print(f"URL: {url}")
        print(f"Titre: {title}")
        print(f"Dimensions: {width}x{height}")
        print(f"Cookies stockés dans: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies')}")
        print("Pour exécuter l'application, utilisez un environnement avec interface graphique.")
        sys.exit(0)
    
    # Chargement de la configuration
    url, title, width, height = load_config()
    
    # Créer l'application
    app = WebApp(url, title, width, height)
    
    # Exécuter la boucle de message
    cef.MessageLoop()
    
    # Fermer l'application
    app.close()

if __name__ == "__main__":
    main()