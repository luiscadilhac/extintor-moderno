# Script para atualizar responsáveis técnicos por empresa
import json

# Carregar dados atuais
with open('dados_riscos.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Definir responsáveis por empresa
responsaveis_por_empresa = {
    "ABC Indústria": "Eng. João Silva - CREA 12345-SP",
    "XYZ Química": "Eng. Maria Santos - CREA 67890-RJ", 
    "DEF Construção": "Eng. Pedro Costa - CREA 11111-MG"
}

# Atualizar responsáveis
for registro in dados["empresas"]:
    empresa = registro["empresa"]
    if empresa in responsaveis_por_empresa:
        registro["responsavel"] = responsaveis_por_empresa[empresa]

# Salvar dados atualizados
with open('dados_riscos.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("Responsáveis técnicos atualizados:")
for empresa, responsavel in responsaveis_por_empresa.items():
    print(f"- {empresa}: {responsavel}")