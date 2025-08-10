@echo off
echo Deploy GitHub - Extintor Manager
echo.
echo 1. Primeiro crie o repositorio no GitHub:
echo    - Acesse: https://github.com/new
echo    - Nome: extintor-moderno
echo    - Publico
echo    - NAO marque README
echo    - Clique Create repository
echo.
pause
echo.
echo 2. Fazendo push...
git push -u origin main
echo.
echo Concluido! Acesse: https://github.com/luiscadilhac/extintor-moderno
pause