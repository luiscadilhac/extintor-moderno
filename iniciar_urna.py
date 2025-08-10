#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URNA ELETRÔNICA CIPA - Sistema Completo
Desenvolvido para eleições CIPA com interface moderna

Funcionalidades:
- Gestão de empresas e candidatos
- Sistema de votação com interface similar à urna oficial
- Reconhecimento facial (opcional)
- Geração de relatórios e comprovantes
- Sons da urna eletrônica
- Backup automático dos dados

Para executar: python iniciar_urna.py
"""

import sys
import os
import subprocess

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    dependencias = [
        'kivy', 'reportlab', 'opencv-python', 
        'face-recognition', 'numpy', 'Pillow'
    ]
    
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            faltando.append(dep)
    
    if faltando:
        print("❌ Dependências faltando:")
        for dep in faltando:
            print(f"   - {dep}")
        
        print("\n📦 Para instalar as dependências, execute:")
        print("pip install -r requirements_urna_eletronica.txt")
        
        resposta = input("\n❓ Deseja instalar automaticamente? (s/n): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_urna_eletronica.txt'])
                print("✅ Dependências instaladas com sucesso!")
            except subprocess.CalledProcessError:
                print("❌ Erro ao instalar dependências. Instale manualmente.")
                return False
        else:
            return False
    
    return True

def criar_estrutura_diretorios():
    """Cria a estrutura de diretórios necessária"""
    diretorios = [
        'sons',
        'fotos_candidatos', 
        'relatorios',
        'backups'
    ]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"📁 Diretório criado: {diretorio}")

def main():
    """Função principal"""
    print("🗳️  URNA ELETRÔNICA CIPA - Sistema Completo")
    print("=" * 50)
    
    # Verificar dependências
    print("🔍 Verificando dependências...")
    if not verificar_dependencias():
        print("❌ Não foi possível iniciar o sistema.")
        return
    
    # Criar estrutura de diretórios
    print("📁 Criando estrutura de diretórios...")
    criar_estrutura_diretorios()
    
    # Importar e executar a aplicação
    print("🚀 Iniciando a Urna Eletrônica...")
    try:
        from urna_eletronica_cipa import UrnaEletronicaCIPA
        app = UrnaEletronicaCIPA()
        app.run()
    except ImportError as e:
        print(f"❌ Erro ao importar a aplicação: {e}")
        print("Certifique-se de que o arquivo 'urna_eletronica_cipa.py' está no mesmo diretório.")
    except Exception as e:
        print(f"❌ Erro ao executar a aplicação: {e}")

if __name__ == '__main__':
    main()