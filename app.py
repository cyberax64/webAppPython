#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import platform
import configparser
import json
import http.cookiejar
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
try:
    from PyQt5.QtWebEngineCore import QWebEngineCookieStore
except ImportError:
    # Dans certaines versions de PyQt5, QWebEngineCookieStore est dans QtWebEngineWidgets
    pass

class CustomWebPage(QWebEnginePage):
    """Page web personnalisée pour utiliser un profil spécifique"""
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)

class WebApp(QMainWindow):
    def __init__(self, url, title, width, height):
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.setWindowTitle(title)
        self.resize(width, height)
        
        # Définir le chemin pour stocker les cookies
        self.data_path = os.path.join(QDir.currentPath(), "cookies")
        os.makedirs(self.data_path, exist_ok=True)
        
        # Création du profil pour gérer les cookies
        self.profile = QWebEngineProfile("WebAppProfile", self)
        self.profile.setPersistentStoragePath(self.data_path)
        
        try:
            # Essayer d'accéder au cookie store (peut ne pas être disponible dans toutes les versions)
            self.cookie_store = self.profile.cookieStore()
            # Connecter les signaux pour la gestion des cookies si disponible
            self.cookie_store.cookieAdded.connect(self.on_cookie_added)
            # Charger les cookies existants
            self.load_cookies()
        except (AttributeError, NameError):
            print("Avertissement: La gestion avancée des cookies n'est pas disponible dans cette version de PyQt5.")
            print("Les cookies seront toujours stockés, mais certaines fonctionnalités peuvent être limitées.")
        
        # Création de la vue web avec une page personnalisée
        self.web_view = QWebEngineView(self)
        
        # Créer une page web personnalisée avec notre profil
        custom_page = CustomWebPage(self.profile, self.web_view)
        self.web_view.setPage(custom_page)
        
        # Chargement de l'URL
        self.web_view.load(QUrl(url))
        
        # Définir la vue web comme widget central
        self.setCentralWidget(self.web_view)
        
        # Supprimer les menus et barres d'outils
        self.setMenuBar(None)
        self.setStatusBar(None)
    
    def on_cookie_added(self, cookie):
        """Appelé lorsqu'un cookie est ajouté"""
        # Les cookies sont déjà gérés par QWebEngineProfile, mais on peut
        # ajouter une logique supplémentaire ici si nécessaire
        pass
    
    def load_cookies(self):
        """Charge les cookies depuis le stockage persistant"""
        # QWebEngineProfile gère automatiquement le chargement des cookies
        # depuis le stockage persistant, donc cette méthode est principalement
        # pour la documentation et pour ajouter une logique supplémentaire si nécessaire
        pass

def load_config():
    """Charge la configuration depuis le fichier config.ini"""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not os.path.exists(config_path):
        print(f"Erreur: Le fichier de configuration '{config_path}' n'existe pas.")
        sys.exit(1)
    
    config.read(config_path, encoding='utf-8')  # Spécifier l'encodage pour la compatibilité Windows
    
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
        print(f"Cookies stockés dans: {os.path.join(QDir.currentPath(), 'cookies')}")
        print("Pour exécuter l'application, utilisez un environnement avec interface graphique.")
        sys.exit(0)
    
    # Création de l'application
    app = QApplication(sys.argv)
    
    # Chargement de la configuration
    url, title, width, height = load_config()
    
    # Création et affichage de la fenêtre
    web_app = WebApp(url, title, width, height)
    web_app.show()
    
    # Exécution de l'application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()