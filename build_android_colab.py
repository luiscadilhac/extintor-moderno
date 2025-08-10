# Execute este código no Google Colab para gerar APK
# 1. Acesse: https://colab.research.google.com
# 2. Cole este código em uma célula
# 3. Execute

!apt update
!apt install -y git zip unzip openjdk-17-jdk wget
!pip install buildozer cython

# Clone seu repositório
!git clone https://github.com/luiscadilhac/extintor-moderno.git
%cd extintor-moderno

# Build APK
!buildozer android debug

# Download do APK
from google.colab import files
files.download('bin/extintormanager-1.0-armeabi-v7a-debug.apk')