@echo off
echo === SOLUCAO FINAL PARA GITHUB ===

echo 1. Configurando Git...
git config --global user.name "Luis Cadilhac"
git config --global user.email "cadilhac.luis@gmail.com"

echo 2. Verificando status atual...
git status

echo 3. Removendo remote anterior...
git remote remove origin 2>nul

echo 4. Adicionando todos os arquivos...
git add -A

echo 5. Fazendo commit forçado...
git commit -m "Extintor Manager - Aplicativo completo para Android" --allow-empty

echo 6. Conectando ao repositorio...
git remote add origin https://github.com/luiscadilhac/extintor-moderno.git

echo 7. Criando branch main...
git checkout -b main

echo 8. Enviando para GitHub...
git push -u origin main --force

echo.
echo === CONCLUIDO! ===
echo Acesse: https://github.com/luiscadilhac/extintor-moderno
echo O GitHub Actions vai gerar o APK automaticamente!
echo.
pause