@echo off
echo === CORRIGINDO UPLOAD PARA GITHUB ===

echo Removendo configuracao anterior...
git remote remove origin

echo Verificando status...
git status

echo Adicionando arquivos novamente...
git add .

echo Fazendo commit...
git commit -m "Extintor Manager - App completo"

echo.
echo IMPORTANTE: Digite seu NOME DE USUARIO do GitHub (nao o email!)
echo Exemplo: se sua URL for github.com/joaosilva, digite: joaosilva
echo.

set /p usuario="Digite seu NOME DE USUARIO do GitHub: "

echo.
echo Conectando ao repositorio correto...
git remote add origin https://github.com/%usuario%/extintor-moderno.git

echo.
echo Criando e enviando branch main...
git branch -M main
git push -u origin main

echo.
echo === CONCLUIDO! ===
echo Acesse: https://github.com/%usuario%/extintor-moderno
echo.
pause