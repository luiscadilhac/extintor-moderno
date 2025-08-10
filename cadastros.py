import tkinter as tk
from tkinter import ttk, messagebox
from ui.main_window import MainWindow

class CadastrosTab:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.frame = ttk.Frame(parent)
        
        # Variáveis de controle
        self.current_empresa = 0
        self.current_setor = 0
        self.current_cargo = 0
        self.current_atividade = 0
        self.current_ambiente = 0
        
        # Listas para armazenar os dados
        self.empresas = []
        self.setores = []
        self.cargos = []
        self.atividades = []
        self.ambientes = []
        
        # Carregar dados iniciais
        self.load_data()
        
        # Criar interface
        self.create_widgets()
        
        # Exibir primeiro registro
        self.show_empresa(0)
    
    def load_data(self):
        self.empresas = self.db.get_empresas()
        self.setores = self.db.get_setores()
        # ... (carregar demais dados)
    
    def create_widgets(self):
        # Criar frames para cada entidade
        self.create_empresa_widgets()
        self.create_setor_widgets()
        self.create_cargo_widgets()
        self.create_atividade_widgets()
        self.create_ambiente_widgets()
    
    def create_empresa_widgets(self):
        # Frame principal para Empresa
        empresa_main_frame = ttk.Frame(self.frame)
        empresa_main_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame para formulário de Empresa
        empresa_frame = ttk.LabelFrame(empresa_main_frame, text="Empresa")
        empresa_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame para visualização de Empresa
        empresa_view_frame = ttk.LabelFrame(empresa_main_frame, text="Visualização")
        empresa_view_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # ... (campos e botões de empresa)
    
    # ... (demais métodos create_* e show_*)