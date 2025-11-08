@echo off
REM Script di build per Windows
REM Crea l'eseguibile KeyboardFinder.exe

echo ======================================
echo   Keyboard Finder - Build Script
echo ======================================
echo.

REM Verifica che Python sia installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato!
    echo Installa Python da https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installazione dipendenze...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERRORE: Installazione dipendenze fallita!
    pause
    exit /b 1
)

echo.
echo [2/4] Pulizia build precedenti...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist KeyboardFinder.exe del /f KeyboardFinder.exe

echo.
echo [3/4] Creazione eseguibile con PyInstaller...
echo Questo potrebbe richiedere alcuni minuti...
pyinstaller --clean keyboard_finder.spec
if errorlevel 1 (
    echo ERRORE: Build fallita!
    pause
    exit /b 1
)

echo.
echo [4/4] Spostamento eseguibile nella directory principale...
if exist dist\KeyboardFinder.exe (
    move dist\KeyboardFinder.exe KeyboardFinder.exe
    echo.
    echo ======================================
    echo   BUILD COMPLETATA CON SUCCESSO!
    echo ======================================
    echo.
    echo L'eseguibile e' disponibile in:
    echo %CD%\KeyboardFinder.exe
    echo.
    echo Per avviarlo, fai doppio clic su KeyboardFinder.exe
    echo.
) else (
    echo ERRORE: Eseguibile non trovato in dist\
    pause
    exit /b 1
)

REM Pulizia file temporanei (opzionale)
echo Vuoi eliminare i file temporanei di build? (Y/N)
set /p cleanup=
if /i "%cleanup%"=="Y" (
    echo Pulizia in corso...
    rmdir /s /q build
    rmdir /s /q dist
    echo Pulizia completata!
)

echo.
pause
