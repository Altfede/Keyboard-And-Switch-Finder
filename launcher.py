#!/usr/bin/env python
"""
Launcher con auto-apertura browser per l'applicazione
"""
import webbrowser
import threading
import time
import sys
import os
from app.main import create_app

def open_browser():
    """Apre il browser dopo 1.5 secondi"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Se eseguito come exe, cambia directory alla cartella dell'exe
    if getattr(sys, 'frozen', False):
        # Eseguito come exe
        application_path = sys._MEIPASS
    else:
        # Eseguito come script normale
        application_path = os.path.dirname(os.path.abspath(__file__))

    os.chdir(application_path)

    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      🎹  Keyboard & Switch Finder  🎹                   ║
    ║                                                          ║
    ║      Sistema di raccomandazione per tastiere            ║
    ║      meccaniche, switch e keycaps                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝

    ✓ Server in avvio...
    🌐 Il browser si aprirà automaticamente su http://localhost:5000

    ⚠️  IMPORTANTE: NON chiudere questa finestra!

    Per terminare l'applicazione, premi CTRL+C
    """)

    # Avvia thread per aprire il browser
    threading.Thread(target=open_browser, daemon=True).start()

    # Avvia Flask
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
