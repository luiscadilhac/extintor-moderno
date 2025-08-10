@echo off
echo === SUBINDO CODIGO PARA GITHUB ===

echo 1. Instalando Git...
winget install --id Git.Git -e --source winget

echo 2. Inicializando repositorio...
git init

echo 3. Adicionando arquivos...
git add .

echo 4. Fazendo primeiro commit...
git commit -m "Primeiro commit - Extintor Manager App"

echo 5. Agora va para github.com e:
echo    - Clique em "New repository"
echo    - Nome: extintor-manager
echo    - Deixe publico
echo    - Nao marque "Initialize with README"
echo    - Clique "Create repository"

echo 6. Copie a URL do repositorio e execute:
echo    git remote add origin https://github.com/SEU_USUARIO/extintor-manager.git
echo    git branch -M main
echo    git push -u origin main

pause