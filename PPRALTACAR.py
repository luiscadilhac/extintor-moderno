import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class PPRAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa Preventivo de Riscos Ambientais e LTCAT")
        self.root.geometry("1200x800")
        
        # Configurar fonte e cor padrão
        self.fonte_padrao = ("Verdana", 12)
        self.cor_fonte = "#ffd700"  # Cor dourada
        
        # Configurar estilo padrão
        self.style = ttk.Style()
        self.style.configure("TLabel", font=self.fonte_padrao, foreground=self.cor_fonte)
        self.style.configure("TButton", font=self.fonte_padrao)
        self.style.configure("TEntry", font=self.fonte_padrao)
        self.style.configure("TCombobox", font=self.fonte_padrao)
        self.style.configure("TFrame", background="#f0e68c")  # Cor de fundo amarela clara
        self.style.configure("TLabelframe", font=("Verdana", 12, "bold"), foreground=self.cor_fonte, background="#f0e68c")
        self.style.configure("TLabelframe.Label", font=("Verdana", 12, "bold"), foreground=self.cor_fonte, background="#f0e68c")
        self.style.configure("Treeview", font=self.fonte_padrao, foreground=self.cor_fonte, background="#f0e68c")
        self.style.configure("Treeview.Heading", font=("Verdana", 12, "bold"), foreground=self.cor_fonte, background="#f0e68c")
        self.style.configure("TNotebook", font=self.fonte_padrao, background="#f0e68c")
        self.style.configure("TNotebook.Tab", font=self.fonte_padrao, background="#f0e68c")
        
        # Conectar ao banco de dados
        self.conn = sqlite3.connect('ppra.db')
        self.cursor = self.conn.cursor()
        
        # Criar tabelas se não existirem
        self.create_tables()
        
        # Inserir dados iniciais
        self.insert_initial_data()
        
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
        
        # Criar interface com rolagem
        self.create_scrollable_interface()
        
        # Exibir primeiro registro
        self.show_empresa(0)
        
    def create_tables(self):
        # Tabela de Empresas
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            endereco TEXT NOT NULL
        )
        ''')
        
        # Tabela de Setores
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS setores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            id_empresa INTEGER,
            FOREIGN KEY (id_empresa) REFERENCES empresas(id)
        )
        ''')
        
        # Tabela de Cargos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS cargos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            id_setor INTEGER,
            FOREIGN KEY (id_setor) REFERENCES setores(id)
        )
        ''')
        
        # Tabela de Atividades
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            id_cargo INTEGER,
            FOREIGN KEY (id_cargo) REFERENCES cargos(id)
        )
        ''')
        
        # Tabela de Ambientes Laborativos
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS ambientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            id_cargo INTEGER,
            FOREIGN KEY (id_cargo) REFERENCES cargos(id)
        )
        ''')
        
        self.conn.commit()
    
    def insert_initial_data(self):
        # Verificar se já existem dados
        self.cursor.execute("SELECT COUNT(*) FROM empresas")
        if self.cursor.fetchone()[0] > 0:
            return
        
        # Inserir empresas
        empresas = [
            ("Indústria Alfa S.A.", "12.345.678/0001-00", "Rua das Indústrias, 100 - São Paulo/SP"),
            ("Construtora Beta Ltda.", "98.765.432/0001-11", "Av. das Construções, 200 - Rio de Janeiro/RJ"),
            ("Comércio Gama & Cia", "45.678.901/0001-22", "Rua do Comércio, 300 - Belo Horizonte/MG")
        ]
        
        for empresa in empresas:
            self.cursor.execute("INSERT INTO empresas (nome, cnpj, endereco) VALUES (?, ?, ?)", empresa)
        
        # Inserir setores
        setores = [
            # Setores da Indústria Alfa
            ("Produção", "Setor responsável pela fabricação dos produtos", 1),
            ("Manutenção", "Setor responsável pela manutenção dos equipamentos", 1),
            ("Administrativo", "Setor administrativo da empresa", 1),
            
            # Setores da Construtora Beta
            ("Engenharia", "Setor de projetos e planejamento", 2),
            ("Obras", "Setor de execução das obras", 2),
            ("Compras", "Setor de aquisição de materiais", 2),
            
            # Setores do Comércio Gama
            ("Vendas", "Setor de vendas e atendimento ao cliente", 3),
            ("Estoque", "Setor de controle de estoque", 3),
            ("Financeiro", "Setor financeiro e contábil", 3)
        ]
        
        for setor in setores:
            self.cursor.execute("INSERT INTO setores (nome, descricao, id_empresa) VALUES (?, ?, ?)", setor)
        
        # Inserir cargos
        cargos = [
            # Cargos do setor Produção (Indústria Alfa)
            ("Operador de Máquina", "Responsável pela operação das máquinas industriais", 1),
            ("Supervisor de Produção", "Supervisiona a equipe de produção", 1),
            ("Auxiliar de Produção", "Auxilia nas atividades de produção", 1),
            
            # Cargos do setor Manutenção (Indústria Alfa)
            ("Técnico de Manutenção", "Realiza manutenção preventiva e corretiva", 2),
            ("Engenheiro de Manutenção", "Planeja e coordena as atividades de manutenção", 2),
            ("Auxiliar de Manutenção", "Auxilia os técnicos nas atividades", 2),
            
            # Cargos do setor Administrativo (Indústria Alfa)
            ("Administrativo", "Realiza tarefas administrativas", 3),
            ("Secretário(a)", "Atendimento e organização de documentos", 3),
            ("Gerente Administrativo", "Gerencia o setor administrativo", 3),
            
            # Cargos do setor Engenharia (Construtora Beta)
            ("Engenheiro Civil", "Projetos e acompanhamento de obras", 4),
            ("Arquiteto", "Desenvolvimento de projetos arquitetônicos", 4),
            ("Desenhista", "Criação de desenhos técnicos", 4),
            
            # Cargos do setor Obras (Construtora Beta)
            ("Mestre de Obras", "Coordenação das equipes na obra", 5),
            ("Pedreiro", "Execução de serviços de alvenaria", 5),
            ("Servente", "Auxilia nas atividades da obra", 5),
            
            # Cargos do setor Compras (Construtora Beta)
            ("Comprador", "Aquisição de materiais e serviços", 6),
            ("Auxiliar de Compras", "Auxilia nas atividades de compras", 6),
            ("Gerente de Compras", "Gerencia o setor de compras", 6),
            
            # Cargos do setor Vendas (Comércio Gama)
            ("Vendedor", "Realização de vendas e atendimento", 7),
            ("Gerente de Vendas", "Gerencia a equipe de vendas", 7),
            ("Atendente", "Atendimento ao cliente", 7),
            
            # Cargos do setor Estoque (Comércio Gama)
            ("Auxiliar de Estoque", "Organização e controle do estoque", 8),
            ("Conferente", "Conferência de mercadorias", 8),
            ("Gerente de Estoque", "Gerencia o setor de estoque", 8),
            
            # Cargos do setor Financeiro (Comércio Gama)
            ("Contador", "Responsável pela contabilidade", 9),
            ("Auxiliar Financeiro", "Auxilia nas atividades financeiras", 9),
            ("Gerente Financeiro", "Gerencia o setor financeiro", 9)
        ]
        
        for cargo in cargos:
            self.cursor.execute("INSERT INTO cargos (nome, descricao, id_setor) VALUES (?, ?, ?)", cargo)
        
        # Inserir atividades
        atividades = [
            # Atividades do cargo Operador de Máquina
            ("Operar máquinas de produção", 1),
            ("Controlar qualidade dos produtos", 1),
            ("Realizar limpeza das máquinas", 1),
            
            # Atividades do cargo Técnico de Manutenção
            ("Realizar manutenção preventiva", 4),
            ("Diagnosticar falhas em equipamentos", 4),
            ("Executar reparos em máquinas", 4),
            
            # Atividades do cargo Engenheiro Civil
            ("Elaborar projetos estruturais", 10),
            ("Acompanhar execuções de obras", 10),
            ("Fiscalizar qualidade de materiais", 10),
            
            # Atividades do cargo Mestre de Obras
            ("Coordenar equipes de trabalho", 13),
            ("Controlar cronograma da obra", 13),
            ("Fiscalizar segurança no trabalho", 13),
            
            # Atividades do cargo Comprador
            ("Pesquisar fornecedores", 16),
            ("Negociar preços e prazos", 16),
            ("Emitir pedidos de compra", 16),
            
            # Atividades do cargo Vendedor
            ("Atender clientes", 19),
            ("Apresentar produtos", 19),
            ("Fechar vendas", 19),
            
            # Atividades do cargo Auxiliar de Estoque
            ("Organizar produtos no estoque", 22),
            ("Controlar entrada e saída de mercadorias", 22),
            ("Realizar inventário", 22),
            
            # Atividades do cargo Contador
            ("Lançar movimentações financeiras", 25),
            ("Preparar relatórios contábeis", 25),
            ("Assessorar nas decisões financeiras", 25),
            
            # Atividades do cargo Supervisor de Produção
            ("Supervisionar equipe de produção", 2),
            ("Controlar metas de produção", 2),
            ("Garantir qualidade dos produtos", 2),
            
            # Atividades do cargo Engenheiro de Manutenção
            ("Planejar manutenções", 5),
            ("Analisar falhas recorrentes", 5),
            ("Implementar melhorias", 5),
            
            # Atividades do cargo Arquiteto
            ("Desenvolver projetos arquitetônicos", 11),
            ("Acompanhar obras", 11),
            ("Selecionar materiais de construção", 11),
            
            # Atividades do cargo Pedreiro
            ("Executar alvenaria", 14),
            ("Assentar pisos e azulejos", 14),
            ("Realizar acabamentos", 14),
            
            # Atividades do cargo Auxiliar de Compras
            ("Auxiliar na pesquisa de fornecedores", 17),
            ("Organizar documentos de compra", 17),
            ("Acompanhar entregas", 17),
            
            # Atividades do cargo Gerente de Vendas
            ("Gerenciar equipe de vendas", 20),
            ("Definir metas de vendas", 20),
            ("Analisar resultados", 20),
            
            # Atividades do cargo Conferente
            ("Conferir mercadorias recebidas", 23),
            ("Verificar notas fiscais", 23),
            ("Registrar divergências", 23),
            
            # Atividades do cargo Auxiliar Financeiro
            ("Auxiliar no lançamento de dados", 26),
            ("Organizar documentos financeiros", 26),
            ("Preparar relatórios simples", 26),
            
            # Atividades do cargo Auxiliar de Produção
            ("Auxiliar na alimentação das máquinas", 3),
            ("Realizar embalagem de produtos", 3),
            ("Manter organização do setor", 3),
            
            # Atividades do cargo Auxiliar de Manutenção
            ("Auxiliar técnicos em manutenções", 6),
            ("Organizar ferramentas e equipamentos", 6),
            ("Realizar limpeza após manutenções", 6),
            
            # Atividades do cargo Desenhista
            ("Criar desenhos técnicos", 12),
            ("Auxiliar no desenvolvimento de projetos", 12),
            ("Revisar desenhos", 12),
            
            # Atividades do cargo Servente
            ("Auxiliar pedreiros e mestres", 15),
            ("Transportar materiais na obra", 15),
            ("Manter limpeza da obra", 15),
            
            # Atividades do cargo Gerente de Compras
            ("Gerenciar equipe de compras", 18),
            ("Definir estratégias de compras", 18),
            ("Aprovar grandes compras", 18),
            
            # Atividades do cargo Atendente
            ("Receber clientes", 21),
            ("Tirar dúvidas sobre produtos", 21),
            ("Direcionar clientes para vendedores", 21),
            
            # Atividades do cargo Gerente de Estoque
            ("Gerenciar equipe de estoque", 24),
            ("Controlar níveis de estoque", 24),
            ("Definir políticas de armazenamento", 24),
            
            # Atividades do cargo Gerente Financeiro
            ("Gerenciar equipe financeira", 27),
            ("Planejar orçamentos", 27),
            ("Analisar resultados financeiros", 27)
        ]
        
        for atividade in atividades:
            self.cursor.execute("INSERT INTO atividades (descricao, id_cargo) VALUES (?, ?)", atividade)
        
        # Inserir ambientes laborativos
        ambientes = [
            # Ambientes do cargo Operador de Máquina
            ("Área de produção com máquinas industriais", 1),
            ("Setor de embalagem", 1),
            ("Almoxarifado de insumos", 1),
            
            # Ambientes do cargo Técnico de Manutenção
            ("Oficina de manutenção", 4),
            ("Área industrial próxima às máquinas", 4),
            ("Almoxarifado de peças", 4),
            
            # Ambientes do cargo Engenheiro Civil
            ("Escritório de projetos", 10),
            ("Canteiro de obras", 10),
            ("Sala de reuniões", 10),
            
            # Ambientes do cargo Mestre de Obras
            ("Canteiro de obras", 13),
            ("Escritório de campo", 13),
            ("Área de convivência da obra", 13),
            
            # Ambientes do cargo Comprador
            ("Escritório de compras", 16),
            ("Salas de reunião com fornecedores", 16),
            ("Almoxarifado para inspeção de materiais", 16),
            
            # Ambientes do cargo Vendedor
            ("Salão de vendas", 19),
            ("Área de exposição de produtos", 19),
            ("Escritório para fechamento de vendas", 19),
            
            # Ambientes do cargo Auxiliar de Estoque
            ("Área de armazenamento de produtos", 22),
            ("Setor de expedição", 22),
            ("Escritório de controle de estoque", 22),
            
            # Ambientes do cargo Contador
            ("Escritório contábil", 25),
            ("Sala de arquivos", 25),
            ("Área de reuniões financeiras", 25),
            
            # Ambientes do cargo Supervisor de Produção
            ("Área de produção", 2),
            ("Escritório na produção", 2),
            ("Sala de reuniões da produção", 2),
            
            # Ambientes do cargo Engenheiro de Manutenção
            ("Escritório de engenharia", 5),
            ("Oficina de manutenção", 5),
            ("Área industrial", 5),
            
            # Ambientes do cargo Arquiteto
            ("Escritório de projetos", 11),
            ("Canteiro de obras", 11),
            ("Laboratório de materiais", 11),
            
            # Ambientes do cargo Pedreiro
            ("Área de construção", 14),
            ("Setor de preparação de materiais", 14),
            ("Área de descanso da obra", 14),
            
            # Ambientes do cargo Auxiliar de Compras
            ("Escritório de compras", 17),
            ("Arquivo de documentos", 17),
            ("Área de recebimento de materiais", 17),
            
            # Ambientes do cargo Gerente de Vendas
            ("Escritório de gerência", 20),
            ("Salão de vendas", 20),
            ("Sala de reuniões", 20),
            
            # Ambientes do cargo Conferente
            ("Área de recebimento de mercadorias", 23),
            ("Setor de inspeção", 23),
            ("Escritório de registro", 23),
            
            # Ambientes do cargo Auxiliar Financeiro
            ("Escritório financeiro", 26),
            ("Setor de arquivos", 26),
            ("Área de processamento de dados", 26),
            
            # Ambientes do cargo Auxiliar de Produção
            ("Área de produção", 3),
            ("Setor de embalagem", 3),
            ("Área de armazenamento temporário", 3),
            
            # Ambientes do cargo Auxiliar de Manutenção
            ("Oficina de manutenção", 6),
            ("Almoxarifado de peças", 6),
            ("Área industrial", 6),
            
            # Ambientes do cargo Desenhista
            ("Escritório de projetos", 12),
            ("Sala de desenho técnico", 12),
            ("Arquivo de projetos", 12),
            
            # Ambientes do cargo Servente
            ("Canteiro de obras", 15),
            ("Área de armazenamento de materiais", 15),
            ("Setor de apoio geral", 15),
            
            # Ambientes do cargo Gerente de Compras
            ("Escritório de gerência", 18),
            ("Sala de reuniões", 18),
            ("Escritório de compras", 18),
            
            # Ambientes do cargo Atendente
            ("Recepção da loja", 21),
            ("Salão de vendas", 21),
            ("Área de espera", 21),
            
            # Ambientes do cargo Gerente de Estoque
            ("Escritório de gerência", 24),
            ("Área de armazenamento", 24),
            ("Setor de expedição", 24),
            
            # Ambientes do cargo Gerente Financeiro
            ("Escritório de gerência", 27),
            ("Sala de reuniões diretoria", 27),
            ("Escritório financeiro", 27)
        ]
        
        for ambiente in ambientes:
            self.cursor.execute("INSERT INTO ambientes (descricao, id_cargo) VALUES (?, ?)", ambiente)
        
        self.conn.commit()
    
    def load_data(self):
        # Carregar empresas
        self.cursor.execute("SELECT * FROM empresas ORDER BY nome")
        self.empresas = self.cursor.fetchall()
        
        # Carregar setores
        self.cursor.execute("SELECT * FROM setores ORDER BY id_empresa, nome")
        self.setores = self.cursor.fetchall()
        
        # Carregar cargos
        self.cursor.execute("SELECT * FROM cargos ORDER BY id_setor, nome")
        self.cargos = self.cursor.fetchall()
        
        # Carregar atividades
        self.cursor.execute("SELECT * FROM atividades ORDER BY id_cargo")
        self.atividades = self.cursor.fetchall()
        
        # Carregar ambientes
        self.cursor.execute("SELECT * FROM ambientes ORDER BY id_cargo")
        self.ambientes = self.cursor.fetchall()
    
    def create_scrollable_interface(self):
        # Criar frame principal com rolagem
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar canvas
        self.canvas = tk.Canvas(self.main_frame, bg="#f0e68c")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Criar scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Criar frame dentro do canvas
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        
        # Criar notebook para abas
        self.notebook = ttk.Notebook(self.canvas_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Cadastros
        self.cadastro_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cadastro_frame, text="Cadastros")
        
        # Aba de Relatórios
        self.relatorio_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.relatorio_frame, text="Relatórios")
        
        # Nova aba PPRA/LTCAT
        self.ppra_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ppra_frame, text="PPRA/LTCAT")
        
        # Criar frames para cada entidade na aba de cadastros
        self.create_empresa_widgets()
        self.create_setor_widgets()
        self.create_cargo_widgets()
        self.create_atividade_widgets()
        self.create_ambiente_widgets()
        
        # Criar widgets para relatórios
        self.create_relatorio_widgets()
        
        # Criar widgets para PPRA/LTCAT
        self.create_ppra_widgets()
        
        # Atualizar região de rolagem
        self.canvas_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def create_empresa_widgets(self):
        # Frame para Empresa
        empresa_frame = ttk.LabelFrame(self.cadastro_frame, text="Empresa")
        empresa_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos de Empresa
        ttk.Label(empresa_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.empresa_id = ttk.Entry(empresa_frame, width=10, font=self.fonte_padrao)
        self.empresa_id.grid(row=0, column=1, padx=5, pady=2)
        self.empresa_id.config(state='readonly')
        
        ttk.Label(empresa_frame, text="Nome:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.empresa_nome = ttk.Entry(empresa_frame, width=50, font=self.fonte_padrao)
        self.empresa_nome.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        ttk.Label(empresa_frame, text="CNPJ:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.empresa_cnpj = ttk.Entry(empresa_frame, width=20, font=self.fonte_padrao)
        self.empresa_cnpj.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(empresa_frame, text="Endereço:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.empresa_endereco = ttk.Entry(empresa_frame, width=50, font=self.fonte_padrao)
        self.empresa_endereco.grid(row=3, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        # Botões de navegação
        nav_empresa_frame = ttk.Frame(empresa_frame)
        nav_empresa_frame.grid(row=4, column=0, columnspan=4, pady=5)
        
        ttk.Button(nav_empresa_frame, text="Primeiro", command=lambda: self.show_empresa(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_empresa_frame, text="Anterior", command=lambda: self.show_empresa(self.current_empresa - 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_empresa_frame, text="Próximo", command=lambda: self.show_empresa(self.current_empresa + 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_empresa_frame, text="Último", command=lambda: self.show_empresa(len(self.empresas) - 1)).pack(side=tk.LEFT, padx=2)
        
        # Botões de operação
        op_empresa_frame = ttk.Frame(empresa_frame)
        op_empresa_frame.grid(row=5, column=0, columnspan=4, pady=5)
        
        ttk.Button(op_empresa_frame, text="Novo", command=self.new_empresa).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_empresa_frame, text="Editar", command=self.edit_empresa).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_empresa_frame, text="Salvar", command=self.save_empresa).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_empresa_frame, text="Excluir", command=self.delete_empresa).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_empresa_frame, text="Listar", command=self.list_empresa).pack(side=tk.LEFT, padx=2)
    
    def create_setor_widgets(self):
        # Frame para Setor
        setor_frame = ttk.LabelFrame(self.cadastro_frame, text="Setor")
        setor_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos de Setor
        ttk.Label(setor_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.setor_id = ttk.Entry(setor_frame, width=10, font=self.fonte_padrao)
        self.setor_id.grid(row=0, column=1, padx=5, pady=2)
        self.setor_id.config(state='readonly')
        
        ttk.Label(setor_frame, text="Empresa:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.setor_empresa = ttk.Entry(setor_frame, width=30, font=self.fonte_padrao)
        self.setor_empresa.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.setor_empresa.config(state='readonly')
        
        ttk.Label(setor_frame, text="Nome:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.setor_nome = ttk.Entry(setor_frame, width=50, font=self.fonte_padrao)
        self.setor_nome.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        ttk.Label(setor_frame, text="Descrição:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.setor_descricao = ttk.Entry(setor_frame, width=50, font=self.fonte_padrao)
        self.setor_descricao.grid(row=2, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        # Botões de navegação
        nav_setor_frame = ttk.Frame(setor_frame)
        nav_setor_frame.grid(row=3, column=0, columnspan=4, pady=5)
        
        ttk.Button(nav_setor_frame, text="Primeiro", command=lambda: self.show_setor(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_setor_frame, text="Anterior", command=lambda: self.show_setor(self.current_setor - 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_setor_frame, text="Próximo", command=lambda: self.show_setor(self.current_setor + 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_setor_frame, text="Último", command=lambda: self.show_setor(len(self.setores) - 1)).pack(side=tk.LEFT, padx=2)
        
        # Botões de operação
        op_setor_frame = ttk.Frame(setor_frame)
        op_setor_frame.grid(row=4, column=0, columnspan=4, pady=5)
        
        ttk.Button(op_setor_frame, text="Novo", command=self.new_setor).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_setor_frame, text="Editar", command=self.edit_setor).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_setor_frame, text="Salvar", command=self.save_setor).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_setor_frame, text="Excluir", command=self.delete_setor).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_setor_frame, text="Listar", command=self.list_setor).pack(side=tk.LEFT, padx=2)
    
    def create_cargo_widgets(self):
        # Frame para Cargo
        cargo_frame = ttk.LabelFrame(self.cadastro_frame, text="Cargo")
        cargo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos de Cargo
        ttk.Label(cargo_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.cargo_id = ttk.Entry(cargo_frame, width=10, font=self.fonte_padrao)
        self.cargo_id.grid(row=0, column=1, padx=5, pady=2)
        self.cargo_id.config(state='readonly')
        
        ttk.Label(cargo_frame, text="Setor:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.cargo_setor = ttk.Entry(cargo_frame, width=30, font=self.fonte_padrao)
        self.cargo_setor.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.cargo_setor.config(state='readonly')
        
        ttk.Label(cargo_frame, text="Nome:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.cargo_nome = ttk.Entry(cargo_frame, width=50, font=self.fonte_padrao)
        self.cargo_nome.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        ttk.Label(cargo_frame, text="Descrição:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.cargo_descricao = ttk.Entry(cargo_frame, width=50, font=self.fonte_padrao)
        self.cargo_descricao.grid(row=2, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        # Botões de navegação
        nav_cargo_frame = ttk.Frame(cargo_frame)
        nav_cargo_frame.grid(row=3, column=0, columnspan=4, pady=5)
        
        ttk.Button(nav_cargo_frame, text="Primeiro", command=lambda: self.show_cargo(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_cargo_frame, text="Anterior", command=lambda: self.show_cargo(self.current_cargo - 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_cargo_frame, text="Próximo", command=lambda: self.show_cargo(self.current_cargo + 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_cargo_frame, text="Último", command=lambda: self.show_cargo(len(self.cargos) - 1)).pack(side=tk.LEFT, padx=2)
        
        # Botões de operação
        op_cargo_frame = ttk.Frame(cargo_frame)
        op_cargo_frame.grid(row=4, column=0, columnspan=4, pady=5)
        
        ttk.Button(op_cargo_frame, text="Novo", command=self.new_cargo).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_cargo_frame, text="Editar", command=self.edit_cargo).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_cargo_frame, text="Salvar", command=self.save_cargo).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_cargo_frame, text="Excluir", command=self.delete_cargo).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_cargo_frame, text="Listar", command=self.list_cargo).pack(side=tk.LEFT, padx=2)
    
    def create_atividade_widgets(self):
        # Frame para Atividade
        atividade_frame = ttk.LabelFrame(self.cadastro_frame, text="Atividade")
        atividade_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos de Atividade
        ttk.Label(atividade_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.atividade_id = ttk.Entry(atividade_frame, width=10, font=self.fonte_padrao)
        self.atividade_id.grid(row=0, column=1, padx=5, pady=2)
        self.atividade_id.config(state='readonly')
        
        ttk.Label(atividade_frame, text="Cargo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.atividade_cargo = ttk.Entry(atividade_frame, width=30, font=self.fonte_padrao)
        self.atividade_cargo.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.atividade_cargo.config(state='readonly')
        
        ttk.Label(atividade_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.atividade_descricao = ttk.Entry(atividade_frame, width=50, font=self.fonte_padrao)
        self.atividade_descricao.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        # Botões de operação (sem navegação)
        op_atividade_frame = ttk.Frame(atividade_frame)
        op_atividade_frame.grid(row=2, column=0, columnspan=4, pady=5)
        
        ttk.Button(op_atividade_frame, text="Novo", command=self.new_atividade).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_atividade_frame, text="Editar", command=self.edit_atividade).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_atividade_frame, text="Salvar", command=self.save_atividade).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_atividade_frame, text="Excluir", command=self.delete_atividade).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_atividade_frame, text="Listar", command=self.list_atividade).pack(side=tk.LEFT, padx=2)
    
    def create_ambiente_widgets(self):
        # Frame para Ambiente Laborativo
        ambiente_frame = ttk.LabelFrame(self.cadastro_frame, text="Ambiente Laborativo")
        ambiente_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Campos de Ambiente
        ttk.Label(ambiente_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.ambiente_id = ttk.Entry(ambiente_frame, width=10, font=self.fonte_padrao)
        self.ambiente_id.grid(row=0, column=1, padx=5, pady=2)
        self.ambiente_id.config(state='readonly')
        
        ttk.Label(ambiente_frame, text="Cargo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.ambiente_cargo = ttk.Entry(ambiente_frame, width=30, font=self.fonte_padrao)
        self.ambiente_cargo.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.ambiente_cargo.config(state='readonly')
        
        ttk.Label(ambiente_frame, text="Descrição:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.ambiente_descricao = ttk.Entry(ambiente_frame, width=50, font=self.fonte_padrao)
        self.ambiente_descricao.grid(row=1, column=1, columnspan=3, padx=5, pady=2, sticky=tk.W+tk.E)
        
        # Botões de operação (sem navegação)
        op_ambiente_frame = ttk.Frame(ambiente_frame)
        op_ambiente_frame.grid(row=2, column=0, columnspan=4, pady=5)
        
        ttk.Button(op_ambiente_frame, text="Novo", command=self.new_ambiente).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_ambiente_frame, text="Editar", command=self.edit_ambiente).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_ambiente_frame, text="Salvar", command=self.save_ambiente).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_ambiente_frame, text="Excluir", command=self.delete_ambiente).pack(side=tk.LEFT, padx=2)
        ttk.Button(op_ambiente_frame, text="Listar", command=self.list_ambiente).pack(side=tk.LEFT, padx=2)
    
    def create_relatorio_widgets(self):
        # Frame para Relatórios
        relatorio_options_frame = ttk.Frame(self.relatorio_frame)
        relatorio_options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(relatorio_options_frame, text="Selecione o tipo de relatório:").pack(side=tk.LEFT, padx=5)
        
        self.relatorio_tipo = ttk.Combobox(relatorio_options_frame, values=[
            "Relatório de Empresas", 
            "Relatório de Setores por Empresa", 
            "Relatório de Cargos por Setor",
            "Relatório de Atividades por Cargo",
            "Relatório de Ambientes por Cargo",
            "Relatório Completo (PPRA)"
        ])
        self.relatorio_tipo.pack(side=tk.LEFT, padx=5)
        self.relatorio_tipo.current(0)
        
        ttk.Button(relatorio_options_frame, text="Gerar Relatório", command=self.gerar_relatorio).pack(side=tk.LEFT, padx=5)
        
        # Área de visualização do relatório com rolagem
        relatorio_text_frame = ttk.Frame(self.relatorio_frame)
        relatorio_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Criar canvas para o texto do relatório
        self.relatorio_canvas = tk.Canvas(relatorio_text_frame, bg="#f0e68c")
        self.relatorio_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Criar scrollbar para o relatório
        self.relatorio_scrollbar = ttk.Scrollbar(relatorio_text_frame, orient=tk.VERTICAL, command=self.relatorio_canvas.yview)
        self.relatorio_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar canvas
        self.relatorio_canvas.configure(yscrollcommand=self.relatorio_scrollbar.set)
        self.relatorio_canvas.bind('<Configure>', lambda e: self.relatorio_canvas.configure(scrollregion=self.relatorio_canvas.bbox("all")))
        
        # Criar frame dentro do canvas
        self.relatorio_canvas_frame = ttk.Frame(self.relatorio_canvas)
        self.relatorio_canvas.create_window((0, 0), window=self.relatorio_canvas_frame, anchor="nw")
        
        # Criar widget de texto
        self.relatorio_text = tk.Text(self.relatorio_canvas_frame, wrap=tk.WORD, font=self.fonte_padrao, fg=self.cor_fonte, bg="#ffffff")
        self.relatorio_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar a cor de fundo do canvas
        self.relatorio_canvas.config(bg="#f0e68c")
    
    def create_ppra_widgets(self):
        # Frame para PPRA/LTCAT
        ppra_frame = ttk.LabelFrame(self.ppra_frame, text="PPRA/LTCAT")
        ppra_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Área de visualização do PPRA com rolagem
        ppra_text_frame = ttk.Frame(ppra_frame)
        ppra_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Criar canvas para o texto do PPRA
        self.ppra_canvas = tk.Canvas(ppra_text_frame, bg="#f0e68c")
        self.ppra_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Criar scrollbar para o PPRA
        self.ppra_scrollbar = ttk.Scrollbar(ppra_text_frame, orient=tk.VERTICAL, command=self.ppra_canvas.yview)
        self.ppra_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar canvas
        self.ppra_canvas.configure(yscrollcommand=self.ppra_scrollbar.set)
        self.ppra_canvas.bind('<Configure>', lambda e: self.ppra_canvas.configure(scrollregion=self.ppra_canvas.bbox("all")))
        
        # Criar frame dentro do canvas
        self.ppra_canvas_frame = ttk.Frame(self.ppra_canvas)
        self.ppra_canvas.create_window((0, 0), window=self.ppra_canvas_frame, anchor="nw")
        
        # Criar widget de texto
        self.ppra_text = tk.Text(self.ppra_canvas_frame, wrap=tk.WORD, font=self.fonte_padrao, fg=self.cor_fonte, bg="#ffffff")
        self.ppra_text.pack(fill=tk.BOTH, expand=True)
        
        # Botão para gerar PPRA
        ttk.Button(ppra_frame, text="Gerar PPRA/LTCAT", command=self.gerar_ppra).pack(pady=5)
        
        # Configurar a cor de fundo do canvas
        self.ppra_canvas.config(bg="#f0e68c")
    
    # Métodos para Empresa
    def show_empresa(self, index):
        if not self.empresas:
            messagebox.showwarning("Aviso", "Não há empresas cadastradas.")
            return
            
        if index < 0:
            index = 0
        elif index >= len(self.empresas):
            index = len(self.empresas) - 1
            
        self.current_empresa = index
        empresa = self.empresas[index]
        
        self.empresa_id.config(state='normal')
        self.empresa_id.delete(0, tk.END)
        self.empresa_id.insert(0, str(empresa[0]))
        self.empresa_id.config(state='readonly')
        
        self.empresa_nome.delete(0, tk.END)
        self.empresa_nome.insert(0, empresa[1])
        
        self.empresa_cnpj.delete(0, tk.END)
        self.empresa_cnpj.insert(0, empresa[2])
        
        self.empresa_endereco.delete(0, tk.END)
        self.empresa_endereco.insert(0, empresa[3])
        
        # Atualizar setores relacionados
        self.update_setores_empresa(empresa[0])
    
    def update_setores_empresa(self, empresa_id):
        # Filtrar setores da empresa atual
        setores_empresa = [s for s in self.setores if s[3] == empresa_id]
        
        if setores_empresa:
            # Encontrar o primeiro setor da empresa
            self.current_setor = self.setores.index(setores_empresa[0])
            self.show_setor(self.current_setor)
        else:
            # Limpar campos de setor
            self.setor_id.config(state='normal')
            self.setor_id.delete(0, tk.END)
            self.setor_id.config(state='readonly')
            
            self.setor_empresa.delete(0, tk.END)
            self.setor_nome.delete(0, tk.END)
            self.setor_descricao.delete(0, tk.END)
            
            # Limpar campos dependentes
            self.update_cargos_setor(0)
    
    def new_empresa(self):
        self.empresa_id.config(state='normal')
        self.empresa_id.delete(0, tk.END)
        self.empresa_id.insert(0, "NOVO")
        self.empresa_id.config(state='readonly')
        
        self.empresa_nome.delete(0, tk.END)
        self.empresa_cnpj.delete(0, tk.END)
        self.empresa_endereco.delete(0, tk.END)
        
        self.empresa_nome.focus_set()
    
    def edit_empresa(self):
        if not self.empresas:
            messagebox.showwarning("Aviso", "Não há empresas cadastradas.")
            return
            
        self.empresa_nome.config(state='normal')
        self.empresa_cnpj.config(state='normal')
        self.empresa_endereco.config(state='normal')
        
        self.empresa_nome.focus_set()
    
    def save_empresa(self):
        id_value = self.empresa_id.get()
        nome = self.empresa_nome.get()
        cnpj = self.empresa_cnpj.get()
        endereco = self.empresa_endereco.get()
        
        if not nome or not cnpj or not endereco:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
            return
        
        if id_value == "NOVO":
            # Inserir novo registro
            self.cursor.execute("INSERT INTO empresas (nome, cnpj, endereco) VALUES (?, ?, ?)", (nome, cnpj, endereco))
            self.conn.commit()
            
            # Atualizar lista de empresas
            self.cursor.execute("SELECT * FROM empresas ORDER BY nome")
            self.empresas = self.cursor.fetchall()
            
            # Exibir o novo registro
            self.show_empresa(len(self.empresas) - 1)
            
            messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")
        else:
            # Atualizar registro existente
            empresa_id = int(id_value)
            self.cursor.execute("UPDATE empresas SET nome=?, cnpj=?, endereco=? WHERE id=?", 
                               (nome, cnpj, endereco, empresa_id))
            self.conn.commit()
            
            # Atualizar lista de empresas
            self.cursor.execute("SELECT * FROM empresas ORDER BY nome")
            self.empresas = self.cursor.fetchall()
            
            # Exibir o registro atualizado
            self.show_empresa(self.current_empresa)
            
            messagebox.showinfo("Sucesso", "Empresa atualizada com sucesso!")
        
        # Bloquear campos novamente
        self.empresa_nome.config(state='readonly')
        self.empresa_cnpj.config(state='readonly')
        self.empresa_endereco.config(state='readonly')
    
    def delete_empresa(self):
        if not self.empresas:
            messagebox.showwarning("Aviso", "Não há empresas cadastradas.")
            return
            
        empresa_id = int(self.empresa_id.get())
        
        # Verificar se existem setores vinculados
        self.cursor.execute("SELECT COUNT(*) FROM setores WHERE id_empresa=?", (empresa_id,))
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            messagebox.showwarning("Aviso", "Não é possível excluir esta empresa. Existem setores vinculados.")
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta empresa?"):
            self.cursor.execute("DELETE FROM empresas WHERE id=?", (empresa_id,))
            self.conn.commit()
            
            # Atualizar lista de empresas
            self.cursor.execute("SELECT * FROM empresas ORDER BY nome")
            self.empresas = self.cursor.fetchall()
            
            # Exibir o primeiro registro ou limpar se não houver mais
            if self.empresas:
                self.show_empresa(0)
            else:
                self.empresa_id.config(state='normal')
                self.empresa_id.delete(0, tk.END)
                self.empresa_id.config(state='readonly')
                
                self.empresa_nome.delete(0, tk.END)
                self.empresa_cnpj.delete(0, tk.END)
                self.empresa_endereco.delete(0, tk.END)
                
                # Limpar campos dependentes
                self.setor_id.config(state='normal')
                self.setor_id.delete(0, tk.END)
                self.setor_id.config(state='readonly')
                
                self.setor_empresa.delete(0, tk.END)
                self.setor_nome.delete(0, tk.END)
                self.setor_descricao.delete(0, tk.END)
                
                self.update_cargos_setor(0)
            
            messagebox.showinfo("Sucesso", "Empresa excluída com sucesso!")
    
    def list_empresa(self):
        # Criar janela de listagem
        list_window = tk.Toplevel(self.root)
        list_window.title("Listagem de Empresas")
        list_window.geometry("600x400")
        
        # Criar treeview
        tree = ttk.Treeview(list_window, columns=("ID", "Nome", "CNPJ", "Endereço"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("CNPJ", text="CNPJ")
        tree.heading("Endereço", text="Endereço")
        
        # Adicionar dados
        for empresa in self.empresas:
            tree.insert("", tk.END, values=empresa)
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão para selecionar
        def select_empresa():
            selected = tree.focus()
            if selected:
                item = tree.item(selected)
                empresa_id = item['values'][0]
                
                # Encontrar o índice da empresa na lista
                for i, emp in enumerate(self.empresas):
                    if emp[0] == empresa_id:
                        self.show_empresa(i)
                        list_window.destroy()
                        break
        
        ttk.Button(list_window, text="Selecionar", command=select_empresa).pack(pady=5)
    
    # Métodos para Setor
    def show_setor(self, index):
        if not self.setores:
            messagebox.showwarning("Aviso", "Não há setores cadastrados.")
            return
            
        if index < 0:
            index = 0
        elif index >= len(self.setores):
            index = len(self.setores) - 1
            
        self.current_setor = index
        setor = self.setores[index]
        
        self.setor_id.config(state='normal')
        self.setor_id.delete(0, tk.END)
        self.setor_id.insert(0, str(setor[0]))
        self.setor_id.config(state='readonly')
        
        # Buscar nome da empresa
        empresa_id = setor[3]
        empresa_nome = ""
        for emp in self.empresas:
            if emp[0] == empresa_id:
                empresa_nome = emp[1]
                break
        
        self.setor_empresa.delete(0, tk.END)
        self.setor_empresa.insert(0, empresa_nome)
        
        self.setor_nome.delete(0, tk.END)
        self.setor_nome.insert(0, setor[1])
        
        self.setor_descricao.delete(0, tk.END)
        self.setor_descricao.insert(0, setor[2])
        
        # Atualizar cargos relacionados
        self.update_cargos_setor(setor[0])
    
    def update_cargos_setor(self, setor_id):
        # Filtrar cargos do setor atual
        cargos_setor = [c for c in self.cargos if c[3] == setor_id]
        
        if cargos_setor:
            # Encontrar o primeiro cargo do setor
            self.current_cargo = self.cargos.index(cargos_setor[0])
            self.show_cargo(self.current_cargo)
        else:
            # Limpar campos de cargo
            self.cargo_id.config(state='normal')
            self.cargo_id.delete(0, tk.END)
            self.cargo_id.config(state='readonly')
            
            self.cargo_setor.delete(0, tk.END)
            self.cargo_nome.delete(0, tk.END)
            self.cargo_descricao.delete(0, tk.END)
            
            # Limpar campos dependentes
            self.update_atividades_cargo(0)
            self.update_ambientes_cargo(0)
    
    def new_setor(self):
        if not self.empresas:
            messagebox.showwarning("Aviso", "Não há empresas cadastradas. Cadastre uma empresa primeiro.")
            return
            
        self.setor_id.config(state='normal')
        self.setor_id.delete(0, tk.END)
        self.setor_id.insert(0, "NOVO")
        self.setor_id.config(state='readonly')
        
        # Manter a empresa atual
        empresa_atual = self.empresas[self.current_empresa]
        self.setor_empresa.delete(0, tk.END)
        self.setor_empresa.insert(0, empresa_atual[1])
        
        self.setor_nome.delete(0, tk.END)
        self.setor_descricao.delete(0, tk.END)
        
        self.setor_nome.focus_set()
    
    def edit_setor(self):
        if not self.setores:
            messagebox.showwarning("Aviso", "Não há setores cadastrados.")
            return
            
        self.setor_nome.config(state='normal')
        self.setor_descricao.config(state='normal')
        
        self.setor_nome.focus_set()
    
    def save_setor(self):
        id_value = self.setor_id.get()
        nome = self.setor_nome.get()
        descricao = self.setor_descricao.get()
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome do setor deve ser preenchido.")
            return
        
        # Obter ID da empresa atual
        empresa_atual = self.empresas[self.current_empresa]
        empresa_id = empresa_atual[0]
        
        if id_value == "NOVO":
            # Inserir novo registro
            self.cursor.execute("INSERT INTO setores (nome, descricao, id_empresa) VALUES (?, ?, ?)", 
                               (nome, descricao, empresa_id))
            self.conn.commit()
            
            # Atualizar lista de setores
            self.cursor.execute("SELECT * FROM setores ORDER BY id_empresa, nome")
            self.setores = self.cursor.fetchall()
            
            # Exibir o novo registro
            setores_empresa = [s for s in self.setores if s[3] == empresa_id]
            if setores_empresa:
                self.current_setor = self.setores.index(setores_empresa[-1])
                self.show_setor(self.current_setor)
            
            messagebox.showinfo("Sucesso", "Setor cadastrado com sucesso!")
        else:
            # Atualizar registro existente
            setor_id = int(id_value)
            self.cursor.execute("UPDATE setores SET nome=?, descricao=?, id_empresa=? WHERE id=?", 
                               (nome, descricao, empresa_id, setor_id))
            self.conn.commit()
            
            # Atualizar lista de setores
            self.cursor.execute("SELECT * FROM setores ORDER BY id_empresa, nome")
            self.setores = self.cursor.fetchall()
            
            # Exibir o registro atualizado
            self.show_setor(self.current_setor)
            
            messagebox.showinfo("Sucesso", "Setor atualizado com sucesso!")
        
        # Bloquear campos novamente
        self.setor_nome.config(state='readonly')
        self.setor_descricao.config(state='readonly')
    
    def delete_setor(self):
        if not self.setores:
            messagebox.showwarning("Aviso", "Não há setores cadastrados.")
            return
            
        setor_id = int(self.setor_id.get())
        
        # Verificar se existem cargos vinculados
        self.cursor.execute("SELECT COUNT(*) FROM cargos WHERE id_setor=?", (setor_id,))
        count = self.cursor.fetchone()[0]
        
        if count > 0:
            messagebox.showwarning("Aviso", "Não é possível excluir este setor. Existem cargos vinculados.")
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este setor?"):
            self.cursor.execute("DELETE FROM setores WHERE id=?", (setor_id,))
            self.conn.commit()
            
            # Atualizar lista de setores
            self.cursor.execute("SELECT * FROM setores ORDER BY id_empresa, nome")
            self.setores = self.cursor.fetchall()
            
            # Exibir o primeiro registro da empresa atual ou limpar se não houver mais
            empresa_atual = self.empresas[self.current_empresa]
            empresa_id = empresa_atual[0]
            setores_empresa = [s for s in self.setores if s[3] == empresa_id]
            
            if setores_empresa:
                self.current_setor = self.setores.index(setores_empresa[0])
                self.show_setor(self.current_setor)
            else:
                self.setor_id.config(state='normal')
                self.setor_id.delete(0, tk.END)
                self.setor_id.config(state='readonly')
                
                self.setor_empresa.delete(0, tk.END)
                self.setor_nome.delete(0, tk.END)
                self.setor_descricao.delete(0, tk.END)
                
                self.update_cargos_setor(0)
            
            messagebox.showinfo("Sucesso", "Setor excluído com sucesso!")
    
    def list_setor(self):
        # Criar janela de listagem
        list_window = tk.Toplevel(self.root)
        list_window.title("Listagem de Setores")
        list_window.geometry("700x400")
        
        # Criar treeview
        tree = ttk.Treeview(list_window, columns=("ID", "Nome", "Descrição", "Empresa"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Empresa", text="Empresa")
        
        # Adicionar dados
        for setor in self.setores:
            # Buscar nome da empresa
            empresa_nome = ""
            for emp in self.empresas:
                if emp[0] == setor[3]:
                    empresa_nome = emp[1]
                    break
            
            tree.insert("", tk.END, values=(setor[0], setor[1], setor[2], empresa_nome))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão para selecionar
        def select_setor():
            selected = tree.focus()
            if selected:
                item = tree.item(selected)
                setor_id = item['values'][0]
                
                # Encontrar o índice do setor na lista
                for i, setr in enumerate(self.setores):
                    if setr[0] == setor_id:
                        self.show_setor(i)
                        list_window.destroy()
                        break
        
        ttk.Button(list_window, text="Selecionar", command=select_setor).pack(pady=5)
    
    # Métodos para Cargo
    def show_cargo(self, index):
        if not self.cargos:
            messagebox.showwarning("Aviso", "Não há cargos cadastrados.")
            return
            
        if index < 0:
            index = 0
        elif index >= len(self.cargos):
            index = len(self.cargos) - 1
            
        self.current_cargo = index
        cargo = self.cargos[index]
        
        self.cargo_id.config(state='normal')
        self.cargo_id.delete(0, tk.END)
        self.cargo_id.insert(0, str(cargo[0]))
        self.cargo_id.config(state='readonly')
        
        # Buscar nome do setor
        setor_id = cargo[3]
        setor_nome = ""
        for setr in self.setores:
            if setr[0] == setor_id:
                setor_nome = setr[1]
                break
        
        self.cargo_setor.delete(0, tk.END)
        self.cargo_setor.insert(0, setor_nome)
        
        self.cargo_nome.delete(0, tk.END)
        self.cargo_nome.insert(0, cargo[1])
        
        self.cargo_descricao.delete(0, tk.END)
        self.cargo_descricao.insert(0, cargo[2])
        
        # Atualizar atividades e ambientes relacionados
        self.update_atividades_cargo(cargo[0])
        self.update_ambientes_cargo(cargo[0])
    
    def update_atividades_cargo(self, cargo_id):
        # Filtrar atividades do cargo atual
        atividades_cargo = [a for a in self.atividades if a[2] == cargo_id]
        
        if atividades_cargo:
            # Encontrar a primeira atividade do cargo
            self.current_atividade = self.atividades.index(atividades_cargo[0])
            self.show_atividade(self.current_atividade)
        else:
            # Limpar campos de atividade
            self.atividade_id.config(state='normal')
            self.atividade_id.delete(0, tk.END)
            self.atividade_id.config(state='readonly')
            
            self.atividade_cargo.delete(0, tk.END)
            self.atividade_descricao.delete(0, tk.END)
    
    def update_ambientes_cargo(self, cargo_id):
        # Filtrar ambientes do cargo atual
        ambientes_cargo = [a for a in self.ambientes if a[2] == cargo_id]
        
        if ambientes_cargo:
            # Encontrar o primeiro ambiente do cargo
            self.current_ambiente = self.ambientes.index(ambientes_cargo[0])
            self.show_ambiente(self.current_ambiente)
        else:
            # Limpar campos de ambiente
            self.ambiente_id.config(state='normal')
            self.ambiente_id.delete(0, tk.END)
            self.ambiente_id.config(state='readonly')
            
            self.ambiente_cargo.delete(0, tk.END)
            self.ambiente_descricao.delete(0, tk.END)
    
    def new_cargo(self):
        if not self.setores:
            messagebox.showwarning("Aviso", "Não há setores cadastrados. Cadastre um setor primeiro.")
            return
            
        self.cargo_id.config(state='normal')
        self.cargo_id.delete(0, tk.END)
        self.cargo_id.insert(0, "NOVO")
        self.cargo_id.config(state='readonly')
        
        # Manter o setor atual
        setor_atual = self.setores[self.current_setor]
        self.cargo_setor.delete(0, tk.END)
        self.cargo_setor.insert(0, setor_atual[1])
        
        self.cargo_nome.delete(0, tk.END)
        self.cargo_descricao.delete(0, tk.END)
        
        self.cargo_nome.focus_set()
    
    def edit_cargo(self):
        if not self.cargos:
            messagebox.showwarning("Aviso", "Não há cargos cadastrados.")
            return
            
        self.cargo_nome.config(state='normal')
        self.cargo_descricao.config(state='normal')
        
        self.cargo_nome.focus_set()
    
    def save_cargo(self):
        id_value = self.cargo_id.get()
        nome = self.cargo_nome.get()
        descricao = self.cargo_descricao.get()
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome do cargo deve ser preenchido.")
            return
        
        # Obter ID do setor atual
        setor_atual = self.setores[self.current_setor]
        setor_id = setor_atual[0]
        
        if id_value == "NOVO":
            # Inserir novo registro
            self.cursor.execute("INSERT INTO cargos (nome, descricao, id_setor) VALUES (?, ?, ?)", 
                               (nome, descricao, setor_id))
            self.conn.commit()
            
            # Atualizar lista de cargos
            self.cursor.execute("SELECT * FROM cargos ORDER BY id_setor, nome")
            self.cargos = self.cursor.fetchall()
            
            # Exibir o novo registro
            cargos_setor = [c for c in self.cargos if c[3] == setor_id]
            if cargos_setor:
                self.current_cargo = self.cargos.index(cargos_setor[-1])
                self.show_cargo(self.current_cargo)
            
            messagebox.showinfo("Sucesso", "Cargo cadastrado com sucesso!")
        else:
            # Atualizar registro existente
            cargo_id = int(id_value)
            self.cursor.execute("UPDATE cargos SET nome=?, descricao=?, id_setor=? WHERE id=?", 
                               (nome, descricao, setor_id, cargo_id))
            self.conn.commit()
            
            # Atualizar lista de cargos
            self.cursor.execute("SELECT * FROM cargos ORDER BY id_setor, nome")
            self.cargos = self.cursor.fetchall()
            
            # Exibir o registro atualizado
            self.show_cargo(self.current_cargo)
            
            messagebox.showinfo("Sucesso", "Cargo atualizado com sucesso!")
        
        # Bloquear campos novamente
        self.cargo_nome.config(state='readonly')
        self.cargo_descricao.config(state='readonly')
    
    def delete_cargo(self):
        if not self.cargos:
            messagebox.showwarning("Aviso", "Não há cargos cadastrados.")
            return
            
        cargo_id = int(self.cargo_id.get())
        
        # Verificar se existem atividades ou ambientes vinculados
        self.cursor.execute("SELECT COUNT(*) FROM atividades WHERE id_cargo=?", (cargo_id,))
        count_atividades = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM ambientes WHERE id_cargo=?", (cargo_id,))
        count_ambientes = self.cursor.fetchone()[0]
        
        if count_atividades > 0 or count_ambientes > 0:
            messagebox.showwarning("Aviso", "Não é possível excluir este cargo. Existem atividades ou ambientes vinculados.")
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este cargo?"):
            self.cursor.execute("DELETE FROM cargos WHERE id=?", (cargo_id,))
            self.conn.commit()
            
            # Atualizar lista de cargos
            self.cursor.execute("SELECT * FROM cargos ORDER BY id_setor, nome")
            self.cargos = self.cursor.fetchall()
            
            # Exibir o primeiro registro do setor atual ou limpar se não houver mais
            setor_atual = self.setores[self.current_setor]
            setor_id = setor_atual[0]
            cargos_setor = [c for c in self.cargos if c[3] == setor_id]
            
            if cargos_setor:
                self.current_cargo = self.cargos.index(cargos_setor[0])
                self.show_cargo(self.current_cargo)
            else:
                self.cargo_id.config(state='normal')
                self.cargo_id.delete(0, tk.END)
                self.cargo_id.config(state='readonly')
                
                self.cargo_setor.delete(0, tk.END)
                self.cargo_nome.delete(0, tk.END)
                self.cargo_descricao.delete(0, tk.END)
                
                self.update_atividades_cargo(0)
                self.update_ambientes_cargo(0)
            
            messagebox.showinfo("Sucesso", "Cargo excluído com sucesso!")
    
    def list_cargo(self):
        # Criar janela de listagem
        list_window = tk.Toplevel(self.root)
        list_window.title("Listagem de Cargos")
        list_window.geometry("700x400")
        
        # Criar treeview
        tree = ttk.Treeview(list_window, columns=("ID", "Nome", "Descrição", "Setor", "Empresa"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nome", text="Nome")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Setor", text="Setor")
        tree.heading("Empresa", text="Empresa")
        
        # Adicionar dados
        for cargo in self.cargos:
            # Buscar nome do setor e empresa
            setor_nome = ""
            empresa_nome = ""
            
            for setr in self.setores:
                if setr[0] == cargo[3]:
                    setor_nome = setr[1]
                    
                    for emp in self.empresas:
                        if emp[0] == setr[3]:
                            empresa_nome = emp[1]
                            break
                    break
            
            tree.insert("", tk.END, values=(cargo[0], cargo[1], cargo[2], setor_nome, empresa_nome))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão para selecionar
        def select_cargo():
            selected = tree.focus()
            if selected:
                item = tree.item(selected)
                cargo_id = item['values'][0]
                
                # Encontrar o índice do cargo na lista
                for i, crg in enumerate(self.cargos):
                    if crg[0] == cargo_id:
                        self.show_cargo(i)
                        list_window.destroy()
                        break
        
        ttk.Button(list_window, text="Selecionar", command=select_cargo).pack(pady=5)
    
    # Métodos para Atividade
    def show_atividade(self, index):
        if not self.atividades:
            messagebox.showwarning("Aviso", "Não há atividades cadastradas.")
            return
            
        if index < 0:
            index = 0
        elif index >= len(self.atividades):
            index = len(self.atividades) - 1
            
        self.current_atividade = index
        atividade = self.atividades[index]
        
        self.atividade_id.config(state='normal')
        self.atividade_id.delete(0, tk.END)
        self.atividade_id.insert(0, str(atividade[0]))
        self.atividade_id.config(state='readonly')
        
        # Buscar nome do cargo
        cargo_id = atividade[2]
        cargo_nome = ""
        for crg in self.cargos:
            if crg[0] == cargo_id:
                cargo_nome = crg[1]
                break
        
        self.atividade_cargo.delete(0, tk.END)
        self.atividade_cargo.insert(0, cargo_nome)
        
        self.atividade_descricao.delete(0, tk.END)
        self.atividade_descricao.insert(0, atividade[1])
    
    def new_atividade(self):
        if not self.cargos:
            messagebox.showwarning("Aviso", "Não há cargos cadastrados. Cadastre um cargo primeiro.")
            return
            
        self.atividade_id.config(state='normal')
        self.atividade_id.delete(0, tk.END)
        self.atividade_id.insert(0, "NOVO")
        self.atividade_id.config(state='readonly')
        
        # Manter o cargo atual
        cargo_atual = self.cargos[self.current_cargo]
        self.atividade_cargo.delete(0, tk.END)
        self.atividade_cargo.insert(0, cargo_atual[1])
        
        self.atividade_descricao.delete(0, tk.END)
        
        self.atividade_descricao.focus_set()
    
    def edit_atividade(self):
        if not self.atividades:
            messagebox.showwarning("Aviso", "Não há atividades cadastradas.")
            return
            
        self.atividade_descricao.config(state='normal')
        self.atividade_descricao.focus_set()
    
    def save_atividade(self):
        id_value = self.atividade_id.get()
        descricao = self.atividade_descricao.get()
        
        if not descricao:
            messagebox.showwarning("Aviso", "A descrição da atividade deve ser preenchida.")
            return
        
        # Obter ID do cargo atual
        cargo_atual = self.cargos[self.current_cargo]
        cargo_id = cargo_atual[0]
        
        if id_value == "NOVO":
            # Inserir novo registro
            self.cursor.execute("INSERT INTO atividades (descricao, id_cargo) VALUES (?, ?)", 
                               (descricao, cargo_id))
            self.conn.commit()
            
            # Atualizar lista de atividades
            self.cursor.execute("SELECT * FROM atividades ORDER BY id_cargo")
            self.atividades = self.cursor.fetchall()
            
            # Exibir o novo registro
            atividades_cargo = [a for a in self.atividades if a[2] == cargo_id]
            if atividades_cargo:
                self.current_atividade = self.atividades.index(atividades_cargo[-1])
                self.show_atividade(self.current_atividade)
            
            messagebox.showinfo("Sucesso", "Atividade cadastrada com sucesso!")
        else:
            # Atualizar registro existente
            atividade_id = int(id_value)
            self.cursor.execute("UPDATE atividades SET descricao=?, id_cargo=? WHERE id=?", 
                               (descricao, cargo_id, atividade_id))
            self.conn.commit()
            
            # Atualizar lista de atividades
            self.cursor.execute("SELECT * FROM atividades ORDER BY id_cargo")
            self.atividades = self.cursor.fetchall()
            
            # Exibir o registro atualizado
            self.show_atividade(self.current_atividade)
            
            messagebox.showinfo("Sucesso", "Atividade atualizada com sucesso!")
        
        # Bloquear campos novamente
        self.atividade_descricao.config(state='readonly')
    
    def delete_atividade(self):
        if not self.atividades:
            messagebox.showwarning("Aviso", "Não há atividades cadastradas.")
            return
            
        atividade_id = int(self.atividade_id.get())
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir esta atividade?"):
            self.cursor.execute("DELETE FROM atividades WHERE id=?", (atividade_id,))
            self.conn.commit()
            
            # Atualizar lista de atividades
            self.cursor.execute("SELECT * FROM atividades ORDER BY id_cargo")
            self.atividades = self.cursor.fetchall()
            
            # Exibir o primeiro registro do cargo atual ou limpar se não houver mais
            cargo_atual = self.cargos[self.current_cargo]
            cargo_id = cargo_atual[0]
            atividades_cargo = [a for a in self.atividades if a[2] == cargo_id]
            
            if atividades_cargo:
                self.current_atividade = self.atividades.index(atividades_cargo[0])
                self.show_atividade(self.current_atividade)
            else:
                self.atividade_id.config(state='normal')
                self.atividade_id.delete(0, tk.END)
                self.atividade_id.config(state='readonly')
                
                self.atividade_cargo.delete(0, tk.END)
                self.atividade_descricao.delete(0, tk.END)
            
            messagebox.showinfo("Sucesso", "Atividade excluída com sucesso!")
    
    def list_atividade(self):
        # Criar janela de listagem
        list_window = tk.Toplevel(self.root)
        list_window.title("Listagem de Atividades")
        list_window.geometry("800x400")
        
        # Criar treeview
        tree = ttk.Treeview(list_window, columns=("ID", "Descrição", "Cargo", "Setor", "Empresa"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Cargo", text="Cargo")
        tree.heading("Setor", text="Setor")
        tree.heading("Empresa", text="Empresa")
        
        # Adicionar dados
        for atividade in self.atividades:
            # Buscar nome do cargo, setor e empresa
            cargo_nome = ""
            setor_nome = ""
            empresa_nome = ""
            
            for crg in self.cargos:
                if crg[0] == atividade[2]:
                    cargo_nome = crg[1]
                    
                    for setr in self.setores:
                        if setr[0] == crg[3]:
                            setor_nome = setr[1]
                            
                            for emp in self.empresas:
                                if emp[0] == setr[3]:
                                    empresa_nome = emp[1]
                                    break
                            break
                    break
            
            tree.insert("", tk.END, values=(atividade[0], atividade[1], cargo_nome, setor_nome, empresa_nome))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão para selecionar
        def select_atividade():
            selected = tree.focus()
            if selected:
                item = tree.item(selected)
                atividade_id = item['values'][0]
                
                # Encontrar o índice da atividade na lista
                for i, atv in enumerate(self.atividades):
                    if atv[0] == atividade_id:
                        self.show_atividade(i)
                        list_window.destroy()
                        break
        
        ttk.Button(list_window, text="Selecionar", command=select_atividade).pack(pady=5)
    
    # Métodos para Ambiente Laborativo
    def show_ambiente(self, index):
        if not self.ambientes:
            messagebox.showwarning("Aviso", "Não há ambientes laborativos cadastrados.")
            return
            
        if index < 0:
            index = 0
        elif index >= len(self.ambientes):
            index = len(self.ambientes) - 1
            
        self.current_ambiente = index
        ambiente = self.ambientes[index]
        
        self.ambiente_id.config(state='normal')
        self.ambiente_id.delete(0, tk.END)
        self.ambiente_id.insert(0, str(ambiente[0]))
        self.ambiente_id.config(state='readonly')
        
        # Buscar nome do cargo
        cargo_id = ambiente[2]
        cargo_nome = ""
        for crg in self.cargos:
            if crg[0] == cargo_id:
                cargo_nome = crg[1]
                break
        
        self.ambiente_cargo.delete(0, tk.END)
        self.ambiente_cargo.insert(0, cargo_nome)
        
        self.ambiente_descricao.delete(0, tk.END)
        self.ambiente_descricao.insert(0, ambiente[1])
    
    def new_ambiente(self):
        if not self.cargos:
            messagebox.showwarning("Aviso", "Não há cargos cadastrados. Cadastre um cargo primeiro.")
            return
            
        self.ambiente_id.config(state='normal')
        self.ambiente_id.delete(0, tk.END)
        self.ambiente_id.insert(0, "NOVO")
        self.ambiente_id.config(state='readonly')
        
        # Manter o cargo atual
        cargo_atual = self.cargos[self.current_cargo]
        self.ambiente_cargo.delete(0, tk.END)
        self.ambiente_cargo.insert(0, cargo_atual[1])
        
        self.ambiente_descricao.delete(0, tk.END)
        
        self.ambiente_descricao.focus_set()
    
    def edit_ambiente(self):
        if not self.ambientes:
            messagebox.showwarning("Aviso", "Não há ambientes laborativos cadastrados.")
            return
            
        self.ambiente_descricao.config(state='normal')
        self.ambiente_descricao.focus_set()
    
    def save_ambiente(self):
        id_value = self.ambiente_id.get()
        descricao = self.ambiente_descricao.get()
        
        if not descricao:
            messagebox.showwarning("Aviso", "A descrição do ambiente deve ser preenchida.")
            return
        
        # Obter ID do cargo atual
        cargo_atual = self.cargos[self.current_cargo]
        cargo_id = cargo_atual[0]
        
        if id_value == "NOVO":
            # Inserir novo registro
            self.cursor.execute("INSERT INTO ambientes (descricao, id_cargo) VALUES (?, ?)", 
                               (descricao, cargo_id))
            self.conn.commit()
            
            # Atualizar lista de ambientes
            self.cursor.execute("SELECT * FROM ambientes ORDER BY id_cargo")
            self.ambientes = self.cursor.fetchall()
            
            # Exibir o novo registro
            ambientes_cargo = [a for a in self.ambientes if a[2] == cargo_id]
            if ambientes_cargo:
                self.current_ambiente = self.ambientes.index(ambientes_cargo[-1])
                self.show_ambiente(self.current_ambiente)
            
            messagebox.showinfo("Sucesso", "Ambiente laborativo cadastrado com sucesso!")
        else:
            # Atualizar registro existente
            ambiente_id = int(id_value)
            self.cursor.execute("UPDATE ambientes SET descricao=?, id_cargo=? WHERE id=?", 
                               (descricao, cargo_id, ambiente_id))
            self.conn.commit()
            
            # Atualizar lista de ambientes
            self.cursor.execute("SELECT * FROM ambientes ORDER BY id_cargo")
            self.ambientes = self.cursor.fetchall()
            
            # Exibir o registro atualizado
            self.show_ambiente(self.current_ambiente)
            
            messagebox.showinfo("Sucesso", "Ambiente laborativo atualizado com sucesso!")
        
        # Bloquear campos novamente
        self.ambiente_descricao.config(state='readonly')
    
    def delete_ambiente(self):
        if not self.ambientes:
            messagebox.showwarning("Aviso", "Não há ambientes laborativos cadastrados.")
            return
            
        ambiente_id = int(self.ambiente_id.get())
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este ambiente laborativo?"):
            self.cursor.execute("DELETE FROM ambientes WHERE id=?", (ambiente_id,))
            self.conn.commit()
            
            # Atualizar lista de ambientes
            self.cursor.execute("SELECT * FROM ambientes ORDER BY id_cargo")
            self.ambientes = self.cursor.fetchall()
            
            # Exibir o primeiro registro do cargo atual ou limpar se não houver mais
            cargo_atual = self.cargos[self.current_cargo]
            cargo_id = cargo_atual[0]
            ambientes_cargo = [a for a in self.ambientes if a[2] == cargo_id]
            
            if ambientes_cargo:
                self.current_ambiente = self.ambientes.index(ambientes_cargo[0])
                self.show_ambiente(self.current_ambiente)
            else:
                self.ambiente_id.config(state='normal')
                self.ambiente_id.delete(0, tk.END)
                self.ambiente_id.config(state='readonly')
                
                self.ambiente_cargo.delete(0, tk.END)
                self.ambiente_descricao.delete(0, tk.END)
            
            messagebox.showinfo("Sucesso", "Ambiente laborativo excluído com sucesso!")
    
    def list_ambiente(self):
        # Criar janela de listagem
        list_window = tk.Toplevel(self.root)
        list_window.title("Listagem de Ambientes Laborativos")
        list_window.geometry("800x400")
        
        # Criar treeview
        tree = ttk.Treeview(list_window, columns=("ID", "Descrição", "Cargo", "Setor", "Empresa"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Descrição", text="Descrição")
        tree.heading("Cargo", text="Cargo")
        tree.heading("Setor", text="Setor")
        tree.heading("Empresa", text="Empresa")
        
        # Adicionar dados
        for ambiente in self.ambientes:
            # Buscar nome do cargo, setor e empresa
            cargo_nome = ""
            setor_nome = ""
            empresa_nome = ""
            
            for crg in self.cargos:
                if crg[0] == ambiente[2]:
                    cargo_nome = crg[1]
                    
                    for setr in self.setores:
                        if setr[0] == crg[3]:
                            setor_nome = setr[1]
                            
                            for emp in self.empresas:
                                if emp[0] == setr[3]:
                                    empresa_nome = emp[1]
                                    break
                            break
                    break
            
            tree.insert("", tk.END, values=(ambiente[0], ambiente[1], cargo_nome, setor_nome, empresa_nome))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botão para selecionar
        def select_ambiente():
            selected = tree.focus()
            if selected:
                item = tree.item(selected)
                ambiente_id = item['values'][0]
                
                # Encontrar o índice do ambiente na lista
                for i, amb in enumerate(self.ambientes):
                    if amb[0] == ambiente_id:
                        self.show_ambiente(i)
                        list_window.destroy()
                        break
        
        ttk.Button(list_window, text="Selecionar", command=select_ambiente).pack(pady=5)
    
    # Método para gerar relatórios
    def gerar_relatorio(self):
        tipo_relatorio = self.relatorio_tipo.get()
        self.relatorio_text.delete(1.0, tk.END)
        
        # Cabeçalho do relatório
        self.relatorio_text.insert(tk.END, "PROGRAMA PREVENTIVO DE RISCOS AMBIENTAIS E LTCAT\n")
        self.relatorio_text.insert(tk.END, "=" * 80 + "\n\n")
        self.relatorio_text.insert(tk.END, f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        if tipo_relatorio == "Relatório de Empresas":
            self.relatorio_text.insert(tk.END, "RELATÓRIO DE EMPRESAS\n")
            self.relatorio_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for empresa in self.empresas:
                self.relatorio_text.insert(tk.END, f"ID: {empresa[0]}\n")
                self.relatorio_text.insert(tk.END, f"Nome: {empresa[1]}\n")
                self.relatorio_text.insert(tk.END, f"CNPJ: {empresa[2]}\n")
                self.relatorio_text.insert(tk.END, f"Endereço: {empresa[3]}\n")
                self.relatorio_text.insert(tk.END, "-" * 80 + "\n")
        
        elif tipo_relatorio == "Relatório de Setores por Empresa":
            self.relatorio_text.insert(tk.END, "RELATÓRIO DE SETORES POR EMPRESA\n")
            self.relatorio_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for empresa in self.empresas:
                self.relatorio_text.insert(tk.END, f"EMPRESA: {empresa[1]}\n")
                self.relatorio_text.insert(tk.END, f"CNPJ: {empresa[2]}\n\n")
                
                # Buscar setores da empresa
                setores_empresa = [s for s in self.setores if s[3] == empresa[0]]
                
                if setores_empresa:
                    for setor in setores_empresa:
                        self.relatorio_text.insert(tk.END, f"  ID: {setor[0]}\n")
                        self.relatorio_text.insert(tk.END, f"  Nome: {setor[1]}\n")
                        self.relatorio_text.insert(tk.END, f"  Descrição: {setor[2]}\n")
                        self.relatorio_text.insert(tk.END, "  " + "-" * 60 + "\n")
                else:
                    self.relatorio_text.insert(tk.END, "  Nenhum setor cadastrado para esta empresa.\n")
                
                self.relatorio_text.insert(tk.END, "=" * 80 + "\n")
        
        elif tipo_relatorio == "Relatório de Cargos por Setor":
            self.relatorio_text.insert(tk.END, "RELATÓRIO DE CARGOS POR SETOR\n")
            self.relatorio_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for empresa in self.empresas:
                self.relatorio_text.insert(tk.END, f"EMPRESA: {empresa[1]}\n")
                
                # Buscar setores da empresa
                setores_empresa = [s for s in self.setores if s[3] == empresa[0]]
                
                for setor in setores_empresa:
                    self.relatorio_text.insert(tk.END, f"\n  SETOR: {setor[1]}\n")
                    
                    # Buscar cargos do setor
                    cargos_setor = [c for c in self.cargos if c[3] == setor[0]]
                    
                    if cargos_setor:
                        for cargo in cargos_setor:
                            self.relatorio_text.insert(tk.END, f"    ID: {cargo[0]}\n")
                            self.relatorio_text.insert(tk.END, f"    Nome: {cargo[1]}\n")
                            self.relatorio_text.insert(tk.END, f"    Descrição: {cargo[2]}\n")
                            self.relatorio_text.insert(tk.END, "    " + "-" * 60 + "\n")
                    else:
                        self.relatorio_text.insert(tk.END, "    Nenhum cargo cadastrado para este setor.\n")
                
                self.relatorio_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        
        elif tipo_relatorio == "Relatório de Atividades por Cargo":
            self.relatorio_text.insert(tk.END, "RELATÓRIO DE ATIVIDADES POR CARGO\n")
            self.relatorio_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for empresa in self.empresas:
                self.relatorio_text.insert(tk.END, f"EMPRESA: {empresa[1]}\n")
                
                # Buscar setores da empresa
                setores_empresa = [s for s in self.setores if s[3] == empresa[0]]
                
                for setor in setores_empresa:
                    self.relatorio_text.insert(tk.END, f"\n  SETOR: {setor[1]}\n")
                    
                    # Buscar cargos do setor
                    cargos_setor = [c for c in self.cargos if c[3] == setor[0]]
                    
                    for cargo in cargos_setor:
                        self.relatorio_text.insert(tk.END, f"\n    CARGO: {cargo[1]}\n")
                        
                        # Buscar atividades do cargo
                        atividades_cargo = [a for a in self.atividades if a[2] == cargo[0]]
                        
                        if atividades_cargo:
                            for atividade in atividades_cargo:
                                self.relatorio_text.insert(tk.END, f"      ID: {atividade[0]}\n")
                                self.relatorio_text.insert(tk.END, f"      Descrição: {atividade[1]}\n")
                                self.relatorio_text.insert(tk.END, "      " + "-" * 60 + "\n")
                        else:
                            self.relatorio_text.insert(tk.END, "      Nenhuma atividade cadastrada para este cargo.\n")
                
                self.relatorio_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        
        elif tipo_relatorio == "Relatório de Ambientes por Cargo":
            self.relatorio_text.insert(tk.END, "RELATÓRIO DE AMBIENTES LABORATIVOS POR CARGO\n")
            self.relatorio_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for empresa in self.empresas:
                self.relatorio_text.insert(tk.END, f"EMPRESA: {empresa[1]}\n")
                
                # Buscar setores da empresa
                setores_empresa = [s for s in self.setores if s[3] == empresa[0]]
                
                for setor in setores_empresa:
                    self.relatorio_text.insert(tk.END, f"\n  SETOR: {setor[1]}\n")
                    
                    # Buscar cargos do setor
                    cargos_setor = [c for c in self.cargos if c[3] == setor[0]]
                    
                    for cargo in cargos_setor:
                        self.relatorio_text.insert(tk.END, f"\n    CARGO: {cargo[1]}\n")
                        
                        # Buscar ambientes do cargo
                        ambientes_cargo = [a for a in self.ambientes if a[2] == cargo[0]]
                        
                        if ambientes_cargo:
                            for ambiente in ambientes_cargo:
                                self.relatorio_text.insert(tk.END, f"      ID: {ambiente[0]}\n")
                                self.relatorio_text.insert(tk.END, f"      Descrição: {ambiente[1]}\n")
                                self.relatorio_text.insert(tk.END, "      " + "-" * 60 + "\n")
                        else:
                            self.relatorio_text.insert(tk.END, "      Nenhum ambiente laborativo cadastrado para este cargo.\n")
                
                self.relatorio_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        
        elif tipo_relatorio == "Relatório Completo (PPRA)":
            self.relatorio_text.insert(tk.END, "RELATÓRIO COMPLETO DO PPRA\n")
            self.relatorio_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for empresa in self.empresas:
                self.relatorio_text.insert(tk.END, f"EMPRESA: {empresa[1]}\n")
                self.relatorio_text.insert(tk.END, f"CNPJ: {empresa[2]}\n")
                self.relatorio_text.insert(tk.END, f"Endereço: {empresa[3]}\n\n")
                
                # Buscar setores da empresa
                setores_empresa = [s for s in self.setores if s[3] == empresa[0]]
                
                for setor in setores_empresa:
                    self.relatorio_text.insert(tk.END, f"  SETOR: {setor[1]}\n")
                    self.relatorio_text.insert(tk.END, f"  Descrição: {setor[2]}\n\n")
                    
                    # Buscar cargos do setor
                    cargos_setor = [c for c in self.cargos if c[3] == setor[0]]
                    
                    for cargo in cargos_setor:
                        self.relatorio_text.insert(tk.END, f"    CARGO: {cargo[1]}\n")
                        self.relatorio_text.insert(tk.END, f"    Descrição: {cargo[2]}\n\n")
                        
                        # Buscar atividades do cargo
                        atividades_cargo = [a for a in self.atividades if a[2] == cargo[0]]
                        
                        self.relatorio_text.insert(tk.END, "    ATIVIDADES:\n")
                        if atividades_cargo:
                            for atividade in atividades_cargo:
                                self.relatorio_text.insert(tk.END, f"      - {atividade[1]}\n")
                        else:
                            self.relatorio_text.insert(tk.END, "      Nenhuma atividade cadastrada.\n")
                        
                        self.relatorio_text.insert(tk.END, "\n")
                        
                        # Buscar ambientes do cargo
                        ambientes_cargo = [a for a in self.ambientes if a[2] == cargo[0]]
                        
                        self.relatorio_text.insert(tk.END, "    AMBIENTES LABORATIVOS:\n")
                        if ambientes_cargo:
                            for ambiente in ambientes_cargo:
                                self.relatorio_text.insert(tk.END, f"      - {ambiente[1]}\n")
                        else:
                            self.relatorio_text.insert(tk.END, "      Nenhum ambiente laborativo cadastrado.\n")
                        
                        self.relatorio_text.insert(tk.END, "\n    " + "-" * 60 + "\n")
                
                self.relatorio_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        
        # Rodapé do relatório
        self.relatorio_text.insert(tk.END, "\n\nFIM DO RELATÓRIO\n")
        
        # Atualizar a região de rolagem do canvas do relatório
        self.relatorio_canvas_frame.update_idletasks()
        self.relatorio_canvas.configure(scrollregion=self.relatorio_canvas.bbox("all"))
    
    # Método para gerar PPRA/LTCAT
    def gerar_ppra(self):
        self.ppra_text.delete(1.0, tk.END)
        
        # Cabeçalho do PPRA
        self.ppra_text.insert(tk.END, "PROGRAMA DE PREVENÇÃO DE RISCOS AMBIENTAIS (PPRA)\n")
        self.ppra_text.insert(tk.END, "LAUDO TÉCNICO DE CONDIÇÕES AMBIENTAIS DO TRABALHO (LTCAT)\n")
        self.ppra_text.insert(tk.END, "=" * 80 + "\n\n")
        self.ppra_text.insert(tk.END, f"Data de Emissão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
        
        for empresa in self.empresas:
            self.ppra_text.insert(tk.END, f"EMPRESA: {empresa[1]}\n")
            self.ppra_text.insert(tk.END, f"CNPJ: {empresa[2]}\n")
            self.ppra_text.insert(tk.END, f"Endereço: {empresa[3]}\n\n")
            
            # Buscar setores da empresa
            setores_empresa = [s for s in self.setores if s[3] == empresa[0]]
            
            for setor in setores_empresa:
                self.ppra_text.insert(tk.END, f"  SETOR: {setor[1]}\n")
                self.ppra_text.insert(tk.END, f"  Descrição: {setor[2]}\n\n")
                
                # Buscar cargos do setor
                cargos_setor = [c for c in self.cargos if c[3] == setor[0]]
                
                for cargo in cargos_setor:
                    self.ppra_text.insert(tk.END, f"    CARGO: {cargo[1]}\n")
                    self.ppra_text.insert(tk.END, f"    Descrição: {cargo[2]}\n\n")
                    
                    # Buscar atividades do cargo
                    atividades_cargo = [a for a in self.atividades if a[2] == cargo[0]]
                    
                    self.ppra_text.insert(tk.END, "    ATIVIDADES DESENVOLVIDAS:\n")
                    if atividades_cargo:
                        for atividade in atividades_cargo:
                            self.ppra_text.insert(tk.END, f"      - {atividade[1]}\n")
                    else:
                        self.ppra_text.insert(tk.END, "      Nenhuma atividade cadastrada.\n")
                    
                    self.ppra_text.insert(tk.END, "\n")
                    
                    # Buscar ambientes do cargo
                    ambientes_cargo = [a for a in self.ambientes if a[2] == cargo[0]]
                    
                    self.ppra_text.insert(tk.END, "    AMBIENTES LABORATIVOS:\n")
                    if ambientes_cargo:
                        for ambiente in ambientes_cargo:
                            self.ppra_text.insert(tk.END, f"      - {ambiente[1]}\n")
                    else:
                        self.ppra_text.insert(tk.END, "      Nenhum ambiente laborativo cadastrado.\n")
                    
                    self.ppra_text.insert(tk.END, "\n    " + "-" * 60 + "\n")
            
            self.ppra_text.insert(tk.END, "\n" + "=" * 80 + "\n")
        
        # Rodapé do PPRA
        self.ppra_text.insert(tk.END, "\n\nFIM DO PPRA/LTCAT\n")
        
        # Atualizar a região de rolagem do canvas do PPRA
        self.ppra_canvas_frame.update_idletasks()
        self.ppra_canvas.configure(scrollregion=self.ppra_canvas.bbox("all"))

# Função principal
def main():
    root = tk.Tk()
    app = PPRAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()