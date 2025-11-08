# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file per Keyboard & Switch Finder
"""

block_cipher = None

# Tutti i file dati da includere
datas = [
    ('app/templates', 'app/templates'),
    ('app/static', 'app/static'),
    ('app/data', 'app/data'),
]

# Moduli nascosti che PyInstaller potrebbe non rilevare
hiddenimports = [
    'flask',
    'flask_cors',
    'numpy',
    'pydantic',
    'pydantic.main',
    'pydantic.fields',
    'pydantic.types',
]

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeyboardFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mostra la console per vedere i log
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Aggiungi un file .ico se vuoi un'icona personalizzata
)
