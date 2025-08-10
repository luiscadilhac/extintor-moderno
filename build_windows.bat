@echo off
echo Build Windows EXE - Extintor Manager
echo.
echo 1. Instalando PyInstaller...
pip install pyinstaller

echo.
echo 2. Gerando executavel...
pyinstaller --onefile --windowed --name="ExtintorManager" main.py

echo.
echo 3. Executavel gerado em: dist\
dir dist\*.exe

echo.
echo Concluido! Executavel pronto para uso.
pause