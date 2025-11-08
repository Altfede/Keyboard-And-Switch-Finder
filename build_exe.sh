#!/bin/bash
# Script di build per Linux/Mac
# Crea l'eseguibile KeyboardFinder

echo "======================================"
echo "  Keyboard Finder - Build Script"
echo "======================================"
echo ""

# Verifica che Python sia installato
if ! command -v python3 &> /dev/null; then
    echo "ERRORE: Python3 non trovato!"
    echo "Installa Python da https://www.python.org/"
    exit 1
fi

echo "[1/4] Installazione dipendenze..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERRORE: Installazione dipendenze fallita!"
    exit 1
fi

echo ""
echo "[2/4] Pulizia build precedenti..."
rm -rf build dist KeyboardFinder

echo ""
echo "[3/4] Creazione eseguibile con PyInstaller..."
echo "Questo potrebbe richiedere alcuni minuti..."
pyinstaller --clean keyboard_finder.spec
if [ $? -ne 0 ]; then
    echo "ERRORE: Build fallita!"
    exit 1
fi

echo ""
echo "[4/4] Spostamento eseguibile nella directory principale..."
if [ -f "dist/KeyboardFinder" ]; then
    mv dist/KeyboardFinder KeyboardFinder
    chmod +x KeyboardFinder
    echo ""
    echo "======================================"
    echo "  BUILD COMPLETATA CON SUCCESSO!"
    echo "======================================"
    echo ""
    echo "L'eseguibile è disponibile in:"
    echo "$(pwd)/KeyboardFinder"
    echo ""
    echo "Per avviarlo: ./KeyboardFinder"
    echo ""
else
    echo "ERRORE: Eseguibile non trovato in dist/"
    exit 1
fi

# Pulizia file temporanei (opzionale)
read -p "Vuoi eliminare i file temporanei di build? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pulizia in corso..."
    rm -rf build dist
    echo "Pulizia completata!"
fi

echo ""
