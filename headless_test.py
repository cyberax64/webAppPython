#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import configparser
from PyQt5.QtCore import QUrl, QDir, QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from PyQt5.QtWebEngineCore import QWebEngineCookieStore

def load_config():
    """Charge la configuration depuis le fichier config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not os.path.exists(config_path):
        print(f"Erreur: Le fichier de configuration '{config_path}' n'existe pas.")
        sys.exit(1)
    
    config.read(config_path)
    
    try:
        url = config.get('WebApp', 'url')
        title = config.get('WebApp', 'window_title')
        width = config.getint('WebApp', 'window_width')
        height = config.getint('WebApp', 'window_height')
        return url, title, width, height
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Erreur dans le fichier de configuration: {e}")
        sys.exit(1)

def main():
    # Création de l'application sans interface graphique
    app = QCoreApplication(sys.argv)
    
    # Chargement de la configuration
    url, title, width, height = load_config()
    
    # Affichage des informations de configuration
    print(f"Configuration chargée avec succès:")
    print(f"URL: {url}")
    print(f"Titre: {title}")
    print(f"Dimensions: {width}x{height}")
    
    # Création du profil pour gérer les cookies
    profile = QWebEngineProfile("WebAppProfile")
    cookie_store = profile.cookieStore()
    
    # Définir le chemin pour stocker les cookies
    data_path = os.path.join(QDir.currentPath(), "cookies")
    profile.setPersistentStoragePath(data_path)
    print(f"Cookies stockés dans: {data_path}")
    
    print("Test de configuration réussi!")
    sys.exit(0)

if __name__ == "__main__":
    main()