# Script para adicionar mais dados de teste
import json

dados_completos = {
    "empresas": [
        {
            "empresa": "ABC Indústria Ltda",
            "setor": "Produção",
            "cargo": "Operador de Máquinas",
            "atividade": "Operação de equipamentos industriais",
            "ambiente": "Galpão industrial com ventilação natural",
            "agentes": [
                {"agente": "Ruído", "concentracao": "85 dB(A)", "exposicao": "8h/dia", "analise": "Acima do limite", "medidas_existentes": "Protetor auricular", "medidas_necessarias": "Enclausuramento da fonte"},
                {"agente": "Calor", "concentracao": "28°C IBUTG", "exposicao": "6h/dia", "analise": "Dentro do limite", "medidas_existentes": "Ventiladores", "medidas_necessarias": "Manutenção preventiva"}
            ],
            "parecer": "Ambiente com exposição a ruído acima do limite. Recomenda-se implementação de medidas coletivas.",
            "responsavel": "Eng. João Silva - CREA 12345",
            "data_criacao": "15/12/2024 10:30:00"
        },
        {
            "empresa": "XYZ Química S.A.",
            "setor": "Laboratório",
            "cargo": "Técnico Químico",
            "atividade": "Análises químicas e controle de qualidade",
            "ambiente": "Laboratório com capela de exaustão",
            "agentes": [
                {"agente": "Vapores Químicos", "concentracao": "0.5 ppm", "exposicao": "4h/dia", "analise": "Dentro do limite", "medidas_existentes": "Capela de exaustão", "medidas_necessarias": "Monitoramento contínuo"}
            ],
            "parecer": "Ambiente controlado com medidas adequadas de proteção coletiva e individual.",
            "responsavel": "Eng. Maria Santos - CREA 67890",
            "data_criacao": "14/12/2024 14:15:00"
        },
        {
            "empresa": "DEF Construção Civil",
            "setor": "Obra",
            "cargo": "Pedreiro",
            "atividade": "Construção e acabamento",
            "ambiente": "Canteiro de obras ao ar livre",
            "agentes": [
                {"agente": "Poeira de Sílica", "concentracao": "0.8 mg/m³", "exposicao": "8h/dia", "analise": "Próximo ao limite", "medidas_existentes": "Máscara PFF2", "medidas_necessarias": "Umidificação do ambiente"}
            ],
            "parecer": "Necessário implementar medidas de controle para poeira e proteção solar.",
            "responsavel": "Eng. Pedro Costa - CREA 11111",
            "data_criacao": "13/12/2024 09:45:00"
        },
        {
            "empresa": "GHI Metalúrgica",
            "setor": "Soldagem",
            "cargo": "Soldador",
            "atividade": "Soldagem de estruturas metálicas",
            "ambiente": "Oficina com sistema de exaustão",
            "agentes": [
                {"agente": "Fumos Metálicos", "concentracao": "2.5 mg/m³", "exposicao": "7h/dia", "analise": "Acima do limite", "medidas_existentes": "Respirador PFF3", "medidas_necessarias": "Melhoria da exaustão"}
            ],
            "parecer": "Exposição a fumos metálicos requer melhoria no sistema de ventilação local exaustora.",
            "responsavel": "Eng. Ana Lima - CREA 22222",
            "data_criacao": "12/12/2024 16:20:00"
        },
        {
            "empresa": "JKL Alimentícia",
            "setor": "Produção",
            "cargo": "Operador de Linha",
            "atividade": "Processamento de alimentos",
            "ambiente": "Área refrigerada com controle de temperatura",
            "agentes": [
                {"agente": "Frio", "concentracao": "5°C", "exposicao": "8h/dia", "analise": "Dentro do limite", "medidas_existentes": "Roupa térmica", "medidas_necessarias": "Rodízio de atividades"}
            ],
            "parecer": "Ambiente controlado adequadamente para atividade de processamento de alimentos.",
            "responsavel": "Eng. Carlos Mendes - CREA 33333",
            "data_criacao": "11/12/2024 11:10:00"
        },
        {
            "empresa": "MNO Têxtil",
            "setor": "Tecelagem",
            "cargo": "Tecelão",
            "atividade": "Operação de teares",
            "ambiente": "Galpão com controle de umidade",
            "agentes": [
                {"agente": "Fibras Têxteis", "concentracao": "1.2 mg/m³", "exposicao": "8h/dia", "analise": "Dentro do limite", "medidas_existentes": "Máscara descartável", "medidas_necessarias": "Limpeza frequente"}
            ],
            "parecer": "Ambiente com condições adequadas de trabalho, manter medidas preventivas.",
            "responsavel": "Eng. Lucia Ferreira - CREA 44444",
            "data_criacao": "10/12/2024 13:25:00"
        },
        {
            "empresa": "PQR Farmacêutica",
            "setor": "Produção",
            "cargo": "Operador Farmacêutico",
            "atividade": "Manipulação de medicamentos",
            "ambiente": "Sala limpa com pressão positiva",
            "agentes": [
                {"agente": "Pós Farmacêuticos", "concentracao": "0.3 mg/m³", "exposicao": "6h/dia", "analise": "Controlado", "medidas_existentes": "Cabine de fluxo laminar", "medidas_necessarias": "Validação semestral"}
            ],
            "parecer": "Ambiente com excelente controle de contaminantes, manter padrões atuais.",
            "responsavel": "Eng. Roberto Alves - CREA 55555",
            "data_criacao": "09/12/2024 08:50:00"
        },
        {
            "empresa": "STU Mineração",
            "setor": "Extração",
            "cargo": "Operador de Britador",
            "atividade": "Britagem de minério",
            "ambiente": "Área externa com equipamentos pesados",
            "agentes": [
                {"agente": "Poeira Mineral", "concentracao": "3.5 mg/m³", "exposicao": "8h/dia", "analise": "Acima do limite", "medidas_existentes": "Respirador PFF3", "medidas_necessarias": "Aspersão de água"}
            ],
            "parecer": "Necessário implementar sistema de aspersão para controle de poeira mineral.",
            "responsavel": "Eng. Fernanda Rocha - CREA 66666",
            "data_criacao": "08/12/2024 15:35:00"
        },
        {
            "empresa": "VWX Gráfica",
            "setor": "Impressão",
            "cargo": "Operador de Impressora",
            "atividade": "Impressão offset",
            "ambiente": "Galpão com ventilação mecânica",
            "agentes": [
                {"agente": "Vapores de Tinta", "concentracao": "15 ppm", "exposicao": "8h/dia", "analise": "Dentro do limite", "medidas_existentes": "Ventilação local", "medidas_necessarias": "Manutenção dos filtros"}
            ],
            "parecer": "Ambiente com controles adequados, manter programa de manutenção preventiva.",
            "responsavel": "Eng. Marcos Oliveira - CREA 77777",
            "data_criacao": "07/12/2024 12:40:00"
        },
        {
            "empresa": "YZA Hospitalar",
            "setor": "Laboratório",
            "cargo": "Técnico em Análises Clínicas",
            "atividade": "Análises laboratoriais",
            "ambiente": "Laboratório hospitalar climatizado",
            "agentes": [
                {"agente": "Agentes Biológicos", "concentracao": "Variável", "exposicao": "8h/dia", "analise": "Controlado", "medidas_existentes": "Cabine de segurança", "medidas_necessarias": "Vacinação atualizada"}
            ],
            "parecer": "Ambiente hospitalar com controles biológicos e químicos adequados.",
            "responsavel": "Eng. Patricia Souza - CREA 88888",
            "data_criacao": "06/12/2024 07:15:00"
        }
    ]
}

# Salvar dados de teste
with open('dados.json', 'w', encoding='utf-8') as f:
    json.dump(dados_completos, f, ensure_ascii=False, indent=2)

print("Dados de teste criados com sucesso!")
print("10 registros adicionados ao arquivo dados.json")