@echo off
echo === FINALIZANDO UPLOAD PARA GITHUB ===

echo Agora execute estes comandos um por vez:
echo.

set /p usuario="Digite seu usuario do GitHub: "
set /p repo="Digite o nome do repositorio (extintor-manager): "

if "%repo%"=="" set repo=extintor-manager

echo.
echo 1. Conectando ao repositorio...
git remote add origin https://github.com/%usuario%/%repo%.git

echo.
echo 2. Definindo branch principal...
git branch -M main

echo.
echo 3. Enviando codigo para GitHub...
git push -u origin main

echo.
echo === CONCLUIDO! ===
echo Seu codigo esta no GitHub em: https://github.com/%usuario%/%repo%
echo.
echo O GitHub Actions vai gerar o APK automaticamente!
echo Verifique na aba "Actions" do seu repositorio.
echo.
pause