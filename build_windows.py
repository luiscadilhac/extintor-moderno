#!/usr/bin/env python3
"""
Script para criar executável Windows usando PyInstaller
Para Android, use GitHub Actions ou WSL
"""

import os
import subprocess
import sys

def install_requirements():
    """Instala dependências necessárias"""
    requirements = [
        'pyinstaller',
        'kivy[base]',
        'reportlab'
    ]
    
    for req in requirements:
        print(f"Instalando {req}...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', req])

def create_exe():
    """Cria executável Windows"""
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=ExtintorManager',
        '--icon=icon.ico',  # Adicione um ícone se tiver
        'extintor_managerModerno.py'
    ]
    
    print("Criando executável Windows...")
    subprocess.run(cmd)
    print("Executável criado em dist/ExtintorManager.exe")

if __name__ == '__main__':
    print("=== Build Extintor Manager ===")
    install_requirements()
    create_exe()
    print("Build concluído!")