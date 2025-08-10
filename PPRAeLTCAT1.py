import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime

class SistemaPPRA:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema PPRA - Programa Preventivo de Riscos Ambientais e LTCAT")
        self.root.geometry("1200x800")
        self.root.state('zoomed')  # Maximizar janela no Windows
        
        # Criar banco de dados
        self.criar_banco()
        
        # Variáveis de controle
        self.registro_atual = {'empresa': 0, 'setor': 0, 'cargo': 0, 'atividade': 0, 'ambiente': 0}
        
        # Criar interface
        self.criar_interface()
        
        # Carregar primeiro registro
        self.carregar_primeiro_registro()
    
    def criar_banco(self):
        """Criar banco de dados SQLite"""
        self.conn = sqlite3.connect('ppra_ltcat.db')
        cursor = self.conn.cursor()
        
        # Tabela Empresas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empresas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cnpj TEXT,
                endereco TEXT,
                telefone TEXT,
                email TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela Setores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                empresa_id INTEGER,
                FOREIGN KEY (empresa_id) REFERENCES empresas (id)
            )
        ''')
        
        # Tabela Cargos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cargos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                cbo TEXT,
                setor_id INTEGER,
                FOREIGN KEY (setor_id) REFERENCES setores (id)
            )
        ''')
        
        # Tabela Atividades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                risco TEXT,
                frequencia TEXT,
                duracao TEXT,
                cargo_id INTEGER,
                FOREIGN KEY (cargo_id) REFERENCES cargos (id)
            )
        ''')
        
        # Tabela Ambientes Laborativos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ambientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                tipo TEXT,
                area REAL,
                ventilacao TEXT,
                iluminacao TEXT,
                ruido REAL,
                temperatura REAL,
                umidade REAL,
                cargo_id INTEGER,
                FOREIGN KEY (cargo_id) REFERENCES cargos (id)
            )
        ''')
        
        self.conn.commit()
    
    def criar_interface(self):
        """Criar interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema PPRA - Programa Preventivo de Riscos Ambientais e LTCAT", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aba Principal - Cadastros
        self.frame_cadastros = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cadastros, text="Cadastros")
        
        # Aba Relatórios
        self.frame_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_relatorios, text="Relatórios")
        
        self.criar_secao_cadastros()
        self.criar_secao_relatorios()
    
    def criar_secao_cadastros(self):
        """Criar seção de cadastros"""
        # Canvas e Scrollbar para scroll vertical
        canvas = tk.Canvas(self.frame_cadastros)
        scrollbar = ttk.Scrollbar(self.frame_cadastros, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # === SEÇÃO EMPRESA ===
        self.criar_secao_empresa(scrollable_frame)
        
        # === SEÇÃO SETOR ===
        self.criar_secao_setor(scrollable_frame)
        
        # === SEÇÃO CARGO ===
        self.criar_secao_cargo(scrollable_frame)
        
        # === SEÇÃO ATIVIDADE ===
        self.criar_secao_atividade(scrollable_frame)
        
        # === SEÇÃO AMBIENTE LABORATIVO ===
        self.criar_secao_ambiente(scrollable_frame)
        
        # Botões gerais
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(btn_frame, text="Salvar Tudo", command=self.salvar_tudo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar Tudo", command=self.limpar_tudo).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Criar Dados Exemplo", command=self.criar_dados_exemplo).pack(side=tk.LEFT, padx=5)
    
    def criar_secao_empresa(self, parent):
        """Criar seção de empresa"""
        # Frame da empresa
        empresa_frame = ttk.LabelFrame(parent, text="EMPRESA", padding=10)
        empresa_frame.pack(fill=tk.X, pady=10)
        
        # Botões de navegação
        nav_frame = ttk.Frame(empresa_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="<<", command=lambda: self.navegar('empresa', 'primeiro')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="<", command=lambda: self.navegar('empresa', 'anterior')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">", command=lambda: self.navegar('empresa', 'proximo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">>", command=lambda: self.navegar('empresa', 'ultimo')).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(nav_frame, text="Novo", command=lambda: self.novo_registro('empresa')).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Salvar", command=lambda: self.salvar_registro('empresa')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Editar", command=lambda: self.editar_registro('empresa')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Excluir", command=lambda: self.excluir_registro('empresa')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Listar", command=lambda: self.listar_registros('empresa')).pack(side=tk.LEFT, padx=2)
        
        # Campos da empresa
        campos_frame = ttk.Frame(empresa_frame)
        campos_frame.pack(fill=tk.X)
        
        # Linha 1
        linha1 = ttk.Frame(campos_frame)
        linha1.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha1, text="Nome:").pack(side=tk.LEFT, padx=(0, 5))
        self.empresa_nome = ttk.Entry(linha1, width=40)
        self.empresa_nome.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha1, text="CNPJ:").pack(side=tk.LEFT, padx=(0, 5))
        self.empresa_cnpj = ttk.Entry(linha1, width=20)
        self.empresa_cnpj.pack(side=tk.LEFT, padx=(0, 20))
        
        # Linha 2
        linha2 = ttk.Frame(campos_frame)
        linha2.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha2, text="Endereço:").pack(side=tk.LEFT, padx=(0, 5))
        self.empresa_endereco = ttk.Entry(linha2, width=60)
        self.empresa_endereco.pack(side=tk.LEFT, padx=(0, 20))
        
        # Linha 3
        linha3 = ttk.Frame(campos_frame)
        linha3.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha3, text="Telefone:").pack(side=tk.LEFT, padx=(0, 5))
        self.empresa_telefone = ttk.Entry(linha3, width=20)
        self.empresa_telefone.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha3, text="Email:").pack(side=tk.LEFT, padx=(0, 5))
        self.empresa_email = ttk.Entry(linha3, width=40)
        self.empresa_email.pack(side=tk.LEFT)
    
    def criar_secao_setor(self, parent):
        """Criar seção de setor"""
        setor_frame = ttk.LabelFrame(parent, text="SETOR", padding=10)
        setor_frame.pack(fill=tk.X, pady=10)
        
        # Botões de navegação
        nav_frame = ttk.Frame(setor_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="<<", command=lambda: self.navegar('setor', 'primeiro')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="<", command=lambda: self.navegar('setor', 'anterior')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">", command=lambda: self.navegar('setor', 'proximo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">>", command=lambda: self.navegar('setor', 'ultimo')).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(nav_frame, text="Novo", command=lambda: self.novo_registro('setor')).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Salvar", command=lambda: self.salvar_registro('setor')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Editar", command=lambda: self.editar_registro('setor')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Excluir", command=lambda: self.excluir_registro('setor')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Listar", command=lambda: self.listar_registros('setor')).pack(side=tk.LEFT, padx=2)
        
        # Campos do setor
        campos_frame = ttk.Frame(setor_frame)
        campos_frame.pack(fill=tk.X)
        
        linha1 = ttk.Frame(campos_frame)
        linha1.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha1, text="Nome:").pack(side=tk.LEFT, padx=(0, 5))
        self.setor_nome = ttk.Entry(linha1, width=40)
        self.setor_nome.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha1, text="Descrição:").pack(side=tk.LEFT, padx=(0, 5))
        self.setor_descricao = ttk.Entry(linha1, width=60)
        self.setor_descricao.pack(side=tk.LEFT)
    
    def criar_secao_cargo(self, parent):
        """Criar seção de cargo"""
        cargo_frame = ttk.LabelFrame(parent, text="CARGO", padding=10)
        cargo_frame.pack(fill=tk.X, pady=10)
        
        # Botões de navegação
        nav_frame = ttk.Frame(cargo_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="<<", command=lambda: self.navegar('cargo', 'primeiro')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="<", command=lambda: self.navegar('cargo', 'anterior')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">", command=lambda: self.navegar('cargo', 'proximo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">>", command=lambda: self.navegar('cargo', 'ultimo')).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(nav_frame, text="Novo", command=lambda: self.novo_registro('cargo')).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Salvar", command=lambda: self.salvar_registro('cargo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Editar", command=lambda: self.editar_registro('cargo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Excluir", command=lambda: self.excluir_registro('cargo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Listar", command=lambda: self.listar_registros('cargo')).pack(side=tk.LEFT, padx=2)
        
        # Campos do cargo
        campos_frame = ttk.Frame(cargo_frame)
        campos_frame.pack(fill=tk.X)
        
        linha1 = ttk.Frame(campos_frame)
        linha1.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha1, text="Nome:").pack(side=tk.LEFT, padx=(0, 5))
        self.cargo_nome = ttk.Entry(linha1, width=40)
        self.cargo_nome.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha1, text="CBO:").pack(side=tk.LEFT, padx=(0, 5))
        self.cargo_cbo = ttk.Entry(linha1, width=20)
        self.cargo_cbo.pack(side=tk.LEFT)
        
        linha2 = ttk.Frame(campos_frame)
        linha2.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha2, text="Descrição:").pack(side=tk.LEFT, padx=(0, 5))
        self.cargo_descricao = ttk.Entry(linha2, width=80)
        self.cargo_descricao.pack(side=tk.LEFT)
    
    def criar_secao_atividade(self, parent):
        """Criar seção de atividade"""
        atividade_frame = ttk.LabelFrame(parent, text="ATIVIDADE", padding=10)
        atividade_frame.pack(fill=tk.X, pady=10)
        
        # Botões de navegação
        nav_frame = ttk.Frame(atividade_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="<<", command=lambda: self.navegar('atividade', 'primeiro')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="<", command=lambda: self.navegar('atividade', 'anterior')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">", command=lambda: self.navegar('atividade', 'proximo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">>", command=lambda: self.navegar('atividade', 'ultimo')).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(nav_frame, text="Novo", command=lambda: self.novo_registro('atividade')).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Salvar", command=lambda: self.salvar_registro('atividade')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Editar", command=lambda: self.editar_registro('atividade')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Excluir", command=lambda: self.excluir_registro('atividade')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Listar", command=lambda: self.listar_registros('atividade')).pack(side=tk.LEFT, padx=2)
        
        # Campos da atividade
        campos_frame = ttk.Frame(atividade_frame)
        campos_frame.pack(fill=tk.X)
        
        linha1 = ttk.Frame(campos_frame)
        linha1.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha1, text="Descrição:").pack(side=tk.LEFT, padx=(0, 5))
        self.atividade_descricao = ttk.Entry(linha1, width=60)
        self.atividade_descricao.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha1, text="Risco:").pack(side=tk.LEFT, padx=(0, 5))
        self.atividade_risco = ttk.Combobox(linha1, values=["Baixo", "Médio", "Alto", "Crítico"], width=15)
        self.atividade_risco.pack(side=tk.LEFT)
        
        linha2 = ttk.Frame(campos_frame)
        linha2.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha2, text="Frequência:").pack(side=tk.LEFT, padx=(0, 5))
        self.atividade_frequencia = ttk.Entry(linha2, width=20)
        self.atividade_frequencia.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha2, text="Duração:").pack(side=tk.LEFT, padx=(0, 5))
        self.atividade_duracao = ttk.Entry(linha2, width=20)
        self.atividade_duracao.pack(side=tk.LEFT)
    
    def criar_secao_ambiente(self, parent):
        """Criar seção de ambiente laborativo"""
        ambiente_frame = ttk.LabelFrame(parent, text="AMBIENTE LABORATIVO", padding=10)
        ambiente_frame.pack(fill=tk.X, pady=10)
        
        # Botões de navegação
        nav_frame = ttk.Frame(ambiente_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="<<", command=lambda: self.navegar('ambiente', 'primeiro')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="<", command=lambda: self.navegar('ambiente', 'anterior')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">", command=lambda: self.navegar('ambiente', 'proximo')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text=">>", command=lambda: self.navegar('ambiente', 'ultimo')).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(nav_frame, text="Novo", command=lambda: self.novo_registro('ambiente')).pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="Salvar", command=lambda: self.salvar_registro('ambiente')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Editar", command=lambda: self.editar_registro('ambiente')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Excluir", command=lambda: self.excluir_registro('ambiente')).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Listar", command=lambda: self.listar_registros('ambiente')).pack(side=tk.LEFT, padx=2)
        
        # Campos do ambiente
        campos_frame = ttk.Frame(ambiente_frame)
        campos_frame.pack(fill=tk.X)
        
        linha1 = ttk.Frame(campos_frame)
        linha1.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha1, text="Nome:").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_nome = ttk.Entry(linha1, width=40)
        self.ambiente_nome.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha1, text="Tipo:").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_tipo = ttk.Combobox(linha1, values=["Administrativo", "Produção", "Armazém", "Laboratório", "Oficina"], width=15)
        self.ambiente_tipo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha1, text="Área (m²):").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_area = ttk.Entry(linha1, width=10)
        self.ambiente_area.pack(side=tk.LEFT)
        
        linha2 = ttk.Frame(campos_frame)
        linha2.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha2, text="Ventilação:").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_ventilacao = ttk.Combobox(linha2, values=["Natural", "Artificial", "Mista"], width=15)
        self.ambiente_ventilacao.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha2, text="Iluminação:").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_iluminacao = ttk.Combobox(linha2, values=["Natural", "Artificial", "Mista"], width=15)
        self.ambiente_iluminacao.pack(side=tk.LEFT, padx=(0, 20))
        
        linha3 = ttk.Frame(campos_frame)
        linha3.pack(fill=tk.X, pady=2)
        
        ttk.Label(linha3, text="Ruído (dB):").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_ruido = ttk.Entry(linha3, width=10)
        self.ambiente_ruido.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha3, text="Temp. (°C):").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_temperatura = ttk.Entry(linha3, width=10)
        self.ambiente_temperatura.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(linha3, text="Umidade (%):").pack(side=tk.LEFT, padx=(0, 5))
        self.ambiente_umidade = ttk.Entry(linha3, width=10)
        self.ambiente_umidade.pack(side=tk.LEFT)
    
    def criar_secao_relatorios(self):
        """Criar seção de relatórios"""
        relatorios_frame = ttk.Frame(self.frame_relatorios)
        relatorios_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(relatorios_frame, text="Relatórios", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # Botões de relatórios
        btn_frame = ttk.Frame(relatorios_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Relatório Geral", command=self.gerar_relatorio_geral).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Relatório por Empresa", command=self.gerar_relatorio_empresa).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Relatório de Riscos", command=self.gerar_relatorio_riscos).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="LTCAT", command=self.gerar_ltcat).pack(side=tk.LEFT, padx=10)
        
        # Área de texto para relatórios
        texto_frame = ttk.Frame(relatorios_frame)
        texto_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        self.texto_relatorio = tk.Text(texto_frame, wrap=tk.WORD, height=30)
        scrollbar_rel = ttk.Scrollbar(texto_frame, orient="vertical", command=self.texto_relatorio.yview)
        
        self.texto_relatorio.pack(side="left", fill="both", expand=True)
        scrollbar_rel.pack(side="right", fill="y")
        self.texto_relatorio.configure(yscrollcommand=scrollbar_rel.set)
    
    # === MÉTODOS DE NAVEGAÇÃO ===
    def navegar(self, tipo, direcao):
        """Navegar entre registros"""
        cursor = self.conn.cursor()
        tabelas = {'empresa': 'empresas', 'setor': 'setores', 'cargo': 'cargos', 'atividade': 'atividades', 'ambiente': 'ambientes'}
        tabela = tabelas.get(tipo)
        
        if not tabela:
            return
        
        current_id = self.registro_atual[tipo]
        
        try:
            if direcao == 'primeiro':
                cursor.execute(f"SELECT MIN(id) FROM {tabela}")
                result = cursor.fetchone()
                if result and result[0]:
                    self.registro_atual[tipo] = result[0]
            elif direcao == 'ultimo':
                cursor.execute(f"SELECT MAX(id) FROM {tabela}")
                result = cursor.fetchone()
                if result and result[0]:
                    self.registro_atual[tipo] = result[0]
            elif direcao == 'anterior':
                cursor.execute(f"SELECT MAX(id) FROM {tabela} WHERE id < ?", (current_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    self.registro_atual[tipo] = result[0]
                else:
                    messagebox.showinfo("Info", "Você já está no primeiro registro.")
                    return
            elif direcao == 'proximo':
                cursor.execute(f"SELECT MIN(id) FROM {tabela} WHERE id > ?", (current_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    self.registro_atual[tipo] = result[0]
                else:
                    messagebox.showinfo("Info", "Você já está no último registro.")
                    return
            
            self.carregar_registro(tipo)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao navegar: {str(e)}")
    
    def carregar_registro(self, tipo):
        """Carregar dados de um registro específico"""
        cursor = self.conn.cursor()
        
        try:
            if tipo == 'empresa' and self.registro_atual['empresa'] != 0:
                cursor.execute("SELECT * FROM empresas WHERE id = ?", (self.registro_atual['empresa'],))
                result = cursor.fetchone()
                if result:
                    self.empresa_nome.delete(0, tk.END)
                    self.empresa_nome.insert(0, result[1] or "")
                    self.empresa_cnpj.delete(0, tk.END)
                    self.empresa_cnpj.insert(0, result[2] or "")
                    self.empresa_endereco.delete(0, tk.END)
                    self.empresa_endereco.insert(0, result[3] or "")
                    self.empresa_telefone.delete(0, tk.END)
                    self.empresa_telefone.insert(0, result[4] or "")
                    self.empresa_email.delete(0, tk.END)
                    self.empresa_email.insert(0, result[5] or "")
            
            elif tipo == 'setor' and self.registro_atual['setor'] != 0:
                cursor.execute("SELECT * FROM setores WHERE id = ?", (self.registro_atual['setor'],))
                result = cursor.fetchone()
                if result:
                    self.setor_nome.delete(0, tk.END)
                    self.setor_nome.insert(0, result[1] or "")
                    self.setor_descricao.delete(0, tk.END)
                    self.setor_descricao.insert(0, result[2] or "")
            
            elif tipo == 'cargo' and self.registro_atual['cargo'] != 0:
                cursor.execute("SELECT * FROM cargos WHERE id = ?", (self.registro_atual['cargo'],))
                result = cursor.fetchone()
                if result:
                    self.cargo_nome.delete(0, tk.END)
                    self.cargo_nome.insert(0, result[1] or "")
                    self.cargo_descricao.delete(0, tk.END)
                    self.cargo_descricao.insert(0, result[2] or "")
                    self.cargo_cbo.delete(0, tk.END)
                    self.cargo_cbo.insert(0, result[3] or "")
            
            elif tipo == 'atividade' and self.registro_atual['atividade'] != 0:
                cursor.execute("SELECT * FROM atividades WHERE id = ?", (self.registro_atual['atividade'],))
                result = cursor.fetchone()
                if result:
                    self.atividade_descricao.delete(0, tk.END)
                    self.atividade_descricao.insert(0, result[1] or "")
                    self.atividade_risco.set(result[2] or "")
                    self.atividade_frequencia.delete(0, tk.END)
                    self.atividade_frequencia.insert(0, result[3] or "")
                    self.atividade_duracao.delete(0, tk.END)
                    self.atividade_duracao.insert(0, result[4] or "")
            
            elif tipo == 'ambiente' and self.registro_atual['ambiente'] != 0:
                cursor.execute("SELECT * FROM ambientes WHERE id = ?", (self.registro_atual['ambiente'],))
                result = cursor.fetchone()
                if result:
                    self.ambiente_nome.delete(0, tk.END)
                    self.ambiente_nome.insert(0, result[1] or "")
                    self.ambiente_tipo.set(result[2] or "")
                    self.ambiente_area.delete(0, tk.END)
                    self.ambiente_area.insert(0, str(result[3] or ""))
                    self.ambiente_ventilacao.set(result[4] or "")
                    self.ambiente_iluminacao.set(result[5] or "")
                    self.ambiente_ruido.delete(0, tk.END)
                    self.ambiente_ruido.insert(0, str(result[6] or ""))
                    self.ambiente_temperatura.delete(0, tk.END)
                    self.ambiente_temperatura.insert(0, str(result[7] or ""))
                    self.ambiente_umidade.delete(0, tk.END)
                    self.ambiente_umidade.insert(0, str(result[8] or ""))
                    
        except Exception as e:
            print(f"Erro ao carregar registro {tipo}: {str(e)}")  # Debug
    
    def carregar_primeiro_registro(self):
        """Carregar o primeiro registro disponível"""
        cursor = self.conn.cursor()
        
        # Carregar empresa
        cursor.execute("SELECT MIN(id) FROM empresas")
        result = cursor.fetchone()
        if result and result[0]:
            self.registro_atual['empresa'] = result[0]
            self.carregar_registro('empresa')
        else:
            self.registro_atual['empresa'] = 0
        
        # Carregar setor
        cursor.execute("SELECT MIN(id) FROM setores")
        result = cursor.fetchone()
        if result and result[0]:
            self.registro_atual['setor'] = result[0]
            self.carregar_registro('setor')
        else:
            self.registro_atual['setor'] = 0
        
        # Carregar cargo
        cursor.execute("SELECT MIN(id) FROM cargos")
        result = cursor.fetchone()
        if result and result[0]:
            self.registro_atual['cargo'] = result[0]
            self.carregar_registro('cargo')
        else:
            self.registro_atual['cargo'] = 0
        
        # Carregar atividade
        cursor.execute("SELECT MIN(id) FROM atividades")
        result = cursor.fetchone()
        if result and result[0]:
            self.registro_atual['atividade'] = result[0]
            self.carregar_registro('atividade')
        else:
            self.registro_atual['atividade'] = 0
        
        # Carregar ambiente
        cursor.execute("SELECT MIN(id) FROM ambientes")
        result = cursor.fetchone()
        if result and result[0]:
            self.registro_atual['ambiente'] = result[0]
            self.carregar_registro('ambiente')
        else:
            self.registro_atual['ambiente'] = 0
    
    # === MÉTODOS CRUD ===
    def novo_registro(self, tipo):
        """Criar novo registro"""
        if tipo == 'empresa':
            self.limpar_campos_empresa()
            self.registro_atual['empresa'] = 0
        elif tipo == 'setor':
            self.limpar_campos_setor()
            self.registro_atual['setor'] = 0
        elif tipo == 'cargo':
            self.limpar_campos_cargo()
            self.registro_atual['cargo'] = 0
        elif tipo == 'atividade':
            self.limpar_campos_atividade()
            self.registro_atual['atividade'] = 0
        elif tipo == 'ambiente':
            self.limpar_campos_ambiente()
            self.registro_atual['ambiente'] = 0
    
    def salvar_registro(self, tipo):
        """Salvar registro no banco"""
        cursor = self.conn.cursor()
        
        try:
            if tipo == 'empresa':
                if self.registro_atual['empresa'] == 0:
                    # Inserir novo
                    cursor.execute('''
                        INSERT INTO empresas (nome, cnpj, endereco, telefone, email)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        self.empresa_nome.get(),
                        self.empresa_cnpj.get(),
                        self.empresa_endereco.get(),
                        self.empresa_telefone.get(),
                        self.empresa_email.get()
                    ))
                    self.registro_atual['empresa'] = cursor.lastrowid
                else:
                    # Atualizar existente
                    cursor.execute('''
                        UPDATE empresas SET nome=?, cnpj=?, endereco=?, telefone=?, email=?
                        WHERE id=?
                    ''', (
                        self.empresa_nome.get(),
                        self.empresa_cnpj.get(),
                        self.empresa_endereco.get(),
                        self.empresa_telefone.get(),
                        self.empresa_email.get(),
                        self.registro_atual['empresa']
                    ))
            
            elif tipo == 'setor':
                if self.registro_atual['empresa'] == 0:
                    messagebox.showwarning("Aviso", "Selecione uma empresa primeiro!")
                    return
                
                if self.registro_atual['setor'] == 0:
                    cursor.execute('''
                        INSERT INTO setores (nome, descricao, empresa_id)
                        VALUES (?, ?, ?)
                    ''', (
                        self.setor_nome.get(),
                        self.setor_descricao.get(),
                        self.registro_atual['empresa']
                    ))
                    self.registro_atual['setor'] = cursor.lastrowid
                else:
                    cursor.execute('''
                        UPDATE setores SET nome=?, descricao=?, empresa_id=?
                        WHERE id=?
                    ''', (
                        self.setor_nome.get(),
                        self.setor_descricao.get(),
                        self.registro_atual['empresa'],
                        self.registro_atual['setor']
                    ))
            
            elif tipo == 'cargo':
                if self.registro_atual['setor'] == 0:
                    messagebox.showwarning("Aviso", "Selecione um setor primeiro!")
                    return
                
                if self.registro_atual['cargo'] == 0:
                    cursor.execute('''
                        INSERT INTO cargos (nome, descricao, cbo, setor_id)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        self.cargo_nome.get(),
                        self.cargo_descricao.get(),
                        self.cargo_cbo.get(),
                        self.registro_atual['setor']
                    ))
                    self.registro_atual['cargo'] = cursor.lastrowid
                else:
                    cursor.execute('''
                        UPDATE cargos SET nome=?, descricao=?, cbo=?, setor_id=?
                        WHERE id=?
                    ''', (
                        self.cargo_nome.get(),
                        self.cargo_descricao.get(),
                        self.cargo_cbo.get(),
                        self.registro_atual['setor'],
                        self.registro_atual['cargo']
                    ))
            
            elif tipo == 'atividade':
                if self.registro_atual['cargo'] == 0:
                    messagebox.showwarning("Aviso", "Selecione um cargo primeiro!")
                    return
                
                if self.registro_atual['atividade'] == 0:
                    cursor.execute('''
                        INSERT INTO atividades (descricao, risco, frequencia, duracao, cargo_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        self.atividade_descricao.get(),
                        self.atividade_risco.get(),
                        self.atividade_frequencia.get(),
                        self.atividade_duracao.get(),
                        self.registro_atual['cargo']
                    ))
                    self.registro_atual['atividade'] = cursor.lastrowid
                else:
                    cursor.execute('''
                        UPDATE atividades SET descricao=?, risco=?, frequencia=?, duracao=?, cargo_id=?
                        WHERE id=?
                    ''', (
                        self.atividade_descricao.get(),
                        self.atividade_risco.get(),
                        self.atividade_frequencia.get(),
                        self.atividade_duracao.get(),
                        self.registro_atual['cargo'],
                        self.registro_atual['atividade']
                    ))
            
            elif tipo == 'ambiente':
                if self.registro_atual['cargo'] == 0:
                    messagebox.showwarning("Aviso", "Selecione um cargo primeiro!")
                    return
                
                area = float(self.ambiente_area.get()) if self.ambiente_area.get() else 0
                ruido = float(self.ambiente_ruido.get()) if self.ambiente_ruido.get() else 0
                temp = float(self.ambiente_temperatura.get()) if self.ambiente_temperatura.get() else 0
                umidade = float(self.ambiente_umidade.get()) if self.ambiente_umidade.get() else 0
                
                if self.registro_atual['ambiente'] == 0:
                    cursor.execute('''
                        INSERT INTO ambientes (nome, tipo, area, ventilacao, iluminacao, ruido, temperatura, umidade, cargo_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        self.ambiente_nome.get(),
                        self.ambiente_tipo.get(),
                        area,
                        self.ambiente_ventilacao.get(),
                        self.ambiente_iluminacao.get(),
                        ruido,
                        temp,
                        umidade,
                        self.registro_atual['cargo']
                    ))
                    self.registro_atual['ambiente'] = cursor.lastrowid
                else:
                    cursor.execute('''
                        UPDATE ambientes SET nome=?, tipo=?, area=?, ventilacao=?, iluminacao=?, ruido=?, temperatura=?, umidade=?, cargo_id=?
                        WHERE id=?
                    ''', (
                        self.ambiente_nome.get(),
                        self.ambiente_tipo.get(),
                        area,
                        self.ambiente_ventilacao.get(),
                        self.ambiente_iluminacao.get(),
                        ruido,
                        temp,
                        umidade,
                        self.registro_atual['cargo'],
                        self.registro_atual['ambiente']
                    ))
            
            self.conn.commit()
            messagebox.showinfo("Sucesso", f"Registro de {tipo} salvo com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar {tipo}: {str(e)}")
    
    def editar_registro(self, tipo):
        """Habilitar edição do registro atual"""
        messagebox.showinfo("Editar", f"Modo de edição ativado para {tipo}. Modifique os campos e clique em Salvar.")
    
    def excluir_registro(self, tipo):
        """Excluir registro atual"""
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir este {tipo}?"):
            cursor = self.conn.cursor()
            tabelas = {'empresa': 'empresas', 'setor': 'setores', 'cargo': 'cargos', 'atividade': 'atividades', 'ambiente': 'ambientes'}
            
            try:
                cursor.execute(f"DELETE FROM {tabelas[tipo]} WHERE id = ?", (self.registro_atual[tipo],))
                self.conn.commit()
                messagebox.showinfo("Sucesso", f"{tipo.capitalize()} excluído com sucesso!")
                
                # Limpar campos e navegar para próximo registro
                self.novo_registro(tipo)
                self.navegar(tipo, 'primeiro')
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir {tipo}: {str(e)}")
    
    def listar_registros(self, tipo):
        """Abrir janela de listagem de registros"""
        try:
            janela_lista = tk.Toplevel(self.root)
            janela_lista.title(f"Lista de {tipo.capitalize()}s")
            janela_lista.geometry("900x500")
            
            # Frame principal
            main_frame = ttk.Frame(janela_lista)
            main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Título
            ttk.Label(main_frame, text=f"Lista de {tipo.capitalize()}s", 
                     font=('Arial', 12, 'bold')).pack(pady=(0, 10))
            
            # Frame para Treeview e scrollbar
            tree_frame = ttk.Frame(main_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True)
            
            # Criar Treeview
            colunas = self.obter_colunas_tabela(tipo)
            tree = ttk.Treeview(tree_frame, columns=colunas, show='tree headings', height=15)
            
            # Scrollbars
            v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # Configurar colunas
            tree.column('#0', width=50, anchor='center')
            tree.heading('#0', text='ID')
            
            for i, col in enumerate(colunas):
                width = 150 if i < 2 else 100  # Primeiras colunas maiores
                tree.column(col, width=width, anchor='w')
                tree.heading(col, text=col.replace('_', ' ').title())
            
            # Posicionar elementos
            tree.grid(row=0, column=0, sticky='nsew')
            v_scrollbar.grid(row=0, column=1, sticky='ns')
            h_scrollbar.grid(row=1, column=0, sticky='ew')
            
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            # Carregar dados
            cursor = self.conn.cursor()
            tabelas = {'empresa': 'empresas', 'setor': 'setores', 'cargo': 'cargos', 
                      'atividade': 'atividades', 'ambiente': 'ambientes'}
            
            tabela = tabelas.get(tipo)
            if not tabela:
                messagebox.showerror("Erro", f"Tipo de registro '{tipo}' não reconhecido")
                janela_lista.destroy()
                return
            
            cursor.execute(f"SELECT * FROM {tabela} ORDER BY id")
            registros = cursor.fetchall()
            
            if not registros:
                ttk.Label(main_frame, text="Nenhum registro encontrado.", 
                         font=('Arial', 10)).pack(pady=20)
            else:
                for registro in registros:
                    # Limitar o tamanho dos valores exibidos
                    valores_limitados = []
                    for val in registro[1:]:  # Pular o ID
                        if val is None:
                            valores_limitados.append("")
                        elif len(str(val)) > 50:
                            valores_limitados.append(str(val)[:47] + "...")
                        else:
                            valores_limitados.append(str(val))
                    
                    tree.insert('', 'end', text=registro[0], values=valores_limitados)
            
            # Frame para botões
            btn_frame = ttk.Frame(main_frame)
            btn_frame.pack(fill=tk.X, pady=10)
            
            # Função para selecionar registro
            def selecionar():
                selection = tree.selection()
                if not selection:
                    messagebox.showwarning("Aviso", "Selecione um registro primeiro!")
                    return
                
                item = selection[0]
                registro_id = int(tree.item(item, 'text'))
                self.registro_atual[tipo] = registro_id
                self.carregar_registro(tipo)
                messagebox.showinfo("Sucesso", f"Registro {registro_id} carregado!")
                janela_lista.destroy()
            
            # Função para atualizar lista
            def atualizar():
                # Limpar árvore
                for item in tree.get_children():
                    tree.delete(item)
                
                # Recarregar dados
                cursor.execute(f"SELECT * FROM {tabela} ORDER BY id")
                registros = cursor.fetchall()
                
                for registro in registros:
                    valores_limitados = []
                    for val in registro[1:]:
                        if val is None:
                            valores_limitados.append("")
                        elif len(str(val)) > 50:
                            valores_limitados.append(str(val)[:47] + "...")
                        else:
                            valores_limitados.append(str(val))
                    
                    tree.insert('', 'end', text=registro[0], values=valores_limitados)
                
                messagebox.showinfo("Info", "Lista atualizada!")
            
            # Botões
            ttk.Button(btn_frame, text="Selecionar", command=selecionar).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Atualizar Lista", command=atualizar).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Fechar", command=janela_lista.destroy).pack(side=tk.RIGHT, padx=5)
            
            # Duplo clique para selecionar
            tree.bind('<Double-1>', lambda e: selecionar())
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao listar registros: {str(e)}")
    
    def obter_colunas_tabela(self, tipo):
        """Obter nomes das colunas da tabela"""
        colunas_map = {
            'empresa': ['nome', 'cnpj', 'endereco', 'telefone', 'email'],
            'setor': ['nome', 'descricao'],
            'cargo': ['nome', 'descricao', 'cbo'],
            'atividade': ['descricao', 'risco', 'frequencia', 'duracao'],
            'ambiente': ['nome', 'tipo', 'area', 'ventilacao', 'iluminacao', 'ruido', 'temperatura', 'umidade']
        }
        return colunas_map.get(tipo, [])
    
    # === MÉTODOS DE LIMPEZA ===
    def limpar_campos_empresa(self):
        """Limpar campos da empresa"""
        self.empresa_nome.delete(0, tk.END)
        self.empresa_cnpj.delete(0, tk.END)
        self.empresa_endereco.delete(0, tk.END)
        self.empresa_telefone.delete(0, tk.END)
        self.empresa_email.delete(0, tk.END)
    
    def limpar_campos_setor(self):
        """Limpar campos do setor"""
        self.setor_nome.delete(0, tk.END)
        self.setor_descricao.delete(0, tk.END)
    
    def limpar_campos_cargo(self):
        """Limpar campos do cargo"""
        self.cargo_nome.delete(0, tk.END)
        self.cargo_descricao.delete(0, tk.END)
        self.cargo_cbo.delete(0, tk.END)
    
    def limpar_campos_atividade(self):
        """Limpar campos da atividade"""
        self.atividade_descricao.delete(0, tk.END)
        self.atividade_risco.set('')
        self.atividade_frequencia.delete(0, tk.END)
        self.atividade_duracao.delete(0, tk.END)
    
    def limpar_campos_ambiente(self):
        """Limpar campos do ambiente"""
        self.ambiente_nome.delete(0, tk.END)
        self.ambiente_tipo.set('')
        self.ambiente_area.delete(0, tk.END)
        self.ambiente_ventilacao.set('')
        self.ambiente_iluminacao.set('')
        self.ambiente_ruido.delete(0, tk.END)
        self.ambiente_temperatura.delete(0, tk.END)
        self.ambiente_umidade.delete(0, tk.END)
    
    def limpar_tudo(self):
        """Limpar todos os campos"""
        self.limpar_campos_empresa()
        self.limpar_campos_setor()
        self.limpar_campos_cargo()
        self.limpar_campos_atividade()
        self.limpar_campos_ambiente()
        
        # Resetar IDs
        for key in self.registro_atual:
            self.registro_atual[key] = 0
    
    def salvar_tudo(self):
        """Salvar todos os registros"""
        try:
            if self.empresa_nome.get():
                self.salvar_registro('empresa')
            if self.setor_nome.get():
                self.salvar_registro('setor')
            if self.cargo_nome.get():
                self.salvar_registro('cargo')
            if self.atividade_descricao.get():
                self.salvar_registro('atividade')
            if self.ambiente_nome.get():
                self.salvar_registro('ambiente')
            
            messagebox.showinfo("Sucesso", "Todos os registros foram salvos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
    
    def criar_dados_exemplo(self):
        """Criar dados de exemplo conforme solicitado"""
        if messagebox.askyesno("Confirmar", "Isso criará dados de exemplo no sistema. Continuar?"):
            cursor = self.conn.cursor()
            
            try:
                # Dados das empresas
                empresas_dados = [
                    ("TechCorp Indústria Ltda", "12.345.678/0001-90", "Av. Industrial, 1000 - São Paulo/SP", "(11) 3333-4444", "contato@techcorp.com.br"),
                    ("MegaServ Comércio S.A.", "98.765.432/0001-11", "Rua Comercial, 500 - Rio de Janeiro/RJ", "(21) 2222-5555", "info@megaserv.com.br"),
                    ("EcoSolutions Ltda", "11.222.333/0001-44", "Av. Sustentável, 200 - Curitiba/PR", "(41) 9999-7777", "eco@solutions.com.br")
                ]
                
                # Inserir empresas
                empresa_ids = []
                for empresa in empresas_dados:
                    cursor.execute('''
                        INSERT INTO empresas (nome, cnpj, endereco, telefone, email)
                        VALUES (?, ?, ?, ?, ?)
                    ''', empresa)
                    empresa_ids.append(cursor.lastrowid)
                
                # Dados dos setores para cada empresa
                setores_dados = [
                    # TechCorp
                    [
                        ("Produção", "Setor responsável pela fabricação de produtos tecnológicos"),
                        ("Administrativo", "Setor de gestão e administração da empresa"),
                        ("Qualidade", "Setor de controle e garantia da qualidade")
                    ],
                    # MegaServ
                    [
                        ("Vendas", "Setor comercial e atendimento ao cliente"),
                        ("Logística", "Setor de armazenagem e distribuição"),
                        ("Recursos Humanos", "Setor de gestão de pessoas")
                    ],
                    # EcoSolutions
                    [
                        ("Pesquisa & Desenvolvimento", "Setor de inovação em soluções sustentáveis"),
                        ("Operações", "Setor operacional de projetos ambientais"),
                        ("Consultoria", "Setor de consultoria ambiental")
                    ]
                ]
                
                # Inserir setores
                setor_ids = []
                for i, empresa_id in enumerate(empresa_ids):
                    empresa_setores = []
                    for setor in setores_dados[i]:
                        cursor.execute('''
                            INSERT INTO setores (nome, descricao, empresa_id)
                            VALUES (?, ?, ?)
                        ''', (setor[0], setor[1], empresa_id))
                        empresa_setores.append(cursor.lastrowid)
                    setor_ids.append(empresa_setores)
                
                # Dados dos cargos
                cargos_dados = [
                    # Produção, Administrativo, Qualidade (TechCorp)
                    [
                        [
                            ("Operador de Máquina", "Opera equipamentos de produção", "7233-10"),
                            ("Técnico em Eletrônica", "Manutenção de equipamentos eletrônicos", "3133-05"),
                            ("Supervisor de Produção", "Supervisiona equipe de produção", "1412-06")
                        ],
                        [
                            ("Assistente Administrativo", "Atividades administrativas gerais", "4110-10"),
                            ("Analista Financeiro", "Análise e controle financeiro", "2522-10"),
                            ("Gerente Administrativo", "Gestão do setor administrativo", "1421-05")
                        ],
                        [
                            ("Inspetor de Qualidade", "Inspeção de produtos e processos", "3941-05"),
                            ("Técnico em Metrologia", "Calibração e medição", "3135-05"),
                            ("Coordenador da Qualidade", "Coordenação do sistema de qualidade", "1412-99")
                        ]
                    ],
                    # Vendas, Logística, RH (MegaServ)
                    [
                        [
                            ("Vendedor", "Vendas diretas ao consumidor", "3542-10"),
                            ("Promotor de Vendas", "Promoção de produtos", "3542-20"),
                            ("Gerente de Vendas", "Gestão da equipe comercial", "1414-20")
                        ],
                        [
                            ("Auxiliar de Estoque", "Organização e controle de estoque", "4141-05"),
                            ("Operador de Empilhadeira", "Movimentação de materiais", "7826-10"),
                            ("Coordenador Logístico", "Coordenação de atividades logísticas", "1414-15")
                        ],
                        [
                            ("Auxiliar de RH", "Apoio nas atividades de recursos humanos", "4110-05"),
                            ("Analista de RH", "Gestão de pessoas e processos", "2521-05"),
                            ("Gerente de RH", "Gestão estratégica de recursos humanos", "1421-10")
                        ]
                    ],
                    # P&D, Operações, Consultoria (EcoSolutions)
                    [
                        [
                            ("Pesquisador", "Pesquisa em soluções sustentáveis", "2030-15"),
                            ("Técnico em Meio Ambiente", "Apoio técnico ambiental", "3516-05"),
                            ("Coordenador de P&D", "Coordenação de projetos de pesquisa", "1238-05")
                        ],
                        [
                            ("Técnico Ambiental", "Execução de projetos ambientais", "3516-10"),
                            ("Operador de ETE", "Operação de estação de tratamento", "9214-25"),
                            ("Supervisor Operacional", "Supervisão de operações", "1412-12")
                        ],
                        [
                            ("Consultor Júnior", "Consultoria ambiental básica", "2030-25"),
                            ("Consultor Sênior", "Consultoria ambiental especializada", "2030-20"),
                            ("Gerente de Consultoria", "Gestão de projetos de consultoria", "1421-25")
                        ]
                    ]
                ]
                
                # Inserir cargos
                cargo_ids = []
                for i, empresa_setores in enumerate(setor_ids):
                    empresa_cargos = []
                    for j, setor_id in enumerate(empresa_setores):
                        setor_cargos = []
                        for cargo in cargos_dados[i][j]:
                            cursor.execute('''
                                INSERT INTO cargos (nome, descricao, cbo, setor_id)
                                VALUES (?, ?, ?, ?)
                            ''', (cargo[0], cargo[1], cargo[2], setor_id))
                            setor_cargos.append(cursor.lastrowid)
                        empresa_cargos.append(setor_cargos)
                    cargo_ids.append(empresa_cargos)
                
                # Dados das atividades
                atividades_dados = {
                    # TechCorp - Produção
                    "Operador de Máquina": [
                        ("Operação de torno CNC", "Médio", "8 horas/dia", "Diário"),
                        ("Inspeção dimensional de peças", "Baixo", "2 horas/dia", "Diário"),
                        ("Limpeza e lubrificação de máquinas", "Baixo", "1 hora/dia", "Diário")
                    ],
                    "Técnico em Eletrônica": [
                        ("Manutenção preventiva de equipamentos", "Médio", "4 horas/dia", "Semanal"),
                        ("Diagnóstico de falhas eletrônicas", "Alto", "6 horas/dia", "Conforme demanda"),
                        ("Calibração de instrumentos", "Médio", "3 horas/dia", "Mensal")
                    ],
                    "Supervisor de Produção": [
                        ("Supervisão da equipe de produção", "Baixo", "8 horas/dia", "Diário"),
                        ("Análise de indicadores de produção", "Baixo", "2 horas/dia", "Diário"),
                        ("Reuniões de planejamento", "Baixo", "1 hora/dia", "Diário")
                    ],
                    # TechCorp - Administrativo
                    "Assistente Administrativo": [
                        ("Atendimento telefônico", "Baixo", "4 horas/dia", "Diário"),
                        ("Organização de arquivos", "Baixo", "2 horas/dia", "Diário"),
                        ("Digitação de documentos", "Baixo", "3 horas/dia", "Diário")
                    ],
                    "Analista Financeiro": [
                        ("Análise de fluxo de caixa", "Baixo", "4 horas/dia", "Diário"),
                        ("Elaboração de relatórios financeiros", "Baixo", "3 horas/dia", "Semanal"),
                        ("Conciliação bancária", "Baixo", "2 horas/dia", "Diário")
                    ],
                    "Gerente Administrativo": [
                        ("Gestão de equipes", "Baixo", "6 horas/dia", "Diário"),
                        ("Reuniões estratégicas", "Baixo", "2 horas/dia", "Semanal"),
                        ("Análise de custos operacionais", "Baixo", "2 horas/dia", "Mensal")
                    ],
                    # Adicionar mais atividades para os outros cargos...
                    "Default": [
                        ("Atividade padrão 1", "Baixo", "2 horas", "Diário"),
                        ("Atividade padrão 2", "Médio", "4 horas", "Semanal"),
                        ("Atividade padrão 3", "Baixo", "1 hora", "Mensal")
                    ]
                }
                
                # Inserir atividades para todos os cargos
                for i, empresa_cargos in enumerate(cargo_ids):
                    for j, setor_cargos in enumerate(empresa_cargos):
                        for k, cargo_id in enumerate(setor_cargos):
                            # Buscar nome do cargo
                            cursor.execute("SELECT nome FROM cargos WHERE id = ?", (cargo_id,))
                            cargo_nome = cursor.fetchone()[0]
                            
                            # Usar atividades específicas se existirem, senão usar padrão
                            atividades = atividades_dados.get(cargo_nome, atividades_dados["Default"])
                            
                            for atividade in atividades:
                                cursor.execute('''
                                    INSERT INTO atividades (descricao, risco, frequencia, duracao, cargo_id)
                                    VALUES (?, ?, ?, ?, ?)
                                ''', (atividade[0], atividade[1], atividade[2], atividade[3], cargo_id))
                
                # Dados dos ambientes
                ambientes_dados = {
                    "Operador de Máquina": [
                        ("Área de Usinagem", "Produção", 120.5, "Artificial", "Artificial", 85.2, 28.5, 65.0),
                        ("Área de Soldagem", "Produção", 80.0, "Natural", "Artificial", 78.5, 35.0, 55.0),
                        ("Estoque de Matéria Prima", "Armazém", 200.0, "Natural", "Natural", 65.0, 25.0, 70.0)
                    ],
                    "Técnico em Eletrônica": [
                        ("Oficina Eletrônica", "Oficina", 45.0, "Artificial", "Artificial", 68.5, 24.0, 60.0),
                        ("Laboratório de Testes", "Laboratório", 30.0, "Artificial", "Artificial", 55.0, 22.0, 55.0),
                        ("Bancada de Calibração", "Laboratório", 15.0, "Artificial", "Artificial", 50.0, 23.0, 50.0)
                    ],
                    "Default": [
                        ("Ambiente Padrão 1", "Administrativo", 25.0, "Artificial", "Artificial", 55.0, 24.0, 60.0),
                        ("Ambiente Padrão 2", "Administrativo", 30.0, "Natural", "Artificial", 50.0, 25.0, 65.0),
                        ("Ambiente Padrão 3", "Administrativo", 35.0, "Mista", "Mista", 45.0, 26.0, 55.0)
                    ]
                }
                
                # Inserir ambientes para todos os cargos
                for i, empresa_cargos in enumerate(cargo_ids):
                    for j, setor_cargos in enumerate(empresa_cargos):
                        for k, cargo_id in enumerate(setor_cargos):
                            # Buscar nome do cargo
                            cursor.execute("SELECT nome FROM cargos WHERE id = ?", (cargo_id,))
                            cargo_nome = cursor.fetchone()[0]
                            
                            # Usar ambientes específicos se existirem, senão usar padrão
                            ambientes = ambientes_dados.get(cargo_nome, ambientes_dados["Default"])
                            
                            for ambiente in ambientes:
                                cursor.execute('''
                                    INSERT INTO ambientes (nome, tipo, area, ventilacao, iluminacao, ruido, temperatura, umidade, cargo_id)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (*ambiente, cargo_id))
                
                self.conn.commit()
                messagebox.showinfo("Sucesso", 
                    "Dados de exemplo criados com sucesso!\n\n" +
                    "• 3 empresas\n" +
                    "• 9 setores (3 por empresa)\n" +
                    "• 27 cargos (3 por setor)\n" +
                    "• 81 atividades (3 por cargo)\n" +
                    "• 81 ambientes (3 por cargo)")
                
                # Carregar primeiro registro para visualização
                self.carregar_primeiro_registro()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar dados de exemplo: {str(e)}")
                self.conn.rollback()
    
    # === MÉTODOS DE RELATÓRIOS ===
    def gerar_relatorio_geral(self):
        """Gerar relatório geral do sistema"""
        cursor = self.conn.cursor()
        
        relatorio = "RELATÓRIO GERAL - SISTEMA PPRA/LTCAT\n"
        relatorio += "=" * 50 + "\n\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        # Estatísticas
        cursor.execute("SELECT COUNT(*) FROM empresas")
        total_empresas = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM setores")
        total_setores = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM cargos")
        total_cargos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM atividades")
        total_atividades = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM ambientes")
        total_ambientes = cursor.fetchone()[0]
        
        relatorio += "ESTATÍSTICAS:\n"
        relatorio += f"Total de Empresas: {total_empresas}\n"
        relatorio += f"Total de Setores: {total_setores}\n"
        relatorio += f"Total de Cargos: {total_cargos}\n"
        relatorio += f"Total de Atividades: {total_atividades}\n"
        relatorio += f"Total de Ambientes: {total_ambientes}\n\n"
        
        # Listar empresas
        cursor.execute("SELECT nome, cnpj FROM empresas ORDER BY nome")
        empresas = cursor.fetchall()
        
        relatorio += "EMPRESAS CADASTRADAS:\n"
        relatorio += "-" * 30 + "\n"
        for empresa in empresas:
            relatorio += f"• {empresa[0]} - CNPJ: {empresa[1] or 'Não informado'}\n"
        
        self.texto_relatorio.delete(1.0, tk.END)
        self.texto_relatorio.insert(1.0, relatorio)
    
    def gerar_relatorio_empresa(self):
        """Gerar relatório por empresa"""
        if self.registro_atual['empresa'] == 0:
            messagebox.showwarning("Aviso", "Selecione uma empresa primeiro!")
            return
        
        cursor = self.conn.cursor()
        
        # Dados da empresa
        cursor.execute("SELECT * FROM empresas WHERE id = ?", (self.registro_atual['empresa'],))
        empresa = cursor.fetchone()
        
        if not empresa:
            messagebox.showerror("Erro", "Empresa não encontrada!")
            return
        
        relatorio = "RELATÓRIO POR EMPRESA - SISTEMA PPRA/LTCAT\n"
        relatorio += "=" * 50 + "\n\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        relatorio += f"EMPRESA: {empresa[1]}\n"
        relatorio += f"CNPJ: {empresa[2] or 'Não informado'}\n"
        relatorio += f"Endereço: {empresa[3] or 'Não informado'}\n"
        relatorio += f"Telefone: {empresa[4] or 'Não informado'}\n"
        relatorio += f"Email: {empresa[5] or 'Não informado'}\n\n"
        
        # Setores da empresa
        cursor.execute("SELECT * FROM setores WHERE empresa_id = ?", (self.registro_atual['empresa'],))
        setores = cursor.fetchall()
        
        relatorio += "SETORES:\n"
        relatorio += "-" * 20 + "\n"
        
        for setor in setores:
            relatorio += f"\n• {setor[1]}\n"
            relatorio += f"  Descrição: {setor[2] or 'Não informado'}\n"
            
            # Cargos do setor
            cursor.execute("SELECT * FROM cargos WHERE setor_id = ?", (setor[0],))
            cargos = cursor.fetchall()
            
            for cargo in cargos:
                relatorio += f"  \n  CARGO: {cargo[1]}\n"
                relatorio += f"  CBO: {cargo[3] or 'Não informado'}\n"
                relatorio += f"  Descrição: {cargo[2] or 'Não informado'}\n"
                
                # Atividades do cargo
                cursor.execute("SELECT * FROM atividades WHERE cargo_id = ?", (cargo[0],))
                atividades = cursor.fetchall()
                
                if atividades:
                    relatorio += "    ATIVIDADES:\n"
                    for atividade in atividades:
                        relatorio += f"    - {atividade[1]}\n"
                        relatorio += f"      Risco: {atividade[2] or 'Não informado'}\n"
                        relatorio += f"      Frequência: {atividade[3] or 'Não informado'}\n"
                        relatorio += f"      Duração: {atividade[4] or 'Não informado'}\n"
                
                # Ambientes do cargo
                cursor.execute("SELECT * FROM ambientes WHERE cargo_id = ?", (cargo[0],))
                ambientes = cursor.fetchall()
                
                if ambientes:
                    relatorio += "    AMBIENTES:\n"
                    for ambiente in ambientes:
                        relatorio += f"    - {ambiente[1]}\n"
                        relatorio += f"      Tipo: {ambiente[2] or 'Não informado'}\n"
                        relatorio += f"      Área: {ambiente[3] or 'Não informado'} m²\n"
                        relatorio += f"      Ventilação: {ambiente[4] or 'Não informado'}\n"
                        relatorio += f"      Iluminação: {ambiente[5] or 'Não informado'}\n"
                        relatorio += f"      Ruído: {ambiente[6] or 'Não informado'} dB\n"
                        relatorio += f"      Temperatura: {ambiente[7] or 'Não informado'}°C\n"
                        relatorio += f"      Umidade: {ambiente[8] or 'Não informado'}%\n"
        
        self.texto_relatorio.delete(1.0, tk.END)
        self.texto_relatorio.insert(1.0, relatorio)
    
    def gerar_relatorio_riscos(self):
        """Gerar relatório de riscos"""
        cursor = self.conn.cursor()
        
        relatorio = "RELATÓRIO DE RISCOS - SISTEMA PPRA/LTCAT\n"
        relatorio += "=" * 50 + "\n\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        # Atividades por nível de risco
        niveis_risco = ['Crítico', 'Alto', 'Médio', 'Baixo']
        
        for nivel in niveis_risco:
            cursor.execute("""
                SELECT a.descricao, a.frequencia, a.duracao, c.nome, s.nome, e.nome
                FROM atividades a
                JOIN cargos c ON a.cargo_id = c.id
                JOIN setores s ON c.setor_id = s.id
                JOIN empresas e ON s.empresa_id = e.id
                WHERE a.risco = ?
                ORDER BY e.nome, s.nome, c.nome
            """, (nivel,))
            
            atividades = cursor.fetchall()
            
            if atividades:
                relatorio += f"RISCOS {nivel.upper()}:\n"
                relatorio += "-" * 30 + "\n"
                
                for atividade in atividades:
                    relatorio += f"• Atividade: {atividade[0]}\n"
                    relatorio += f"  Cargo: {atividade[3]}\n"
                    relatorio += f"  Setor: {atividade[4]}\n"
                    relatorio += f"  Empresa: {atividade[5]}\n"
                    relatorio += f"  Frequência: {atividade[1] or 'Não informado'}\n"
                    relatorio += f"  Duração: {atividade[2] or 'Não informado'}\n\n"
        
        self.texto_relatorio.delete(1.0, tk.END)
        self.texto_relatorio.insert(1.0, relatorio)
    
    def gerar_ltcat(self):
        """Gerar Laudo Técnico das Condições Ambientais do Trabalho"""
        cursor = self.conn.cursor()
        
        relatorio = "LAUDO TÉCNICO DAS CONDIÇÕES AMBIENTAIS DO TRABALHO - LTCAT\n"
        relatorio += "=" * 60 + "\n\n"
        relatorio += f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        relatorio += "1. IDENTIFICAÇÃO DA EMPRESA\n"
        relatorio += "-" * 30 + "\n"
        
        if self.registro_atual['empresa'] != 0:
            cursor.execute("SELECT * FROM empresas WHERE id = ?", (self.registro_atual['empresa'],))
            empresa = cursor.fetchone()
            
            if empresa:
                relatorio += f"Razão Social: {empresa[1]}\n"
                relatorio += f"CNPJ: {empresa[2] or 'Não informado'}\n"
                relatorio += f"Endereço: {empresa[3] or 'Não informado'}\n"
                relatorio += f"Telefone: {empresa[4] or 'Não informado'}\n"
                relatorio += f"Email: {empresa[5] or 'Não informado'}\n\n"
        
        relatorio += "2. METODOLOGIA\n"
        relatorio += "-" * 15 + "\n"
        relatorio += "Este laudo foi elaborado com base em:\n"
        relatorio += "• Inspeção visual dos ambientes de trabalho\n"
        relatorio += "• Análise das atividades desenvolvidas\n"
        relatorio += "• Medições ambientais quando aplicável\n"
        relatorio += "• Normas regulamentadoras aplicáveis\n\n"
        
        relatorio += "3. ANÁLISE DOS AMBIENTES E ATIVIDADES\n"
        relatorio += "-" * 40 + "\n"
        
        # Buscar todos os ambientes e atividades
        cursor.execute("""
            SELECT DISTINCT 
                e.nome as empresa,
                s.nome as setor,
                c.nome as cargo,
                c.cbo,
                amb.nome as ambiente,
                amb.tipo,
                amb.area,
                amb.ventilacao,
                amb.iluminacao,
                amb.ruido,
                amb.temperatura,
                amb.umidade
            FROM empresas e
            JOIN setores s ON e.id = s.empresa_id
            JOIN cargos c ON s.id = c.setor_id
            JOIN ambientes amb ON c.id = amb.cargo_id
            ORDER BY e.nome, s.nome, c.nome
        """)
        
        ambientes = cursor.fetchall()
        
        for ambiente in ambientes:
            relatorio += f"\nCARGO: {ambiente[2]} (CBO: {ambiente[3] or 'N/I'})\n"
            relatorio += f"Setor: {ambiente[1]}\n"
            relatorio += f"Empresa: {ambiente[0]}\n\n"
            
            relatorio += f"AMBIENTE: {ambiente[4]}\n"
            relatorio += f"Tipo: {ambiente[5] or 'Não especificado'}\n"
            relatorio += f"Área: {ambiente[6] or 'N/I'} m²\n"
            relatorio += f"Ventilação: {ambiente[7] or 'Não especificado'}\n"
            relatorio += f"Iluminação: {ambiente[8] or 'Não especificado'}\n"
            relatorio += f"Nível de Ruído: {ambiente[9] or 'N/M'} dB(A)\n"
            relatorio += f"Temperatura: {ambiente[10] or 'N/M'}°C\n"
            relatorio += f"Umidade Relativa: {ambiente[11] or 'N/M'}%\n"
            
            # Buscar atividades do cargo
            cursor.execute("""
                SELECT descricao, risco, frequencia, duracao
                FROM atividades
                WHERE cargo_id = (
                    SELECT c.id FROM cargos c
                    JOIN ambientes amb ON c.id = amb.cargo_id
                    WHERE amb.nome = ?
                )
            """, (ambiente[4],))
            
            atividades_cargo = cursor.fetchall()
            
            if atividades_cargo:
                relatorio += "\nATIVIDADES DESENVOLVIDAS:\n"
                for ativ in atividades_cargo:
                    relatorio += f"• {ativ[0]}\n"
                    relatorio += f"  Nível de Risco: {ativ[1] or 'Não avaliado'}\n"
                    relatorio += f"  Frequência: {ativ[2] or 'Não informado'}\n"
                    relatorio += f"  Duração: {ativ[3] or 'Não informado'}\n"
            
            relatorio += "\n" + "-" * 50 + "\n"
        
        relatorio += "\n4. CONCLUSÕES E RECOMENDAÇÕES\n"
        relatorio += "-" * 35 + "\n"
        relatorio += "Com base na análise realizada, recomenda-se:\n\n"
        relatorio += "• Implementação de medidas de controle coletivo quando necessário\n"
        relatorio += "• Fornecimento de Equipamentos de Proteção Individual (EPI)\n"
        relatorio += "• Treinamento periódico dos trabalhadores\n"
        relatorio += "• Monitoramento contínuo das condições ambientais\n"
        relatorio += "• Revisão periódica deste laudo\n\n"
        
        relatorio += "5. RESPONSÁVEL TÉCNICO\n"
        relatorio += "-" * 25 + "\n"
        relatorio += "Nome: _________________________\n"
        relatorio += "Registro: ______________________\n"
        relatorio += "Assinatura: ____________________\n"
        relatorio += f"Data: {datetime.now().strftime('%d/%m/%Y')}\n\n"
        
        relatorio += "Legenda: N/I = Não Informado, N/M = Não Medido\n"
        
        self.texto_relatorio.delete(1.0, tk.END)
        self.texto_relatorio.insert(1.0, relatorio)
    
    def __del__(self):
        """Fechar conexão com banco de dados"""
        if hasattr(self, 'conn'):
            self.conn.close()


# Função principal para executar o sistema
def main():
    root = tk.Tk()
    app = SistemaPPRA(root)
    root.mainloop()

# Executar o sistema
if __name__ == "__main__":
    main()