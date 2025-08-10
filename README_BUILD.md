# Como Gerar APK para Android

## Problema: Buildozer não funciona no Windows

### Soluções Alternativas:

## 1. **GitHub Actions (Recomendado)**
1. Suba seu código para GitHub
2. O arquivo `.github/workflows/android.yml` fará o build automaticamente
3. Baixe o APK dos "Artifacts" na aba Actions

## 2. **Docker (Se tiver Docker instalado)**
```bash
python docker_build.py
```

## 3. **WSL (Windows Subsystem for Linux)**
```bash
# No WSL Ubuntu
sudo apt update
sudo apt install python3-pip
pip3 install buildozer cython
buildozer android debug
```

## 4. **Executável Windows**
```bash
python build_windows.py
```
Cria um .exe na pasta `dist/`

## 5. **Online (Repl.it/CodeSandbox)**
- Suba o código para Repl.it
- Execute `buildozer android debug`
- Baixe o APK

## Para Google Play Store:
1. Use `buildozer android release`
2. Assine o APK com keystore
3. Suba para Play Console

## Arquivos Necessários:
- ✅ buildozer.spec
- ✅ main.py  
- ✅ requirements.txt
- ✅ extintor_managerModerno.py