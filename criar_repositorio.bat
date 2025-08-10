@echo off
echo.
echo ========================================
echo    🚀 CRIANDO REPOSITÓRIO NO GITHUB
echo ========================================
echo.

echo 1. Primeiro, você precisa criar o repositório no GitHub:
echo.
echo    👉 Acesse: https://github.com/new
echo    👉 Nome do repositório: extintor-moderno
echo    👉 Deixe PÚBLICO
echo    👉 NÃO marque "Add a README file"
echo    👉 Clique em "Create repository"
echo.
echo 2. Após criar, pressione qualquer tecla para continuar...
pause

echo.
echo 3. Fazendo push para o repositório criado...
git push -u origin main

echo.
echo ========================================
echo ✅ DEPLOY CONCLUÍDO!
echo ========================================
echo.
echo 📱 Acesse: https://github.com/luiscadilhac/extintor-moderno
echo 🤖 O GitHub Actions vai gerar o APK automaticamente!
echo.
pause