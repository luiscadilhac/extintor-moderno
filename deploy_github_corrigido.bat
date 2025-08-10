@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🚀 DEPLOY EXTINTOR MANAGER - CORRIGIDO
echo ========================================
echo.

REM Configurar Git primeiro
echo 1. Configurando Git...
git config --global user.name "luiscadilhac"
git config --global user.email "luiscadilhac@users.noreply.github.com"

echo 2. Inicializando repositório...
git init

echo 3. Adicionando todos os arquivos...
git add .

echo 4. Fazendo commit inicial...
git commit -m "🔥 Extintor Manager - Sistema completo com interface moderna"

echo 5. Renomeando branch para main...
git branch -M main

echo 6. Conectando ao repositório GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/luiscadilhac/extintor-moderno.git

echo 7. Enviando para GitHub...
git push -u origin main --force

echo.
echo ========================================
echo ✅ DEPLOY CONCLUÍDO COM SUCESSO!
echo ========================================
echo.
echo 📱 Acesse: https://github.com/luiscadilhac/extintor-moderno
echo 🤖 O GitHub Actions vai gerar o APK automaticamente!
echo.
pause