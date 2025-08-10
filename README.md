# 🔥 Extintor Manager

Sistema moderno de gerenciamento de extintores desenvolvido em Python com Kivy.

## 📱 Funcionalidades

- ✅ **Cadastro de Extintores** - Registre novos extintores com todos os dados
- 🔍 **Consulta e Filtros** - Busque e filtre extintores por tipo e status  
- 📊 **Dashboard** - Visualize estatísticas e indicadores
- 📋 **Relatórios PDF** - Gere relatórios completos e de vencimentos
- 🎨 **Interface Moderna** - Design colorido e intuitivo

## 🚀 Como Executar

### Desktop (Windows/Linux/Mac)
```bash
pip install kivy reportlab
python extintor_managerModerno.py
```

### Android APK
O build do Android é feito automaticamente via GitHub Actions.

## 📦 Estrutura do Projeto

- `extintor_managerModerno.py` - Aplicativo principal
- `main.py` - Ponto de entrada para Android
- `buildozer.spec` - Configuração do build Android
- `requirements.txt` - Dependências Python

## 🎨 Telas

1. **Home** - Menu principal com cards de navegação
2. **Cadastro** - Formulário completo com navegação entre registros
3. **Consulta** - Lista filtrada de extintores
4. **Dashboard** - Estatísticas e gráficos
5. **Relatórios** - Geração de PDFs

## 🔧 Tecnologias

- **Python 3.8+**
- **Kivy 2.1+** - Framework de interface
- **ReportLab** - Geração de PDFs
- **JSON** - Armazenamento de dados

## 📱 Build Android

O APK é gerado automaticamente via GitHub Actions. Baixe na aba "Actions" após o commit.

## 🎯 Para Google Play Store

1. Faça build de release: `buildozer android release`
2. Assine o APK com keystore
3. Suba para Google Play Console

---

Desenvolvido com ❤️ para gerenciamento profissional de extintores.