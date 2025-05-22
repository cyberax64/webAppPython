#!/bin/bash

# Script de lancement pour WebAppPython (compatible Linux et macOS)

# Fonction pour détecter le système d'exploitation
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)

# Vérifier si le fichier app.py existe
if [ ! -f "app.py" ]; then
    echo "Erreur: Le fichier app.py n'existe pas dans le répertoire courant."
    exit 1
fi

# Définir la commande Python en fonction du système d'exploitation
if [[ "$OS" == "windows" ]]; then
    PY_CMD="python"
else
    PY_CMD="python3"
    
    # Vérifier si le fichier est exécutable (seulement sur Linux/macOS)
    if [ ! -x "app.py" ]; then
        echo "Le fichier app.py n'est pas exécutable. Attribution des droits d'exécution..."
        chmod +x app.py
    fi
fi

# Exécuter l'application
if [[ "$OS" == "windows" ]]; then
    $PY_CMD app.py
else
    ./app.py
fi