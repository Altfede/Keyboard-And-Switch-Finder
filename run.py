#!/usr/bin/env python
"""
Script di avvio per Keyboard & Switch Finder
"""
from app.main import create_app

if __name__ == '__main__':
    app = create_app()
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      🎹  Keyboard & Switch Finder  🎹                   ║
    ║                                                          ║
    ║      Sistema di raccomandazione per tastiere            ║
    ║      meccaniche, switch e keycaps                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝

    ✓ Server avviato con successo!

    🌐 Apri il browser su: http://localhost:5000

    📊 Health check: http://localhost:5000/api/health

    Press CTRL+C to quit
    """)
    app.run()
