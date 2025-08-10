@echo off
echo Instalando Buildozer...
pip install buildozer

echo Instalando Cython...
pip install cython

echo Construindo APK...
buildozer android debug

echo Build concluída! O APK está na pasta bin/
pause