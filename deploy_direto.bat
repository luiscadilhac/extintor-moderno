@echo off
echo Deploy GitHub - Extintor Manager
echo.
echo IMPORTANTE: Primeiro crie o repositorio no GitHub:
echo 1. Acesse: https://github.com/new
echo 2. Nome: extintor-moderno
echo 3. Publico
echo 4. NAO marque README
echo 5. Clique Create repository
echo.
echo Depois pressione qualquer tecla...
pause
echo.
echo Removendo remote anterior...
git remote remove origin
echo.
echo Adicionando novo remote...
git remote add origin https://github.com/luiscadilhac/extintor-moderno.git
echo.
echo Fazendo push...
git push -u origin main
echo.
echo Concluido! Acesse: https://github.com/luiscadilhac/extintor-moderno
echo O GitHub Actions vai gerar o APK automaticamente!
pause