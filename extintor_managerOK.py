import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
import webbrowser
import re
import re

# Cores modernas conforme solicitado
COR_FUNDO = "#FFF8E1"      # Laranja bem claro
COR_BOTAO = "#1976D2"      # Azul moderno
COR_BOTAO_TEXTO = "#FF9800"  # Laranja para fonte dos botões
COR_LABEL = "#1B5E20"      # Verde escuro
COR_CAMPOS = "#fff"
COR_TITULO = "#FF9800"     # Laranja para títulos
COR_ABA = "#FFB74D"  # Laranja médio

class ExtintorManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Extintor Manager - Sistema de Gerenciamento de Extintores")
        self.root.geometry("1000x700")
        self.root.configure(bg=COR_FUNDO)

        # Use tema ttk moderno
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=6, foreground=COR_BOTAO_TEXTO)
        style.configure('TLabel', font=('Arial', 10), background=COR_FUNDO, foreground=COR_LABEL)
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), background=COR_FUNDO, foreground=COR_TITULO)
        style.configure('TFrame', background=COR_FUNDO)
        style.configure('Treeview', font=('Arial', 10), rowheight=28, background=COR_CAMPOS, fieldbackground=COR_CAMPOS, foreground=COR_LABEL)
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'), foreground=COR_LABEL)
        style.configure('Aba.TFrame', background=COR_ABA)
        style.map('TButton', foreground=[('active', COR_BOTAO_TEXTO)], background=[('active', COR_BOTAO)])

        self.center_window()
        
        # Dados dos extintores (10 registros pré-cadastrados)
        self.extintores = [
            {
                "id": 1,
                "tipo": "Água Pressurizada",
                "capacidade": "10L",
                "localizacao": "Recepção - Térreo",
                "setor": "Administrativo",
                "data_fabricacao": "15/03/2022",
                "data_vencimento": "15/03/2025",
                "proxima_inspecao": "15/09/2023",
                "ultima_inspecao": "15/03/2023",
                "responsavel": "João Silva",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 2,
                "tipo": "Pó Químico BC",
                "capacidade": "4kg",
                "localizacao": "Sala de Servidores",
                "setor": "TI",
                "data_fabricacao": "20/05/2021",
                "data_vencimento": "20/05/2024",
                "proxima_inspecao": "20/11/2023",
                "ultima_inspecao": "20/05/2023",
                "responsavel": "Maria Oliveira",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 3,
                "tipo": "CO2",
                "capacidade": "5kg",
                "localizacao": "Laboratório de Química",
                "setor": "Pesquisa",
                "data_fabricacao": "10/01/2023",
                "data_vencimento": "10/01/2026",
                "proxima_inspecao": "10/07/2023",
                "ultima_inspecao": "10/01/2023",
                "responsavel": "Carlos Souza",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 4,
                "tipo": "Pó Químico ABC",
                "capacidade": "6kg",
                "localizacao": "Cozinha Industrial",
                "setor": "Alimentação",
                "data_fabricacao": "05/11/2020",
                "data_vencimento": "05/11/2023",
                "proxima_inspecao": "05/05/2023",
                "ultima_inspecao": "05/11/2022",
                "responsavel": "Ana Costa",
                "status": "Vencido",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Necessário recarga"
            },
            {
                "id": 5,
                "tipo": "Água Pressurizada",
                "capacidade": "10L",
                "localizacao": "Corredor - 1º Andar",
                "setor": "Administrativo",
                "data_fabricacao": "30/07/2022",
                "data_vencimento": "30/07/2025",
                "proxima_inspecao": "30/01/2024",
                "ultima_inspecao": "30/07/2023",
                "responsavel": "Pedro Almeida",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 6,
                "tipo": "Pó Químico BC",
                "capacidade": "4kg",
                "localizacao": "Oficina Mecânica",
                "setor": "Manutenção",
                "data_fabricacao": "12/09/2021",
                "data_vencimento": "12/09/2024",
                "proxima_inspecao": "12/03/2024",
                "ultima_inspecao": "12/09/2023",
                "responsavel": "Luiz Pereira",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 7,
                "tipo": "CO2",
                "capacidade": "5kg",
                "localizacao": "Sala de Arquivos",
                "setor": "Administrativo",
                "data_fabricacao": "22/02/2023",
                "data_vencimento": "22/02/2026",
                "proxima_inspecao": "22/08/2023",
                "ultima_inspecao": "22/02/2023",
                "responsavel": "Fernanda Lima",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 8,
                "tipo": "Pó Químico ABC",
                "capacidade": "6kg",
                "localizacao": "Sala de Máquinas",
                "setor": "Manutenção",
                "data_fabricacao": "08/04/2020",
                "data_vencimento": "08/04/2023",
                "proxima_inspecao": "08/10/2023",
                "ultima_inspecao": "08/04/2023",
                "responsavel": "Ricardo Santos",
                "status": "Vencido",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 9,
                "tipo": "Água Pressurizada",
                "capacidade": "10L",
                "localizacao": "Refeitório",
                "setor": "Alimentação",
                "data_fabricacao": "17/06/2022",
                "data_vencimento": "17/06/2025",
                "proxima_inspecao": "17/12/2023",
                "ultima_inspecao": "17/06/2023",
                "responsavel": "Juliana Oliveira",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            },
            {
                "id": 10,
                "tipo": "Pó Químico BC",
                "capacidade": "4kg",
                "localizacao": "Sala de Reuniões",
                "setor": "Administrativo",
                "data_fabricacao": "25/10/2021",
                "data_vencimento": "25/10/2024",
                "proxima_inspecao": "25/04/2024",
                "ultima_inspecao": "25/10/2023",
                "responsavel": "Marcos Silva",
                "status": "Ativo",
                "pressao": "OK",
                "sinalizacao": "OK",
                "acessorios": "OK",
                "observacoes": "Nenhuma"
            }
        ]
        
        self.current_id = 11  # Próximo ID disponível
        
        # Tipos de extintores conforme normas brasileiras
        self.tipos_extintores = [
            "Água Pressurizada",
            "Pó Químico BC",
            "Pó Químico ABC",
            "CO2",
            "Espuma Mecânica"
        ]
        
        # Capacidades comuns
        self.capacidades = [
            "1kg", "2kg", "4kg", "6kg", "8kg", "10kg",
            "2L", "5L", "10L", "20L", "50L"
        ]
        
        # Status possíveis
        self.status_options = [
            "Ativo",
            "Vencido",
            "Em Manutenção",
            "Recarga Necessária",
            "Descartado"
        ]
        
        # Setores comuns
        self.setores = [
            "Administrativo",
            "TI",
            "Manutenção",
            "Alimentação",
            "Pesquisa",
            "Produção",
            "Recepção",
            "Laboratório",
            "Oficina",
            "Estoque"
        ]
        
        # Criar interface
        self.create_widgets()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        self.title_label = ttk.Label(
            self.main_frame,
            text="Extintor Manager",
            style='Title.TLabel'
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Abas
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Aba de Cadastro
        self.cadastro_frame = ttk.Frame(self.notebook, padding=20, style='Aba.TFrame')
        self.notebook.add(self.cadastro_frame, text="Cadastro")

        # Aba de Consulta
        self.consulta_frame = ttk.Frame(self.notebook, padding=20, style='Aba.TFrame')
        self.notebook.add(self.consulta_frame, text="Consulta")

        # Aba de Relatórios
        self.relatorios_frame = ttk.Frame(self.notebook, padding=20, style='Aba.TFrame')
        self.notebook.add(self.relatorios_frame, text="Relatórios")

        # Configurar grid para expandir
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Criar widgets de cada aba
        self.create_cadastro_widgets()
        self.create_consulta_widgets()
        self.create_relatorios_widgets()
        
    def create_cadastro_widgets(self):
        """Cria os widgets da aba de cadastro"""
        # Frame de formulário
        self.form_frame = ttk.Frame(self.cadastro_frame)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

        # ID (não editável)
        ttk.Label(
            self.form_frame, 
            text="ID:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.id_var,
            state="readonly",
            font=("Arial", 10)
        )
        self.id_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Tipo de Extintor
        ttk.Label(
            self.form_frame, 
            text="Tipo de Extintor:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.tipo_var = tk.StringVar()
        self.tipo_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.tipo_var,
            values=self.tipos_extintores,
            state="readonly",
            font=("Arial", 10)
        )
        self.tipo_combobox.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Capacidade
        ttk.Label(
            self.form_frame, 
            text="Capacidade:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        
        self.capacidade_var = tk.StringVar()
        self.capacidade_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.capacidade_var,
            values=self.capacidades,
            font=("Arial", 10)
        )
        self.capacidade_combobox.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Localização
        ttk.Label(
            self.form_frame, 
            text="Localização:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        
        self.localizacao_var = tk.StringVar()
        self.localizacao_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.localizacao_var,
            font=("Arial", 10)
        )
        self.localizacao_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Setor
        ttk.Label(
            self.form_frame, 
            text="Setor:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        
        self.setor_var = tk.StringVar()
        self.setor_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.setor_var,
            values=self.setores,
            font=("Arial", 10)
        )
        self.setor_combobox.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        # Data de Fabricação
        ttk.Label(
            self.form_frame, 
            text="Data de Fabricação:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        
        self.data_fabricacao_var = tk.StringVar()
        self.data_fabricacao_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.data_fabricacao_var,
            font=("Arial", 10)
        )
        self.data_fabricacao_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.data_fabricacao_entry.insert(0, "dd/mm/aaaa")
        self.data_fabricacao_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "dd/mm/aaaa"))
        self.data_fabricacao_entry.bind("<FocusOut>", lambda e: self.set_placeholder(e, "dd/mm/aaaa"))
        
        # Data de Vencimento
        ttk.Label(
            self.form_frame, 
            text="Data de Vencimento:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=6, column=0, sticky="e", padx=5, pady=5)
        
        self.data_vencimento_var = tk.StringVar()
        self.data_vencimento_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.data_vencimento_var,
            font=("Arial", 10)
        )
        self.data_vencimento_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        self.data_vencimento_entry.insert(0, "dd/mm/aaaa")
        self.data_vencimento_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "dd/mm/aaaa"))
        self.data_vencimento_entry.bind("<FocusOut>", lambda e: self.set_placeholder(e, "dd/mm/aaaa"))
        
        # Próxima Inspeção
        ttk.Label(
            self.form_frame, 
            text="Próxima Inspeção:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=7, column=0, sticky="e", padx=5, pady=5)
        
        self.proxima_inspecao_var = tk.StringVar()
        self.proxima_inspecao_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.proxima_inspecao_var,
            font=("Arial", 10)
        )
        self.proxima_inspecao_entry.grid(row=7, column=1, sticky="w", padx=5, pady=5)
        self.proxima_inspecao_entry.insert(0, "dd/mm/aaaa")
        self.proxima_inspecao_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "dd/mm/aaaa"))
        self.proxima_inspecao_entry.bind("<FocusOut>", lambda e: self.set_placeholder(e, "dd/mm/aaaa"))
        
        # Última Inspeção
        ttk.Label(
            self.form_frame, 
            text="Última Inspeção:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=8, column=0, sticky="e", padx=5, pady=5)
        
        self.ultima_inspecao_var = tk.StringVar()
        self.ultima_inspecao_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.ultima_inspecao_var,
            font=("Arial", 10)
        )
        self.ultima_inspecao_entry.grid(row=8, column=1, sticky="w", padx=5, pady=5)
        self.ultima_inspecao_entry.insert(0, "dd/mm/aaaa")
        self.ultima_inspecao_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(e, "dd/mm/aaaa"))
        self.ultima_inspecao_entry.bind("<FocusOut>", lambda e: self.set_placeholder(e, "dd/mm/aaaa"))
        
        # Responsável
        ttk.Label(
            self.form_frame, 
            text="Responsável:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=9, column=0, sticky="e", padx=5, pady=5)
        
        self.responsavel_var = tk.StringVar()
        self.responsavel_entry = ttk.Entry(
            self.form_frame, 
            textvariable=self.responsavel_var,
            font=("Arial", 10)
        )
        self.responsavel_entry.grid(row=9, column=1, sticky="w", padx=5, pady=5)
        
        # Status
        ttk.Label(
            self.form_frame, 
            text="Status:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=10, column=0, sticky="e", padx=5, pady=5)
        
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.status_var,
            values=self.status_options,
            state="readonly",
            font=("Arial", 10)
        )
        self.status_combobox.grid(row=10, column=1, sticky="w", padx=5, pady=5)
        
        # Pressão
        ttk.Label(
            self.form_frame, 
            text="Pressão:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=11, column=0, sticky="e", padx=5, pady=5)
        
        self.pressao_var = tk.StringVar(value="OK")
        self.pressao_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.pressao_var,
            values=["OK", "Baixa", "Alta", "Sem Indicador"],
            font=("Arial", 10)
        )
        self.pressao_combobox.grid(row=11, column=1, sticky="w", padx=5, pady=5)
        
        # Sinalização
        ttk.Label(
            self.form_frame, 
            text="Sinalização:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=12, column=0, sticky="e", padx=5, pady=5)
        
        self.sinalizacao_var = tk.StringVar(value="OK")
        self.sinalizacao_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.sinalizacao_var,
            values=["OK", "Faltante", "Danificada", "Incompleta"],
            font=("Arial", 10)
        )
        self.sinalizacao_combobox.grid(row=12, column=1, sticky="w", padx=5, pady=5)
        
        # Acessórios
        ttk.Label(
            self.form_frame, 
            text="Acessórios:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=13, column=0, sticky="e", padx=5, pady=5)
        
        self.acessorios_var = tk.StringVar(value="OK")
        self.acessorios_combobox = ttk.Combobox(
            self.form_frame,
            textvariable=self.acessorios_var,
            values=["OK", "Faltante", "Danificado", "Incompleto"],
            font=("Arial", 10)
        )
        self.acessorios_combobox.grid(row=13, column=1, sticky="w", padx=5, pady=5)
        
        # Observações
        ttk.Label(
            self.form_frame, 
            text="Observações:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=14, column=0, sticky="ne", padx=5, pady=5)
        
        self.observacoes_text = tk.Text(
            self.form_frame,
            height=4,
            width=30,
            font=("Arial", 10)
        )
        self.observacoes_text.grid(row=14, column=1, sticky="w", padx=5, pady=5)
        
        # Frame de botões
        self.buttons_frame = ttk.Frame(self.cadastro_frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botões
        self.novo_button = ttk.Button(
            self.buttons_frame,
            text="Novo",
            command=self.novo_extintor,
            style='TButton'
        )
        self.novo_button.pack(side=tk.LEFT, padx=5)
        
        self.salvar_button = ttk.Button(
            self.buttons_frame,
            text="Salvar",
            command=self.salvar_extintor,
            style='TButton'
        )
        self.salvar_button.pack(side=tk.LEFT, padx=5)
        
        self.editar_button = ttk.Button(
            self.buttons_frame,
            text="Editar",
            command=self.editar_extintor,
            style='TButton'
        )
        self.editar_button.pack(side=tk.LEFT, padx=5)
        
        self.excluir_button = ttk.Button(
            self.buttons_frame,
            text="Excluir",
            command=self.excluir_extintor,
            style='TButton'
        )
        self.excluir_button.pack(side=tk.LEFT, padx=5)
        
        self.limpar_button = ttk.Button(
            self.buttons_frame,
            text="Limpar",
            command=self.limpar_formulario,
            style='TButton'
        )
        self.limpar_button.pack(side=tk.LEFT, padx=5)
        
        # Configurar validação de entrada
        self.setup_validation()
        
    def create_consulta_widgets(self):
        """Cria os widgets da aba de consulta"""
        # Frame de filtros
        self.filtros_frame = ttk.Frame(self.consulta_frame)
        self.filtros_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Filtro por Tipo
        ttk.Label(
            self.filtros_frame, 
            text="Filtrar por Tipo:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.filtro_tipo_var = tk.StringVar()
        self.filtro_tipo_combobox = ttk.Combobox(
            self.filtros_frame,
            textvariable=self.filtro_tipo_var,
            values=["Todos"] + self.tipos_extintores,
            state="readonly",
            font=("Arial", 10)
        )
        self.filtro_tipo_combobox.current(0)
        self.filtro_tipo_combobox.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Filtro por Status
        ttk.Label(
            self.filtros_frame, 
            text="Filtrar por Status:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=0, column=2, sticky="e", padx=5, pady=5)
        
        self.filtro_status_var = tk.StringVar()
        self.filtro_status_combobox = ttk.Combobox(
            self.filtros_frame,
            textvariable=self.filtro_status_var,
            values=["Todos"] + self.status_options,
            state="readonly",
            font=("Arial", 10)
        )
        self.filtro_status_combobox.current(0)
        self.filtro_status_combobox.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Filtro por Setor
        ttk.Label(
            self.filtros_frame, 
            text="Filtrar por Setor:", 
            font=("Arial", 10),
            foreground=COR_LABEL
        ).grid(row=0, column=4, sticky="e", padx=5, pady=5)
        
        self.filtro_setor_var = tk.StringVar()
        self.filtro_setor_combobox = ttk.Combobox(
            self.filtros_frame,
            textvariable=self.filtro_setor_var,
            values=["Todos"] + self.setores,
            font=("Arial", 10)
        )
        self.filtro_setor_combobox.current(0)
        self.filtro_setor_combobox.grid(row=0, column=5, sticky="w", padx=5, pady=5)
        
        # Botão de Filtrar
        self.filtrar_button = ttk.Button(
            self.filtros_frame,
            text="Filtrar",
            command=self.filtrar_extintores,
            style='TButton'
        )
        self.filtrar_button.grid(row=0, column=6, padx=10, pady=5)
        
        # Treeview para exibir os extintores
        self.tree_frame = ttk.Frame(self.consulta_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        self.tree_scroll_y = tk.Scrollbar(self.tree_frame)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_scroll_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set,
            selectmode="browse"
        )
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar scrollbars
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        
        # Definir colunas
        self.tree["columns"] = (
            "id", "tipo", "capacidade", "localizacao", "setor", 
            "data_fabricacao", "data_vencimento", "status"
        )
        
        # Formatar colunas
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("tipo", width=150, anchor=tk.W)
        self.tree.column("capacidade", width=80, anchor=tk.CENTER)
        self.tree.column("localizacao", width=200, anchor=tk.W)
        self.tree.column("setor", width=120, anchor=tk.W)
        self.tree.column("data_fabricacao", width=100, anchor=tk.CENTER)
        self.tree.column("data_vencimento", width=100, anchor=tk.CENTER)
        self.tree.column("status", width=120, anchor=tk.W)
        
        # Criar cabeçalhos
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("id", text="ID", anchor=tk.CENTER)
        self.tree.heading("tipo", text="Tipo", anchor=tk.W)
        self.tree.heading("capacidade", text="Capacidade", anchor=tk.CENTER)
        self.tree.heading("localizacao", text="Localização", anchor=tk.W)
        self.tree.heading("setor", text="Setor", anchor=tk.W)
        self.tree.heading("data_fabricacao", text="Fabricação", anchor=tk.CENTER)
        self.tree.heading("data_vencimento", text="Vencimento", anchor=tk.CENTER)
        self.tree.heading("status", text="Status", anchor=tk.W)
        
        # Preencher treeview com dados
        self.atualizar_treeview()
        
        # Configurar evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_extintor)
        
        # Frame de botões
        self.consulta_buttons_frame = ttk.Frame(self.consulta_frame)
        self.consulta_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botão para gerar relatório da consulta
        self.gerar_relatorio_button = ttk.Button(
            self.consulta_buttons_frame,
            text="Gerar Relatório",
            command=self.gerar_relatorio_consulta,
            style='TButton'
        )
        self.gerar_relatorio_button.pack(side=tk.LEFT, padx=5)
        
    def create_relatorios_widgets(self):
        """Cria os widgets da aba de relatórios"""
        # Frame principal
        self.relatorios_main_frame = ttk.Frame(self.relatorios_frame)
        self.relatorios_main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(
            self.relatorios_main_frame, 
            text="Relatórios Disponíveis", 
            font=("Arial", 16, "bold"),
            foreground=COR_LABEL
        ).pack(pady=(0, 20))
        
        # Frame de botões de relatórios
        self.relatorios_buttons_frame = ttk.Frame(self.relatorios_main_frame)
        self.relatorios_buttons_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Botões de relatórios
        self.relatorio_extintores_button = ttk.Button(
            self.relatorios_buttons_frame,
            text="Relatório Completo de Extintores",
            command=lambda: self.gerar_relatorio("completo"),
            style='TButton',
            width=30
        )
        self.relatorio_extintores_button.pack(pady=5)
        
        self.relatorio_vencimentos_button = ttk.Button(
            self.relatorios_buttons_frame,
            text="Relatório de Extintores Próximos ao Vencimento",
            command=lambda: self.gerar_relatorio("vencimento"),
            style='TButton',
            width=30
        )
        self.relatorio_vencimentos_button.pack(pady=5)
        
        self.relatorio_status_button = ttk.Button(
            self.relatorios_buttons_frame,
            text="Relatório por Status",
            command=lambda: self.gerar_relatorio("status"),
            style='TButton',
            width=30
        )
        self.relatorio_status_button.pack(pady=5)
        
        self.relatorio_setor_button = ttk.Button(
            self.relatorios_buttons_frame,
            text="Relatório por Setor",
            command=lambda: self.gerar_relatorio("setor"),
            style='TButton',
            width=30
        )
        self.relatorio_setor_button.pack(pady=5)
        
        self.relatorio_tipo_button = ttk.Button(
            self.relatorios_buttons_frame,
            text="Relatório por Tipo",
            command=lambda: self.gerar_relatorio("tipo"),
            style='TButton',
            width=30
        )
        self.relatorio_tipo_button.pack(pady=5)
        
        self.relatorio_inspecao_button = ttk.Button(
            self.relatorios_buttons_frame,
            text="Relatório de Inspeções Pendentes",
            command=lambda: self.gerar_relatorio("inspecao"),
            style='TButton',
            width=30
        )
        self.relatorio_inspecao_button.pack(pady=5)
        
    def setup_validation(self):
        """Configura a validação de entrada para os campos"""
        # Validar que só contém letras (para campos como responsável)
        vcmd_letters = (self.root.register(self.validate_letters), '%P')
        
        # Validar que só contém números (para campos como capacidade quando kg/L)
        vcmd_numbers = (self.root.register(self.validate_numbers), '%P')
        
        # Validar formato de data
        vcmd_date = (self.root.register(self.validate_date), '%P')
        
        # Aplicar validações
        self.responsavel_entry.config(validate="key", validatecommand=vcmd_letters)
        
        # Para campos de data
        self.data_fabricacao_entry.config(validate="key", validatecommand=vcmd_date)
        self.data_vencimento_entry.config(validate="key", validatecommand=vcmd_date)
        self.proxima_inspecao_entry.config(validate="key", validatecommand=vcmd_date)
        self.ultima_inspecao_entry.config(validate="key", validatecommand=vcmd_date)
        
    def validate_letters(self, value):
        """Valida que o campo contém apenas letras e espaços"""
        if value == "":
            return True
        return all(c.isalpha() or c.isspace() for c in value)
    
    def validate_numbers(self, value):
        """Valida que o campo contém apenas números"""
        if value == "":
            return True
        return value.isdigit()
    
    def validate_date(self, value):
        """Valida o formato da data (dd/mm/aaaa) de forma flexível usando uma expressão regular."""
        # Esta regex verifica se o texto corresponde ao padrão de data parcial ou completo.
        # ^                  -> Início da string
        # \d{0,2}            -> Dia (de 0 a 2 dígitos)
        # (?:/\d{0,2})?      -> Opcional: uma barra seguida pelo Mês (de 0 a 2 dígitos)
        # (?:/\d{0,4})?      -> Opcional: uma barra seguida pelo Ano (de 0 a 4 dígitos)
        # $                  -> Fim da string
        # A combinação permite que o usuário digite a data passo a passo.
        
        # Regex corrigida para permitir a barra no final de dia e mês
        if re.match(r"^\d{0,2}(/?(\d{0,2}(/?(\d{0,4})?)?)?)?$", value):
            return True
        return False
    
    def clear_placeholder(self, event, placeholder):
        """Limpa o placeholder quando o campo recebe foco"""
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            widget.config(fg="black")
    
    def set_placeholder(self, event, placeholder):
        """Coloca o placeholder se o campo estiver vazio"""
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(fg="gray")
    
    def novo_extintor(self):
        """Prepara o formulário para um novo cadastro"""
        self.limpar_formulario()
        self.id_var.set(str(self.current_id))
        self.status_var.set("Ativo")
        
    def salvar_extintor(self):
        """Salva um novo extintor ou atualiza um existente"""
        # Validar campos obrigatórios
        if not self.validar_campos():
            return
            
        # Obter dados do formulário
        extintor = {
            "id": int(self.id_var.get()),
            "tipo": self.tipo_var.get(),
            "capacidade": self.capacidade_var.get(),
            "localizacao": self.localizacao_var.get(),
            "setor": self.setor_var.get(),
            "data_fabricacao": self.data_fabricacao_var.get(),
            "data_vencimento": self.data_vencimento_var.get(),
            "proxima_inspecao": self.proxima_inspecao_var.get(),
            "ultima_inspecao": self.ultima_inspecao_var.get(),
            "responsavel": self.responsavel_var.get(),
            "status": self.status_var.get(),
            "pressao": self.pressao_var.get(),
            "sinalizacao": self.sinalizacao_var.get(),
            "acessorios": self.acessorios_var.get(),
            "observacoes": self.observacoes_text.get("1.0", tk.END).strip()
        }
        
        # Verificar se é um novo registro ou edição
        if extintor["id"] == self.current_id:
            # Novo registro
            self.extintores.append(extintor)
            self.current_id += 1
            messagebox.showinfo("Sucesso", "Extintor cadastrado com sucesso!")
        else:
            # Edição de registro existente
            for i, e in enumerate(self.extintores):
                if e["id"] == extintor["id"]:
                    self.extintores[i] = extintor
                    break
            messagebox.showinfo("Sucesso", "Extintor atualizado com sucesso!")
        
        # Atualizar treeview
        self.atualizar_treeview()
        
        # Limpar formulário
        self.limpar_formulario()
    
    def validar_campos(self):
        """Valida se todos os campos obrigatórios foram preenchidos"""
        campos_obrigatorios = [
            ("Tipo de Extintor", self.tipo_var.get()),
            ("Capacidade", self.capacidade_var.get()),
            ("Localização", self.localizacao_var.get()),
            ("Setor", self.setor_var.get()),
            ("Data de Fabricação", self.data_fabricacao_var.get()),
            ("Data de Vencimento", self.data_vencimento_var.get()),
            ("Próxima Inspeção", self.proxima_inspecao_var.get()),
            ("Status", self.status_var.get())
        ]
        
        for campo, valor in campos_obrigatorios:
            if not valor or valor == "dd/mm/aaaa":
                messagebox.showerror("Erro", f"O campo {campo} é obrigatório!")
                return False
                
        # Validar formato das datas
        try:
            datetime.strptime(self.data_fabricacao_var.get(), "%d/%m/%Y")
            datetime.strptime(self.data_vencimento_var.get(), "%d/%m/%Y")
            datetime.strptime(self.proxima_inspecao_var.get(), "%d/%m/%Y")
            if self.ultima_inspecao_var.get() and self.ultima_inspecao_var.get() != "dd/mm/aaaa":
                datetime.strptime(self.ultima_inspecao_var.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use dd/mm/aaaa.")
            return False
            
        return True
    
    def editar_extintor(self):
        """Edita o extintor selecionado na treeview"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Nenhum extintor selecionado!")
            return
            
        # Obter ID do extintor selecionado
        item = self.tree.item(selected)
        extintor_id = int(item["values"][0])
        
        # Encontrar extintor na lista
        extintor = next((e for e in self.extintores if e["id"] == extintor_id), None)
        if not extintor:
            messagebox.showerror("Erro", "Extintor não encontrado!")
            return
            
        # Preencher formulário com os dados do extintor
        self.limpar_formulario()
        self.id_var.set(str(extintor["id"]))
        self.tipo_var.set(extintor["tipo"])
        self.capacidade_var.set(extintor["capacidade"])
        self.localizacao_var.set(extintor["localizacao"])
        self.setor_var.set(extintor["setor"])
        self.data_fabricacao_var.set(extintor["data_fabricacao"])
        self.data_vencimento_var.set(extintor["data_vencimento"])
        self.proxima_inspecao_var.set(extintor["proxima_inspecao"])
        self.ultima_inspecao_var.set(extintor.get("ultima_inspecao", ""))
        self.responsavel_var.set(extintor.get("responsavel", ""))
        self.status_var.set(extintor["status"])
        self.pressao_var.set(extintor.get("pressao", "OK"))
        self.sinalizacao_var.set(extintor.get("sinalizacao", "OK"))
        self.acessorios_var.set(extintor.get("acessorios", "OK"))
        self.observacoes_text.insert("1.0", extintor.get("observacoes", ""))
    
    def excluir_extintor(self):
        """Exclui o extintor selecionado na treeview"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Nenhum extintor selecionado!")
            return
            
        # Confirmar exclusão
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este extintor?"):
            return
            
        # Obter ID do extintor selecionado
        item = self.tree.item(selected)
        extintor_id = int(item["values"][0])
        
        # Remover extintor da lista
        self.extintores = [e for e in self.extintores if e["id"] != extintor_id]
        
        # Atualizar treeview
        self.atualizar_treeview()
        
        # Limpar formulário
        self.limpar_formulario()
        
        messagebox.showinfo("Sucesso", "Extintor excluído com sucesso!")
    
    def limpar_formulario(self):
        """Limpa todos os campos do formulário"""
        self.id_var.set("")
        self.tipo_var.set("")
        self.capacidade_var.set("")
        self.localizacao_var.set("")
        self.setor_var.set("")
        self.data_fabricacao_var.set("dd/mm/aaaa")
        self.data_fabricacao_entry.config(fg="gray")
        self.data_vencimento_var.set("dd/mm/aaaa")
        self.data_vencimento_entry.config(fg="gray")
        self.proxima_inspecao_var.set("dd/mm/aaaa")
        self.proxima_inspecao_entry.config(fg="gray")
        self.ultima_inspecao_var.set("dd/mm/aaaa")
        self.ultima_inspecao_entry.config(fg="gray")
        self.responsavel_var.set("")
        self.status_var.set("")
        self.pressao_var.set("OK")
        self.sinalizacao_var.set("OK")
        self.acessorios_var.set("OK")
        self.observacoes_text.delete("1.0", tk.END)
        
        # Se não houver ID, definir o próximo disponível
        if not self.id_var.get():
            self.id_var.set(str(self.current_id))
    
    def atualizar_treeview(self):
        """Atualiza a treeview com os dados dos extintores"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Adicionar extintores à treeview
        for extintor in self.extintores:
            self.tree.insert("", tk.END, values=(
                extintor["id"],
                extintor["tipo"],
                extintor["capacidade"],
                extintor["localizacao"],
                extintor["setor"],
                extintor["data_fabricacao"],
                extintor["data_vencimento"],
                extintor["status"]
            ))
    
    def selecionar_extintor(self, event):
        """Preenche o formulário quando um extintor é selecionado na treeview"""
        selected = self.tree.focus()
        if selected:
            self.editar_extintor()
    
    def filtrar_extintores(self):
        """Filtra os extintores com base nos critérios selecionados"""
        tipo = self.filtro_tipo_var.get()
        status = self.filtro_status_var.get()
        setor = self.filtro_setor_var.get()
        
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Adicionar extintores filtrados à treeview
        for extintor in self.extintores:
            if tipo != "Todos" and extintor["tipo"] != tipo:
                continue
            if status != "Todos" and extintor["status"] != status:
                continue
            if setor != "Todos" and extintor["setor"] != setor:
                continue
                
            self.tree.insert("", tk.END, values=(
                extintor["id"],
                extintor["tipo"],
                extintor["capacidade"],
                extintor["localizacao"],
                extintor["setor"],
                extintor["data_fabricacao"],
                extintor["data_vencimento"],
                extintor["status"]
            ))
    
    def gerar_relatorio(self, tipo_relatorio):
        """Gera um relatório PDF com base no tipo especificado"""
        # Solicitar local para salvar o arquivo
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar Relatório Como",
            initialfile=f"relatorio_extintores_{tipo_relatorio}.pdf"
        )
        
        if not filepath:
            return  # Usuário cancelou
            
        # Criar documento PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Title", fontSize=18, alignment=1, spaceAfter=20))
        styles.add(ParagraphStyle(name="Subtitle", fontSize=12, alignment=1, spaceAfter=10))
        styles.add(ParagraphStyle(name="Header", fontSize=10, alignment=1, spaceAfter=5))
        styles.add(ParagraphStyle(name="NormalCenter", fontSize=10, alignment=1))
        
        # Elementos do relatório
        elements = []
        
        # Título do relatório
        title = "Relatório de Extintores"
        if tipo_relatorio == "vencimento":
            title = "Relatório de Extintores Próximos ao Vencimento"
        elif tipo_relatorio == "status":
            title = "Relatório de Extintores por Status"
        elif tipo_relatorio == "setor":
            title = "Relatório de Extintores por Setor"
        elif tipo_relatorio == "tipo":
            title = "Relatório de Extintores por Tipo"
        elif tipo_relatorio == "inspecao":
            title = "Relatório de Inspeções Pendentes"
            
        elements.append(Paragraph(title, styles["Title"]))
        
        # Data de emissão
        data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Emitido em: {data_emissao}", styles["Subtitle"]))
        
        # Filtrar dados conforme o tipo de relatório
        dados_relatorio = []
        if tipo_relatorio == "completo":
            dados_relatorio = self.extintores
            elements.append(Paragraph("Lista Completa de Extintores", styles["Header"]))
        elif tipo_relatorio == "vencimento":
            # Extintores que vencem nos próximos 3 meses
            hoje = datetime.now()
            tres_meses = hoje.replace(month=hoje.month + 3) if hoje.month + 3 <= 12 else hoje.replace(year=hoje.year + 1, month=(hoje.month + 3) % 12)
            
            for extintor in self.extintores:
                try:
                    data_venc = datetime.strptime(extintor["data_vencimento"], "%d/%m/%Y")
                    if hoje <= data_venc <= tres_meses:
                        dados_relatorio.append(extintor)
                except ValueError:
                    continue
                    
            elements.append(Paragraph("Extintores com Vencimento nos Próximos 3 Meses", styles["Header"]))
        elif tipo_relatorio == "status":
            # Agrupar por status
            status_groups = {}
            for extintor in self.extintores:
                status = extintor["status"]
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(extintor)
                
            # Ordenar por status
            for status, extintores in sorted(status_groups.items()):
                elements.append(Paragraph(f"Status: {status}", styles["Header"]))
                dados_relatorio.extend(extintores)
        elif tipo_relatorio == "setor":
            # Agrupar por setor
            setor_groups = {}
            for extintor in self.extintores:
                setor = extintor["setor"]
                if setor not in setor_groups:
                    setor_groups[setor] = []
                setor_groups[setor].append(extintor)
                
            # Ordenar por setor
            for setor, extintores in sorted(setor_groups.items()):
                elements.append(Paragraph(f"Setor: {setor}", styles["Header"]))
                dados_relatorio.extend(extintores)
        elif tipo_relatorio == "tipo":
            # Agrupar por tipo
            tipo_groups = {}
            for extintor in self.extintores:
                tipo = extintor["tipo"]
                if tipo not in tipo_groups:
                    tipo_groups[tipo] = []
                tipo_groups[tipo].append(extintor)
                
            # Ordenar por tipo
            for tipo, extintores in sorted(tipo_groups.items()):
                elements.append(Paragraph(f"Tipo: {tipo}", styles["Header"]))
                dados_relatorio.extend(extintores)
        elif tipo_relatorio == "inspecao":
            # Extintores com inspeção vencida ou próxima
            hoje = datetime.now()
            
            for extintor in self.extintores:
                try:
                    data_inspecao = datetime.strptime(extintor["proxima_inspecao"], "%d/%m/%Y")
                    if data_inspecao <= hoje:
                        dados_relatorio.append(extintor)
                except ValueError:
                    continue
                    
            elements.append(Paragraph("Extintores com Inspeção Pendente", styles["Header"]))
        
        # Se não houver dados, informar
        if not dados_relatorio:
            elements.append(Paragraph("Nenhum dado encontrado para este relatório.", styles["NormalCenter"]))
            doc.build(elements)
            webbrowser.open(filepath)
            return
            
        # Criar tabela com os dados
        data = [["ID", "Tipo", "Capac.", "Localização", "Setor", "Fabricação", "Vencimento", "Status"]]
        
        for extintor in dados_relatorio:
            data.append([
                str(extintor["id"]),
                extintor["tipo"],
                extintor["capacidade"],
                extintor["localizacao"],
                extintor["setor"],
                extintor["data_fabricacao"],
                extintor["data_vencimento"],
                extintor["status"]
            ])
        
        # Criar tabela
        table = Table(data)
        
        # Estilo da tabela
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3A5FCD")),  # Cabeçalho azul
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#EEEE00")),  # Fundo amarelo claro
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ])
        
        table.setStyle(style)
        
        # Adicionar tabela ao relatório
        elements.append(table)
        
        # Adicionar rodapé
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Sistema Extintor Manager - Relatório Gerado Automaticamente", styles["NormalCenter"]))
        
        # Gerar PDF
        doc.build(elements)
        
        # Abrir o PDF
        webbrowser.open(filepath)
    
    def gerar_relatorio_consulta(self):
        """Gera um relatório com os dados atualmente exibidos na consulta"""
        # Obter dados da treeview
        dados = []
        for item in self.tree.get_children():
            dados.append(self.tree.item(item)["values"])
        
        if not dados:
            messagebox.showwarning("Aviso", "Nenhum dado para gerar relatório!")
            return
            
        # Solicitar local para salvar o arquivo
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar Relatório Como",
            initialfile="relatorio_consulta_extintores.pdf"
        )
        
        if not filepath:
            return  # Usuário cancelou
            
        # Criar documento PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name="Title", fontSize=18, alignment=1, spaceAfter=20))
        styles.add(ParagraphStyle(name="Subtitle", fontSize=12, alignment=1, spaceAfter=10))
        styles.add(ParagraphStyle(name="Header", fontSize=10, alignment=1, spaceAfter=5))
        styles.add(ParagraphStyle(name="NormalCenter", fontSize=10, alignment=1))
        
        # Elementos do relatório
        elements = []
        
        # Título do relatório
        elements.append(Paragraph("Relatório de Consulta de Extintores", styles["Title"]))
        
        # Data de emissão
        data_emissao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        elements.append(Paragraph(f"Emitido em: {data_emissao}", styles["Subtitle"]))
        
        # Criar tabela com os dados
        data = [["ID", "Tipo", "Capac.", "Localização", "Setor", "Fabricação", "Vencimento", "Status"]]
        data.extend(dados)
        
        # Criar tabela
        table = Table(data)
        
        # Estilo da tabela
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4C63A9")),  # Cabeçalho azul
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#EEEE00")),  # Fundo amarelo claro
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ])
        
        table.setStyle(style)
        
        # Adicionar tabela ao relatório
        elements.append(table)
        
        # Adicionar rodapé
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Sistema Extintor Manager - Relatório Gerado Automaticamente", styles["NormalCenter"]))
        
        # Gerar PDF
        doc.build(elements)
        
        # Abrir o PDF
        webbrowser.open(filepath)

# Função principal
def main():
    root = tk.Tk()
    app = ExtintorManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()