@echo off
echo Instalando WSL para build Android
echo.
echo 1. Execute como Administrador:
echo    wsl --install
echo.
echo 2. Reinicie o PC
echo.
echo 3. No Ubuntu WSL, execute:
echo    sudo apt update
echo    sudo apt install python3-pip git
echo    pip3 install buildozer
echo    git clone https://github.com/luiscadilhac/extintor-moderno.git
echo    cd extintor-moderno
echo    buildozer android debug
echo.
pause