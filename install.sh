#!/bin/bash

# Script d'installation pour WebAppPython (compatible Linux et Windows via Git Bash)

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
echo "Système d'exploitation détecté: $OS"

# Vérifier si Python est installé
if [[ "$OS" == "windows" ]]; then
    # Sur Windows, vérifier python au lieu de python3
    if ! command -v python &> /dev/null; then
        echo "Python n'est pas installé ou n'est pas dans le PATH. Veuillez l'installer avant de continuer."
        echo "Téléchargez Python depuis https://www.python.org/downloads/"
        exit 1
    fi
    PY_CMD="python"
    PIP_CMD="pip"
else
    # Sur Linux/macOS, vérifier python3
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 n'est pas installé. Veuillez l'installer avant de continuer."
        exit 1
    fi
    PY_CMD="python3"
    PIP_CMD="pip3"
fi

# Vérifier si pip est installé
if ! command -v $PIP_CMD &> /dev/null; then
    echo "$PIP_CMD n'est pas installé ou n'est pas dans le PATH."
    if [[ "$OS" == "linux" ]]; then
        echo "Sur Linux, vous pouvez l'installer avec:"
        echo "sudo apt-get update && sudo apt-get install -y python3-pip"
    elif [[ "$OS" == "windows" ]]; then
        echo "Sur Windows, pip devrait être installé avec Python."
        echo "Vérifiez votre installation Python ou réinstallez-le en cochant l'option 'Add Python to PATH'."
    fi
    exit 1
fi

# Installer les dépendances système pour Linux
if [[ "$OS" == "linux" ]]; then
    echo "Installation des dépendances système pour Linux..."
    if command -v apt-get &> /dev/null; then
        echo "Gestionnaire de paquets apt-get détecté."
        echo "Si vous rencontrez des erreurs lors de l'exécution de l'application, vous devrez peut-être installer les paquets suivants:"
        echo "sudo apt-get update && sudo apt-get install -y libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0 libxcb-shape0 libxcb-xfixes0 libxtst6"
    else
        echo "Gestionnaire de paquets apt-get non détecté."
        echo "Si vous rencontrez des erreurs lors de l'exécution de l'application, vous devrez peut-être installer les dépendances système manuellement."
    fi
fi

# Installer les dépendances Python
echo "Installation des dépendances Python..."
$PIP_CMD install -r requirements.txt

# Rendre le script principal exécutable (seulement sur Linux/macOS)
if [[ "$OS" != "windows" ]]; then
    chmod +x app.py
    chmod +x run.sh
fi

echo "Installation terminée avec succès !"
if [[ "$OS" == "windows" ]]; then
    echo "Pour exécuter l'application, utilisez la commande : python app.py"
else
    echo "Pour exécuter l'application, utilisez la commande : ./app.py ou ./run.sh"
fi