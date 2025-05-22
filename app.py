#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import platform
import configparser
import json
import http.cookiejar
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl, QDir, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
try:
    from PyQt5.QtWebEngineCore import QWebEngineCookieStore
except ImportError:
    # Dans certaines versions de PyQt5, QWebEngineCookieStore est dans QtWebEngineWidgets
    pass

class CustomWebPage(QWebEnginePage):
    """Page web personnalisée pour utiliser un profil spécifique"""
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        
    def userAgentForUrl(self, url):
        # Utiliser un User-Agent moderne de Chrome pour une meilleure compatibilité
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    def javaScriptConsoleMessage(self, level, message, line, source):
        # Gérer les messages de la console JavaScript
        # Décommenter pour déboguer les problèmes JavaScript
        # print(f"JS [{level}] {message} (ligne {line}, source: {source})")
        pass
        
    def certificateError(self, error):
        # Ignorer les erreurs de certificat pour une meilleure compatibilité
        return True

class WebApp(QMainWindow):
    def __init__(self, url, title, width, height):
        super().__init__()
        
        # Stocker les paramètres comme attributs de l'instance
        self.url = url
        self.title = title
        self.width = width
        self.height = height
        
        # Configuration de la fenêtre principale
        self.setWindowTitle(title)
        self.resize(width, height)
        
        # Définir le chemin pour stocker les cookies
        self.data_path = os.path.join(QDir.currentPath(), "cookies")
        os.makedirs(self.data_path, exist_ok=True)
        
        # Création du profil pour gérer les cookies
        self.profile = QWebEngineProfile("WebAppProfile", self)
        self.profile.setPersistentStoragePath(self.data_path)
        
        # Configuration avancée du profil pour un meilleur rendu
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        self.profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        self.profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Activer les plugins, CSS et JavaScript
        settings = QWebEngineSettings.globalSettings()
        
        # Activer JavaScript et ses fonctionnalités
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        
        # Activer le stockage local et les cookies
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        
        # Activer les fonctionnalités multimédias et graphiques
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadIconsForPage, True)
        settings.setAttribute(QWebEngineSettings.TouchIconsEnabled, True)
        
        # Désactiver les restrictions de sécurité qui pourraient affecter le rendu
        settings.setAttribute(QWebEngineSettings.XSSAuditingEnabled, False)
        
        # Activer les fonctionnalités CSS avancées
        settings.setFontFamily(QWebEngineSettings.StandardFont, "Arial")
        settings.setFontFamily(QWebEngineSettings.FixedFont, "Courier New")
        settings.setFontSize(QWebEngineSettings.DefaultFontSize, 16)
        settings.setDefaultTextEncoding("UTF-8")
        
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
        
        # Configuration spécifique à la page
        page_settings = custom_page.settings()
        
        # Activer les barres de défilement et le mode plein écran
        page_settings.setAttribute(QWebEngineSettings.ShowScrollBars, True)
        page_settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        
        # Permettre le contenu mixte (HTTP/HTTPS) pour une meilleure compatibilité
        page_settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        page_settings.setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, True)
        
        # Activer explicitement CSS et JavaScript au niveau de la page
        page_settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        page_settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        page_settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        
        # Activer les fonctionnalités CSS avancées au niveau de la page
        page_settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        page_settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        page_settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        
        # Configurer l'encodage du texte
        page_settings.setDefaultTextEncoding("UTF-8")
        
        # Configurer la mise en cache des pages
        custom_page.setBackgroundColor(Qt.white)  # Fond blanc par défaut
        
        # Connecter les signaux pour gérer les événements de chargement
        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadProgress.connect(self.on_load_progress)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
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
        
    def save_cookies(self):
        """Sauvegarde les cookies dans le stockage persistant"""
        # QWebEngineProfile gère automatiquement la sauvegarde des cookies
        # dans le stockage persistant, donc cette méthode est principalement
        # pour la documentation et pour ajouter une logique supplémentaire si nécessaire
        pass
        
    def on_load_started(self):
        """Appelé lorsque le chargement de la page commence"""
        self.setWindowTitle(f"{self.title} (Chargement...)")
        # Vous pourriez ajouter un indicateur de chargement ici si nécessaire
        
    def on_load_progress(self, progress):
        """Appelé pendant le chargement de la page avec la progression"""
        self.setWindowTitle(f"{self.title} (Chargement {progress}%)")
        
    def on_load_finished(self, success):
        """Appelé lorsque le chargement de la page est terminé"""
        if success:
            self.setWindowTitle(self.title)
        else:
            self.setWindowTitle(f"{self.title} (Erreur de chargement)")
            # Vous pourriez afficher une page d'erreur personnalisée ici
    
    def closeEvent(self, event):
        """Gestion de l'événement de fermeture de la fenêtre"""
        # Sauvegarder les cookies avant de fermer
        self.save_cookies()
        event.accept()

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