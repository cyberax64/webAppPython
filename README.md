# Web App Python

Une application Python simple qui ouvre une fenêtre sans menu ni onglets pour afficher un site web spécifié dans un fichier de configuration, avec gestion des cookies.

## Fonctionnalités

- Affichage d'un site web dans une fenêtre minimaliste (sans menu, onglets, etc.)
- Rendu optimal des pages web avec support complet de CSS et JavaScript
- Moteur de rendu basé sur Chromium pour une compatibilité maximale avec les sites modernes
- Configuration du site web via un fichier config.ini
- Gestion et persistance des cookies entre les sessions
- Compatible avec Windows, Linux et macOS
- Indicateur de progression du chargement des pages

## Prérequis

- Python 3.6 ou supérieur
- PyQt5 (version 5.15.0 ou supérieure recommandée)
- PyQtWebEngine (version 5.15.0 ou supérieure recommandée)

> **Note**: L'application est compatible avec différentes versions de PyQt5, mais certaines fonctionnalités avancées de gestion des cookies peuvent être limitées avec des versions plus anciennes.

## Installation

### Sous Windows

#### Méthode 1 : Script d'installation automatique

Double-cliquez sur le fichier `install.bat` ou exécutez-le depuis une invite de commande :

```cmd
install.bat
```

#### Méthode 2 : Installation manuelle

Installez les dépendances Python :

```cmd
pip install -r requirements.txt
```

### Sous Linux/macOS

#### Méthode 1 : Script d'installation automatique

Utilisez le script d'installation fourni pour installer toutes les dépendances nécessaires :

```bash
./install.sh
```

Ce script installera automatiquement les dépendances Python et vous indiquera les dépendances système à installer si nécessaire.

#### Méthode 2 : Installation manuelle

1. Installez les dépendances système (sous Debian/Ubuntu) :

```bash
sudo apt-get update
sudo apt-get install -y libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0 libxcb-shape0 libxcb-xfixes0 libxtst6
```

2. Installez les dépendances Python :

```bash
pip3 install -r requirements.txt
```

## Configuration

Modifiez le fichier `config.ini` pour spécifier l'URL du site web à afficher et les dimensions de la fenêtre :

```ini
[WebApp]
url = https://www.example.com
window_title = Web App
window_width = 1024
window_height = 768
```

## Utilisation

### Sous Windows

#### Méthode 1 : Script de lancement

Double-cliquez sur le fichier `run.bat` ou exécutez-le depuis une invite de commande :

```cmd
run.bat
```

#### Méthode 2 : Exécution directe

Exécutez l'application directement avec Python :

```cmd
python app.py
```

### Sous Linux/macOS

#### Méthode 1 : Script de lancement

Utilisez le script de lancement fourni :

```bash
./run.sh
```

#### Méthode 2 : Exécution directe

Exécutez l'application directement avec Python :

```bash
python3 app.py
```

ou si le fichier est exécutable :

```bash
./app.py
```

## Stockage des cookies

Les cookies sont automatiquement enregistrés dans un dossier `cookies` créé dans le répertoire de l'application. Ils sont rechargés à chaque démarrage de l'application pour maintenir les sessions.

## Remarques

- L'application nécessite un environnement graphique pour fonctionner correctement.
- Si vous exécutez l'application dans un environnement sans interface graphique (Linux sans serveur X), elle passera en mode test et affichera uniquement les informations de configuration.
- Sur Windows et macOS, l'application suppose qu'un environnement graphique est toujours disponible.