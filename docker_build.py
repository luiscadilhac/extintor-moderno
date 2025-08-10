#!/usr/bin/env python3
"""
Build Android APK usando Docker (funciona no Windows)
"""

import subprocess
import os

def build_with_docker():
    """Build usando Docker"""
    
    # Criar Dockerfile
    dockerfile_content = """
FROM kivy/buildozer:latest

WORKDIR /app
COPY . /app

RUN buildozer android debug

CMD ["cp", "bin/*.apk", "/output/"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)
    
    print("Construindo APK com Docker...")
    
    # Build da imagem
    subprocess.run(['docker', 'build', '-t', 'extintor-builder', '.'])
    
    # Executar build
    subprocess.run([
        'docker', 'run', '--rm', 
        '-v', f'{os.getcwd()}\\output:/output',
        'extintor-builder'
    ])
    
    print("APK criado em output/")

if __name__ == '__main__':
    build_with_docker()