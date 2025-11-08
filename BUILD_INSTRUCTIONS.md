# 🔧 Istruzioni per Build dell'Eseguibile

Questa guida spiega come creare un file eseguibile standalone (.exe su Windows, binario su Linux/Mac) dell'applicazione Keyboard & Switch Finder.

## 📋 Indice
- [Windows (.exe)](#windows-exe)
- [Linux/Mac](#linuxmac)
- [Troubleshooting](#troubleshooting)
- [Build manuale avanzato](#build-manuale-avanzato)

---

## Windows (.exe)

### Metodo Automatico (Consigliato)

1. **Apri il terminale** (cmd o PowerShell) nella cartella del progetto

2. **Esegui lo script di build**:
   ```cmd
   build_exe.bat
   ```

3. **Attendi il completamento** (3-5 minuti)

4. **Trova l'eseguibile**: `KeyboardFinder.exe` nella cartella principale

5. **Distribuisci**: Copia `KeyboardFinder.exe` su qualsiasi PC Windows (no Python richiesto!)

### Cosa fa lo script:
1. ✅ Installa PyInstaller e dipendenze
2. ✅ Pulisce build precedenti
3. ✅ Crea l'eseguibile con tutti i file necessari
4. ✅ Sposta l'exe nella cartella principale
5. ✅ (Opzionale) Pulisce i file temporanei

### Dimensione attesa
L'eseguibile sarà circa **50-70 MB** perché include:
- Interprete Python
- Flask e tutte le librerie
- NumPy
- Tutti i file HTML/CSS/JS
- Database JSON

---

## Linux/Mac

### Metodo Automatico (Consigliato)

1. **Apri il terminale** nella cartella del progetto

2. **Dai i permessi allo script**:
   ```bash
   chmod +x build_exe.sh
   ```

3. **Esegui lo script**:
   ```bash
   ./build_exe.sh
   ```

4. **Attendi il completamento** (3-5 minuti)

5. **Trova l'eseguibile**: `KeyboardFinder` nella cartella principale

6. **Avvia**:
   ```bash
   ./KeyboardFinder
   ```

---

## Troubleshooting

### ❌ "Python non trovato"

**Soluzione**: Installa Python 3.8+ da [python.org](https://www.python.org/)

Durante l'installazione su Windows, seleziona **"Add Python to PATH"**

---

### ❌ "pip non trovato"

**Soluzione**:
```bash
# Windows
python -m ensurepip --upgrade

# Linux/Mac
sudo apt-get install python3-pip  # Debian/Ubuntu
brew install python3               # Mac con Homebrew
```

---

### ❌ "ModuleNotFoundError" durante la build

**Soluzione**: Reinstalla le dipendenze
```bash
pip install -r requirements.txt --force-reinstall
```

---

### ❌ L'exe non si avvia / crash immediato

**Cause comuni**:

1. **Antivirus blocca l'exe**
   - Soluzione: Aggiungi `KeyboardFinder.exe` alle esclusioni dell'antivirus

2. **File mancanti**
   - Soluzione: Verifica che i file nella cartella temporanea `_MEI*` siano accessibili
   - Prova a eseguire come amministratore

3. **Porta 5000 occupata**
   - Soluzione: Chiudi altre applicazioni che usano la porta 5000
   - Oppure modifica la porta in `launcher.py`

---

### ❌ "UPX is not available"

**Opzionale**: UPX comprime l'exe per ridurne la dimensione

**Soluzione**:
1. Scarica UPX da [upx.github.io](https://upx.github.io/)
2. Estrai e aggiungi al PATH
3. Oppure disabilita UPX nel file `.spec`: `upx=False`

---

### ❌ Errore "Failed to execute script"

**Soluzione**: Usa la build con console per vedere gli errori

Nel file `keyboard_finder.spec`, cambia:
```python
console=True,  # Mostra la finestra console per debug
```

Poi ricompila e leggi gli errori nella console.

---

## Build Manuale Avanzato

Se vuoi personalizzare il processo:

### 1. Installa PyInstaller
```bash
pip install pyinstaller
```

### 2. Build base (senza spec file)
```bash
pyinstaller --onefile --add-data "app/templates:app/templates" --add-data "app/static:app/static" --add-data "app/data:app/data" launcher.py
```

### 3. Build con spec file (personalizzabile)
```bash
pyinstaller keyboard_finder.spec
```

### 4. Trova l'eseguibile
```
dist/KeyboardFinder.exe  (Windows)
dist/KeyboardFinder      (Linux/Mac)
```

---

## Personalizzazioni Avanzate

### Aggiungere un'icona personalizzata

1. Crea o scarica un file `.ico` (Windows) o `.icns` (Mac)

2. Modifica `keyboard_finder.spec`:
   ```python
   exe = EXE(
       ...
       icon='path/to/icon.ico',  # Percorso all'icona
   )
   ```

3. Ricompila con `pyinstaller keyboard_finder.spec`

---

### Creare exe senza finestra console (solo GUI)

Utile se vuoi nascondere la console nera.

Modifica `keyboard_finder.spec`:
```python
exe = EXE(
    ...
    console=False,  # Nasconde la console
)
```

⚠️ **Attenzione**: Senza console non vedrai i log del server. Usa solo per release finale.

---

### Ridurre dimensione dell'exe

1. **Usa UPX** (compressione)
   ```python
   upx=True,
   upx_exclude=[],
   ```

2. **Escludi moduli non necessari**
   ```python
   excludes=['tkinter', 'matplotlib', 'scipy'],
   ```

3. **Build in 2 file** invece di 1 (più veloce da avviare)
   Usa `pyinstaller --onedir` invece di `--onefile`

---

## Test dell'Eseguibile

Dopo aver creato l'exe, testalo:

1. **Test base**: Avvia e verifica che il browser si apra
2. **Test funzionalità**: Prova tutte e 3 le modalità (Switch, Keycaps, Board)
3. **Test su PC pulito**: Copia l'exe su un PC senza Python installato
4. **Test antivirus**: Verifica che non venga bloccato

---

## Distribuzione

### Per distribuzione locale:
1. Copia solo `KeyboardFinder.exe`
2. L'exe è standalone e include tutto

### Per distribuzione online:
1. Crea un installer con [Inno Setup](https://jrsoftware.org/isinfo.php) (Windows)
2. Oppure distribuisci come ZIP con istruzioni
3. Firma digitalmente l'exe per evitare warning antivirus (opzionale, richiede certificato)

---

## Note Tecniche

### Cosa include l'eseguibile:
- ✅ Interprete Python embedded
- ✅ Tutte le librerie (Flask, NumPy, Pydantic)
- ✅ File HTML/CSS/JS
- ✅ Database JSON (switches, keycaps, boards)
- ✅ Configurazioni

### Come funziona:
1. Avvio: Estrae i file in una cartella temp `_MEI*`
2. Lancia Flask server su `localhost:5000`
3. Apre il browser automaticamente
4. Alla chiusura: Pulisce i file temporanei

### Compatibilità:
- **Windows**: 7, 8, 10, 11 (32-bit e 64-bit)
- **Linux**: Qualsiasi distribuzione recente
- **Mac**: macOS 10.13+

---

## FAQ

**Q: Posso creare l'exe su Linux e usarlo su Windows?**
A: No, devi compilare su ogni sistema operativo target.

**Q: L'exe è sicuro?**
A: Sì, ma gli antivirus potrebbero flaggarlo perché è un exe Python non firmato. Aggiungi un'esclusione o firma digitalmente.

**Q: Posso vendere l'exe?**
A: Controlla la licenza del progetto. Ricorda di rispettare le licenze di Flask, NumPy, etc.

**Q: Come aggiorno il database prodotti nell'exe?**
A: Modifica i file JSON in `app/data/` e ricompila l'exe.

**Q: L'exe è lento all'avvio**
A: Sì, la prima volta estrae i file (~2-3 secondi). Usa `--onedir` invece di `--onefile` per startup più veloce.

---

## Supporto

Se hai problemi:
1. Leggi il [Troubleshooting](#troubleshooting)
2. Apri una issue su GitHub
3. Controlla i log nella console (se `console=True`)

---

**Buona build! 🚀**
