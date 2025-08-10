@echo off
echo Build Local APK - Extintor Manager
echo.
echo 1. Instalando Buildozer...
pip install buildozer

echo.
echo 2. Gerando APK...
buildozer android debug

echo.
echo 3. APK gerado em: bin\
dir bin\*.apk

echo.
echo Concluido! APK pronto para instalacao.
pause